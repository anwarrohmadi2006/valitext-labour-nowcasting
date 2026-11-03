"""Bangun panel provinsi x tahun dari indikator BPS agregat.

Target: proporsi informal (var 1162) atau formal (var 1168).
Fitur: TPT provinsi (var 543), upah (var 583 bila tersedia per provinsi).
Plus sinyal NLP (bila tersedia) sebagai fitur tambahan -> inti konsep 'fusion'.
"""

from __future__ import annotations

import pandas as pd

from ..paths import processed, raw

TARGET_VAR = 1162       # Proporsi Lapangan Kerja Informal Non-Pertanian Menurut Provinsi
TARGET_VAR_ALT = 1168   # Persentase Tenaga Kerja Formal Menurut Provinsi
FEATURE_VARS = {
    543: "tpt_provinsi",
    583: "upah_provinsi",
    1429: "rls_provinsi",
    406: "internet_provinsi",
    1225: "internet_pct",
    288: "pdrb_per_kapita",
    192: "kemiskinan_pct",
    1344: "agri_value_per_worker",
    1181: "setengah_pengangguran",
    494: "ipm",
    2263: "inflasi_pct",
    2396: "tpak",
    220: "ump_provinsi",
}


def load_indicators() -> pd.DataFrame:
    df = pd.read_csv(raw("bps", "indicators.csv"))
    df["tahun"] = df["tahun"].astype(str)
    return df


def _norm(values: pd.Series) -> pd.Series:
    return values.astype(str).str.strip().str.upper()


def build_province_panel(indicators: pd.DataFrame | None = None) -> pd.DataFrame:
    df = indicators if indicators is not None else load_indicators()
    df = df.copy()
    df["vervar"] = _norm(df["vervar"])

    def wide(var_id: int, name: str) -> pd.DataFrame:
        sub = df[df["var_id"] == var_id]
        if sub.empty:
            return pd.DataFrame(columns=["provinsi", "tahun", name])
        cols = ["vervar", "tahun", "value"]
        if "turtahun" in sub.columns:
            cols.append("turtahun")
        out = sub[cols].rename(columns={"vervar": "provinsi", "value": name})
        if "turtahun" in out.columns:
            pri = {"Tahunan": 0, "Tahun": 0, "Agustus": 1, "November": 2, "Februari": 3}
            out["_pri"] = out["turtahun"].map(lambda x: pri.get(str(x), 9))
            out = out.sort_values("_pri").drop(columns=["_pri", "turtahun"])
        return out.drop_duplicates(subset=["provinsi", "tahun"])

    panel = wide(TARGET_VAR, "informal_pct")
    alt = wide(TARGET_VAR_ALT, "formal_pct")
    panel = panel.merge(alt, on=["provinsi", "tahun"], how="outer")

    province_names = set(panel["provinsi"].dropna())
    for var_id, name in FEATURE_VARS.items():
        feature = wide(var_id, name)
        if feature.empty:
            continue
        # Hanya gabungkan bila dimensi variabel benar-benar provinsi.
        overlap = set(feature["provinsi"]) & province_names
        if len(overlap) < 0.5 * max(1, feature["provinsi"].nunique()):
            continue
        panel = panel.merge(feature, on=["provinsi", "tahun"], how="left")

    panel = panel[panel["provinsi"].notna()]
    return panel.sort_values(["provinsi", "tahun"]).reset_index(drop=True)


def attach_nlp_signal(panel: pd.DataFrame, nlp_by_year: pd.DataFrame | None = None) -> pd.DataFrame:
    """Gabungkan sinyal NLP (nasional per tahun) sebagai fitur fusion."""
    if nlp_by_year is None or nlp_by_year.empty:
        return panel
    return panel.merge(nlp_by_year, on="tahun", how="left")


def main() -> int:
    panel = build_province_panel()
    out = processed("panel_provinsi.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(out, index=False)
    print(f"panel: {panel.shape} -> {out}")
    print(panel.head(8).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
