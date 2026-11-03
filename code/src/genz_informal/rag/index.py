"""Indeks RAG atas metadata statistik (SIRUSA/StatMetaQA + katalog indikator).

Retrieval berbasis TF-IDF (tanpa model bahasa besar) sehingga ringan dan
reproducible. Bila tersedia LLM, modul `chat.py` dapat merangkai jawaban.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import pandas as pd

from ..paths import processed, raw


@dataclass
class RagIndex:
    texts: list[str]
    meta: list[dict]
    vectorizer: object = None
    matrix: object = None


def _load_documents() -> tuple[list[str], list[dict]]:
    texts: list[str] = []
    meta: list[dict] = []

    ind = raw("bps", "indicators.csv")
    if ind.exists():
        df = pd.read_csv(ind).drop_duplicates(subset=["var_id"])
        for _, row in df.iterrows():
            texts.append(f"Indikator {row['var_id']}: {row['var_name']} (dimensi {row['dimensi']})")
            meta.append({"tipe": "indikator_bps", "var_id": int(row["var_id"]),
                         "nama": row["var_name"]})

    facts = processed("nlp_by_year.csv")
    if facts.exists():
        df = pd.read_csv(facts)
        for _, row in df.iterrows():
            texts.append(f"Sinyal NLP tahun {row['tahun']}: " +
                         ", ".join(f"{c}={row[c]:.3f}" for c in df.columns if c != "tahun"))
            meta.append({"tipe": "sinyal_nlp", "tahun": str(row["tahun"])})
    return texts, meta


def build() -> RagIndex:
    from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: PLC0415
    texts, meta = _load_documents()
    if not texts:
        return RagIndex([], [], None, None)
    vec = TfidfVectorizer(ngram_range=(1, 2))
    matrix = vec.fit_transform(texts)
    return RagIndex(texts, meta, vec, matrix)


def search(index: RagIndex, query: str, k: int = 4) -> list[dict]:
    if index.vectorizer is None:
        return []
    from sklearn.metrics.pairwise import cosine_similarity  # noqa: PLC0415
    qv = index.vectorizer.transform([query])
    sims = cosine_similarity(qv, index.matrix).ravel()
    order = sims.argsort()[::-1][:k]
    return [{"text": index.texts[i], **index.meta[i], "score": float(sims[i])} for i in order]


def main() -> int:
    index = build()
    print(json.dumps(search(index, "informal provinsi"), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
