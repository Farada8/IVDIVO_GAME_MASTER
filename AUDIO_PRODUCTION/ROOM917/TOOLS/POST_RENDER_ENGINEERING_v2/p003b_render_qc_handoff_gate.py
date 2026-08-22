#!/usr/bin/env python3
"""Bind ROOM917 P003B listener handoff to the exact full-mix bytes that pass render QC.

The gate re-runs render receipt validation from the same manifest+receipt, then
requires the listener-target audio SHA-256 to equal the receipt's declared full
mix SHA-256. This closes the identity gap between machine QC and human listening.
It does not build the blind package and never grants release authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List

from render_manifest_and_receipt_qc import QC_PASS, validate_receipt

PASS = "PASS_P003B_RENDER_QC_HANDOFF"
HOLD = "HOLD_P003B_RENDER_QC_HANDOFF"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def evaluate_handoff(
    contract: Dict[str, Any],
    manifest: Dict[str, Any],
    receipt: Dict[str, Any],
    *,
    audio_sha256: str,
    manifest_sha256: str,
    receipt_sha256: str,
) -> Dict[str, Any]:
    reasons: List[str] = []
    machine = validate_receipt(contract, manifest, receipt, manifest_sha256=manifest_sha256)
    if machine.get("status") != QC_PASS or machine.get("render_receipt_accepted") is not True:
        reasons.append("render_machine_qc_not_pass")

    full_mix = manifest.get("full_mix") if isinstance(manifest.get("full_mix"), dict) else {}
    full_name = full_mix.get("file_name")
    outputs = receipt.get("outputs") if isinstance(receipt.get("outputs"), list) else []
    full_records = [o for o in outputs if isinstance(o, dict) and o.get("file_name") == full_name]
    if len(full_records) != 1:
        reasons.append("receipt_full_mix_record_missing_or_ambiguous")
        full_record = {}
    else:
        full_record = full_records[0]

    declared_sha = str(full_record.get("sha256", ""))
    if not SHA256_RE.match(audio_sha256):
        reasons.append("listener_audio_sha256_invalid")
    if not SHA256_RE.match(declared_sha):
        reasons.append("receipt_full_mix_sha256_invalid")
    elif declared_sha.lower() != audio_sha256.lower():
        reasons.append("listener_audio_not_same_bytes_as_qc_full_mix")

    if not SHA256_RE.match(manifest_sha256):
        reasons.append("manifest_sha256_invalid")
    if not SHA256_RE.match(receipt_sha256):
        reasons.append("receipt_sha256_invalid")

    reasons = list(dict.fromkeys(reasons))
    return {
        "schema_version": "ivdivo.room917_p003b_render_qc_handoff/1.0",
        "project": contract.get("project", "ROOM917"),
        "episode": contract.get("episode", "E01"),
        "status": PASS if not reasons else HOLD,
        "handoff_authorized": not reasons,
        "release_authority": False,
        "listener_audio_sha256": audio_sha256,
        "qc_full_mix_sha256": declared_sha or None,
        "manifest_sha256": manifest_sha256,
        "receipt_sha256": receipt_sha256,
        "machine_qc_status": machine.get("status"),
        "machine_qc_reasons": machine.get("reasons", []),
        "reasons": reasons,
        "next": (
            "RUN_EXISTING_P003B_LISTENER_PACKAGE_BUILDER_AND_KEEP_PASS_A_BLIND"
            if not reasons
            else "DO_NOT_BUILD_P003B_PACKAGE__REPAIR_IDENTITY_OR_MACHINE_QC_EVIDENCE"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    for path in (args.contract, args.manifest, args.receipt, args.audio):
        if not path.is_file():
            raise SystemExit(f"missing input: {path}")

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    manifest_bytes = args.manifest.read_bytes()
    receipt_bytes = args.receipt.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    receipt = json.loads(receipt_bytes.decode("utf-8"))
    result = evaluate_handoff(
        contract,
        manifest,
        receipt,
        audio_sha256=sha256_file(args.audio),
        manifest_sha256=sha256_bytes(manifest_bytes),
        receipt_sha256=sha256_bytes(receipt_bytes),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"])
    for reason in result.get("reasons", []):
        print(f"- {reason}")
    return 0 if result["status"] == PASS else 4


if __name__ == "__main__":
    raise SystemExit(main())
