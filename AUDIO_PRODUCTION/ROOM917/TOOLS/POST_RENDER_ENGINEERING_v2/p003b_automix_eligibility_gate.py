#!/usr/bin/env python3
"""Mandatory ROOM917 AutoMix-specific eligibility gate before P003B packaging.

This is intentionally separate from the legacy listener package builder. Any
ROOM917 E01 audio produced through the AutoMix v1 pipeline must pass this gate
first. The gate binds the exact listener audio bytes to the passed render-QC
handoff, revalidates the immutable manifest/receipt identities, and emits a
single-use eligibility receipt for downstream packaging. It never grants
release authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List

PASS = "PASS_P003B_AUTOMIX_ELIGIBILITY"
HOLD = "HOLD_P003B_AUTOMIX_ELIGIBILITY"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def evaluate(
    *,
    manifest: Dict[str, Any],
    receipt: Dict[str, Any],
    handoff: Dict[str, Any],
    manifest_sha256: str,
    receipt_sha256: str,
    handoff_sha256: str,
    audio_sha256: str,
) -> Dict[str, Any]:
    reasons: List[str] = []

    if manifest.get("schema_version") != "ivdivo.room917_render_manifest_result/1.0":
        reasons.append("render_manifest_schema_invalid")
    if manifest.get("status") != "PASS_RENDER_MANIFEST_COMPILED":
        reasons.append("render_manifest_not_pass")
    if manifest.get("render_authority") is not True or manifest.get("release_authority") is not False:
        reasons.append("render_manifest_authority_boundary_invalid")

    if receipt.get("schema_version") != "ivdivo.room917_render_machine_qc_result/1.0":
        reasons.append("render_machine_qc_schema_invalid")
    if receipt.get("status") != "PASS_RENDER_MACHINE_QC":
        reasons.append("render_machine_qc_not_pass")
    if receipt.get("render_receipt_accepted") is not True or receipt.get("release_authority") is not False:
        reasons.append("render_machine_qc_authority_boundary_invalid")

    if handoff.get("schema_version") != "ivdivo.room917_p003b_render_qc_handoff/1.0":
        reasons.append("p003b_render_qc_handoff_schema_invalid")
    if handoff.get("status") != "PASS_P003B_RENDER_QC_HANDOFF":
        reasons.append("p003b_render_qc_handoff_not_pass")
    if handoff.get("handoff_authorized") is not True or handoff.get("release_authority") is not False:
        reasons.append("p003b_render_qc_handoff_authority_boundary_invalid")

    if handoff.get("manifest_sha256") != manifest_sha256:
        reasons.append("handoff_manifest_sha256_mismatch")
    if handoff.get("receipt_sha256") != receipt_sha256:
        reasons.append("handoff_receipt_sha256_mismatch")
    if handoff.get("listener_audio_sha256") != audio_sha256:
        reasons.append("handoff_listener_audio_sha256_mismatch")
    if handoff.get("qc_full_mix_sha256") != audio_sha256:
        reasons.append("handoff_qc_full_mix_sha256_mismatch")

    full_mix = manifest.get("full_mix") if isinstance(manifest.get("full_mix"), dict) else {}
    full_name = full_mix.get("file_name")
    outputs = receipt.get("outputs") if isinstance(receipt.get("outputs"), list) else []
    matches = [o for o in outputs if isinstance(o, dict) and o.get("file_name") == full_name]
    if len(matches) != 1:
        reasons.append("qc_full_mix_record_missing_or_ambiguous")
    else:
        if matches[0].get("sha256") != audio_sha256:
            reasons.append("qc_full_mix_record_sha256_mismatch")

    for label, value in (
        ("manifest_sha256", manifest_sha256),
        ("receipt_sha256", receipt_sha256),
        ("handoff_sha256", handoff_sha256),
        ("audio_sha256", audio_sha256),
    ):
        if not SHA256_RE.match(str(value)):
            reasons.append(label + "_invalid")

    reasons = list(dict.fromkeys(reasons))
    return {
        "schema_version": "ivdivo.room917_p003b_automix_eligibility/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "pipeline": "AUTOMIX_V1",
        "status": PASS if not reasons else HOLD,
        "eligible_for_p003b_packaging": not reasons,
        "release_authority": False,
        "audio_sha256": audio_sha256,
        "manifest_sha256": manifest_sha256,
        "receipt_sha256": receipt_sha256,
        "render_qc_handoff_sha256": handoff_sha256,
        "reasons": reasons,
        "law": "AUTO_MIX_V1_AUDIO_MUST_PRESENT_THIS_PASS_RECEIPT_BEFORE_P003B_PACKAGE_BUILD; LEGACY_PACKAGE_PATH_IS_NOT_AUTHORITY_FOR_AUTOMIX_V1",
        "next": (
            "BUILD_P003B_PACKAGE_WITH_AUTOMIX_ELIGIBILITY_RECEIPT_THEN_FREEZE_PASS_A"
            if not reasons
            else "DO_NOT_BUILD_P003B_PACKAGE"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--receipt", required=True, type=Path)
    ap.add_argument("--handoff", required=True, type=Path)
    ap.add_argument("--audio", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    for p in (args.manifest, args.receipt, args.handoff, args.audio):
        if not p.is_file():
            raise SystemExit(f"missing input: {p}")

    manifest_bytes = args.manifest.read_bytes()
    receipt_bytes = args.receipt.read_bytes()
    handoff_bytes = args.handoff.read_bytes()
    result = evaluate(
        manifest=json.loads(manifest_bytes.decode("utf-8")),
        receipt=json.loads(receipt_bytes.decode("utf-8")),
        handoff=json.loads(handoff_bytes.decode("utf-8")),
        manifest_sha256=sha256_bytes(manifest_bytes),
        receipt_sha256=sha256_bytes(receipt_bytes),
        handoff_sha256=sha256_bytes(handoff_bytes),
        audio_sha256=sha256_file(args.audio),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"])
    for reason in result.get("reasons", []):
        print(f"- {reason}")
    return 0 if result["status"] == PASS else 4


if __name__ == "__main__":
    raise SystemExit(main())
