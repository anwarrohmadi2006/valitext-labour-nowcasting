"""Filter ketat "narasi kerja" untuk korpus.

Tujuan: sisakan dokumen yang benar-benar bercerita tentang pekerjaan/kondisi
kerja, buang keuangan pribadi, pajak, investasi, berita, dan spam.

Aturan (transparan):
  keep  <=  labour_hits >= 1
            AND labour_hits > finance_hits
            AND news_hits == 0
            AND spam_hits == 0
            AND bukan sekadar tanya produk keuangan
"""

from __future__ import annotations

import re

LABOUR = [
    r"\bkerja\b", r"\bkerjaan\b", r"\bbekerja\b", r"\bpekerja\b", r"\bpekerjaan\b",
    r"\bkaryawan\b", r"\bburuh\b", r"\bpegawai\b", r"\bmagang\b", r"\binternship\b",
    r"\bfreelance\w*\b", r"\bkontrak kerja\b", r"\bphk\b", r"\bresign\b", r"\bresign\b",
    r"\blowongan\b", r"\bloker\b", r"\brekrut\w*\b", r"\binterview\b", r"\bwawancara kerja\b",
    r"\bgaji\b", r"\bupah\b", r"\bumr\b", r"\bump\b", r"\bumk\b", r"\bhonor\b",
    r"\blembur\b", r"\bovertime\b", r"\batasan\b", r"\bkantor\b", r"\bpesangon\b",
    r"\btunjangan\b", r"\bbpjs\b", r"\bkarir\b", r"\bkarier\b", r"\bcareer\b",
    r"\bmelamar\b", r"\blamaran\b", r"\bmutasi\b", r"\bcuti\b", r"\bpensiun\b",
    r"\bwirausaha\b", r"\bjam kerja\b", r"\bkerja remote\b", r"\bremote\b",
    r"\bgaji pokok\b", r"\bthp\b", r"\btake home pay\b", r"\bprobation\b",
]

FINANCE = [
    r"\bkartu kredit\b", r"\bmiles\b", r"\bcashback\b", r"\bpaylater\b", r"\bsaham\b",
    r"\betf\b", r"\breksadana\b", r"\bdeposito\b", r"\blps\b", r"\bobligasi\b",
    r"\bemas\b", r"\bpajak\b", r"\bnpwp\b", r"\bspt\b", r"\bcoretax\b", r"\bpph\b",
    r"\bppn\b", r"\bbea cukai\b", r"\bunit link\b", r"\bkpr\b", r"\bdana darurat\b",
    r"\binvestasi\b", r"\bpinjol\b", r"\bpaypal\b", r"\bpayoneer\b", r"\bwise\b",
    r"\bbunga\b", r"\bcicilan\b", r"\bcrypto\b", r"\bbitcoin\b", r"\bihsg\b",
]

NEWS = [
    # Catatan: sebelumnya ada pola "\bantara\b" yang memakai huruf Cyrillic 'а'
    # (U+0430), sehingga tidak pernah cocok. Perbaikan naif berbahaya karena
    # "antara" juga kata depan umum ("antara A dan B"). Karena itu dipakai pola
    # yang terdisambiguasi ke lembaga berita, bukan katanya.
    r"\bkantor berita\b", r"\bantara news\b", r"\bantaranews\b",
    r"\bpemerintah\b", r"\bpresiden\b", r"\bmenteri\b", r"\bpasal\b", r"\buu\b",
    r"\bdpr\b", r"\bpolisi\b", r"\bkompas\b", r"\bdetik\b",
    r"\bberita\b", r"\bkasus\b", r"\bkorupsi\b",
]

SPAM = [r"\bjudi\b", r"\bslot\b", r"\bpoker\b", r"\bbonus new member\b", r"\bmaxwin\b"]


def _hits(text: str, patterns: list[str]) -> int:
    low = (text or "").lower()
    return sum(1 for p in patterns if re.search(p, low))


def score(text: str) -> dict[str, int]:
    return {
        "labour": _hits(text, LABOUR),
        "finance": _hits(text, FINANCE),
        "news": _hits(text, NEWS),
        "spam": _hits(text, SPAM),
    }


def is_labour_narrative(text: str) -> bool:
    s = score(text)
    return (s["labour"] >= 1 and s["labour"] > s["finance"]
            and s["news"] == 0 and s["spam"] == 0)
