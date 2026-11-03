"""Bangun korpus dari data mentah media sosial: Reddit, Threads, Quora.

Alur: data/raw/{reddit,threads,quora}  ->  praproses + anonimisasi  ->  data/processed/corpus.csv
Kanal berita (Antara) sengaja tidak dipakai lagi: ia hanya menyediakan cakupan
provinsi-tahun yang terlalu tipis, sehingga tidak menambah daya prediksi.
"""

from __future__ import annotations

import glob
import json
from pathlib import Path

import pandas as pd

from ..annotation.schema import (
    argmax_or_default, keyword_scores, guideline_markdown,
)
from ..nlp.preprocess import clean_dataframe, corpus_stats
from ..paths import ensure, processed, raw


SOCIAL_SOURCES = {"reddit", "threads", "quora"}


def load_raw() -> pd.DataFrame:
    rows: list[dict] = []
    for path in glob.glob(str(raw("**", "*.jsonl")), recursive=True):
        parts = Path(path).parts
        if not (SOCIAL_SOURCES & set(parts)):
            continue
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return pd.DataFrame(rows)


def label_row(errors: str) -> dict:
    return {
        "sentiment": argmax_or_default(keyword_scores(errors, "sentiment"), "netral"),
        "emotion": argmax_or_default(keyword_scores(errors, "emotion"), "neutral"),
        "stance": argmax_or_default(keyword_scores(errors, "stance"), "netral"),
        "dilemma": argmax_or_default(keyword_scores(errors, "dilemma"), "lainnya"),
    }


def build() -> pd.DataFrame:
    df = load_raw()
    if df.empty:
        return df
    df = clean_dataframe(df)
    labels = df["text"].map(label_row).apply(pd.Series)
    df = pd.concat([df, labels], axis=1)
    return df


def main() -> int:
    df = build()
    if df.empty:
        print("Tidak ada data mentah. Jalankan scripts/pull_reddit.py dulu.")
        return 1
    out = ensure(processed("corpus.csv"))
    df.to_csv(out, index=False)
    try:  # parquet opsional
        df.to_parquet(processed("corpus.parquet"), index=False)
    except Exception:  # noqa: BLE001
        pass

    stats = corpus_stats(df)
    sheet = ensure(processed("DATASHEET.md"))
    sheet.write_text(
        "# Datasheet Korpus\n\n"
        f"- Jumlah dokumen: {stats['n_docs']}\n"
        f"- Token rata-rata: {stats['token_mean']:.1f} (median {stats['token_median']:.0f})\n"
        f"- Sumber: {', '.join(sorted(df['source'].unique()))}\n"
        f"- Rentang tanggal: {df['date'].min()} s/d {df['date'].max()}\n"
        "- Anonimisasi: nama penulis di-hash (SHA-256, salted); teks tidak dipublikasikan verbatim.\n"
        "- Lisensi/kepatuhan: UU PDP No. 27/2022; retensi minimum; hapus-saat-dihapus.\n\n"
        "## Distribusi label kasar (leksikon)\n\n"
        + df["dilemma"].value_counts().to_markdown()
        + "\n\n"
        + guideline_markdown(),
        encoding="utf-8",
    )
    print(f"korpus: {len(df)} dok -> {out}")
    print(stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
