"""Klasifikasi emosi (6 kelas).

Fallback berbasis leksikon bila model transformer belum tersedia.
"""

from __future__ import annotations

from typing import Sequence

from ..annotation.schema import EMOTIONS, keyword_scores


class EmotionClassifier:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name
        self._pipe = None

    def _load(self):
        if self._pipe is not None:
            return
        from transformers import pipeline  # noqa: PLC0415
        self._pipe = pipeline("text-classification", model=self.model_name) if self.model_name else None

    def predict(self, texts: Sequence[str]) -> list[str]:
        if self.model_name:
            self._load()
            if self._pipe:
                return [r["label"].lower() for r in self._pipe(list(texts))]
        out: list[str] = []
        for text in texts:
            scores = keyword_scores(text, "emotion")
            best = max(scores.items(), key=lambda kv: kv[1]) if scores else ("neutral", 0)
            out.append(best[0] if best[1] > 0 else "neutral")
        return out
