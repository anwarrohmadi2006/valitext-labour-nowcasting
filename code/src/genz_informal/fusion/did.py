"""DiD event-study baseline (RQ5, mis. UMP).

Implementasi ini adalah BASELINE transparan: TWFE event-study dengan *fixed
effects* provinsi + tahun dan uji pre-trend (joint F). Untuk publikasi, gunakan
estimator modern (R `did`/`contdid`, Sun–Abraham, Borusyak–Jaravel–Spiess) dan
sensitivitas HonestDiD. Rujukan: Callaway & Sant'Anna (2021); Callaway,
Goodman-Bacon & Sant'Anna (2024); Rambachan & Roth (2023); Roth (2022).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class EventStudyResult:
    coefs: dict[int, float]
    ses: dict[int, float]
    pretrend_f: float
    pretrend_p: float
    n_obs: int
    n_units: int
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "event_time_coef": {k: round(v, 4) for k, v in sorted(self.coefs.items())},
            "event_time_se": {k: round(v, 4) for k, v in sorted(self.ses.items())},
            "pretrend_F": round(self.pretrend_f, 3),
            "pretrend_p": round(self.pretrend_p, 4),
            "n_obs": self.n_obs,
            "n_units": self.n_units,
        }


def _ols_hc1(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    xtx_inv = np.linalg.pinv(X.T @ X)
    beta = xtx_inv @ X.T @ y
    resid = y - X @ beta
    meat = X.T @ (X * (resid ** 2)[:, None])
    cov = xtx_inv @ meat @ xtx_inv
    return beta, np.sqrt(np.clip(np.diag(cov), 0, None))


def twfe_event_study(
    df: pd.DataFrame, y: str, unit: str, rel: str, ref: int = -1,
    cluster: str | None = None,
) -> EventStudyResult:
    """df harus punya kolom: y, unit, time (untuk FE tahun), rel (waktu relatif).

    `rel` = periode relatif terhadap perlakuan (mis. -3..+3); ref = periode basis
    yang dikeluarkan (default -1).
    """
    data = df.dropna(subset=[y, unit, "time", rel]).copy()
    if data.empty:
        raise ValueError("tidak ada observasi lengkap")

    # dummies
    unit_d = pd.get_dummies(data[unit].astype(str), prefix="u", drop_first=True, dtype=float)
    time_d = pd.get_dummies(data["time"].astype(str), prefix="t", drop_first=True, dtype=float)
    rels = sorted(data[rel].unique())
    event_rels = [r for r in rels if r != ref]
    event_d = pd.get_dummies(data[rel], prefix="e", dtype=float)
    event_d = event_d[[f"e_{r}" for r in event_rels]]

    X = np.column_stack([np.ones(len(data)), event_d.to_numpy(),
                         unit_d.to_numpy(), time_d.to_numpy()])
    yv = data[y].to_numpy(dtype=float)
    beta, se = _ols_hc1(X, yv)

    coefs = {int(r): float(beta[1 + i]) for i, r in enumerate(event_rels)}
    ses = {int(r): float(se[1 + i]) for i, r in enumerate(event_rels)}

    # joint test pre-trend (rel < ref)
    pre_rels = [r for r in event_rels if r < ref]
    if pre_rels:
        idx = [1 + event_rels.index(r) for r in pre_rels]
        R = np.zeros((len(idx), X.shape[1]))
        for row, col in enumerate(idx):
            R[row, col] = 1.0
        b = beta[idx]
        # cov diperlukan penuh; hitung ulang HC1 penuh
        xtx_inv = np.linalg.pinv(X.T @ X)
        resid = yv - X @ beta
        cov = xtx_inv @ (X.T @ (X * (resid ** 2)[:, None])) @ xtx_inv
        rb = R @ beta
        rc = R @ cov @ R.T
        f_stat = float(rb @ np.linalg.pinv(rc) @ rb / len(idx))
        p_val = float(1 - stats.f.cdf(f_stat, len(idx), max(1, len(data) - X.shape[1])))
    else:
        f_stat, p_val = float("nan"), float("nan")

    return EventStudyResult(
        coefs=coefs, ses=ses, pretrend_f=f_stat, pretrend_p=p_val,
        n_obs=int(len(data)), n_units=int(data[unit].nunique()),
        notes=[
            "Baseline TWFE; untuk publikasi gunakan R `did`/`contdid` + HonestDiD.",
            "Pre-trend tidak signifikan BUKAN bukti parallel trends (Roth, 2022).",
        ],
    )


def demo() -> EventStudyResult:
    """Demonstrasi sintetis: efek 0 sebelum, +2 sesudah perlakuan."""
    rng = np.random.default_rng(0)
    rows = []
    for u in range(30):
        fe = rng.normal(0, 1)
        treat = 4 if u % 2 == 0 else np.nan
        for t in range(8):
            rel = t - treat if not np.isnan(treat) else -4
            y = fe + 0.3 * t + (2.0 if (not np.isnan(treat) and rel >= 0) else 0.0) + rng.normal(0, 0.5)
            rows.append({"unit": f"P{u}", "time": t, "rel": int(rel) if not np.isnan(treat) else -4, "y": y})
    return twfe_event_study(pd.DataFrame(rows), "y", "unit", "rel", ref=-1)
