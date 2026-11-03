"""Klien TypeSafe AI "System One" (model Jev) : model keputusan, bukan chatbot.

Endpoint: POST https://api.typesafe.ai/v1/systemone
Model:    jev-latest (alias jev-1.13.0)
Auth:     Authorization: Bearer <TYPESAFE_API_KEY>

Jev mengembalikan keputusan terstruktur:
  - "noul"   : probabilitas ya/tidak (0..1)
  - "choice" : satu opsi terpilih + distribusi probabilitas
  - "score"  : nilai berbobot probabilitas atas level yang kita definisikan

Dipakai untuk AUDIT TOPIK: memberi label dilema + skor koherensi secara
terstruktur. Catatan: bahasa utama Jev = Inggris; untuk teks Indonesia harus
diuji (docs.typesafe.ai/models), jadi audit ini adalah pelengkap, bukan
pengganti human audit.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import requests

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODELS_ENDPOINT = "https://api.typesafe.ai/v1/models"
DEFAULT_MODEL = "jev-latest"


class JevError(RuntimeError):
    """Kesalahan dari API TypeSafe."""


@dataclass
class JevClient:
    api_key: str
    model: str = DEFAULT_MODEL
    timeout: int = 90
    max_retries: int = 4
    pause: float = 0.0
    _last: float = field(default=0.0, init=False, repr=False)

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def evaluate(self, state: Any, questions: dict[str, dict]) -> dict[str, Any]:
        payload = {"state": state, "model": self.model, "questions": questions}
        last_err: str | None = None
        for attempt in range(self.max_retries):
            if self.pause:
                wait = self.pause - (time.monotonic() - self._last)
                if wait > 0:
                    time.sleep(wait)
            try:
                resp = requests.post(ENDPOINT, headers=self._headers(), json=payload,
                                     timeout=self.timeout)
                self._last = time.monotonic()
                if resp.status_code == 200:
                    return resp.json()
                if resp.status_code in (401, 422):
                    raise JevError(f"HTTP {resp.status_code}: {resp.text[:300]}")
                last_err = f"HTTP {resp.status_code}: {resp.text[:200]}"
            except JevError:
                raise
            except Exception as exc:  # noqa: BLE001
                last_err = str(exc)
            time.sleep(2.0 * (attempt + 1))
        raise JevError(f"Jev gagal setelah {self.max_retries} percobaan: {last_err}")

    def models(self) -> dict[str, Any]:
        resp = requests.get(MODELS_ENDPOINT, headers=self._headers(), timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()


# ------------------------------------------------------------------ pembantu
def choice_question(instructions: str | dict, options: dict[str, str | None]) -> dict:
    return {"type": "choice", "instructions": instructions, "criteria": options}


def score_question(instructions: str | dict, levels: list[str]) -> dict:
    return {"type": "score", "instructions": instructions, "criteria": levels}


def noul_question(instructions: str | dict, true: str | None = None,
                  false: str | None = None) -> dict:
    q: dict[str, Any] = {"type": "noul", "instructions": instructions}
    if true or false:
        q["criteria"] = {"true": true, "false": false}
    return q


def is_available() -> bool:
    from ..config import get  # noqa: PLC0415
    return bool(get("TYPESAFE_API_KEY"))
