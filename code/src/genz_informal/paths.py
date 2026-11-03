"""Utilitas lokasi berkas hasil (data lakehouse sederhana)."""

from __future__ import annotations

from pathlib import Path

from .config import data_dir


def root() -> Path:
    return Path(__file__).resolve().parents[2]


def raw(*parts: str) -> Path:
    p = data_dir() / "raw"
    for part in parts:
        p = p / part
    return p


def interim(*parts: str) -> Path:
    p = data_dir() / "interim"
    for part in parts:
        p = p / part
    return p


def processed(*parts: str) -> Path:
    p = data_dir() / "processed"
    for part in parts:
        p = p / part
    return p


def outputs(*parts: str) -> Path:
    p = root() / "outputs"
    for part in parts:
        p = p / part
    return p


def ensure(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
