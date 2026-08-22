#!/usr/bin/env python3
"""Bridge ROOM917 A01/A02 machine QC output into the generic blind-package builder.

The bridge copies no audio and grants no human or production PASS. It verifies the
normalized candidate bytes and emits only a deterministic receipt describing those
bytes for build_sound_asset_blind_package.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import wave
from pathlib import Path

EXPECTED_ASSETS = {
    "A01_GREYHAVEN_LOBBY_30S_LOOP",
    "A02_SWITCHBOARD_ALCOVE_30S_LOOP",
}


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def wav_meta(path: Path) -> dict:
    with wave.open(str(path), "rb") as w:
        return {
            "sample_rate_hz": w.getframerate(),
            "bit_depth": w.getsampwidth() * 8,
            "channels": w.getnchannels(),
            "duration_seconds": w.getnframes() / w.getframerate(),
            "compression": w.getcomptype(),
        }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build verified A01/A02 receipt for ROOM917 blind audition package builder")
    ap.add_argument("--machine-qc", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--require-one-per-asset", action="store_true")
    args = ap.parse_args()

    qc = json.loads(args.machine_qc.read_text(encoding="utf-8"))
    errors: list[str] = []
    if qc.get("status") != "PREPARED_FOR_HUMAN_AUDITION_NOT_BOUND":
        errors.append("MACHINE_QC_STATUS_NOT_READY_FOR_HUMAN_AUDITION")
    if qc.get("machine_may_award_artistic_pass") is not False:
        errors.append("MACHINE_QC_ARTISTIC_PASS_LAW_VIOLATION")
    if qc.get("production_binding_authorized") is not False:
        errors.append("MACHINE_QC_UNEXPECTED_BINDING_AUTHORITY")

    rows = qc.get("rows") or []
    by_asset: dict[str, list[dict]] = {}
    receipt_rows: list[dict] = []
    for row in rows:
        aid = row.get("asset_id")
        cid = row.get("candidate_id")
        if aid not in EXPECTED_ASSETS:
            errors.append(f"UNEXPECTED_ASSET:{aid}")
            continue
        if row.get("machine_status") != "PREPARED_FOR_HUMAN_AUDITION":
            errors.append(f"MACHINE_STATUS_NOT_READY:{cid}")
            continue
        if row.get("production_binding_authorized") is not False:
            errors.append(f"CANDIDATE_UNEXPECTED_BINDING_AUTHORITY:{cid}")
            continue

        normalized = row.get("normalized") or {}
        p = Path(str(normalized.get("path") or ""))
        if not p.is_file():
            errors.append(f"NORMALIZED_BYTES_MISSING:{cid}")
            continue
        observed_sha = sha256_file(p)
        declared_sha = str(normalized.get("sha256") or "").lower()
        if observed_sha != declared_sha:
            errors.append(f"NORMALIZED_SHA_MISMATCH:{cid}")
            continue
        meta = wav_meta(p)
        if meta["compression"] != "NONE":
            errors.append(f"NOT_PCM_WAV:{cid}")
            continue
        if (meta["sample_rate_hz"], meta["bit_depth"], meta["channels"]) != (48000, 24, 2):
            errors.append(f"NORMALIZATION_TARGET_MISMATCH:{cid}")
            continue
        if normalized.get("sample_rate_hz") != 48000 or normalized.get("bit_depth") != 24 or normalized.get("channels") != 2:
            errors.append(f"DECLARED_NORMALIZATION_METADATA_MISMATCH:{cid}")
            continue

        rec = {
            "contract_asset_id": aid,
            "candidate_id": cid,
            "filename": p.name,
            "sha256": observed_sha,
            "size_bytes": p.stat().st_size,
            "duration_seconds": meta["duration_seconds"],
            "sample_rate_hz": 48000,
            "bit_depth": 24,
            "channels": 2,
            "human_audition_status": "HOLD_PENDING_BLIND_LISTEN",
            "production_binding_authorized": False,
        }
        receipt_rows.append(rec)
        by_asset.setdefault(aid, []).append(rec)

    if set(by_asset) != EXPECTED_ASSETS:
        errors.append("A01_A02_ASSET_SET_INCOMPLETE")
    if args.require_one_per_asset and any(len(by_asset.get(aid, [])) != 1 for aid in EXPECTED_ASSETS):
        errors.append("ROOM_BED_BLIND_MODE_REQUIRES_EXACTLY_ONE_CANDIDATE_PER_A01_A02")

    status = "READY_FOR_BLIND_PACKAGE_BUILDER" if not errors else "HOLD"
    out = {
        "schema_version": "room917.e01_a01_a02_blind_builder_receipt/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "status": status,
        "source_machine_qc": str(args.machine_qc),
        "assets": receipt_rows if not errors else [],
        "errors": errors,
        "human_audition_status": "NOT_PERFORMED",
        "production_binding_authorized": False,
        "law": "Receipt proves normalized candidate byte identity only. It authorizes blind package construction, not candidate preference, production gain, renderer binding, D003 repair, or Scene3 changes.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "candidate_count": len(out["assets"]), "errors": errors}))
    return 0 if status == "READY_FOR_BLIND_PACKAGE_BUILDER" else 4


if __name__ == "__main__":
    raise SystemExit(main())
