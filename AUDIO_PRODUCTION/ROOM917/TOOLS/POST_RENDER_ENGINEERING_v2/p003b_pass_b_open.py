#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

QUESTION_CLASSES = {"ACTOR_BELIEF", "AI_AUDIBLE", "DEAD_SCENE", "GEOGRAPHY", "MYSTERY", "SFX_MASKING"}
FREEZE_SCHEMA = "ivdivo.room917_p003b_pass_a_freeze_receipt/1.0"
QUEUE_SCHEMA = "ivdivo.room917_p003b_pass_b_verification_queue/1.0"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def validate_freeze(manifest_path: Path, notes_path: Path, manifest: dict[str, Any], notes: dict[str, Any], receipt: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if receipt.get("schema_version") != FREEZE_SCHEMA:
        errors.append("PASS_A_FREEZE_SCHEMA_INVALID")
    if receipt.get("status") != "PASS_A_FROZEN_PASS_B_AUTHORIZED":
        errors.append("PASS_A_FREEZE_NOT_AUTHORIZED")
    if receipt.get("pass_a_notes_frozen") is not True:
        errors.append("PASS_A_NOTES_NOT_FROZEN")
    if receipt.get("pass_b_authorized") is not True:
        errors.append("PASS_B_NOT_AUTHORIZED_BY_FREEZE")
    if receipt.get("pass_c_authorized") is not False:
        errors.append("PASS_A_FREEZE_MUST_NOT_PREAUTHORIZE_PASS_C")
    if sha256_file(manifest_path) != receipt.get("manifest_sha256"):
        errors.append("PUBLIC_MANIFEST_CHANGED_AFTER_PASS_A_FREEZE")
    if sha256_file(notes_path) != receipt.get("notes_sha256"):
        errors.append("PASS_A_NOTES_CHANGED_AFTER_FREEZE")
    if manifest.get("package_id") != receipt.get("package_id"):
        errors.append("PUBLIC_MANIFEST_PACKAGE_ID_MISMATCH")
    if notes.get("package_id") != receipt.get("package_id"):
        errors.append("PASS_A_NOTES_PACKAGE_ID_MISMATCH")
    target_sha = ((manifest.get("files") or {}).get("stereo_target") or {}).get("sha256")
    if target_sha != receipt.get("target_sha256"):
        errors.append("PUBLIC_TARGET_SHA_MISMATCH")
    if notes.get("target_sha256") != receipt.get("target_sha256"):
        errors.append("PASS_A_NOTES_TARGET_SHA_MISMATCH")
    return errors


def validate_queue(queue: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if queue.get("schema_version") != QUEUE_SCHEMA:
        errors.append("PASS_B_QUEUE_SCHEMA_INVALID")
    if queue.get("status") != "READY_AFTER_BLIND_PASS_A_ONLY":
        errors.append("PASS_B_QUEUE_STATUS_INVALID")
    firewall = queue.get("blind_firewall") or {}
    if firewall.get("pass_a_must_not_read_this_queue") is not True:
        errors.append("PASS_B_QUEUE_FIREWALL_PASS_A_GUARD_MISSING")
    if firewall.get("open_queue_only_after_pass_a_notes_are_frozen") is not True:
        errors.append("PASS_B_QUEUE_FREEZE_GUARD_MISSING")
    candidates = queue.get("verification_candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append("PASS_B_QUEUE_EMPTY")
        return errors
    ids: list[str] = []
    for idx, row in enumerate(candidates):
        if not isinstance(row, dict):
            errors.append(f"PASS_B_CANDIDATE_NOT_OBJECT:{idx}")
            continue
        cid = str(row.get("candidate_id") or "").strip()
        if not cid:
            errors.append(f"PASS_B_CANDIDATE_ID_MISSING:{idx}")
        else:
            ids.append(cid)
        if row.get("question_class") not in QUESTION_CLASSES:
            errors.append(f"PASS_B_CANDIDATE_QUESTION_CLASS_INVALID:{cid or idx}")
        if not str(row.get("verify_by_ear") or "").strip():
            errors.append(f"PASS_B_VERIFY_BY_EAR_MISSING:{cid or idx}")
        if not str(row.get("minimal_fix_if_confirmed") or "").strip():
            errors.append(f"PASS_B_MINIMAL_FIX_MISSING:{cid or idx}")
        if not isinstance(row.get("do_not_touch"), list):
            errors.append(f"PASS_B_DO_NOT_TOUCH_INVALID:{cid or idx}")
    if len(ids) != len(set(ids)):
        errors.append("PASS_B_CANDIDATE_IDS_NOT_UNIQUE")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Authorize ROOM917 P003B targeted Pass B only after cryptographically frozen blind Pass A.")
    ap.add_argument("--public-manifest", required=True, type=Path)
    ap.add_argument("--pass-a-notes", required=True, type=Path)
    ap.add_argument("--pass-a-freeze", required=True, type=Path)
    ap.add_argument("--pass-b-queue", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    manifest = load(args.public_manifest)
    notes = load(args.pass_a_notes)
    freeze = load(args.pass_a_freeze)
    queue = load(args.pass_b_queue)
    errors = validate_freeze(args.public_manifest, args.pass_a_notes, manifest, notes, freeze)
    errors += validate_queue(queue)
    errors = sorted(set(errors))

    receipt = {
        "schema_version": "ivdivo.room917_p003b_pass_b_open_receipt/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "package_id": freeze.get("package_id"),
        "target_sha256": freeze.get("target_sha256"),
        "queue_sha256": sha256_file(args.pass_b_queue),
        "manifest_sha256": sha256_file(args.public_manifest),
        "pass_a_notes_sha256": sha256_file(args.pass_a_notes),
        "status": "HOLD" if errors else "PASS_B_AUTHORIZED",
        "pass_b_authorized": not errors,
        "pass_c_authorized": False,
        "release_authority": False,
        "candidate_count": len(queue.get("verification_candidates") or []),
        "question_classes": sorted({row.get("question_class") for row in (queue.get("verification_candidates") or []) if isinstance(row, dict) and row.get("question_class")}),
        "errors": errors,
        "authorized_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z") if not errors else None,
        "law": "PASS_B_MAY_OPEN_ONLY_WHILE_BLIND_MANIFEST_AND_PASS_A_NOTES_STILL_MATCH_THE_FREEZE_RECEIPT. CANDIDATES_REMAIN_UNPROVEN_UNTIL_VERIFIED_BY_EAR_ON_THIS_TARGET_SHA.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(receipt["status"])
    for error in errors:
        print("- " + error)
    return 0 if not errors else 4


if __name__ == "__main__":
    raise SystemExit(main())
