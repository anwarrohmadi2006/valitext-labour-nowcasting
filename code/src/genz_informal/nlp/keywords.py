"""Taksonomi kata kunci untuk SELEKSI KORPUS (pra-anotasi).

Disusun dari riset "apa yang diinginkan Gen Z" dan isu ketenagakerjaan:
  - Deloitte Global Gen Z & Millennial Survey 2025 (work-life balance, makna, belajar)
  - IDN Research (gaji, fleksibilitas, kendali; pengangguran muda 17,37%)
  - Jakpat 2024 (gaji kompetitif + insentif transparan, jam fleksibel)
  - CSIS 2026 (pengangguran muda terdidik, pendidikan belum menjawab kebutuhan)
  - Apindo 2025 (17% Gen Z menganggur), BPS Feb-2025 (3,55 juta penganggur 15-24)

Ini PRA-FILTER, bukan pengganti anotasi manusia.
"""

from __future__ import annotations

import re

THEMES: dict[str, list[str]] = {
    "aspirasi_kerja_ideal": [
        r"work.?life.?balance", r"\bwlb\b", r"\bfleksib\w+", r"\bflexible\b", r"\bremote\b",
        r"\bhybrid\b", r"makna kerja", r"\bpassion\b", r"bermakna", r"\bpurpose\b",
        r"gaji (besar|tinggi|layak)", r"career growth", r"pengembangan diri",
        r"jam kerja", r"kerja santai", r"\bmindful\b", r"kesehatan mental", r"toxic",
    ],
    "kekecewaan_pasar_kerja": [
        r"susah (cari )?kerja", r"sulit (dapat|nyari) kerja", r"fresh ?graduat\w*",
        r"fresh ?grad", r"\bnganggur\b", r"pengangguran", r"ditolak", r"\breject\b",
        r"\blamaran\b", r"melamar", r"\bapply\b", r"\binterview\b", r"\bgap ?year\b",
        r"persaingan", r"kompetitif", r"lowongan", r"\bloker\b", r"sulit kerja",
    ],
    "kritik_kebijakan_kerja": [
        r"lapangan kerja", r"kemnaker", r"kebijakan (upah|kerja|tenaga)", r"\bphk\b",
        r"\bump\b", r"\bumr\b", r"tenaga kerja", r"\bapindo\b", r"bonus demografi",
        r"pemerintah (gagal|belum)", r"pengangguran (muda|gen z)",
    ],
    "informal_gig": [
        r"\bojol\b", r"driver online", r"\bgojek\b", r"\bgrab\b", r"\bfreelance\w*\b",
        r"\bkontrak\b", r"outsourc\w+", r"\bmagang\b", r"\binternship\b", r"part.?time",
        r"paruh waktu", r"jualan online", r"\bumkm\b", r"wirausaha", r"\bmitra\b",
        r"pekerja (lepas|bebas)",
    ],
    "keamanan_sosial": [
        r"\bbpjs\b", r"jaminan sosial", r"\bpesangon\b", r"\bjht\b", r"\bjkk\b", r"\bjkm\b",
        r"\bthr\b", r"cuti", r"tidak (ada )?jaminan", r"tanpa jaminan",
    ],
}

_COMPILED = {k: [re.compile(p, re.I) for p in v] for k, v in THEMES.items()}


def match_themes(text: str) -> list[str]:
    low = text or ""
    return [t for t, pats in _COMPILED.items() if any(p.search(low) for p in pats)]


def theme_hits(text: str) -> dict[str, int]:
    low = text or ""
    return {t: sum(1 for p in pats if p.search(low)) for t, pats in _COMPILED.items()}
