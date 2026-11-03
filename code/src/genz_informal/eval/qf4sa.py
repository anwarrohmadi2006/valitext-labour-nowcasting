"""Evaluasi kualitas mengikuti QF4SA (UNECE).

Lima dimensi: Accuracy, Explainability, Reproducibility, Timeliness,
Cost Effectiveness.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np


def expected_calibration_error(y_true: np.ndarray, y_prob: np.ndarray, bins: int = 10) -> float:
    """ECE untuk klasifikasi biner (probabilitas kelas positif)."""
    edges = np.linspace(0.0, 1.0, bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (y_prob >= lo) & (y_prob < hi)
        if not mask.any():
            continue
        conf = float(y_prob[mask].mean())
        acc = float(y_true[mask].mean())
        ece += float(mask.mean()) * abs(acc - conf)
    return ece


def data_hash(paths: list[Path]) -> str:
    h = hashlib.sha256()
    for p in sorted(paths):
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()[:16]


def environment_fingerprint() -> dict:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
    }


@dataclass
class QF4SAReport:
    accuracy: dict = field(default_factory=dict)
    explainability: dict = field(default_factory=dict)
    reproducibility: dict = field(default_factory=dict)
    timeliness_seconds: float = 0.0
    cost: dict = field(default_factory=dict)

    def to_markdown(self) -> str:
        lines = ["# Evaluasi QF4SA (UNECE)", ""]
        for section in ["accuracy", "explainability", "reproducibility"]:
            lines.append(f"## {section.capitalize()}")
            lines.append("```json")
            lines.append(json.dumps(getattr(self, section), indent=2, ensure_ascii=False))
            lines.append("```")
            lines.append("")
        lines.append(f"## Timeliness\n- waktu pemrosesan: {self.timeliness_seconds:.2f} detik\n")
        lines.append("## Cost Effectiveness")
        lines.append("```json")
        lines.append(json.dumps(self.cost, indent=2, ensure_ascii=False))
        lines.append("```")
        return "\n".join(lines)
