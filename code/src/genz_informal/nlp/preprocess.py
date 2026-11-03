"""Praproses teks informal Bahasa Indonesia.

Prinsip: JANGAN menghapus slang secara agresif (IndoBERTweet terbaik tanpa
normalisasi berat). Fokus pada: normalisasi URL/handle/emoji, anonimisasi
penulis, deduplikasi, dan penyaringan panjang minimum.
"""

from __future__ import annotations

import hashlib
import html
import re
from typing import Iterable

import pandas as pd

URL_RE = re.compile(r"https?://\S+|www\.\S+")
MENTION_RE = re.compile(r"@[\w.]+")
SPACE_RE = re.compile(r"[ \t]+")
HANDBOOK_RE = re.compile(r"&amp;|&lt;|&gt;|&quot;")

EMOJI_MAP = {
    "😂": " ketawa ", "🤣": " ketawa ", "😭": " menangis ", "😅": " lega ",
    "😊": " senang ", "🙂": " senang ", "😔": " sedih ", "😩": " lelah ",
    "😡": " marah ", "😤": " kesal ", "🔥": " semangat ", "💀": " mati ",
    "👍": " bagus ", "🙏": " mohon ", "💸": " uang ", "📉": " turun ",
    "😞": " kecewa ", "😴": " capek ",
}

STOPWORDS_MIN = {"yang", "di", "ke", "dan", "atau", "ini", "itu", "aku", "saya", "kamu"}


def _emoji_to_text(text: str) -> str:
    for emo, word in EMOJI_MAP.items():
        text = text.replace(emo, word)
    return text


def normalize(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = HANDBOOK_RE.sub(" ", text)
    text = _emoji_to_text(text)
    text = URL_RE.sub(" <url> ", text)
    text = MENTION_RE.sub(" @user ", text)
    text = text.replace("\r", " ").replace("\n", " ")
    text = SPACE_RE.sub(" ", text)
    return text.strip()


def token_count(text: str) -> int:
    return len(re.findall(r"\w+", text))


def anon_id(value: str, salt: str = "stis-kemnaker-2026") -> str:
    if not value:
        return ""
    digest = hashlib.sha256(f"{salt}:{value}".encode("utf-8")).hexdigest()
    return digest[:16]


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def has_indonesian_markers(text: str) -> bool:
    """Filter kasar: buang dokumen yang hampir pasti bukan Bahasa Indonesia."""
    low = f" {text.lower()} "
    markers = [" yang ", " dan ", " saya ", " aku ", " kerja ", " gaji ", " tidak ",
               " dengan ", " untuk ", " dari ", " kalau ", " udah ", " banget "]
    return any(m in low for m in markers)


def clean_dataframe(
    df: pd.DataFrame, text_col: str = "text", author_col: str = "author",
    min_tokens: int = 4, require_id_markers: bool = True,
) -> pd.DataFrame:
    df = df.copy()
    df[text_col] = df[text_col].fillna("").map(normalize)
    df["n_tokens"] = df[text_col].map(token_count)
    df = df[df["n_tokens"] >= min_tokens]
    if require_id_markers:
        df = df[df[text_col].map(has_indonesian_markers)]
    df["doc_hash"] = df[text_col].map(text_hash)
    df = df.drop_duplicates(subset="doc_hash")
    if author_col in df.columns:
        df["author_hash"] = df[author_col].fillna("").map(anon_id)
        df = df.drop(columns=[author_col])
    return df.reset_index(drop=True)


def corpus_stats(df: pd.DataFrame, text_col: str = "text") -> dict:
    return {
        "n_docs": int(len(df)),
        "n_unique": int(df["doc_hash"].nunique()) if "doc_hash" in df else int(len(df)),
        "token_mean": float(df["n_tokens"].mean()) if len(df) else 0.0,
        "token_median": float(df["n_tokens"].median()) if len(df) else 0.0,
    }


def iter_texts(df: pd.DataFrame, text_col: str = "text") -> Iterable[str]:
    yield from df[text_col].astype(str).tolist()
