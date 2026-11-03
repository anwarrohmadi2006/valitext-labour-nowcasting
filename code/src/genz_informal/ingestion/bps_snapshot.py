"""Tarik seluruh indikator BPS terkonfigurasi menjadi tabel tidy.

Menghasilkan data/raw/bps/indicators.jsonl dan data/raw/bps/indicators.csv
dengan kolom: var_id, var_name, dimensi, tahun, vervar, value.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

from ..config import get_bps_key
from ..paths import ensure, raw
from .bps_api import BPSClient, decode_rows, year_windows


def load_config(path: Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def iter_indicators(cfg: dict):
    for group, items in (cfg.get("indicators") or {}).items():
        for item in items or []:
            if "var" in item:
                yield group, item


def main(config_path: str = "configs/bps_indicators.yaml") -> int:
    cfg = load_config(Path(config_path))
    th = cfg.get("meta", {}).get("th_default", "123:125")
    domain = cfg.get("meta", {}).get("domain_nasional", "0000")
    client = BPSClient(app_key=get_bps_key())

    rows: list[dict] = []
    start, _, end = th.partition(":")
    windows = year_windows(int(start), int(end or start), 3)
    for group, item in iter_indicators(cfg):
        var = item["var"]
        decoded: list[dict] = []
        for win in windows:
            try:
                payload = client.data(var, f"{win[0]}:{win[1]}", domain=domain)
            except Exception as exc:  # noqa: BLE001
                print(f"[skip] var {var} th {win}: {exc}")
                continue
            decoded.extend(decode_rows(payload))
        for r in decoded:
            rows.append({
                "var_id": var,
                "var_name": item.get("nama", ""),
                "dimensi": item.get("dimensi", ""),
                "grup_rq": group,
                "tahun": r["tahun"],
                "vervar": r["vervar"],
                "turtahun": r.get("turtahun", ""),
                "value": r["value"],
            })
        print(f"[ok] var {var}: {len(decoded)} baris")

    out_dir = raw("bps")
    jsonl = ensure(out_dir / "indicators.jsonl")
    with open(jsonl, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    csv_path = ensure(out_dir / "indicators.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["var_id"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"tersimpan: {jsonl} ({len(rows)} baris)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
