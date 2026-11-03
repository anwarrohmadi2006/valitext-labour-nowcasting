"""Penarikan Reddit via Data API resmi (PRAW) : butuh kredensial.

Lewati modul ini bila tidak punya kredensial Reddit; gunakan
`reddit_arctic.py` (tanpa autentikasi) sebagai gantinya.

Buat aplikasi tipe `script` di https://www.reddit.com/prefs/apps
lalu isi .env: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT.
"""

from __future__ import annotations

import json
from typing import Any, Iterable

from ..config import get


def _client():
    try:
        import praw  # noqa: PLC0415
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("PRAW belum terpasang: pip install praw") from exc
    cid, secret, ua = get("REDDIT_CLIENT_ID"), get("REDDIT_CLIENT_SECRET"), get("REDDIT_USER_AGENT")
    if not (cid and secret and ua):
        raise RuntimeError("Kredensial Reddit belum lengkap di .env")
    reddit = praw.Reddit(client_id=cid, client_secret=secret, user_agent=ua)
    reddit.read_only = True
    return reddit


def search(subreddits: Iterable[str], query: str, limit: int = 200) -> list[dict[str, Any]]:
    """Cari pos pada beberapa subreddit (batas ±1000 item per listing)."""
    reddit = _client()
    docs: list[dict[str, Any]] = []
    for sub in subreddits:
        for s in reddit.subreddit(sub).search(query, limit=limit, sort="new"):
            docs.append({
                "id": s.id, "source": "reddit", "subreddit": sub, "author": str(s.author),
                "created_utc": s.created_utc, "title": s.title, "body": s.selftext,
                "text": f"{s.title}\n{s.selftext}".strip(), "score": s.score,
                "num_comments": s.num_comments, "url": s.url,
            })
    return docs


def dump(docs: list[dict[str, Any]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        for doc in docs:
            fh.write(json.dumps(doc, ensure_ascii=False) + "\n")
