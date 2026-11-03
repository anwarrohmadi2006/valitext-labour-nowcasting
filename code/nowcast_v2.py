"""Nowcast v2: seri TPT semesteran PANJANG (2005-2025) + indeks teks bulanan.

Perbaikan atas v1:
  - target LF = TPT nasional SEMESTERAN (var 543, 2005-2025) -> ~42 titik;
  - evaluasi rolling-origin (expanding) pada periode yang bertumpang dengan teks;
  - model: AR(1); bridge (teks); bridge+inflasi; U-MIDAS K=2; inflation-only;
  - uji: Diebold-Mariano (HLN) & Clark-West (model bersarang), MASE, Theil U2;
  - laporan jujur tentang daya uji pada N kecil.

Jalankan: python scripts/nowcast_v2.py
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from genz_informal.paths import ensure, outputs, processed, raw  # noqa: E402

BULAN = {"Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5, "Juni": 6,
         "Juli": 7, "Agustus": 8, "September": 9, "Oktober": 10, "November": 11, "Desember": 12}


# ---------------------------------------------------------------- data
def lf_tpt_semesteran() -> pd.DataFrame:
    """TPT nasional semesteran = rata-rata provinsi per (tahun, Februari/Agustus)."""
    path = raw("bps", "labour_long.csv")
    df = pd.read_csv(path if path.exists() else raw("bps", "indicators.csv"))
    s = df[df["var_id"] == 543].copy()
    s["sem"] = s["turtahun"].map({"Februari": "S1", "Agustus": "S2"})
    s = s.dropna(subset=["sem"])
    g = s.groupby(["tahun", "sem"])["value"].mean().reset_index()
    g = g.sort_values(["tahun", "sem"]).reset_index(drop=True)
    g["per"] = g["tahun"].astype(str) + g["sem"]
    g["t"] = range(len(g))
    return g[["per", "tahun", "sem", "t", "value"]].rename(columns={"value": "tpt"})


def hf_bulanan() -> pd.DataFrame:
    """HF: indeks teks bulanan (PC-1 dilema) + inflasi nasional bulanan."""
    c = pd.read_csv(processed("corpus.csv"))
    c["bulan"] = pd.to_datetime(c["date"], errors="coerce").dt.to_period("M")
    c = c.dropna(subset=["bulan"])
    counts = c.groupby(["bulan", "dilemma"]).size().unstack(fill_value=0)
    shares = counts.div(counts.sum(axis=1).replace(0, 1), axis=0)
    if shares.shape[0] >= 6 and shares.shape[1] >= 2:
        X = shares.to_numpy(float); X -= X.mean(0)
        u, s, _ = np.linalg.svd(X, full_matrices=False)
        shares["text_idx"] = u[:, 0] * s[0]
    else:
        shares["text_idx"] = shares.mean(axis=1)
    txt = shares[["text_idx"]].reset_index()
    txt["bulan"] = txt["bulan"].astype(str)

    d = pd.read_csv(raw("bps", "indicators.csv"))
    inf = d[d["var_id"] == 2263].copy()
    inf["m"] = inf["turtahun"].map(BULAN)
    inf = inf.dropna(subset=["m"])
    inf = (inf.groupby(["tahun", "m"])["value"].mean().reset_index())
    inf["bulan"] = inf.apply(lambda r: f"{int(r['tahun'])}-{int(r['m']):02d}", axis=1)
    inf = inf[["bulan", "value"]].rename(columns={"value": "inflasi"})

    hf = txt.merge(inf, on="bulan", how="outer").sort_values("bulan")

    tpath = raw("trends", "trends_monthly.csv")
    if tpath.exists():
        tr = pd.read_csv(tpath)
        tr["bulan"] = pd.to_datetime(tr["bulan"], errors="coerce").dt.strftime("%Y-%m")
        kcols = [c for c in tr.columns if c != "bulan"]
        z = (tr[kcols] - tr[kcols].mean()) / tr[kcols].std().replace(0, 1)
        tr["trends_idx"] = z.mean(axis=1)
        hf = hf.merge(tr[["bulan", "trends_idx"]], on="bulan", how="left")
    else:
        hf["trends_idx"] = np.nan

    hf[["text_idx", "inflasi", "trends_idx"]] = (
        hf[["text_idx", "inflasi", "trends_idx"]].fillna(method="ffill").fillna(0.0)
    )
    return hf


def semester_of(bulan: str) -> str:
    y, m = bulan.split("-")
    return f"{y}{'S1' if int(m) <= 6 else 'S2'}"


# ---------------------------------------------------------------- statistik
def _ols(X, y):
    return np.linalg.lstsq(X, y, rcond=None)[0]


def dm_hln(e1, e2):
    d = e1 ** 2 - e2 ** 2
    T = len(d)
    if T < 3 or d.var(ddof=1) <= 0:
        return float("nan"), float("nan")
    dm = d.mean() / np.sqrt(d.var(ddof=1) / T)
    dm *= np.sqrt((T + 1 - 2) / T)
    return float(dm), float(2 * (1 - stats.t.cdf(abs(dm), df=T - 1)))


def clark_west(e1, e2, f1, f2):
    """Clark-West untuk model bersarang (model1 ⊂ model2)."""
    adj = e1 ** 2 - (e2 ** 2 - (f1 - f2) ** 2)
    T = len(adj)
    if T < 3:
        return float("nan"), float("nan")
    m = adj.mean()
    # Newey-West (lag 1)
    g0 = ((adj - m) ** 2).mean()
    g1 = ((adj[1:] - m) * (adj[:-1] - m)).mean()
    S = g0 + 2 * g1
    if S <= 0:
        return float("nan"), float("nan")
    cw = m / np.sqrt(S / T)
    return float(cw), float(1 - stats.norm.cdf(cw))


# ---------------------------------------------------------------- main
def main() -> int:
    lf = lf_tpt_semesteran()
    hf = hf_bulanan()
    hf["per"] = hf["bulan"].map(semester_of)
    hfs = hf.groupby("per").agg(text=("text_idx", "mean"), infl=("inflasi", "mean"),
                                trends=("trends_idx", "mean")).reset_index()

    d = lf.merge(hfs, on="per", how="left")
    ev = d.dropna(subset=["text"]).reset_index(drop=True)
    print(f"LF total={len(d)} ({d['per'].iloc[0]}..{d['per'].iloc[-1]}); "
          f"berteks={len(ev)} ({ev['per'].iloc[0]}..{ev['per'].iloc[-1]})")
    if len(ev) < 10:
        print("tumpang-tindih terlalu kecil untuk evaluasi.")
        return 1

    min_train = 6
    res = {k: [] for k in ["ar", "bridge", "bridge_infl", "umidas", "infl_only",
                           "trends_only", "bridge_full"]}
    ytrue = []
    for t in range(min_train, len(ev)):
        tr = ev.iloc[:t]
        y_next = float(ev["tpt"].iloc[t])
        y_lag = tr["tpt"].to_numpy(float)
        T = len(tr)
        # AR(1)
        b = _ols(np.column_stack([np.ones(T - 1), y_lag[:-1]]), y_lag[1:])
        res["ar"].append(y_next - (b[0] + b[1] * y_lag[-1]))
        # bridge: AR + teks semester
        Xb = np.column_stack([np.ones(T - 1), y_lag[:-1], tr["text"].to_numpy(float)[:-1]])
        bb = _ols(Xb, y_lag[1:])
        res["bridge"].append(y_next - (bb[0] + bb[1] * y_lag[-1] + bb[2] * tr["text"].iloc[-1]))
        # bridge + inflasi
        Xc = np.column_stack([np.ones(T - 1), y_lag[:-1], tr["text"].to_numpy(float)[:-1],
                              tr["infl"].to_numpy(float)[:-1]])
        bc = _ols(Xc, y_lag[1:])
        res["bridge_infl"].append(y_next - (bc[0] + bc[1] * y_lag[-1]
                                            + bc[2] * tr["text"].iloc[-1] + bc[3] * tr["infl"].iloc[-1]))
        # U-MIDAS K=2 (teks semester ini & sebelumnya)
        if T >= 5:
            x0 = tr["text"].to_numpy(float)
            x1 = np.r_[np.nan, x0[:-1]]
            yl1 = y_lag[:-1]                 # prediktor untuk y[1:]
            x0p, x1p = x0[:-1], x1[:-1]
            valid = ~np.isnan(x1p) & ~np.isnan(yl1)
            if valid.sum() >= 4:
                Xu = np.column_stack([np.ones(valid.sum()), yl1[valid],
                                      x0p[valid], x1p[valid]])
                bu = _ols(Xu, y_lag[1:][valid])
                pred = bu[0] + bu[1] * y_lag[-1] + bu[2] * x0[-1] + bu[3] * x1[-1]
                res["umidas"].append(y_next - pred)
            else:
                res["umidas"].append(np.nan)
        else:
            res["umidas"].append(np.nan)
        # inflation only
        Xi = np.column_stack([np.ones(T - 1), y_lag[:-1], tr["infl"].to_numpy(float)[:-1]])
        bi = _ols(Xi, y_lag[1:])
        res["infl_only"].append(y_next - (bi[0] + bi[1] * y_lag[-1] + bi[2] * tr["infl"].iloc[-1]))
        # trends only (benchmark sinyal HF mapan)
        Xt = np.column_stack([np.ones(T - 1), y_lag[:-1], tr["trends"].to_numpy(float)[:-1]])
        bt = _ols(Xt, y_lag[1:])
        res["trends_only"].append(y_next - (bt[0] + bt[1] * y_lag[-1] + bt[2] * tr["trends"].iloc[-1]))
        # full: teks + inflasi + trends
        Xf = np.column_stack([np.ones(T - 1), y_lag[:-1], tr["text"].to_numpy(float)[:-1],
                              tr["infl"].to_numpy(float)[:-1], tr["trends"].to_numpy(float)[:-1]])
        bf = _ols(Xf, y_lag[1:])
        res["bridge_full"].append(y_next - (bf[0] + bf[1] * y_lag[-1] + bf[2] * tr["text"].iloc[-1]
                                            + bf[3] * tr["infl"].iloc[-1] + bf[4] * tr["trends"].iloc[-1]))
        ytrue.append(y_next)

    y = np.array(ytrue)
    rows = []
    for k, e in res.items():
        e = np.array(e, float)
        m = ~np.isnan(e)
        rmse = float(np.sqrt((e[m] ** 2).mean())); mae = float(np.abs(e[m]).mean())
        denom = np.abs(np.diff(ev["tpt"].to_numpy(float)[:min_train + len(e)])).mean()
        mase = mae / (denom if denom else 1)
        rows.append({"model": k, "n": int(m.sum()), "RMSE": round(rmse, 4),
                     "MAE": round(mae, 4), "MASE": round(mase, 3)})
    tab = pd.DataFrame(rows).sort_values("RMSE")
    print("\n", tab.to_string(index=False))

    e_ar = np.array(res["ar"], float); e_br = np.array(res["bridge"], float)
    e_in = np.array(res["infl_only"], float)
    naive = np.array([ev["tpt"].iloc[i - 1] - ev["tpt"].iloc[i] for i in range(min_train, len(ev))])
    theil = float(np.sqrt((e_br ** 2).mean()) / np.sqrt((naive ** 2).mean()))
    dm_br, p_br = dm_hln(e_ar, e_br)
    dm_in, p_in = dm_hln(e_ar, e_in)
    cw, p_cw = clark_west(e_ar, e_br,
                          np.array(res["ar"], float) + e_ar, np.array(res["bridge"], float) + e_br)
    print(f"\nTheil U2 (bridge vs naif) = {theil:.3f}")
    print(f"DM-HLN bridge vs AR: DM={dm_br:+.3f} p={p_br:.3f} | inflation-only: DM={dm_in:+.3f} p={p_in:.3f}")
    print(f"Clark-West (nested, bridge vs AR): CW={cw:+.3f} p(one-sided)={p_cw:.3f}")
    print(f"N evaluasi = {len(y)} (daya uji rendah: MDE ~ 2.8/sqrt(N) = {2.8/np.sqrt(len(y)):.2f})")

    ensure(outputs("nowcast_v2_report.md")).write_text(
        "# Nowcast v2 (TPT semesteran panjang + indeks teks)\n\n"
        f"- Target: TPT nasional semesteran (var 543), {d['per'].iloc[0]}..{d['per'].iloc[-1]}\n"
        f"- Periode evaluasi (bertumpang teks): {ev['per'].iloc[0]}..{ev['per'].iloc[-1]} "
        f"(N={len(y)})\n\n" + tab.to_markdown(index=False) +
        f"\n\n- Theil U2 (bridge vs naif) = {theil:.3f}\n"
        f"- DM-HLN bridge vs AR = {dm_br:+.3f} (p={p_br:.3f})\n"
        f"- DM-HLN inflation-only vs AR = {dm_in:+.3f} (p={p_in:.3f})\n"
        f"- Clark-West (nested) = {cw:+.3f} (p={p_cw:.3f})\n"
        f"- N={len(y)} -> MDE (80% power) ~ {2.8/np.sqrt(len(y)):.2f} sd: daya rendah; "
        "nilai p harus dibaca sebagai diagnostik, bukan bukti.\n",
        encoding="utf-8")
    print("-> outputs/nowcast_v2_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
