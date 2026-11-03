"""Penarikan komentar YouTube via Data API v3 : butuh kunci.

Aktifkan "YouTube Data API v3" di Google Cloud Console lalu isi
YOUTUBE_API_KEY di .env. Kuota default 10.000 unit/hari;
commentThreads.list = 1 unit.
"""

from __future__ import annotations

from typing import Any

import requests

from ..config import get

API = "https://www.googleapis.com/youtube/v3"


def _key() -> str:
    key = get("YOUTUBE_API_KEY")
    if not key:
        raise RuntimeError("YOUTUBE_API_KEY belum diset di .env")
    return key


def search_videos(query: str, max_results: int = 25, region: str = "ID") -> list[dict[str, Any]]:
    resp = requests.get(
        f"{API}/search",
        params={
            "key": _key(), "part": "snippet", "q": query, "type": "video",
            "maxResults": max_results, "regionCode": region, "relevanceLanguage": "id",
        },
        timeout=60,
    )
    resp.raise_for_status()
    items = resp.json().get("items", [])
    return [
        {
            "video_id": it["id"]["videoId"],
            "title": it["snippet"]["title"],
            "channel": it["snippet"]["channelTitle"],
            "published_at": it["snippet"]["publishedAt"],
        }
        for it in items
    ]


def video_comments(video_id: str, max_pages: int = 5) -> list[dict[str, Any]]:
    """Tarik komentar tingkat atas; 100 komentar per halaman = 1 unit."""
    collected: list[dict[str, Any]] = []
    token = None
    for _ in range(max_pages):
        params = {
            "key": _key(), "part": "snippet", "videoId": video_id,
            "maxResults": 100, "textFormat": "plainText", "order": "relevance",
        }
        if token:
            params["pageToken"] = token
        resp = requests.get(f"{API}/commentThreads", params=params, timeout=60)
        resp.raise_for_status()
        payload = resp.json()
        for item in payload.get("items", []):
            sn = item["snippet"]["topLevelComment"]["snippet"]
            collected.append({
                "source": "youtube", "video_id": video_id,
                "author": sn.get("authorDisplayName"), "text": sn.get("textDisplay", ""),
                "published_at": sn.get("publishedAt"), "like_count": sn.get("likeCount", 0),
            })
        token = payload.get("nextPageToken")
        if not token:
            break
    return collected
