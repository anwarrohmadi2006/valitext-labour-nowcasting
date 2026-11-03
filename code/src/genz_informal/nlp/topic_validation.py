"""Validasi topik BERTopic (BERTopic-as-measurement).

Menyediakan metrik yang diminta reviewer statistik:
  - outlier share (sebelum/sesudah reduksi)
  - topic diversity (Dieng dkk., 2020)
  - topic uniqueness (Nan dkk., 2019)
  - coherence NPMI (implementasi ringan; padanan c_npmi Röder dkk., 2015)
  - stabilitas antar-seed (Jaccard)

Rujukan: Grootendorst (2022); de Groot dkk. (2022); Nur'aini dkk. (2026);
Borčin & Jose (2024); Tong dkk. (2026).
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable, Sequence

import numpy as np


def _tokens(texts: Sequence[str]) -> list[list[str]]:
    return [re.findall(r"\w+", (t or "").lower()) for t in texts]


def outlier_share(topics: Sequence[int]) -> float:
    topics = list(topics)
    if not topics:
        return 0.0
    return float(sum(1 for t in topics if t == -1) / len(topics))


def topic_diversity(keywords: dict[int, list[str]], top_n: int = 10) -> float:
    words = [w for t, ws in keywords.items() if t != -1 for w in ws[:top_n]]
    if not words:
        return 0.0
    return float(len(set(words)) / len(words))


def topic_uniqueness(keywords: dict[int, list[str]], top_n: int = 10) -> float:
    """Rata-rata proporsi kata topik yang tidak muncul di topik lain."""
    per_topic = {t: set(ws[:top_n]) for t, ws in keywords.items() if t != -1 and ws}
    if not per_topic:
        return 0.0
    scores = []
    for t, ws in per_topic.items():
        others = set().union(*(w for o, w in per_topic.items() if o != t)) if len(per_topic) > 1 else set()
        if ws:
            scores.append(len(ws - others) / len(ws))
    return float(np.mean(scores)) if scores else 0.0


def npmi_coherence(
    keywords: dict[int, list[str]], texts: Sequence[str], top_n: int = 10,
) -> float:
    """Rata-rata NPMI pasangan kata (ko-occurrence tingkat dokumen).

    Padanan ringan untuk c_npmi tanpa dependensi gensim.
    """
    docs = [set(toks) for toks in _tokens(texts)]
    n_docs = len(docs) or 1
    dfreq: Counter[str] = Counter()
    for d in docs:
        dfreq.update(d)
    topic_scores: list[float] = []
    for t, ws in keywords.items():
        if t == -1:
            continue
        top = [w for w in ws[:top_n] if w]
        if len(top) < 2:
            continue
        pair_scores: list[float] = []
        for i in range(len(top)):
            for j in range(i + 1, len(top)):
                wi, wj = top[i], top[j]
                pw = dfreq[wi] / n_docs
                pv = dfreq[wj] / n_docs
                co = sum(1 for d in docs if wi in d and wj in d) / n_docs
                if co <= 0 or pw <= 0 or pv <= 0:
                    pair_scores.append(-1.0)
                    continue
                pmi = math.log(co / (pw * pv))
                pair_scores.append(pmi / (-math.log(co)))
        if pair_scores:
            topic_scores.append(float(np.mean(pair_scores)))
    return float(np.mean(topic_scores)) if topic_scores else 0.0


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def seed_stability(
    keywords_runs: Sequence[dict[int, list[str]]], top_n: int = 10,
) -> float:
    """Rata-rata Jaccard antar-run (best-match per topik), lintas seed."""
    sets_runs = [
        [set(ws[:top_n]) for t, ws in run.items() if t != -1 and ws]
        for run in keywords_runs
    ]
    sets_runs = [r for r in sets_runs if r]
    if len(sets_runs) < 2:
        return 1.0
    scores: list[float] = []
    for i in range(len(sets_runs)):
        for j in range(i + 1, len(sets_runs)):
            a, b = sets_runs[i], sets_runs[j]
            best = [max(_jaccard(topic, other) for other in b) for topic in a]
            scores.append(float(np.mean(best)) if best else 0.0)
    return float(np.mean(scores)) if scores else 0.0


@dataclass
class TopicValidationReport:
    n_docs: int
    n_topics: int
    outlier_share: float
    diversity: float
    uniqueness: float
    coherence_npmi: float
    seed_stability: float = float("nan")
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "n_docs": self.n_docs,
            "n_topics": self.n_topics,
            "outlier_share": round(self.outlier_share, 4),
            "topic_diversity": round(self.diversity, 4),
            "topic_uniqueness": round(self.uniqueness, 4),
            "coherence_npmi": round(self.coherence_npmi, 4),
            "seed_stability_jaccard": (None if self.seed_stability != self.seed_stability
                                       else round(self.seed_stability, 4)),
        }

    def to_markdown(self) -> str:
        lines = ["| metrik | nilai |", "|---|---|"]
        for key, value in self.to_dict().items():
            lines.append(f"| {key} | {value} |")
        if self.notes:
            lines.append("")
            for note in self.notes:
                lines.append(f"- {note}")
        return "\n".join(lines)


def validate(
    texts: Sequence[str], topics: Sequence[int], keywords: dict[int, list[str]],
    top_n: int = 10, seed_runs: Sequence[dict[int, list[str]]] | None = None,
) -> TopicValidationReport:
    notes = [
        "Outlier (label -1) dilaporkan apa adanya; HDBSCAN pada teks pendek dapat "
        "menandai 49-74% dokumen (de Groot dkk., 2022; Nur'aini dkk., 2026).",
        "Gunakan reduce_outliers() untuk mitigasi dan laporkan share sebelum & sesudah.",
        "Koherensi otomatis != validitas; wajib disertai human audit (Tong dkk., 2026).",
    ]
    return TopicValidationReport(
        n_docs=len(texts),
        n_topics=len({t for t in topics if t != -1}),
        outlier_share=outlier_share(topics),
        diversity=topic_diversity(keywords, top_n),
        uniqueness=topic_uniqueness(keywords, top_n),
        coherence_npmi=npmi_coherence(keywords, texts, top_n),
        seed_stability=(seed_stability(seed_runs, top_n) if seed_runs else float("nan")),
        notes=notes,
    )


def validate_across_seeds(
    texts: Sequence[str], embeddings_fn: Callable[[int], np.ndarray],
    fit_fn: Callable[[Sequence[str], np.ndarray, int], object],
    seeds: Sequence[int] = (42, 1, 7), top_n: int = 10, min_topic_size: int = 8,
) -> tuple[TopicValidationReport, dict[int, list[str]], list[int]]:
    """Jalankan fit_topics lintas seed, kembalikan laporan + hasil seed pertama."""
    runs = []
    first_kw: dict[int, list[str]] = {}
    first_topics: list[int] = []
    for k, seed in enumerate(seeds):
        emb = embeddings_fn(seed)
        result = fit_fn(texts, emb, min_topic_size)  # type: ignore[misc]
        runs.append(result.keywords)  # type: ignore[attr-defined]
        if k == 0:
            first_kw = result.keywords  # type: ignore[attr-defined]
            first_topics = result.topics  # type: ignore[attr-defined]
    report = validate(texts, first_topics, first_kw, top_n=top_n, seed_runs=runs)
    return report, first_kw, first_topics
