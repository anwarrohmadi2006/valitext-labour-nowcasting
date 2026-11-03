"""Pemuat konfigurasi & rahasia (.env) sederhana tanpa dependensi eksternal."""

from __future__ import annotations

import os
from pathlib import Path

_ENV_LOADED = False


def _find_env() -> Path | None:
    here = Path(__file__).resolve()
    for base in [Path.cwd(), *here.parents]:
        candidate = base / ".env"
        if candidate.is_file():
            return candidate
    return None


def load_env(force: bool = False) -> None:
    """Muat variabel dari .env terdekat (tidak menimpa env yang sudah ada)."""
    global _ENV_LOADED
    if _ENV_LOADED and not force:
        return
    env_path = _find_env()
    if env_path is not None:
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())
    _ENV_LOADED = True


def get(name: str, default: str | None = None) -> str | None:
    load_env()
    return os.environ.get(name, default)


def get_bps_key() -> str:
    key = get("BPS_API_KEY")
    if not key:
        raise RuntimeError("BPS_API_KEY belum diset. Salin .env.example menjadi .env lalu isi kuncinya.")
    return key


def data_dir() -> Path:
    path = Path(get("DATA_DIR", "./data") or "./data").expanduser()
    return path
