#!/usr/bin/env python3
"""Validate self-improvement state references against the live registry family.

The validator treats CURRENT_IMPROVEMENT_REGISTRY.json as the base registry and may
also load explicit JSON records from 31_IDEAS/REGISTRY_EXTENSIONS/. It is read-only.
It never promotes a candidate; it only detects missing/incomplete/overclaimed records.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

MANDATORY_ACTIVE_FIELDS = {
    "candidate_id",
    "title",
    "candidate_type",
    "status",
    "scope",
    "source_provenance",
    "owner_role",
    "next_action",
    "next_gate",
}
TERMINAL = {"REJECTED", "SUPERSEDED", "ROLLED_BACK"}
VERIFIED = {"VERIFIED_CURRENT"}
PROMOTED_OR_APPLIED = {"PROMOTED", "APPLIED_UNVERIFIED", "VERIFIED_CURRENT"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_candidates(base_registry: Path, extensions_dir: Path | None) -> dict[str, dict[str, Any]]:
    raw = load_json(base_registry)
    candidates: dict[str, dict[str, Any]] = {}
    for item in raw.get("candidates", []):
        cid = item.get("candidate_id")
        if not cid:
            raise ValueError("base registry candidate missing candidate_id")
        if cid in candidates:
            raise ValueError(f"duplicate candidate_id in base registry: {cid}")
        candidates[cid] = item
    if extensions_dir and extensions_dir.exists():
        for path in sorted(extensions_dir.glob("*.json")):
            item = load_json(path)
            cid = item.get("candidate_id")
            if not cid:
                raise ValueError(f"extension missing candidate_id: {path}")
            if cid in candidates:
                raise ValueError(f"duplicate candidate_id across base/extensions: {cid}")
            candidates[cid] = item
    return candidates


def validate_candidate(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(field for field in MANDATORY_ACTIVE_FIELDS if item.get(field) in (None, "", []))
    if missing:
        errors.append("missing mandatory fields: " + ", ".join(missing))
    status = str(item.get("status", ""))
    if status in PROMOTED_OR_APPLIED and not item.get("application_targets"):
        errors.append("promoted/applied candidate missing application_targets")
    if status in VERIFIED and not item.get("verification_evidence"):
        errors.append("VERIFIED_CURRENT missing verification_evidence")
    if status == "HOLD_WITH_TRIGGER" and not item.get("hold_trigger"):
        errors.append("HOLD_WITH_TRIGGER missing hold_trigger")
    if status in TERMINAL and not item.get("terminal_reason"):
        errors.append(f"{status} missing terminal_reason")
    return errors


def referenced_candidate_ids(state: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for k, v in value.items():
                if k in {"candidate_id", "current_candidate", "registry_candidate_record"} and isinstance(v, str) and v.startswith("SI-"):
                    refs.add(v.split("_")[0] if "_" in v and v.startswith("SI-") and v.count("-") == 1 else v)
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)
        elif isinstance(value, str):
            import re
            refs.update(re.findall(r"SI-\d{4}", value))
    walk(state)
    return refs


def audit(state_path: Path, registry_path: Path, extensions_dir: Path | None) -> dict[str, Any]:
    state = load_json(state_path)
    candidates = collect_candidates(registry_path, extensions_dir)
    errors: list[dict[str, Any]] = []
    refs = sorted(referenced_candidate_ids(state))
    for cid in refs:
        if cid not in candidates:
            errors.append({"candidate_id": cid, "error": "STATE_REFERENCE_NOT_REGISTERED"})
    for cid, item in sorted(candidates.items()):
        for error in validate_candidate(item):
            errors.append({"candidate_id": cid, "error": error})
    return {
        "status": "PASS" if not errors else "FAIL",
        "referenced_candidate_ids": refs,
        "registered_candidate_ids": sorted(candidates),
        "errors": errors,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--state", type=Path, default=Path("CURRENT_IVDIVO_SELF_IMPROVEMENT_STATE.json"))
    p.add_argument("--registry", type=Path, default=Path("31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json"))
    p.add_argument("--extensions", type=Path, default=Path("31_IDEAS/REGISTRY_EXTENSIONS"))
    args = p.parse_args()
    result = audit(args.state, args.registry, args.extensions)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
