"""Penarikan Threads via Meta Content Library : butuh akses akademik.

Bukan API berbasis kunci: akses diberikan lewat telaah (Research Tools Manager).
Isi MCL_ACCESS_TOKEN di .env setelah disetujui, lalu sesuaikan endpoint.

Catatan: data Threads saat ini hanya dapat ditelusuri (browse), belum dapat diunduh.
Modul ini menyediakan kerangka; sesuaikan dengan skema yang diberikan Meta.
"""

from __future__ import annotations

from typing import Any

import requests

from ..config import get

# Ganti dengan endpoint resmi yang tercantum pada dokumentasi akses Anda.
MCL_ENDPOINT = "https://graph.facebook.com/v20.0/content_library/threads"


def search(query: str, limit: int = 100, language: str = "id") -> list[dict[str, Any]]:
    token = get("MCL_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("MCL_ACCESS_TOKEN belum diset (menunggu persetujuan Meta)")
    resp = requests.get(
        MCL_ENDPOINT,
        params={"q": query, "limit": limit, "language": language, "access_token": token},
        timeout=90,
    )
    resp.raise_for_status()
    return resp.json().get("data", [])
