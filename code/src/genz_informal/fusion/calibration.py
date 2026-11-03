"""Kalibrasi desain untuk sampel non-probabilitas (media sosial).

Implementasi raking/IPF untuk margin BPS + diagnostik kualitas bobot.

Catatan identifikasi (penting): kalibrasi hanya dapat menimbang ulang variabel
yang TERAMATI pada sampel. Karena teks Reddit tidak memuat atribut provinsi,
estimasi TINGKAT PROVINSI tidak teridentifikasi dari korpus; provinsi hanya
boleh berasal dari lapisan BPS/SAE. Rujukan: Pitts dkk. (2025); Ben-Michael,
Feller & Hartman (2024); Li & Si (2024); Hogg dkk. (2024).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


def rake_weights(
    df: pd.DataFrame, margins: dict[str, dict[str, float]], cols: list[str] | None = None,
    max_iter: int = 100, tol: float = 1e-7,
) -> np.ndarray:
    """Bobot raking/IPF agar sebaran sampel cocok dengan margin sasaran.

    margins: {nama_kolom: {kategori: proporsi_target}} (jumlah tiap kolom = 1).
    """
    cols = cols or list(margins.keys())
    w = np.ones(len(df), dtype=float)
    for _ in range(max_iter):
        w_before = w.copy()
        for col in cols:
            target = margins[col]
            for cat, share in target.items():
                mask = df[col].astype(str).to_numpy() == str(cat)
                if not mask.any():
                    continue
                cur = w[mask].sum() / w.sum()
                if cur > 0:
                    w[mask] *= share / cur
        w *= len(w) / w.sum()
        if np.max(np.abs(w - w_before)) / (np.mean(w_before) + 1e-12) < tol:
            break
    return w


def kish_ess(weights: np.ndarray) -> float:
    w = np.asarray(weights, dtype=float)
    return float(w.sum() ** 2 / np.sum(w ** 2)) if len(w) else 0.0


def design_effect(weights: np.ndarray) -> float:
    n = len(weights)
    ess = kish_ess(weights)
    return float(n / ess) if ess > 0 else float("inf")


def balance_table(
    df: pd.DataFrame, weights: np.ndarray, margins: dict[str, dict[str, float]],
) -> pd.DataFrame:
    """SMD antara sebaran berbobot sampel dan target populasi."""
    w = np.asarray(weights, dtype=float)
    rows = []
    for col, target in margins.items():
        sample = df[col].astype(str).to_numpy()
        for cat, p_target in target.items():
            mask = sample == str(cat)
            p_w = float(w[mask].sum() / w.sum()) if mask.any() else 0.0
            denom = np.sqrt(max(p_target * (1 - p_target), 1e-12))
            rows.append({
                "variable": col,
                "category": cat,
                "sample_share_unweighted": round(float(mask.mean()), 4),
                "sample_share_weighted": round(p_w, 4),
                "target_share": round(float(p_target), 4),
                "smd": round((p_w - p_target) / denom, 4),
            })
    return pd.DataFrame(rows)


@dataclass
class CalibrationReport:
    n: int
    ess: float
    design_effect: float
    weight_min: float
    weight_max: float
    max_abs_smd: float

    def to_dict(self) -> dict:
        return {
            "n": self.n,
            "kish_ess": round(self.ess, 2),
            "design_effect": round(self.design_effect, 3),
            "weight_min": round(self.weight_min, 4),
            "weight_max": round(self.weight_max, 4),
            "max_abs_smd": round(self.max_abs_smd, 4),
        }


def summarize(df: pd.DataFrame, weights: np.ndarray, balance: pd.DataFrame) -> CalibrationReport:
    w = np.asarray(weights, dtype=float)
    return CalibrationReport(
        n=len(df),
        ess=kish_ess(w),
        design_effect=design_effect(w),
        weight_min=float(w.min()) if len(w) else 0.0,
        weight_max=float(w.max()) if len(w) else 0.0,
        max_abs_smd=float(balance["smd"].abs().max()) if not balance.empty else 0.0,
    )


def demo() -> tuple[CalibrationReport, pd.DataFrame]:
    """Demonstrasi sintetis (bukan estimasi populasi): cocokkan sampel ke margin."""
    rng = np.random.default_rng(42)
    sample = pd.DataFrame({
        "umur": rng.choice(["15-24", "25-34", "35+"], size=1000, p=[0.5, 0.3, 0.2]),
    })
    margins = {"umur": {"15-24": 0.4, "25-34": 0.35, "35+": 0.25}}
    w = rake_weights(sample, margins)
    bal = balance_table(sample, w, margins)
    return summarize(sample, w, bal), bal
