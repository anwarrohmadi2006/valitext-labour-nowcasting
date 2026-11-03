"""Embedding dokumen.

Dua mode:
  - "indobertweet": mean-pooling IndoBERTweet via transformers (butuh unduh model).
  - "tfidf": TF-IDF + SVD (cepat, tanpa unduh; dipakai untuk demo & fallback).
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

DEFAULT_MODEL = "indolem/indobertweet-base-uncased"


class Embedder:
    def __init__(self, method: str = "tfidf", model_name: str = DEFAULT_MODEL, dim: int = 256):
        self.method = method
        self.model_name = model_name
        self.dim = dim
        self._tok = None
        self._model = None
        self._tfidf = None
        self._svd = None

    # -- IndoBERTweet -----------------------------------------------------
    def _load_transformer(self):
        if self._model is not None:
            return
        from transformers import AutoModel, AutoTokenizer  # noqa: PLC0415
        self._tok = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModel.from_pretrained(self.model_name)
        self._model.eval()

    def _encode_transformer(self, texts: Sequence[str], batch: int = 16) -> np.ndarray:
        import torch  # noqa: PLC0415
        self._load_transformer()
        out: list[np.ndarray] = []
        for i in range(0, len(texts), batch):
            chunk = list(texts[i : i + batch])
            enc = self._tok(chunk, padding=True, truncation=True, max_length=128,
                            return_tensors="pt")
            with torch.no_grad():
                hidden = self._model(**enc).last_hidden_state
            mask = enc["attention_mask"].unsqueeze(-1).float()
            pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
            out.append(pooled.cpu().numpy())
        return np.vstack(out) if out else np.zeros((0, 768))

    # -- TF-IDF -----------------------------------------------------------
    def _encode_tfidf(self, texts: Sequence[str], fit: bool) -> np.ndarray:
        from sklearn.decomposition import TruncatedSVD  # noqa: PLC0415
        from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: PLC0415
        if fit:
            self._tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), min_df=2)
            matrix = self._tfidf.fit_transform(texts)
            k = min(self.dim, matrix.shape[1] - 1) if matrix.shape[1] > 1 else 2
            self._svd = TruncatedSVD(n_components=k, random_state=42)
            return self._svd.fit_transform(matrix)
        if self._tfidf is None:
            raise RuntimeError("TF-IDF belum di-fit; panggil encode(..., fit=True)")
        return self._svd.transform(self._tfidf.transform(texts))

    # -- API --------------------------------------------------------------
    def encode(self, texts: Sequence[str], fit: bool = False) -> np.ndarray:
        if self.method == "indobertweet":
            return self._encode_transformer(texts)
        return self._encode_tfidf(texts, fit=fit)
