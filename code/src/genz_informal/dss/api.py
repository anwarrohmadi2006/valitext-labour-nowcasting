"""API layanan Web-DSS (FastAPI).

Endpoints:
  GET /health
  GET /informal/shared          -> proporsi informal per provinsi (BPS)
  GET /nlp/dilemmas             -> komposisi dilema dari korpus
  POST /what-if                 -> simulasi sederhana (berbasis model, bukan kausal)
"""

from __future__ import annotations

from functools import lru_cache

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ..paths import processed

app = FastAPI(title="Web-DSS Gen Z Informal", version="0.1.0")


@lru_cache(maxsize=1)
def _panel() -> pd.DataFrame:
    path = processed("panel_provinsi.csv")
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@lru_cache(maxsize=1)
def _corpus() -> pd.DataFrame:
    path = processed("corpus.csv")
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


class WhatIfRequest(BaseModel):
    provinsi: str
    delta_upah_pct: float = 0.0


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "panel_rows": int(len(_panel())), "corpus_rows": int(len(_corpus()))}


@app.get("/informal/shared")
def informal_share() -> list[dict]:
    panel = _panel()
    if panel.empty or "informal_pct" not in panel:
        raise HTTPException(404, "panel belum tersedia")
    latest = panel.dropna(subset=["informal_pct"]).sort_values("tahun").groupby("provinsi").tail(1)
    return latest[["provinsi", "tahun", "informal_pct"]].to_dict(orient="records")


@app.get("/nlp/dilemmas")
def nlp_dilemmas() -> list[dict]:
    corpus = _corpus()
    if corpus.empty:
        raise HTTPException(404, "korpus belum tersedia")
    counts = corpus["dilemma"].value_counts()
    share = (counts / counts.sum()).round(4)
    return [{"dilemma": k, "share": float(v)} for k, v in share.items()]


@app.post("/what-if")
def what_if(req: WhatIfRequest) -> dict:
    """Simulasi indikatif. Bukan klaim kausal: hanya elastisitas asosiatif kasar."""
    panel = _panel()
    if panel.empty:
        raise HTTPException(404, "panel belum tersedia")
    sub = panel[panel["provinsi"] == req.provinsi].dropna(subset=["informal_pct"]).sort_values("tahun")
    if sub.empty:
        raise HTTPException(404, f"provinsi tidak ditemukan: {req.provinsi}")
    base = float(sub["informal_pct"].iloc[-1])
    assumed_elasticity = -0.15  # asumsi indikatif: upah naik -> informal turun (asosiatif)
    projected = base * (1 + assumed_elasticity * (req.delta_upah_pct / 100.0))
    return {
        "provinsi": req.provinsi,
        "informal_base_pct": round(base, 2),
        "delta_upah_pct": req.delta_upah_pct,
        "informal_projected_pct": round(projected, 2),
        "catatan": "Simulasi indikatif berbasis asosiasi, BUKAN estimasi kausal.",
    }
