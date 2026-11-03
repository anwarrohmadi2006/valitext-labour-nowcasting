"""Deteksi stance: informal sebagai pilihan vs keterpaksaan."""

from __future__ import annotations

from typing import Sequence

from ..annotation.schema import keyword_scores


def predict(texts: Sequence[str]) -> list[str]:
    out: list[str] = []
    for text in texts:
        scores = keyword_scores(text, "stance")
        pro = scores.get("pilihan_sukarela", 0)
        con = scores.get("keterpaksaan", 0)
        if pro > con:
            out.append("pilihan_sukarela")
        elif con > pro:
            out.append("keterpaksaan")
        else:
            out.append("netral")
    return out
