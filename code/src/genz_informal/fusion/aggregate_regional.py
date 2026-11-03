"""Agregasi sinyal NLP per waktu (dan per subreddit sebagai proksi).

Catatan keterbatasan: data Reddit tidak memuat atribut provinsi, sehingga
agregasi spasial tidak dimungkinkan dari kanal ini; agregasi dilakukan per
tahun/bulan dan per subreddit. Untuk analisis spasial gunakan BPS.
"""

from __future__ import annotations

import pandas as pd

from ..paths import processed


def load_corpus() -> pd.DataFrame:
    return pd.read_csv(processed("corpus.csv"))


def by_year(corpus: pd.DataFrame) -> pd.DataFrame:
    df = corpus.copy()
    df["tahun"] = pd.to_datetime(df["date"], errors="coerce").dt.year.astype("Int64").astype(str)
    df = df[df["tahun"] != "<NA>"]
    counts = df.groupby(["tahun", "dilemma"]).size().unstack(fill_value=0)
    share = counts.div(counts.sum(axis=1).replace(0, 1), axis=0)
    share.columns = [f"nlp_{c}" for c in share.columns]
    return share.reset_index()


def topic_mix(corpus: pd.DataFrame) -> pd.Series:
    return corpus["dilemma"].value_counts(normalize=True)


def main() -> int:
    corpus = load_corpus()
    yearly = by_year(corpus)
    yearly.to_csv(processed("nlp_by_year.csv"), index=False)
    print("sinyal NLP per tahun:")
    print(yearly.to_string(index=False))
    print("\nkomposisi dilema:")
    print(topic_mix(corpus).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
