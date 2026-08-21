#!/usr/bin/env python3
"""Append-only checkpoint lineage/retention helper for IVDIVO session recovery."""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

SCHEMA_VERSION = "ivdivo.checkpoint_lineage/1.0"
STATUSES = {"ACTIVE", "SUPERSEDED", "INCIDENT_EVIDENCE", "GC_ELIGIBLE"}


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def _require_string(obj: dict[str, Any], key: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be non-empty string")
    return value.strip()


def validate_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(ledger, dict):
        raise TypeError("ledger must be object")
    entries = ledger.get("entries", [])
    if not isinstance(entries, list):
        raise ValueError("entries must be list")
    by_id: dict[str, dict[str, Any]] = {}
    for raw in entries:
        if not isinstance(raw, dict):
            raise ValueError("entry must be object")
        entry_id = _require_string(raw, "entry_id")
        if entry_id in by_id:
            raise ValueError(f"duplicate entry_id:{entry_id}")
        work_unit = _require_string(raw, "work_unit")
        checkpoint_id = _require_string(raw, "checkpoint_id")
        checkpoint_sha256 = _require_string(raw, "checkpoint_sha256")
        if len(checkpoint_sha256) != 64:
            raise ValueError(f"invalid checkpoint sha:{entry_id}")
        status = str(raw.get("status", "ACTIVE")).upper()
        if status not in STATUSES:
            raise ValueError(f"invalid status:{status}")
        generation = raw.get("generation")
        if not isinstance(generation, int) or generation < 0:
            raise ValueError(f"invalid generation:{entry_id}")
        by_id[entry_id] = {
            "entry_id": entry_id,
            "work_unit": work_unit,
            "checkpoint_id": checkpoint_id,
            "checkpoint_sha256": checkpoint_sha256,
            "parent_entry_id": raw.get("parent_entry_id"),
            "generation": generation,
            "status": status,
            "repo_main_sha": raw.get("repo_main_sha"),
            "state_revision": raw.get("state_revision"),
            "incident_id": raw.get("incident_id"),
            "notes": list(raw.get("notes", [])) if isinstance(raw.get("notes", []), list) else [],
        }

    for entry in by_id.values():
        parent = entry.get("parent_entry_id")
        if parent in (None, ""):
            if entry["generation"] != 0:
                raise ValueError(f"root generation must be 0:{entry['entry_id']}")
            continue
        if parent not in by_id:
            raise ValueError(f"missing parent:{entry['entry_id']}->{parent}")
        parent_entry = by_id[parent]
        if parent_entry["work_unit"] != entry["work_unit"]:
            raise ValueError(f"cross-work-unit parent:{entry['entry_id']}")
        if entry["generation"] != parent_entry["generation"] + 1:
            raise ValueError(f"generation mismatch:{entry['entry_id']}")
        seen = {entry["entry_id"]}
        cur = parent_entry
        while True:
            if cur["entry_id"] in seen:
                raise ValueError(f"cycle:{entry['entry_id']}")
            seen.add(cur["entry_id"])
            p = cur.get("parent_entry_id")
            if not p:
                break
            cur = by_id[p]

    rows = [by_id[k] for k in sorted(by_id)]
    return {"schema_version": SCHEMA_VERSION, "entries": rows, "ledger_sha256": _sha(rows)}


def append_checkpoint(
    ledger: dict[str, Any], *, entry_id: str, work_unit: str, checkpoint_id: str,
    checkpoint_sha256: str, repo_main_sha: str, state_revision: str,
    parent_entry_id: str | None = None, incident_id: str | None = None,
) -> dict[str, Any]:
    normalized = validate_ledger(ledger)
    entries = deepcopy(normalized["entries"])
    existing = {e["entry_id"]: e for e in entries}
    if entry_id in existing:
        raise ValueError(f"duplicate entry_id:{entry_id}")
    if any(e["checkpoint_sha256"] == checkpoint_sha256 for e in entries):
        raise ValueError("duplicate checkpoint_sha256")

    if parent_entry_id:
        if parent_entry_id not in existing:
            raise ValueError("parent_entry_id not found")
        parent = existing[parent_entry_id]
        if parent["work_unit"] != work_unit:
            raise ValueError("parent belongs to another work_unit")
        generation = parent["generation"] + 1
    else:
        roots = [e for e in entries if e["work_unit"] == work_unit]
        if roots:
            raise ValueError("non-empty work_unit requires parent_entry_id")
        generation = 0

    for e in entries:
        if e["work_unit"] == work_unit and e["status"] == "ACTIVE":
            if e["entry_id"] != parent_entry_id:
                raise ValueError("multiple/foreign active head; reconcile before append")
            e["status"] = "INCIDENT_EVIDENCE" if e.get("incident_id") else "SUPERSEDED"

    entries.append({
        "entry_id": entry_id,
        "work_unit": work_unit,
        "checkpoint_id": checkpoint_id,
        "checkpoint_sha256": checkpoint_sha256,
        "parent_entry_id": parent_entry_id,
        "generation": generation,
        "status": "ACTIVE",
        "repo_main_sha": repo_main_sha,
        "state_revision": state_revision,
        "incident_id": incident_id,
        "notes": [],
    })
    return validate_ledger({"entries": entries})


def classify_retention(ledger: dict[str, Any]) -> dict[str, Any]:
    normalized = validate_ledger(ledger)
    rows = deepcopy(normalized["entries"])
    latest_by_work: dict[str, dict[str, Any]] = {}
    for e in rows:
        cur = latest_by_work.get(e["work_unit"])
        if cur is None or e["generation"] > cur["generation"]:
            latest_by_work[e["work_unit"]] = e

    decisions = []
    for e in rows:
        latest = latest_by_work[e["work_unit"]]
        if e["entry_id"] == latest["entry_id"]:
            retention = "EPHEMERAL_RECOVERY_CURRENT"
        elif e.get("incident_id") or e["status"] == "INCIDENT_EVIDENCE":
            retention = "AUDIT_KEEP"
        else:
            retention = "GC_ELIGIBLE"
        decisions.append({
            "entry_id": e["entry_id"], "work_unit": e["work_unit"],
            "generation": e["generation"], "retention": retention,
        })
    return {"decision": "RETENTION_CLASSIFIED", "entries": decisions, "source_ledger_sha256": normalized["ledger_sha256"]}
