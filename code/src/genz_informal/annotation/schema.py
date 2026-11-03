"""Skema anotasi multi-tugas + leksikon kata kunci (fallback tanpa anotasi manual).

Tugas: sentimen (3 kelas), emosi (6 kelas), topik, stance (pilihan vs
keterpaksaan), dan 7 kandidat dilema ketenagakerjaan Gen Z.
"""

from __future__ import annotations

SENTIMENT = ["negatif", "netral", "positif"]

EMOTIONS = ["anxiety", "burnout", "hope", "pride", "frustration", "resignation"]

STANCE = ["pilihan_sukarela", "keterpaksaan", "netral"]

DILEMMAS = [
    "gaji_vs_ekspektasi",
    "fleksibilitas_vs_jaminan",
    "skill_mismatch",
    "burnout_formal",
    "pride_entrepreneur",
    "pendidikan_vs_pekerjaan",
    "stabilitas_vs_kebebasan",
]

# Leksikon kasar untuk demonstran pipeline (bukan pengganti anotasi manusia).
LEXICON: dict[str, dict[str, list[str]]] = {
    "emotion": {
        "anxiety": ["takut", "cemas", "khawatir", "was-was", "deg-degan", "gak tenang"],
        "burnout": ["capek", "burnout", "lelah", "jenuh", "stres", "overwork", "drama"],
        "hope": ["semoga", "harap", "berharap", "peluang", "kesempatan", "insyaallah"],
        "pride": ["bangga", "senang", "bahagia", "mandiri", "ngembangin", "progress"],
        "frustration": ["kesal", "sebal", "nyebelin", "gak fair", "dibayar", "nunggak", "dipaksa"],
        "resignation": ["pasrah", "udah gitu aja", "gimana lagi", "terpaksa", "ngikut aja"],
    },
    "stance": {
        "pilihan_sukarela": ["pilih", "memilih", "suka", "enjoy", "mending", "lebih baik", "bebas"],
        "keterpaksaan": ["terpaksa", "gak ada pilihan", "susah cari", "gak keterima",
                          "mau gimana lagi", "dipaksa keadaan"],
    },
    "dilemma": {
        "gaji_vs_ekspektasi": ["umr", "ump", "upah", "gaji kecil", "gaji ga cukup", "gaji rendah"],
        "fleksibilitas_vs_jaminan": ["fleksibel", "flexible", "bpjs", "jaminan", "asuransi",
                                      "pesangon", "kontrak", "freelance"],
        "skill_mismatch": ["gak sesuai jurusan", "skill", "pengalaman", "fresh graduate",
                            "serba salah", "ilmu gak kepake"],
        "burnout_formal": ["lembur", "overtime", "burnout", "stres kantor", "atasan", "toxic"],
        "pride_entrepreneur": ["usaha", "bisnis", "jualan", "wirausaha", "owner", "brand", "branding"],
        "pendidikan_vs_pekerjaan": ["kuliah", "ijazah", "gelar", "diploma", "smk", "sarjana"],
        "stabilitas_vs_kebebasan": ["stabil", "tetap", "kontrak", "proyek", "serabutan",
                                     "ganti kerja", "kebebasan"],
    },
    "sentiment": {
        "negatif": ["susah", "sulit", "mahal", "sedih", "kecewa", "parah", "payah", "jelek",
                     "gagal", "nggak", "gak", "tidak", "capek", "stres", "masalah"],
        "positif": ["senang", "bagus", "enak", "suka", "mantap", "berhasil", "semangat",
                     "untung", "mudah", "terima kasih"],
    },
}


def keyword_scores(text: str, group: str) -> dict[str, int]:
    low = (text or "").lower()
    table = LEXICON.get(group, {})
    return {label: sum(low.count(kw) for kw in kws) for label, kws in table.items()}


def argmax_or_default(scores: dict[str, int], default: str) -> str:
    best = max(scores.items(), key=lambda kv: kv[1]) if scores else (default, 0)
    return best[0] if best[1] > 0 else default


def guideline_markdown() -> str:
    lines = ["# Pedoman Anotasi Korpus", "", "## Tugas & Label", ""]
    lines += ["### Sentimen", *[f"- {s}" for s in SENTIMENT], ""]
    lines += ["### Emosi", *[f"- {e}" for e in EMOTIONS], ""]
    lines += ["### Stance", *[f"- {s}" for s in STANCE], ""]
    lines += ["### Dilema", *[f"- {d}" for d in DILEMMAS], ""]
    lines += [
        "## Aturan", "",
        "1. Anotasi label tunggal per tugas (single-label).",
        "2. Bila ragu, pilih `netral` dan catat di kolom catatan.",
        "3. Untuk validasi, anotasi ganda minimal 10% sampel; hitung Cohen's kappa.",
        "4. Jangan menyalin teks yang memuat data pribadi secara verbatim.",
    ]
    return "\n".join(lines)
