#!/usr/bin/env python3
"""IVDIVO Audio Novel Studio — controlled production learning registry.

The studio improves from repeated production evidence without silently rewriting
canon. Learning records accumulate; repeated successful repair patterns become
CANDIDATE_FOR_REVIEW. Promotion to ACCEPTED requires explicit human/founder review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

REGISTRY_SCHEMA = "IVDIVO_PRODUCTION_LEARNING_REGISTRY_v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {
            "schema": REGISTRY_SCHEMA,
            "created_at": utc_now(),
            "records": [],
            "candidate_rules": [],
            "accepted_rules": [],
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, registry: Dict[str, Any]) -> None:
    registry["updated_at"] = utc_now()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fingerprint(record: Dict[str, Any]) -> str:
    basis = "|".join([
        str(record.get("defect_class", "")),
        str(record.get("root_cause", "")),
        str(record.get("repair_action", "")),
    ]).lower().strip()
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "project_id", "unit_id", "defect_class", "severity", "symptom",
        "root_cause", "repair_action", "result",
    ]
    missing = [k for k in required if not record.get(k)]
    if missing:
        raise ValueError(f"Learning record missing required fields: {missing}")
    out = dict(record)
    out.setdefault("record_id", f"LRN-{hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()[:12]}")
    out.setdefault("created_at", utc_now())
    out.setdefault("human_result", "NOT_TESTED")
    out.setdefault("automated_result", "UNKNOWN")
    out.setdefault("source_hash", None)
    out.setdefault("provider", None)
    out.setdefault("provider_model", None)
    out.setdefault("authority_versions", [])
    out.setdefault("before_metrics", {})
    out.setdefault("after_metrics", {})
    out.setdefault("evidence", [])
    out["pattern_fingerprint"] = fingerprint(out)
    return out


def ingest(registry: Dict[str, Any], record: Dict[str, Any]) -> Dict[str, Any]:
    r = normalize_record(record)
    if any(x.get("record_id") == r["record_id"] for x in registry.get("records", [])):
        raise ValueError(f"Duplicate record_id: {r['record_id']}")
    registry.setdefault("records", []).append(r)
    return r


def rebuild_candidates(registry: Dict[str, Any], min_successes: int = 3, min_units: int = 2, min_human_passes: int = 2) -> List[Dict[str, Any]]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for r in registry.get("records", []):
        groups.setdefault(r.get("pattern_fingerprint") or fingerprint(r), []).append(r)

    accepted_fps = {r.get("pattern_fingerprint") for r in registry.get("accepted_rules", [])}
    candidates: List[Dict[str, Any]] = []
    for fp, records in groups.items():
        successes = [r for r in records if str(r.get("result", "")).upper() in {"PASS", "IMPROVED", "SUCCESS"}]
        units = {f"{r.get('project_id')}::{r.get('unit_id')}" for r in successes}
        projects = {r.get("project_id") for r in successes}
        human_passes = [r for r in successes if str(r.get("human_result", "")).upper() in {"PASS", "IMPROVED", "SUCCESS"}]
        contradictions = [r for r in records if str(r.get("result", "")).upper() in {"FAIL", "WORSE", "REGRESSION"}]
        if fp in accepted_fps:
            continue
        if len(successes) >= min_successes and len(units) >= min_units and len(human_passes) >= min_human_passes and len(contradictions) < len(successes):
            exemplar = successes[-1]
            candidates.append({
                "candidate_id": f"CR-{fp}",
                "pattern_fingerprint": fp,
                "status": "CANDIDATE_FOR_REVIEW",
                "defect_class": exemplar.get("defect_class"),
                "root_cause": exemplar.get("root_cause"),
                "repair_action": exemplar.get("repair_action"),
                "successful_records": len(successes),
                "distinct_units": len(units),
                "distinct_projects": len(projects),
                "human_pass_records": len(human_passes),
                "contradictory_records": len(contradictions),
                "record_ids": [r.get("record_id") for r in records],
                "promotion_rule": "Explicit founder/human review required; never auto-modify universal canon.",
            })
    registry["candidate_rules"] = candidates
    return candidates


def approve_candidate(registry: Dict[str, Any], candidate_id: str, approver: str, note: str | None) -> Dict[str, Any]:
    cand = next((c for c in registry.get("candidate_rules", []) if c.get("candidate_id") == candidate_id), None)
    if not cand:
        raise ValueError(f"Candidate not found: {candidate_id}")
    accepted = dict(cand)
    accepted["status"] = "ACCEPTED_PRODUCTION_PATTERN"
    accepted["approved_at"] = utc_now()
    accepted["approved_by"] = approver
    accepted["approval_note"] = note
    registry.setdefault("accepted_rules", []).append(accepted)
    registry["candidate_rules"] = [c for c in registry.get("candidate_rules", []) if c.get("candidate_id") != candidate_id]
    return accepted


def cmd_ingest(args: argparse.Namespace) -> None:
    reg_path = Path(args.registry)
    registry = load(reg_path)
    record = json.loads(Path(args.record).read_text(encoding="utf-8"))
    r = ingest(registry, record)
    rebuild_candidates(registry)
    save(reg_path, registry)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_candidates(args: argparse.Namespace) -> None:
    reg_path = Path(args.registry)
    registry = load(reg_path)
    candidates = rebuild_candidates(registry)
    save(reg_path, registry)
    print(json.dumps(candidates, ensure_ascii=False, indent=2))


def cmd_approve(args: argparse.Namespace) -> None:
    reg_path = Path(args.registry)
    registry = load(reg_path)
    accepted = approve_candidate(registry, args.candidate_id, args.approver, args.note)
    save(reg_path, registry)
    print(json.dumps(accepted, ensure_ascii=False, indent=2))


def cmd_status(args: argparse.Namespace) -> None:
    registry = load(Path(args.registry))
    print(json.dumps({
        "records": len(registry.get("records", [])),
        "candidate_rules": len(registry.get("candidate_rules", [])),
        "accepted_rules": len(registry.get("accepted_rules", [])),
        "updated_at": registry.get("updated_at"),
    }, ensure_ascii=False, indent=2))


def main() -> None:
    p = argparse.ArgumentParser(description="IVDIVO controlled production learning registry")
    sub = p.add_subparsers(dest="cmd", required=True)

    x = sub.add_parser("ingest")
    x.add_argument("registry")
    x.add_argument("record")
    x.set_defaults(func=cmd_ingest)

    x = sub.add_parser("candidates")
    x.add_argument("registry")
    x.set_defaults(func=cmd_candidates)

    x = sub.add_parser("approve")
    x.add_argument("registry")
    x.add_argument("candidate_id")
    x.add_argument("--approver", required=True)
    x.add_argument("--note")
    x.set_defaults(func=cmd_approve)

    x = sub.add_parser("status")
    x.add_argument("registry")
    x.set_defaults(func=cmd_status)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
