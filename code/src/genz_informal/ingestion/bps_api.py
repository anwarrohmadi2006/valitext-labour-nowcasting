"""Klien BPS Web API v2 (hanya pustaka standar).

Endpoint yang dipakai:
  domain : /v1/api/domain/type/all/key/{key}/
  subject: /v1/api/list/model/subject/domain/{domain}/key/{key}/page/{page}/
  var    : /v1/api/list/model/var/domain/{domain}/subject/{sub}/key/{key}/page/{page}/
  data   : /v1/api/list/model/data/domain/{domain}/var/{var}/key/{key}/th/{th}/

Catatan: parameter `th` WAJIB (mis. `123:125` untuk 2023-2025). Kode tahun BPS
nonstandar: 123=2023, 124=2024, 125=2025.
"""

from __future__ import annotations

import json
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Iterable

BASE = "https://webapi.bps.go.id/v1/api"
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


class BPSError(RuntimeError):
    """Kesalahan dari BPS Web API."""


@dataclass
class BPSClient:
    app_key: str
    user_agent: str = DEFAULT_UA
    pause: float = 1.0
    _last_call: float = field(default=0.0, init=False, repr=False)

    # -- inti -------------------------------------------------------------
    def _get(self, path: str) -> dict[str, Any]:
        url = f"{BASE}/{path.strip('/')}/"
        wait = self.pause - (time.monotonic() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(
            url, headers={"User-Agent": self.user_agent, "Accept": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        self._last_call = time.monotonic()
        if payload.get("status") == "Error":
            raise BPSError(payload.get("message", "kesalahan tidak diketahui"))
        return payload

    # -- metadata ---------------------------------------------------------
    def domains(self, dtype: str = "all") -> dict[str, Any]:
        return self._get(f"domain/type/{dtype}/key/{self.app_key}")

    def subjects(self, domain: str = "0000", page: int = 1) -> dict[str, Any]:
        return self._get(f"list/model/subject/domain/{domain}/key/{self.app_key}/page/{page}")

    def variables(self, subject: int, domain: str = "0000", page: int = 1) -> dict[str, Any]:
        return self._get(
            f"list/model/var/domain/{domain}/subject/{subject}/key/{self.app_key}/page/{page}"
        )

    # -- data -------------------------------------------------------------
    def data(
        self,
        var: int,
        th: str | int | tuple[int, int] | list[int],
        domain: str = "0000",
        vervar: int | None = None,
        turvar: int | None = None,
    ) -> dict[str, Any]:
        th_s = f"{th[0]}:{th[1]}" if isinstance(th, (tuple, list)) else str(th)
        path = f"list/model/data/domain/{domain}/var/{var}/key/{self.app_key}/th/{th_s}"
        if vervar is not None:
            path += f"/vervar/{vervar}"
        if turvar is not None:
            path += f"/turvar/{turvar}"
        return self._get(path)


def year_windows(start: int, end: int, size: int = 3) -> list[tuple[int, int]]:
    """Pecah rentang tahun menjadi jendela <=3 tahun (batas API BPS)."""
    out: list[tuple[int, int]] = []
    s = start
    while s <= end:
        e = min(s + size - 1, end)
        out.append((s, e))
        s = e + 1
    return out


def decode_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Ubah `datacontent` menjadi baris berlabel dengan mencocokkan kombinasi.

    Kunci gabungan: {vervar}{var}{turvar}{th}{turtahun}. Panjang tiap komponen
    berbeda antarvariabel (mis. turtahun bisa 1 atau 3 digit), sehingga decoding
    dilakukan dengan membangkitkan semua kombinasi dari daftar label : bukan
    dengan pemotongan offset tetap.
    """
    var_list = payload.get("var") or []
    if not var_list:
        return []
    var = var_list[0]["val"]
    dc: dict[str, Any] = payload.get("datacontent") or {}
    if not dc:
        return []

    vervar = payload.get("vervar") or [{"val": "", "label": ""}]
    tahun = payload.get("tahun") or [{"val": "", "label": ""}]
    turvar = payload.get("turvar") or [{"val": "0", "label": ""}]
    turtahun = payload.get("turtahun") or [{"val": "", "label": ""}]

    rows: list[dict[str, Any]] = []
    consumed: set[str] = set()
    for vv in vervar:
        for th in tahun:
            for tv in turvar:
                for tu in turtahun:
                    key = f"{vv['val']}{var}{tv['val']}{th['val']}{tu['val']}"
                    if key in dc:
                        consumed.add(key)
                        rows.append({
                            "vervar": vv.get("label", str(vv.get("val"))),
                            "tahun": th.get("label", str(th.get("val"))),
                            "turvar": tv.get("label", str(tv.get("val"))),
                            "turtahun": tu.get("label", str(tu.get("val"))),
                            "value": dc[key],
                        })

    # Sisa kunci yang tak terpetakan: simpan apa adanya agar tidak hilang diam-diam.
    for key, value in dc.items():
        if key not in consumed:
            rows.append({"vervar": key, "tahun": "", "turvar": "", "turtahun": "",
                         "value": value})
    return rows


def paginate(client: BPSClient, fetch, max_pages: int = 20) -> list[dict[str, Any]]:
    """Kumpulkan seluruh item dari endpoint berhalaman (subject/var)."""
    items: list[dict[str, Any]] = []
    page = 1
    while page <= max_pages:
        payload = fetch(page)
        data = payload.get("data") or []
        if len(data) < 2 or not data[1]:
            break
        items.extend(data[1])
        pages = (data[0] or {}).get("pages", 1)
        if page >= pages:
            break
        page += 1
    return items
