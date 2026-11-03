"""Indeks Dilema berbasis KONSTRUK (label Jev) + uji validasi & nilai tambah.

Berbeda dari indeks lama yang dibangun dari PC-1 seluruh topik (atau dari kolom
leksikon yang terbukti tidak valid, kappa=0,107), indeks di sini dibangun
langsung dari kategori Jev yang memang merupakan taksonomi konstruk:

    idx_t(m) = sum(confidence_i | tema_i = t, bulan_i = m) / N(m)

lalu agregat bulanan = PC-1 dari deret tema (mengikuti protokol lama agar
sebanding).

Keluaran:
  data/processed/dilemma_index_jev_monthly.csv
  outputs/jev_index_validation.md
  outputs/jev_index_validation.json
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

THEMES = ["aspirasi_kerja_ideal", "kekecewaan_pasar_kerja", "kritik_kebijakan_kerja",
          "informal_gig", "keamanan_sosial", "lainnya"]
RELEVAN_MIN = 0.5


def _pc1(M: np.ndarray) -> np.ndarray:
    """Komponen utama pertama, ditandai agar berkorelasi positif dengan total."""
    if M.shape[0] < 6 or M.shape[1] < 2:
        return M.mean(1)
    Xc = M - M.mean(0)
    u, s, _ = np.linalg.svd(Xc, full_matrices=False)
    pc1 = u[:, 0] * s[0]
    if np.corrcoef(pc1, M.sum(1))[0, 1] < 0:
        pc1 = -pc1
    return pc1


def load_labels(path: pathlib.Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["doc_hash", "relevan", "tema"])
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    d = pd.DataFrame(rows)
    d["relevan"] = d["relevan"].astype(float)
    return d


def build_index(min_year: int = 0, include_comments: bool = False,
                thread_weight: bool = False) -> pd.DataFrame:
    parts = []
    p = pd.read_csv(processed("corpus_targeted.csv"))
    p["thread"] = p["id"].astype(str)
    parts.append(p[["doc_hash", "date", "thread"]])
    lab = load_labels(outputs("jev_labels_full.jsonl"))
    if include_comments:
        cpath, lpath = processed("corpus_comments.csv"), outputs("jev_labels_comments.jsonl")
        if cpath.exists() and lpath.exists():
            c = pd.read_csv(cpath)
            # komentar menempel pada thread pos induknya -> kunci klaster
            c["thread"] = c["parent_post"].fillna("").astype(str)
            c.loc[c["thread"].eq("") | c["thread"].eq("nan"), "thread"] = c["id"].astype(str)
            parts.append(c[["doc_hash", "date", "thread"]])
            lab = pd.concat([lab, load_labels(lpath)], ignore_index=True)
            print(f"komentar disertakan: {len(load_labels(lpath)):,} label")
        else:
            print("komentar belum tersedia; lanjut pos saja")
    corpus = pd.concat(parts, ignore_index=True)
    df = corpus.merge(lab, on="doc_hash", how="inner")
    df["tahun"] = df["date"].astype(str).str[:4].astype(int)
    if min_year:
        df = df[df["tahun"] >= min_year]
    df = df[df["relevan"] >= RELEVAN_MIN].copy()
    df["bulan"] = df["date"].astype(str).str[:7]

    n_threads_raw = df["thread"].nunique()
    if thread_weight:
        # tiap thread dihitung satu satuan; dokumen dalam thread yang sama
        # berbagi bobot -> menghapus penggandaan thread besar (lihat paper §2.5)
        df["w"] = 1.0 / df.groupby("thread")["doc_hash"].transform("size").astype(float)
    else:
        df["w"] = 1.0

    total = df.groupby("bulan")["w"].sum().rename("n_docs")
    wide = ((df["relevan"] * df["w"]).groupby([df["bulan"], df["tema"]]).sum()
              .unstack(fill_value=0.0).reindex(columns=THEMES, fill_value=0.0))
    shares = wide.div(total, axis=0)
    shares.columns = [f"tema_{c}" for c in shares.columns]
    out = shares.join(total)

    theme_cols = [c for c in out.columns if c.startswith("tema_")]
    sub_cols = [c for c in theme_cols if c != "tema_lainnya"]
    out["idx_all"] = _pc1(out[theme_cols].to_numpy(float))
    out["idx_sub"] = _pc1(out[sub_cols].to_numpy(float))
    out["idx"] = out["idx_sub"]
    out = out.reset_index().sort_values("bulan")
    mode = "berbobot-thread" if thread_weight else "per-dokumen"
    print(f"bulan: {len(out)} ({out['bulan'].iloc[0]}..{out['bulan'].iloc[-1]}) | mode: {mode}")
    print(f"unit relevan: {total.sum():,.1f} | thread unik: {n_threads_raw:,}")
    print(f"unit/bulan: median={total.median():.1f}, min={total.min():.1f}, max={total.max():.1f}")
    return out


def bps_tpt_semesteran(var: int = 543) -> pd.DataFrame:
    path = raw("bps", "labour_long.csv")
    d = pd.read_csv(path if path.exists() else raw("bps", "indicators.csv"))
    s = d[d["var_id"] == var].copy()
    s["sem"] = s["turtahun"].astype(str).str.strip().map({"Februari": "S1", "Agustus": "S2"})
    s = s.dropna(subset=["sem"])
    g = s.groupby(["tahun", "sem"])["value"].mean().reset_index()
    g["per"] = g["tahun"].astype(str) + g["sem"]
    return g[["per", "value"]].rename(columns={"value": "y"})


def semester_of(bulan: str) -> str:
    y, m = bulan.split("-")
    return f"{y}{'S1' if int(m) <= 6 else 'S2'}"


def granger(x, y, max_lag=2):
    n = len(y); out = {}
    for lag in range(1, max_lag + 1):
        idx = np.arange(lag, n)
        ys = y[idx]
        Xr = np.column_stack([np.ones(len(idx))] + [y[idx - k] for k in range(1, lag + 1)])
        Xu = np.column_stack([Xr] + [x[idx - k] for k in range(1, lag + 1)])
        br, *_ = np.linalg.lstsq(Xr, ys, rcond=None)
        bu, *_ = np.linalg.lstsq(Xu, ys, rcond=None)
        rss_r = ((ys - Xr @ br) ** 2).sum(); rss_u = ((ys - Xu @ bu) ** 2).sum()
        df1, df2 = lag, len(ys) - Xu.shape[1]
        if df2 <= 0 or rss_u <= 0:
            continue
        F = ((rss_r - rss_u) / df1) / (rss_u / df2)
        out[lag] = (float(F), float(1 - stats.f.cdf(F, df1, df2)))
    return out


def partial_corr(a, b, c):
    d = pd.concat([a, b, c], axis=1).dropna()
    if len(d) < 5:
        return float("nan")
    A, B, C = d.iloc[:, 0], d.iloc[:, 1], d.iloc[:, 2]
    ra, rb = np.corrcoef(A, C)[0, 1], np.corrcoef(B, C)[0, 1]
    rab = np.corrcoef(A, B)[0, 1]
    den = np.sqrt((1 - ra ** 2) * (1 - rb ** 2))
    return float((rab - ra * rb) / den) if den > 0 else float("nan")


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-year", type=int, default=0)
    ap.add_argument("--include-comments", action="store_true")
    ap.add_argument("--thread-weight", action="store_true",
                    help="bobot 1/(jumlah dokumen dalam thread) untuk mengoreksi non-independensi")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()

    idx = build_index(min_year=args.min_year, include_comments=args.include_comments,
                      thread_weight=args.thread_weight)
    idx.to_csv(ensure(processed(f"dilemma_index_jev_monthly{args.tag}.csv")), index=False)
    idx["per"] = idx["bulan"].map(semester_of)
    sem = idx.groupby("per").agg(idx=("idx", "mean"), vol=("n_docs", "sum")).reset_index()

    y = bps_tpt_semesteran(543)
    m = sem.merge(y, on="per", how="inner").sort_values("per").reset_index(drop=True)
    print(f"\nperiode bertumpang: {len(m)} ({m['per'].iloc[0]}..{m['per'].iloc[-1]})")
    if len(m) < 8:
        print("terlalu sedikit.")
        return 1

    r_level = float(np.corrcoef(m["idx"], m["y"])[0, 1])
    rho_level = float(stats.spearmanr(m["idx"], m["y"]).statistic)
    r_diff = float(np.corrcoef(np.diff(m["idx"]), np.diff(m["y"]))[0, 1])
    rho_diff = float(stats.spearmanr(np.diff(m["idx"]), np.diff(m["y"])).statistic)

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

    # --- bridge nowcast (expanding) ---
    def ols(X, yy):
        return np.linalg.lstsq(X, yy, rcond=None)[0]

    e_ar, e_br, ytrue = [], [], []
    min_train = 6
    for t in range(min_train, len(m)):
        tr = m.iloc[:t]
        yl = tr["y"].to_numpy(float)
        y_next = float(m["y"].iloc[t])
        b = ols(np.column_stack([np.ones(len(yl) - 1), yl[:-1]]), yl[1:])
        e_ar.append(y_next - (b[0] + b[1] * yl[-1]))
        Xb = np.column_stack([np.ones(len(yl) - 1), yl[:-1], tr["idx"].to_numpy(float)[:-1]])
        bb = ols(Xb, yl[1:])
        e_br.append(y_next - (bb[0] + bb[1] * yl[-1] + bb[2] * tr["idx"].iloc[-1]))
        ytrue.append(y_next)

    e_ar = np.array(e_ar); e_br = np.array(e_br); ytrue = np.array(ytrue)
    rmse_ar = float(np.sqrt((e_ar ** 2).mean())); rmse_br = float(np.sqrt((e_br ** 2).mean()))
    mae_ar = float(np.abs(e_ar).mean()); mae_br = float(np.abs(e_br).mean())
    d = e_ar ** 2 - e_br ** 2
    dm = float(d.mean() / np.sqrt(d.var(ddof=1) / len(d))) if d.var(ddof=1) > 0 else float("nan")
    p_dm = float(2 * (1 - stats.t.cdf(abs(dm), df=len(d) - 1))) if dm == dm else float("nan")

    print(f"r(level)={r_level:+.3f} rho={rho_level:+.3f} | r(delta)={r_diff:+.3f}")
    print(f"CCF={ {k: round(v,3) for k,v in ccf.items()} }")
    print(f"partial r (kendalikan volume)={p_disc:+.3f}")
    print(f"nowcast: RMSE AR={rmse_ar:.3f} bridge={rmse_br:.3f} | DM={dm:+.3f} p={p_dm:.3f} | N={len(ytrue)}")

    lines = [
        "# Indeks Dilema Berbasis Konstruk (Jev) : Validasi & Nilai Tambah",
        "",
        "Indeks dibangun langsung dari taksonomi Jev (terbobot keyakinan relevansi), "
        "bukan dari PC-1 seluruh topik maupun dari label leksikon yang terbukti tidak valid.",
        "",
        "## Indeks",
        "",
        f"- bulan: {len(idx)} ({idx['bulan'].iloc[0]}..{idx['bulan'].iloc[-1]})",
        f"- dokumen relevan (≥{RELEVAN_MIN}): {int(idx['n_docs'].sum()):,}",
        f"- dokumen/bulan: median {int(idx['n_docs'].median())}, min {int(idx['n_docs'].min())}, "
        f"maks {int(idx['n_docs'].max())}",
        "",
        "## Validasi konvergen/robustness vs TPT nasional (var 543)",
        "",
        f"- periode bertumpang: {m['per'].iloc[0]}..{m['per'].iloc[-1]} (**N = {len(m)}** semester)",
        "",
        "| uji | nilai |",
        "|---|---|",
        f"| r level | {r_level:+.3f} |",
        f"| Spearman level | {rho_level:+.3f} |",
        f"| r selisih-1 | {r_diff:+.3f} |",
        f"| partial r (kendalikan volume) | {p_disc:+.3f} |",
        f"| CCF lag 1 | {ccf.get(1, float('nan')):+.3f} |",
        f"| Granger indeks → TPT (lag 1) | F = {g_xtoy.get(1,(float('nan'),))[0]:.3f}; "
        f"p = {g_xtoy.get(1,(0,float('nan')))[1]:.3f} |",
        "",
        "## Nilai tambah (bridge nowcast, expanding window)",
        "",
        "| model | RMSE | MAE |",
        "|---|---:|---:|",
        f"| AR(1) | {rmse_ar:.3f} | {mae_ar:.3f} |",
        f"| bridge (AR + indeks Jev) | {rmse_br:.3f} | {mae_br:.3f} |",
        "",
        f"- Diebold–Mariano (bridge vs AR): **DM = {dm:+.3f}, p = {p_dm:.3f}**",
        f"- N evaluasi = {len(ytrue)} → MDE (80% power) ≈ {2.8/np.sqrt(len(ytrue)):.2f} sd: daya rendah",
        "",
        "**Catatan:** nilai p pada N sekecil ini harus dibaca sebagai diagnostik, bukan bukti.",
    ]
    ensure(outputs(f"jev_index_validation{args.tag}.md")).write_text("\n".join(lines), encoding="utf-8")
    ensure(outputs(f"jev_index_validation{args.tag}.json")).write_text(json.dumps({
        "n_semester": len(m), "r_level": r_level, "rho_level": rho_level, "r_diff": r_diff,
        "partial_r_control_volume": p_disc, "ccf": {str(k): v for k, v in ccf.items()},
        "granger_idx_to_tpt": {str(k): v for k, v in g_xtoy.items()},
        "nowcast": {"rmse_ar": rmse_ar, "rmse_bridge": rmse_br, "mae_ar": mae_ar,
                    "mae_bridge": mae_br, "dm": dm, "p_dm": p_dm, "n_eval": len(ytrue)},
    }, indent=2), encoding="utf-8")
    print(f"-> {outputs('jev_index_validation.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
