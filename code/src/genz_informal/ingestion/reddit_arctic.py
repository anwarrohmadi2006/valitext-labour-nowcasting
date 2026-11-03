"""Penarikan korpus Reddit via Arctic Shift (tanpa autentikasi).

Arctic Shift adalah arsip komunitas (penerus Pushshift). Pencarian teks penuh
(`query=`) kerap timeout, sehingga strategi yang dipakai di sini adalah menarik
pos terbaru per subreddit lalu memfilter kata kunci secara lokal.

Dokumentasi: https://arctic-shift.photon-reddit.com  (endpoint /api/posts/search)
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable

import requests

BASE = "https://arctic-shift.photon-reddit.com/api"
UA = "genz-informal-nlp/0.1 (academic research; STIS x Kemnaker)"

KEYWORDS = [
    "magang", "internship", "freelance", "freelancer", "UMR", "UMP", "upah minimum",
    "gaji", "salary", "kontrak", "outsourcing", "ojol", "driver online", "kurir",
    "resign", "PHK", "honor", "part time", "paruh waktu", "kerja informal",
    "usaha sendiri", "wirausaha", "dagang", "jualan online", "no experience",
    "entry level", "lowongan", "loker", "fresh graduate", "gap year", "nganggur",
]


@dataclass
class ArcticShift:
    user_agent: str = UA
    pause: float = 2.0
    max_retries: int = 4
    _last: float = field(default=0.0, init=False, repr=False)

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        wait = self.pause - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        last_err: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                resp = requests.get(
                    f"{BASE}/{path}", params=params, headers={"User-Agent": self.user_agent},
                    timeout=90,
                )
                self._last = time.monotonic()
                if resp.status_code == 200:
                    return resp.json()
                last_err = RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
                if resp.status_code in (422, 429, 503):
                    time.sleep(5.0 * (attempt + 1))
                    continue
            except Exception as exc:  # noqa: BLE001
                last_err = exc
            time.sleep(2.0 * (attempt + 1))
        raise RuntimeError(f"Arctic Shift gagal: {last_err}")

    def posts(
        self, subreddit: str, limit: int = 100, after: str | None = None,
        before: str | None = None, sort: str = "desc", query: str | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"subreddit": subreddit, "limit": limit, "sort": sort}
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if query:
            params["query"] = query
        payload = self._get("posts/search", params)
        return payload.get("data") or []

    def comments(
        self, subreddit: str, limit: int = 100, after: str | None = None,
        before: str | None = None, sort: str = "desc", query: str | None = None,
        link_id: str | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"subreddit": subreddit, "limit": limit, "sort": sort}
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if query:
            params["query"] = query
        if link_id:
            params["link_id"] = link_id
        payload = self._get("comments/search", params)
        return payload.get("data") or []

    def thread_comments(self, subreddit: str, post_id: str, limit: int = 100) -> list[dict[str, Any]]:
        """Ambil komentar sebuah thread berdasarkan `link_id` (t3_<post_id>)."""
        return self.comments(subreddit, limit=limit, link_id=f"t3_{post_id}")

    def search_posts(self, subreddit: str, query: str, pages: int = 3) -> list[dict[str, Any]]:
        """Cari pos berteks penuh, paginasi mundur hingga `pages` halaman x100."""
        out: list[dict[str, Any]] = []
        before: str | None = None
        for _ in range(pages):
            batch = self.posts(subreddit, limit=100, before=before, query=query)
            if not batch:
                break
            out.extend(batch)
            oldest = min((p.get("created_utc") or 0) for p in batch)
            before = datetime.fromtimestamp(oldest, tz=timezone.utc).strftime("%Y-%m-%d")
            if len(batch) < 100:
                break
        return out

    def search_comments(self, subreddit: str, query: str, pages: int = 3) -> list[dict[str, Any]]:
        """Cari komentar berteks penuh, paginasi mundur."""
        out: list[dict[str, Any]] = []
        before: str | None = None
        for _ in range(pages):
            batch = self.comments(subreddit, limit=100, before=before, query=query)
            if not batch:
                break
            out.extend(batch)
            oldest = min((c.get("created_utc") or 0) for c in batch)
            before = datetime.fromtimestamp(oldest, tz=timezone.utc).strftime("%Y-%m-%d")
            if len(batch) < 100:
                break
        return out

    def pull_posts(
        self, subreddit: str, target: int = 500, page: int = 100, after: str | None = None,
    ) -> list[dict[str, Any]]:
        """Ambil hingga `target` pos terbaru dengan paginasi mundur."""
        collected: list[dict[str, Any]] = []
        before: str | None = None
        while len(collected) < target:
            batch = self.posts(subreddit, limit=page, after=after, before=before)
            if not batch:
                break
            collected.extend(batch)
            oldest = min((p.get("created_utc") or 0) for p in batch)
            before = datetime.fromtimestamp(oldest, tz=timezone.utc).strftime("%Y-%m-%d")
            if len(batch) < page:
                break
        return collected[:target]


def matches_keywords(text: str, keywords: Iterable[str] = KEYWORDS) -> list[str]:
    low = (text or "").lower()
    return [kw for kw in keywords if kw.lower() in low]


def to_document(post: dict[str, Any], subreddit: str) -> dict[str, Any]:
    """Normalisasi satu pos menjadi dokumen korpus."""
    title = post.get("title") or ""
    body = post.get("selftext") or ""
    created = post.get("created_utc")
    return {
        "id": post.get("id"),
        "source": "reddit",
        "subreddit": subreddit,
        "author": post.get("author"),
        "created_utc": created,
        "date": (
            datetime.fromtimestamp(created, tz=timezone.utc).strftime("%Y-%m-%d")
            if created else None
        ),
        "title": title,
        "body": body,
        "text": f"{title}\n{body}".strip(),
        "score": post.get("score"),
        "num_comments": post.get("num_comments"),
        "url": post.get("url"),
        "keywords": matches_keywords(f"{title} {body}"),
    }


def to_comment_document(comment: dict[str, Any], subreddit: str) -> dict[str, Any]:
    """Normalisasi satu komentar menjadi dokumen korpus.

    `parent_post` menyimpan id pos induk agar komentar tetap terhubung ke thread-nya.
    """
    body = comment.get("body") or ""
    created = comment.get("created_utc")
    title = comment.get("link_title") or ""
    parent = str(comment.get("link_id") or "").replace("t3_", "")
    return {
        "id": comment.get("id"),
        "source": "reddit_comment",
        "subreddit": subreddit,
        "author": comment.get("author"),
        "created_utc": created,
        "date": (
            datetime.fromtimestamp(created, tz=timezone.utc).strftime("%Y-%m-%d")
            if created else None
        ),
        "title": title,
        "body": body,
        "text": f"{title}\n{body}".strip(),
        "score": comment.get("score"),
        "num_comments": None,
        "parent_post": parent,
        "url": f"https://reddit.com/comments/{parent}" if parent else None,
        "keywords": matches_keywords(f"{title} {body}"),
    }
