"""Pemodelan topik (penemuan dilema).

Prioritas: pakai BERTopic bila terpasang. Jika tidak, gunakan pipeline
setara buatan sendiri: UMAP -> HDBSCAN -> c-TF-IDF.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np

try:  # opsional
    from bertopic import BERTopic  # type: ignore
    _HAS_BERTOPIC = True
except Exception:  # noqa: BLE001
    _HAS_BERTOPIC = False


@dataclass
class TopicResult:
    topics: list[int]
    keywords: dict[int, list[str]] = field(default_factory=dict)
    n_topics: int = 0
    method: str = "fallback"


def _c_tfidf(texts: Sequence[str], topics: list[int]) -> dict[int, list[str]]:
    """c-TF-IDF dengan stopword Indonesia+Inggris dan token huruf saja.

    Sebelumnya memakai `stop_words=None`, sehingga kata kunci didominasi kata
    fungsi (`yang, dan, di, saya, gw, the`) dan metrik koherensi menjadi tidak
    bermakna. Lihat docs/DESAIN-PENELITIAN.md.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: PLC0415

    from .stopwords import STOPWORDS
    groups: dict[int, list[str]] = {}
    for text, topic in zip(texts, topics):
        if topic == -1:
            continue
        groups.setdefault(topic, []).append(text)
    if not groups:
        return {}
    keys = list(groups)
    docs = [" ".join(groups[k]) for k in keys]
    vec = TfidfVectorizer(
        max_features=5000, ngram_range=(1, 2), stop_words=list(STOPWORDS),
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z\-]{2,}\b",
    )
    matrix = vec.fit_transform(docs)
    terms = np.array(vec.get_feature_names_out())
    out: dict[int, list[str]] = {}
    for i, key in enumerate(keys):
        row = matrix[i].toarray().ravel()
        top = row.argsort()[::-1][:10]
        out[key] = [terms[j] for j in top if row[j] > 0]
    return out


def fit_topics(
    texts: Sequence[str], embeddings: np.ndarray, min_topic_size: int = 10,
    n_neighbors: int = 15, use_bertopic: bool | None = None, random_state: int = 42,
) -> TopicResult:
    texts = list(texts)
    if len(texts) < min_topic_size * 2:
        # Korpus terlalu kecil: satu topik saja.
        return TopicResult(topics=[0] * len(texts), keywords={0: []}, n_topics=1,
                           method="trivial")

    if (use_bertopic or _HAS_BERTOPIC) and _HAS_BERTOPIC:
        model = BERTopic(min_topic_size=min_topic_size, calculate_probabilities=False,
                         verbose=False)
        topics, _ = model.fit_transform(texts, embeddings)
        kw = {t: [w for w, _ in model.get_topic(t) or []] for t in set(topics)}
        return TopicResult(topics=list(topics), keywords=kw,
                           n_topics=len({t for t in topics if t != -1}), method="bertopic")

    # Fallback: UMAP -> HDBSCAN -> c-TF-IDF
    import umap  # noqa: PLC0415
    from sklearn.cluster import HDBSCAN  # noqa: PLC0415
    reducer = umap.UMAP(n_neighbors=n_neighbors, n_components=5, metric="cosine",
                        random_state=random_state)
    reduced = reducer.fit_transform(embeddings)
    clusterer = HDBSCAN(min_cluster_size=min_topic_size, metric="euclidean")
    topics = clusterer.fit_predict(reduced).tolist()
    kw = _c_tfidf(texts, topics)
    return TopicResult(topics=topics, keywords=kw,
                       n_topics=len({t for t in topics if t != -1}), method="umap_hdbscan")
