"""Ekstraksi faktor push-pull (NER/RE ringan berbasis leksikon).

Faktor: gaji/upah, fleksibilitas, kesehatan mental, keluarga, jaminan sosial.
"""

from __future__ import annotations

from typing import Sequence

FACTORS: dict[str, list[str]] = {
    "upah": ["gaji", "upah", "umr", "ump", "honor", "bayaran", "pendapatan", "income"],
    "fleksibilitas": ["fleksibel", "flexible", "waktu", "jam kerja", "work life", "wlb", "remote"],
    "kesehatan_mental": ["stres", "mental", "burnout", "capek", "depresi", "cemas", "lelah"],
    "keluarga": ["keluarga", "anak", "ibu", "bapak", "orang tua", "nikah", "nikah"],
    "jaminan_sosial": ["bpjs", "jaminan", "asuransi", "pesangon", "thr", "cuti", "kesehatan"],
    "pendidikan": ["kuliah", "ijazah", "jurusan", "gelar", "skill", "kursus", "pelatihan", "sertifikat"],
    "digital": ["online", "aplikasi", "internet", "ecommerce", "marketplace", "medsos", "tiktok"],
}


def extract(text: str) -> list[str]:
    low = (text or "").lower()
    return [name for name, kws in FACTORS.items() if any(kw in low for kw in kws)]


def extract_many(texts: Sequence[str]) -> list[list[str]]:
    return [extract(t) for t in texts]
