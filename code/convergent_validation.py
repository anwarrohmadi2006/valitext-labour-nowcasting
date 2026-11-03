"""Validasi konvergen & diskriminan indeks dilema terhadap seri BPS NASIONAL.

Mengikuti protokol yang direkomendasikan literatur:
  - korelasi LEVEL dan SELISIH PERTAMA (Δ)  -> hindari korelasi tren semu
  - cross-correlation function (CCF) lead-lag
  - uji Granger dua arah
  - cek diskriminan: kendalikan volume dokumen (partial correlation)

Jalankan: python scripts/convergent_validation.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from genz_informal.paths import ensure, outputs, processed, raw  # noqa: E402

BULAN = {"Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5, "Juni": 6,
         "Juli": 7, "Agustus": 8, "September": 9, "Oktober": 10, "November": 11, "Desember": 12}


def national_index_monthly() -> pd.DataFrame:
    """Indeks bulanan.

    Bila audits topik tersedia (outputs/audit_llm.json), indeks dibangun HANYA
    dari topik yang lolos audit sebagai 'dilema' (rating >= 3) -> interpretabel
    dan tanda dapat ditafsirkan. Jika tidak, jatuh ke PC-1 semua topik.
    """
    df = pd.read_csv(processed("topic_index_monthly.csv"))
    tcols = [c for c in df.columns if c.startswith("topic_")]
    apath = outputs("audit_llm.json")
    selected: list[str] = []
    if apath.exists():
        raw = json.loads(apath.read_text(encoding="utf-8"))
        for k, v in raw.items():
            if isinstance(v, dict) and "rating" in v:
                if v.get("dilemma") != "bukan_dilema" and float(v["rating"]) >= 3:
                    selected.append(f"topic_{k}")
        selected = [c for c in selected if c in df.columns]
    if selected:
        df["idx"] = df[selected].sum(axis=1)
        df.attrs["mode"] = f"audit_dilemma_topics ({len(selected)})"
        print(f"indeks = jumlah {len(selected)} topik dilema hasil audit")
    else:
        X = df[tcols].to_numpy(float)
        if X.shape[1] >= 2 and X.shape[0] >= 6:
            Xc = X - X.mean(0)
            u, s, _ = np.linalg.svd(Xc, full_matrices=False)
            df["idx"] = u[:, 0] * s[0]
        else:
            df["idx"] = X.mean(1)
        print("indeks = PC-1 semua topik (audit belum tersedia)")
    return df[["bulan", "idx", "n_docs"]]


def bps_national_semesteran(var: int = 543) -> pd.DataFrame:
    path = raw("bps", "labour_long.csv")
    df = pd.read_csv(path if path.exists() else raw("bps", "indicators.csv"))
    s = df[df["var_id"] == var].copy()
    s["turtahun"] = s["turtahun"].astype(str).str.strip()
    s["sem"] = s["turtahun"].map({"Februari": "S1", "Agustus": "S2"})
    s = s.dropna(subset=["sem"])
    g = s.groupby(["tahun", "sem"])["value"].mean().reset_index()
    g["per"] = g["tahun"].astype(str) + g["sem"]
    return g[["per", "value"]].rename(columns={"value": "y"})


def semester_of(bulan: str) -> str:
    y, m = bulan.split("-")
    return f"{y}{'S1' if int(m) <= 6 else 'S2'}"


def granger(x: np.ndarray, y: np.ndarray, max_lag: int = 2) -> dict:
    """Uji Granger sederhana (F-test nested OLS) x -> y."""
    n = len(y)
    out = {}
    for lag in range(1, max_lag + 1):
        idx = np.arange(lag, n)
        ys = y[idx]
        Xr = np.column_stack([np.ones(len(idx))] + [y[idx - k] for k in range(1, lag + 1)])
        Xu = np.column_stack([Xr] + [x[idx - k] for k in range(1, lag + 1)])
        br, *_ = np.linalg.lstsq(Xr, ys, rcond=None)
        bu, *_ = np.linalg.lstsq(Xu, ys, rcond=None)
        rss_r = ((ys - Xr @ br) ** 2).sum()
        rss_u = ((ys - Xu @ bu) ** 2).sum()
        df1, df2 = lag, len(ys) - Xu.shape[1]
        if df2 <= 0 or rss_u <= 0:
            continue
        F = ((rss_r - rss_u) / df1) / (rss_u / df2)
        out[lag] = (float(F), float(1 - stats.f.cdf(F, df1, df2)))
    return out


def partial_corr(a: pd.Series, b: pd.Series, c: pd.Series) -> float:
    d = pd.concat([a, b, c], axis=1).dropna()
    if len(d) < 5:
        return float("nan")
    A, B, C = d.iloc[:, 0], d.iloc[:, 1], d.iloc[:, 2]
    ra, rb = np.corrcoef(A, C)[0, 1], np.corrcoef(B, C)[0, 1]
    rab = np.corrcoef(A, B)[0, 1]
    denom = np.sqrt((1 - ra ** 2) * (1 - rb ** 2))
    return float((rab - ra * rb) / denom) if denom > 0 else float("nan")


def main() -> int:
    idx = national_index_monthly()
    idx["per"] = idx["bulan"].map(semester_of)
    sem = idx.groupby("per").agg(idx=("idx", "mean"), vol=("n_docs", "sum")).reset_index()

    y = bps_national_semesteran(543)          # TPT
    m = sem.merge(y, on="per", how="inner").sort_values("per").reset_index(drop=True)
    print(f"periode bertumpang: {len(m)} ({m['per'].iloc[0]}..{m['per'].iloc[-1]})")
    if len(m) < 8:
        print("terlalu sedikit untuk validasi.")
        return 1

    r_level = float(np.corrcoef(m["idx"], m["y"])[0, 1])
    r_diff = float(np.corrcoef(np.diff(m["idx"]), np.diff(m["y"]))[0, 1])
    rho_level = float(stats.spearmanr(m["idx"], m["y"]).statistic)
    rho_diff = float(stats.spearmanr(np.diff(m["idx"]), np.diff(m["y"])).statistic)

    # CCF
    ccf = {}
    for lag in range(-3, 4):
        if lag < 0:
            a, b = m["idx"][-lag:].to_numpy(), m["y"][:lag].to_numpy()
        elif lag > 0:
            a, b = m["idx"][:-lag].to_numpy(), m["y"][lag:].to_numpy()
        else:
            a, b = m["idx"].to_numpy(), m["y"].to_numpy()
        ccf[lag] = float(np.corrcoef(a, b)[0, 1]) if len(a) > 3 else float("nan")

    g_xtoy = granger(m["idx"].to_numpy(), m["y"].to_numpy())
    g_ytox = granger(m["y"].to_numpy(), m["idx"].to_numpy())
    p_disc = partial_corr(m["idx"], m["y"], m["vol"])

    print(f"r(level)={r_level:+.3f} rho={rho_level:+.3f} | r(delta)={r_diff:+.3f} rho={rho_diff:+.3f}")
    print(f"CCF={ {k: round(v,3) for k,v in ccf.items()} }")
    print(f"Granger idx->TPT={ {k:(round(v[0],2),round(v[1],3)) for k,v in g_xtoy.items()} }")
    print(f"Granger TPT->idx={ {k:(round(v[0],2),round(v[1],3)) for k,v in g_ytox.items()} }")
    print(f"partial corr (kendalikan volume) = {p_disc:+.3f}")

    ensure(outputs("convergent_validation.md")).write_text(
        "# Validasi konvergen & diskriminan (indeks dilema vs BPS nasional)\n\n"
        f"- Periode: {m['per'].iloc[0]}..{m['per'].iloc[-1]} (N={len(m)} semester)\n"
        f"- Target: TPT nasional (var 543)\n\n"
        f"| uji | nilai |\n|---|---|\n"
        f"| r level | {r_level:+.3f} |\n| Spearman level | {rho_level:+.3f} |\n"
        f"| r selisih-1 | {r_diff:+.3f} |\n| Spearman selisih-1 | {rho_diff:+.3f} |\n"
        f"| partial r (kendalikan volume) | {p_disc:+.3f} |\n\n"
        f"## CCF (lag: r)\n\n```json\n{json.dumps({str(k): round(v,3) for k,v in ccf.items()}, indent=2)}\n```\n\n"
        f"## Granger\n\n- indeks → TPT: `{json.dumps({str(k):[round(x,3) for x in v] for k,v in g_xtoy.items()})}`\n"
        f"- TPT → indeks: `{json.dumps({str(k):[round(x,3) for x in v] for k,v in g_ytox.items()})}`\n\n"
        "Catatan: korelasi level bisa mencerminkan tren bersama; nilai Δ dan CCF lebih penting. "
        "Partial correlation menguji apakah hubungan sekadar proksi volume.\n",
        encoding="utf-8")
    ensure(outputs("convergent_validation.json")).write_text(json.dumps({
        "n": len(m), "r_level": r_level, "r_diff": r_diff, "rho_level": rho_level,
        "rho_diff": rho_diff, "ccf": {str(k): v for k, v in ccf.items()},
        "granger_idx_to_tpt": {str(k): v for k, v in g_xtoy.items()},
        "granger_tpt_to_idx": {str(k): v for k, v in g_ytox.items()},
        "partial_r_control_volume": p_disc}, indent=2), encoding="utf-8")
    print("-> outputs/convergent_validation.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
