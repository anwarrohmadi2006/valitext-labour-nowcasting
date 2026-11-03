"""Dasbor Web-DSS (Streamlit).

Jalankan: streamlit run src/genz_informal/dss/app.py
Fitur: (1) sebaran informal per provinsi, (2) visualisasi NLP,
(3) What-If simulator, (4) penjelasan faktor (bila tersedia).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from genz_informal.paths import outputs, processed  # noqa: E402

st.set_page_config(page_title="Web-DSS Gen Z Informal", layout="wide")
st.title("Web-DSS : Dilema Pekerjaan Gen Z di Sektor Informal")
st.caption("Prototipe STIS × Kemnaker 2026 · data agregat BPS + korpus media sosial")


def _read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


tab1, tab2, tab3, tab4 = st.tabs(["Sebaran Informal", "Visualisasi NLP", "What-If", "Penjelasan"])

with tab1:
    st.subheader("Proporsi pekerja informal menurut provinsi (BPS, agregat)")
    panel = _read(processed("panel_provinsi.csv"))
    if panel.empty:
        st.warning("panel_provinsi.csv belum ada : jalankan pipeline dulu.")
    else:
        latest = panel.sort_values("tahun").groupby("provinsi").tail(1).sort_values("informal_pct")
        fig = px.bar(latest, x="informal_pct", y="provinsi", orientation="h",
                     labels={"informal_pct": "Proporsi informal (%)", "provinsi": ""})
        fig.update_layout(height=max(400, 18 * len(latest)))
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Komposisi dilema & emosi dari korpus")
    corpus = _read(processed("corpus.csv"))
    if corpus.empty:
        st.warning("corpus.csv belum ada")
    else:
        c1, c2 = st.columns(2)
        with c1:
            counts = corpus["dilemma"].value_counts().reset_index()
            counts.columns = ["dilemma", "jumlah"]
            st.plotly_chart(px.bar(counts, x="jumlah", y="dilemma", orientation="h",
                                   title="Dilema"), use_container_width=True)
        with c2:
            ec = corpus["emotion"].value_counts().reset_index()
            ec.columns = ["emosi", "jumlah"]
            st.plotly_chart(px.pie(ec, names="emosi", values="jumlah", title="Emosi"),
                            use_container_width=True)

with tab3:
    st.subheader("What-If Simulator (indikatif, bukan kausal)")
    panel = _read(processed("panel_provinsi.csv"))
    if panel.empty:
        st.warning("panel belum tersedia")
    else:
        prov = st.selectbox("Provinsi", sorted(panel["provinsi"].unique()))
        delta = st.slider("Perubahan upah minimum (%)", -20, 30, 10)
        sub = panel[panel["provinsi"] == prov].sort_values("tahun")
        base = float(sub["informal_pct"].iloc[-1])
        projected = base * (1 + (-0.15) * (delta / 100.0))
        st.metric("Informal saat ini", f"{base:.2f}%", f"{projected - base:+.2f} pp (proyeksi)")
        st.info("Angka proyeksi memakai elastisitas asosiatif; bukan estimasi kausal.")

with tab4:
    st.subheader("Penjelasan faktor (SHAP/EBM)")
    imp = outputs("feature_importance.csv")
    if imp.exists():
        df = pd.read_csv(imp)
        st.plotly_chart(px.bar(df, x="importance", y="feature", orientation="h"),
                        use_container_width=True)
    else:
        st.warning("feature_importance.csv belum ada : jalankan pipeline.")
