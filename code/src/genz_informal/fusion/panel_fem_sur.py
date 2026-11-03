"""Baseline ekonometrik: regresi panel fixed-effects (within estimator).

Diterapkan pada panel provinsi x tahun dari indikator agregat BPS.
Diimplementasikan dengan numpy (tanpa statsmodels) agar ringan.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class FEResult:
    coef: dict[str, float]
    r2_within: float
    n_obs: int
    n_groups: int


def _within(df: pd.DataFrame, cols: list[str], group: str) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        out[col] = out[col] - out.groupby(group)[col].transform("mean")
    return out


def fit_fixed_effects(
    df: pd.DataFrame, y: str, x: list[str], group: str = "provinsi",
) -> FEResult:
    data = df.dropna(subset=[y, *x, group]).copy()
    # Within estimator hanya bermakna bila ada >=2 periode per grup.
    counts = data.groupby(group).size()
    keep = counts[counts >= 2].index
    data = data[data[group].isin(keep)]
    if data.empty or data[group].nunique() < 2:
        raise ValueError(
            "observasi tidak cukup untuk estimasi fixed-effects (butuh >=2 periode/grup)"
        )
    demeaned = _within(data, [y, *x], group)
    yv = demeaned[y].to_numpy(dtype=float)
    xv = demeaned[x].to_numpy(dtype=float)
    xv = np.column_stack([np.ones(len(xv)), xv])
    beta, *_ = np.linalg.lstsq(xv, yv, rcond=None)
    pred = xv @ beta
    ss_res = float(((yv - pred) ** 2).sum())
    ss_tot = float(((yv - yv.mean()) ** 2).sum()) or 1.0
    return FEResult(
        coef={"const": float(beta[0]), **{name: float(b) for name, b in zip(x, beta[1:])}},
        r2_within=1.0 - ss_res / ss_tot,
        n_obs=int(len(data)),
        n_groups=int(data[group].nunique()),
    )
