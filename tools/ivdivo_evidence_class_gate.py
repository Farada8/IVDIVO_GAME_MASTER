#!/usr/bin/env python3
"""Evidence-class and claim-satisfaction gate for IVDIVO.

Evidence classes are orthogonal, not a ladder. Machine, AI, provider, human,
specialist, market and Founder evidence cannot silently impersonate one another.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

EVIDENCE_CLASSES = {
    "DETERMINISTIC_MACHINE",
    "INTERNAL_AI_REVIEW",
    "SOURCE_PROVENANCE",
    "PRODUCTION_OBSERVATION",
    "PROVIDER",
    "HUMAN_SIGNAL",
    "SPECIALIST",
    "MARKET",
    "FOUNDER_AUTHORITY",
}

FORBIDDEN_IMPERSONATIONS = {
    ("INTERNAL_AI_REVIEW", "HUMAN_SIGNAL"),
    ("DETERMINISTIC_MACHINE", "PROVIDER"),
    ("DETERMINISTIC_MACHINE", "HUMAN_SIGNAL"),
    ("SOURCE_PROVENANCE", "MARKET"),
    ("SOURCE_PROVENANCE", "SPECIALIST"),
    ("PROVIDER", "HUMAN_SIGNAL"),
    ("HUMAN_SIGNAL", "FOUNDER_AUTHORITY"),
    ("INTERNAL_AI_REVIEW", "FOUNDER_AUTHORITY"),
    ("DETERMINISTIC_MACHINE", "FOUNDER_AUTHORITY"),
}


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    evidence_class: str
    source_locator: str
    source_family: str
    status: str = "PASS"


def validate_evidence(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not item.get("evidence_id"):
        errors.append("MISSING_EVIDENCE_ID")
    cls = item.get("evidence_class")
    if cls not in EVIDENCE_CLASSES:
        errors.append(f"INVALID_EVIDENCE_CLASS:{cls}")
    if not item.get("source_locator"):
        errors.append("MISSING_SOURCE_LOCATOR")
    if not item.get("source_family"):
        errors.append("MISSING_SOURCE_FAMILY")
    if item.get("status") not in {None, "PASS", "FAIL", "HOLD", "BLOCKED"}:
        errors.append(f"INVALID_EVIDENCE_STATUS:{item.get('status')}")
    return errors


def normalize_evidence(items: list[dict[str, Any]]) -> tuple[list[Evidence], list[str]]:
    out: list[Evidence] = []
    errors: list[str] = []
    seen_ids: set[str] = set()
    for raw in items:
        errs = validate_evidence(raw)
        if errs:
            errors.extend(f"{raw.get('evidence_id', '?')}:{e}" for e in errs)
            continue
        eid = str(raw["evidence_id"])
        if eid in seen_ids:
            errors.append(f"DUPLICATE_EVIDENCE_ID:{eid}")
            continue
        seen_ids.add(eid)
        out.append(Evidence(
            evidence_id=eid,
            evidence_class=str(raw["evidence_class"]),
            source_locator=str(raw["source_locator"]),
            source_family=str(raw["source_family"]),
            status=str(raw.get("status", "PASS")),
        ))
    return out, errors


def independent_family_count(evidence: list[Evidence], cls: str) -> int:
    return len({e.source_family for e in evidence if e.evidence_class == cls and e.status == "PASS"})


def audit_claim(claim: dict[str, Any], evidence_raw: list[dict[str, Any]]) -> dict[str, Any]:
    evidence, errors = normalize_evidence(evidence_raw)
    required_classes = claim.get("required_evidence_classes", [])
    if not isinstance(required_classes, list) or not required_classes:
        errors.append("CLAIM_WITHOUT_REQUIRED_EVIDENCE_CLASSES")
        required_classes = []
    for cls in required_classes:
        if cls not in EVIDENCE_CLASSES:
            errors.append(f"CLAIM_REQUIRES_UNKNOWN_CLASS:{cls}")

    passed = [e for e in evidence if e.status == "PASS"]
    satisfied: dict[str, list[str]] = {}
    missing: list[str] = []
    for required in required_classes:
        ids = [e.evidence_id for e in passed if e.evidence_class == required]
        if ids:
            satisfied[required] = ids
        else:
            missing.append(required)

    forbidden_hits: list[dict[str, str]] = []
    for source_cls, target_cls in FORBIDDEN_IMPERSONATIONS:
        if target_cls in required_classes and not any(e.evidence_class == target_cls and e.status == "PASS" for e in passed):
            if any(e.evidence_class == source_cls and e.status == "PASS" for e in passed):
                forbidden_hits.append({"offered_class": source_cls, "required_class": target_cls})

    independence_requirements = claim.get("minimum_independent_source_families", {}) or {}
    independence_failures: list[dict[str, Any]] = []
    for cls, minimum in independence_requirements.items():
        try:
            minimum_int = int(minimum)
        except (TypeError, ValueError):
            errors.append(f"BAD_INDEPENDENCE_REQUIREMENT:{cls}:{minimum}")
            continue
        actual = independent_family_count(passed, cls)
        if actual < minimum_int:
            independence_failures.append({"evidence_class": cls, "required": minimum_int, "actual": actual})

    status = "PASS"
    if errors or missing or forbidden_hits or independence_failures:
        status = "FAIL"

    return {
        "status": status,
        "claim_id": claim.get("claim_id"),
        "claim_text": claim.get("claim_text"),
        "required_evidence_classes": required_classes,
        "satisfied_by": satisfied,
        "missing_classes": missing,
        "forbidden_impersonations_detected": forbidden_hits,
        "independence_failures": independence_failures,
        "evidence": [asdict(e) for e in evidence],
        "errors": sorted(errors),
        "authority_mutation_authorized": False,
    }


def audit_packet(packet: dict[str, Any]) -> dict[str, Any]:
    claims = packet.get("claims", [])
    evidence = packet.get("evidence", [])
    results = [audit_claim(c, evidence) for c in claims]
    status = "PASS" if results and all(r["status"] == "PASS" for r in results) else "FAIL"
    if not claims:
        status = "FAIL"
    return {
        "status": status,
        "claim_results": results,
        "global_rule": "EVIDENCE_CLASSES_ARE_ORTHOGONAL_NOT_A_TOTAL_RANKING",
        "promotion_or_lock": "NOT_AUTHORIZED_BY_THIS_GATE",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("packet", type=Path)
    args = p.parse_args()
    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    result = audit_packet(packet)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
