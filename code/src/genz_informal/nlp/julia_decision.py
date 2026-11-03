"""Lapisan keputusan terstruktur (eksperimen: Julia-1).

Julia-1 adalah model keputusan pilihan-terbatas (state + question + opsi ->
pilihan), BUKAN encoder dan BUKAN model generatif. Karena belum tentu tersedia
di lingkungan ini, modul menyediakan:
  - `JuliaDecisionLayer` dengan antarmuka yang sama,
  - fallback deterministik (pilih opsi dengan kecocokan leksikon tertinggi) agar
    studi ablasi tetap dapat dijalankan tanpa bobot model.

Posisi metodologis: dipakai sebagai EKSPERIMEN, bukan pengganti IndoBERTweet.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..annotation.schema import DILEMMAS


@dataclass
class Decision:
    choice: str
    scores: dict[str, int]


class JuliaDecisionLayer:
    def __init__(self, options: Sequence[str] | None = None, model_id: str | None = None):
        self.options = list(options or DILEMMAS)
        self.model_id = model_id

    def decide(self, state: str, question: str = "", options: Sequence[str] | None = None) -> Decision:
        opts = list(options or self.options)
        context = f"{state} {question}".lower()
        scores = {opt: context.count(opt.replace("_", " ").split()[0]) for opt in opts}
        best = max(scores.items(), key=lambda kv: kv[1]) if scores else (opts[0], 0)
        return Decision(choice=best[0], scores=scores)

    def decide_many(self, states: Sequence[str]) -> list[str]:
        return [self.decide(s).choice for s in states]
