"""Penarikan data Quora.

PENTING (hasil verifikasi): **Quora tidak memiliki API resmi untuk konten**.
Halaman dokumentasi API-nya tidak lagi melayani konten, dan pustaka tidak resmi
terakhir diperbarui 2015. API Poe (2025) adalah gerbang model AI, bukan sumber
data tanya-jawab. Karena itu modul ini TIDAK melakukan skraping otomatis.

Jalur yang disediakan (patuh ToS / etika):
  1. `ingest_manual_jsonl()` : impor berkas JSONL yang disiapkan peneliti
     (mis. ekspor resmi Quora, atau kutipan manual yang lolos telaah etika).
  2. `template_record()` : format baris yang diharapkan.

Format tiap baris:
  {"title": "...", "body": "...", "url": "...", "date": "YYYY-MM-DD",
   "topic": "opsional", "author": "opsional"}

Rujukan: riset internal (Quora tanpa API resmi); Simanjuntak dkk. (2022) untuk
inferensi lokasi teks Indonesia bila diperlukan.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


def template_record() -> dict[str, Any]:
    return {"title": "", "body": "", "url": "", "date": "", "topic": "", "author": ""}


def _to_doc(rec: dict[str, Any]) -> dict[str, Any]:
    title = (rec.get("title") or "").strip()
    body = (rec.get("body") or "").strip()
    return {
        "source": "quora",
        "subreddit": None,
        "author": rec.get("author") or "",
        "date": rec.get("date") or None,
        "title": title,
        "body": body,
        "text": f"{title}\n{body}".strip(),
        "url": rec.get("url") or "",
        "score": None,
        "num_comments": None,
        "topic": rec.get("topic") or "",
    }


def ingest_manual_jsonl(path: str | Path) -> list[dict[str, Any]]:
    """Muat korpus Quora yang disiapkan manual (satu objek JSON per baris)."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"{p} tidak ada. Siapkan berkas JSONL Quora (lihat template_record())."
        )
    docs = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            docs.append(_to_doc(json.loads(line)))
    return docs


def is_available(path: str | Path = "data/raw/quora/manual.jsonl") -> bool:
    return Path(path).exists()


def iter_records(docs: Iterable[dict[str, Any]]):
    for d in docs:
        yield json.dumps(d, ensure_ascii=False)
