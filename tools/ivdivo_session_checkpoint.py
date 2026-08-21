#!/usr/bin/env python3
"""IVDIVO volatile-session checkpoint compiler and fail-closed resume classifier.

This module does not recover browser UI state. It reduces loss from abrupt tab/logout/
runtime termination by turning the current material execution frontier into a small,
hash-bound durable checkpoint that can be reconciled against fresh authority on resume.

It never mutates story canon, calls providers, spends credits, or treats chat memory as
authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "ivdivo.session_checkpoint/1.0"

FORBIDDEN_KEY_FRAGMENTS = (
    "api_key", "apikey", "access_token", "refresh_token", "password",
    "passwd", "secret_key", "authorization", "bearer_token",
)

MATERIAL_STATES = {
    "ACTIVE",
    "WRITE_IN_PROGRESS",
    "RECOVERY_REQUIRED",
    "REBASE_REQUIRED",
    "BLOCKED",
    "COMPLETE",
}

VOLATILE_STATUSES = {"CHAT_LOCAL_ONLY", "LOCAL_ONLY", "UNPERSISTED", "PENDING_WRITE"}

def _canonical(obj: Any) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")

def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()

def _walk_forbidden(obj: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            low = str(key).lower()
            if any(fragment in low for fragment in FORBIDDEN_KEY_FRAGMENTS):
                hits.append(f"{path}.{key}")
            hits.extend(_walk_forbidden(value, f"{path}.{key}"))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            hits.extend(_walk_forbidden(value, f"{path}[{i}]"))
    return hits

def _require_nonempty_string(state: dict[str, Any], key: str) -> str:
    value = state.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()

def _normalize_checkpoint_payload(state: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(state, dict):
        raise TypeError("state must be a JSON object")

    secret_hits = _walk_forbidden(state)
    if secret_hits:
        raise ValueError("forbidden credential-like fields: " + ",".join(secret_hits))

    project_id = _require_nonempty_string(state, "project_id")
    work_unit = _require_nonempty_string(state, "work_unit")
    current_phase = _require_nonempty_string(state, "current_phase")
    selected_next_action = state.get("selected_next_action")
    if not isinstance(selected_next_action, dict):
        raise ValueError("selected_next_action must be an object")

    authority = state.get("authority_snapshot")
    if not isinstance(authority, dict):
        raise ValueError("authority_snapshot must be an object")
    if not str(authority.get("repo_main_sha", "")).strip():
        raise ValueError("authority_snapshot.repo_main_sha is required")
    if not str(authority.get("state_revision", "")).strip():
        raise ValueError("authority_snapshot.state_revision is required")

    writes = state.get("writes", [])
    if not isinstance(writes, list):
        raise ValueError("writes must be a list")

    artifacts = state.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise ValueError("artifacts must be a list")

    blockers = state.get("blockers", [])
    if not isinstance(blockers, list):
        raise ValueError("blockers must be a list")

    durable_write_ids = []
    pending_write_ids = []
    for row in writes:
        if not isinstance(row, dict) or not str(row.get("write_id", "")).strip():
            raise ValueError("every write requires write_id")
        status = str(row.get("status", "")).upper()
        readback = row.get("readback_verified")
        if status == "DURABLE" and readback is True:
            durable_write_ids.append(row["write_id"])
        else:
            pending_write_ids.append(row["write_id"])

    volatile_artifact_ids = []
    durable_artifact_ids = []
    for row in artifacts:
        if not isinstance(row, dict) or not str(row.get("artifact_id", "")).strip():
            raise ValueError("every artifact requires artifact_id")
        status = str(row.get("status", "")).upper()
        if status in VOLATILE_STATUSES or row.get("durable_pointer") in (None, ""):
            volatile_artifact_ids.append(row["artifact_id"])
        else:
            durable_artifact_ids.append(row["artifact_id"])

    checkpoint_status = str(state.get("checkpoint_status", "ACTIVE")).upper()
    if checkpoint_status not in MATERIAL_STATES:
        raise ValueError(f"unknown checkpoint_status: {checkpoint_status}")

    return {
        "schema_version": SCHEMA_VERSION,
        "project_id": project_id,
        "active_line": state.get("active_line"),
        "work_unit": work_unit,
        "current_phase": current_phase,
        "checkpoint_status": checkpoint_status,
        "authority_snapshot": {
            "repo": authority.get("repo"),
            "repo_main_sha": str(authority["repo_main_sha"]).strip(),
            "state_pointer": authority.get("state_pointer"),
            "state_revision": str(authority["state_revision"]).strip(),
            "source_hash": authority.get("source_hash"),
        },
        "last_verified_frontier": state.get("last_verified_frontier"),
        "last_completed_artifact": state.get("last_completed_artifact"),
        "selected_next_action": selected_next_action,
        "blockers": blockers,
        "writes": writes,
        "artifacts": artifacts,
        "durability_summary": {
            "durable_write_ids": durable_write_ids,
            "pending_write_ids": pending_write_ids,
            "durable_artifact_ids": durable_artifact_ids,
            "volatile_artifact_ids": volatile_artifact_ids,
        },
        "evidence_boundary": state.get("evidence_boundary", []),
        "recovery_notes": state.get("recovery_notes", []),
    }

def build_checkpoint(state: dict[str, Any], created_at: str | None = None) -> dict[str, Any]:
    payload = _normalize_checkpoint_payload(state)
    created = created_at or datetime.now(timezone.utc).isoformat()
    envelope = {
        "checkpoint_id": state.get("checkpoint_id") or f"{payload['project_id']}::{payload['work_unit']}",
        "created_at": created,
        "payload": payload,
    }
    envelope["checkpoint_sha256"] = _sha256(envelope)
    return envelope

def verify_checkpoint(checkpoint: dict[str, Any]) -> tuple[bool, str]:
    if not isinstance(checkpoint, dict):
        return False, "CHECKPOINT_NOT_OBJECT"
    expected = checkpoint.get("checkpoint_sha256")
    if not isinstance(expected, str) or len(expected) != 64:
        return False, "CHECKPOINT_HASH_MISSING_OR_INVALID"
    unsigned = deepcopy(checkpoint)
    unsigned.pop("checkpoint_sha256", None)
    actual = _sha256(unsigned)
    if actual != expected:
        return False, "CHECKPOINT_HASH_MISMATCH"
    payload = checkpoint.get("payload")
    if not isinstance(payload, dict):
        return False, "CHECKPOINT_PAYLOAD_MISSING"
    if payload.get("schema_version") != SCHEMA_VERSION:
        return False, "CHECKPOINT_SCHEMA_UNSUPPORTED"
    return True, "PASS"

def classify_resume(
    checkpoint: dict[str, Any],
    *,
    current_repo_main_sha: str,
    current_state_revision: str,
) -> dict[str, Any]:
    ok, reason = verify_checkpoint(checkpoint)
    if not ok:
        return {"decision": "STOP", "reason": reason}

    payload = checkpoint["payload"]
    if payload.get("checkpoint_status") == "BLOCKED":
        return {"decision": "STOP", "reason": "CHECKPOINT_ALREADY_BLOCKED"}

    blockers = payload.get("blockers", [])
    if blockers:
        return {
            "decision": "STOP",
            "reason": "BLOCKERS_PRESENT",
            "blockers": blockers,
            "selected_next_action": payload.get("selected_next_action"),
        }

    snap = payload["authority_snapshot"]
    drift = {}
    if str(snap.get("repo_main_sha")) != str(current_repo_main_sha):
        drift["repo_main_sha"] = {
            "checkpoint": snap.get("repo_main_sha"),
            "current": current_repo_main_sha,
        }
    if str(snap.get("state_revision")) != str(current_state_revision):
        drift["state_revision"] = {
            "checkpoint": snap.get("state_revision"),
            "current": current_state_revision,
        }
    if drift:
        return {
            "decision": "REBASE_FIRST",
            "reason": "AUTHORITY_OR_STATE_DRIFT",
            "drift": drift,
            "selected_next_action": payload.get("selected_next_action"),
        }

    summary = payload.get("durability_summary", {})
    pending = list(summary.get("pending_write_ids", []))
    volatile = list(summary.get("volatile_artifact_ids", []))
    if pending or volatile:
        return {
            "decision": "RECOVER_VOLATILE_FIRST",
            "reason": "UNPERSISTED_MATERIAL_EXISTS",
            "pending_write_ids": pending,
            "volatile_artifact_ids": volatile,
            "selected_next_action": payload.get("selected_next_action"),
        }

    return {
        "decision": "RESUME_EXACT",
        "reason": "CHECKPOINT_VALID_DURABLE_AND_FRESH",
        "project_id": payload.get("project_id"),
        "work_unit": payload.get("work_unit"),
        "current_phase": payload.get("current_phase"),
        "selected_next_action": payload.get("selected_next_action"),
        "last_verified_frontier": payload.get("last_verified_frontier"),
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="IVDIVO volatile-session checkpoint compiler")
    sub = parser.add_subparsers(dest="command", required=True)

    create_p = sub.add_parser("create")
    create_p.add_argument("state", type=Path)
    create_p.add_argument("--out", type=Path, required=True)

    resume_p = sub.add_parser("resume")
    resume_p.add_argument("checkpoint", type=Path)
    resume_p.add_argument("--current-repo-main-sha", required=True)
    resume_p.add_argument("--current-state-revision", required=True)

    verify_p = sub.add_parser("verify")
    verify_p.add_argument("checkpoint", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "create":
            state = json.loads(args.state.read_text(encoding="utf-8"))
            checkpoint = build_checkpoint(state)
            args.out.write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"decision": "CHECKPOINT_WRITTEN", "checkpoint_sha256": checkpoint["checkpoint_sha256"]}))
            return 0

        checkpoint = json.loads(args.checkpoint.read_text(encoding="utf-8"))
        if args.command == "verify":
            ok, reason = verify_checkpoint(checkpoint)
            print(json.dumps({"decision": "PASS" if ok else "STOP", "reason": reason}))
            return 0 if ok else 1

        result = classify_resume(
            checkpoint,
            current_repo_main_sha=args.current_repo_main_sha,
            current_state_revision=args.current_state_revision,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["decision"] in {"RESUME_EXACT", "REBASE_FIRST", "RECOVER_VOLATILE_FIRST"} else 1
    except Exception as exc:
        print(json.dumps({"decision": "STOP", "reason": f"CHECKPOINT_ERROR:{exc}"}, ensure_ascii=False))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
