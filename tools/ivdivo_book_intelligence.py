#!/usr/bin/env python3
"""IVDIVO Book Intelligence Engine v1.0.

Validates source passports, normalizes mechanism cards, applies evidence/promotion
 gates, and builds domain adapter packets. Raw source access is supplied by the
 calling environment; this module does not redistribute copyrighted books.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Dict, Iterable, List, Mapping, Sequence

SOURCE_STAGES = (
    "REGISTERED",
    "INTEGRITY_VERIFIED",
    "STRUCTURE_MAPPED",
    "FULL_READ",
    "CLAIMS_EXTRACTED",
    "MECHANISMS_EXTRACTED",
    "FAILURE_MODES_MAPPED",
    "CROSS_SOURCE_COMPARED",
    "OPERATIONALIZED",
    "PROJECT_VALIDATED",
    "SYNTHESIZED",
)

RIGHTS_STATUSES = {
    "USER_PROVIDED",
    "OPEN_LICENSE",
    "PUBLIC_DOMAIN",
    "ACCESS_ONLY",
    "UNKNOWN",
}

DOMAIN_ADAPTERS = {
    "STORY",
    "AUDIO",
    "BUSINESS",
    "SELF_IMPROVEMENT",
    "RESEARCH",
    "GAME",
    "VISUAL",
    "OPERATIONS",
    "GENERAL",
}


def _norm_text(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[^a-z0-9а-яё _-]+", "", value, flags=re.IGNORECASE)
    return value


def mechanism_semantic_key(statement: str) -> str:
    norm = _norm_text(statement)
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]


def validate_source_passport(passport: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    required = ("source_id", "title", "provenance", "rights_status", "lifecycle_stage")
    for key in required:
        if not passport.get(key):
            errors.append(f"missing:{key}")
    if passport.get("rights_status") not in RIGHTS_STATUSES:
        errors.append("invalid:rights_status")
    stage = passport.get("lifecycle_stage")
    if stage not in SOURCE_STAGES:
        errors.append("invalid:lifecycle_stage")
    if stage in SOURCE_STAGES and SOURCE_STAGES.index(stage) >= SOURCE_STAGES.index("FULL_READ"):
        if not passport.get("content_locator"):
            errors.append("missing:content_locator_for_full_read_or_later")
    if passport.get("independent_source_group") in (None, ""):
        errors.append("missing:independent_source_group")
    return errors


def lifecycle_rank(stage: str) -> int:
    try:
        return SOURCE_STAGES.index(stage)
    except ValueError:
        return -1


def source_can_support_mechanism(passport: Mapping[str, Any]) -> bool:
    return lifecycle_rank(str(passport.get("lifecycle_stage", ""))) >= lifecycle_rank("MECHANISMS_EXTRACTED")


def can_redistribute_source(passport: Mapping[str, Any]) -> bool:
    """Conservative redistribution gate.

    USER_PROVIDED and ACCESS_ONLY sources can be analyzed when authorized/accessed
    by the user, but are not redistributable by this engine by default.
    """
    return passport.get("rights_status") in {"OPEN_LICENSE", "PUBLIC_DOMAIN"}


def build_mechanism_card(
    *,
    mechanism_id: str,
    statement: str,
    source_ids: Sequence[str],
    failure_modes: Sequence[str],
    domain_targets: Sequence[str],
    evidence_locators: Sequence[str],
    abstraction_level: str = "PROJECT_NEUTRAL",
) -> Dict[str, Any]:
    targets = [d for d in domain_targets if d in DOMAIN_ADAPTERS]
    if not statement.strip():
        raise ValueError("statement is required")
    if not source_ids:
        raise ValueError("source_ids required")
    if not evidence_locators:
        raise ValueError("evidence_locators required")
    return {
        "mechanism_id": mechanism_id,
        "semantic_key": mechanism_semantic_key(statement),
        "statement": statement.strip(),
        "source_ids": list(dict.fromkeys(source_ids)),
        "failure_modes": list(dict.fromkeys(failure_modes)),
        "domain_targets": list(dict.fromkeys(targets)) or ["GENERAL"],
        "evidence_locators": list(dict.fromkeys(evidence_locators)),
        "abstraction_level": abstraction_level,
        "project_specific_expression_removed": False,
        "pilot_evidence": [],
        "disposition": "REFERENCE_ONLY",
    }


def originality_gate(card: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    if card.get("abstraction_level") != "PROJECT_NEUTRAL":
        errors.append("not_project_neutral")
    if not card.get("project_specific_expression_removed", False):
        errors.append("distinctive_expression_not_confirmed_removed")
    if len(card.get("source_ids", [])) < 1:
        errors.append("no_sources")
    return errors


def independent_evidence_groups(
    card: Mapping[str, Any],
    source_passports: Mapping[str, Mapping[str, Any]],
) -> int:
    groups = set()
    for sid in card.get("source_ids", []):
        p = source_passports.get(sid)
        if p and source_can_support_mechanism(p):
            grp = p.get("independent_source_group")
            if grp:
                groups.add(str(grp))
    return len(groups)


def project_pilot_summary(card: Mapping[str, Any]) -> Dict[str, Any]:
    pilots = [p for p in card.get("pilot_evidence", []) if isinstance(p, Mapping)]
    passed = [p for p in pilots if p.get("status") == "PASS"]
    projects = {p.get("project_id") for p in passed if p.get("project_id")}
    regressions = [
        p for p in pilots
        if p.get("severity") in {"FATAL", "MAJOR"} or p.get("status") == "REGRESSION"
    ]
    measurable_gain = any(bool(p.get("measurable_gain")) for p in passed)
    return {
        "pass_count": len(passed),
        "distinct_pass_projects": len(projects),
        "fatal_major_regressions": len(regressions),
        "measurable_gain": measurable_gain,
    }


def promotion_decision(
    card: Mapping[str, Any],
    source_passports: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Any]:
    """Fail-closed lifecycle for book-derived reusable mechanisms."""
    orig = originality_gate(card)
    if orig:
        return {"disposition": "HOLD", "reasons": orig}

    supportable_sources = [
        sid for sid in card.get("source_ids", [])
        if sid in source_passports and source_can_support_mechanism(source_passports[sid])
    ]
    if not supportable_sources:
        return {"disposition": "HOLD", "reasons": ["no_mechanism_extracted_source"]}

    groups = independent_evidence_groups(card, source_passports)
    pilot = project_pilot_summary(card)

    if pilot["fatal_major_regressions"] > 0:
        return {"disposition": "REJECT", "reasons": ["fatal_or_major_regression"]}

    if pilot["distinct_pass_projects"] >= 2 and pilot["measurable_gain"] and groups >= 1:
        return {
            "disposition": "PROMOTABLE",
            "reasons": ["two_project_replication", "measurable_gain", "source_provenance_valid"],
        }

    if pilot["distinct_pass_projects"] >= 1:
        reasons: List[str] = ["needs_second_independent_project"]
        if not pilot["measurable_gain"]:
            reasons.append("needs_measurable_gain")
        return {"disposition": "PILOT_READY", "reasons": reasons}

    if groups >= 2:
        return {
            "disposition": "LOCAL_TEST",
            "reasons": ["cross_source_support_present", "project_pilot_missing"],
        }

    return {
        "disposition": "LOCAL_TEST",
        "reasons": ["single_source_mechanism", "project_pilot_missing"],
    }


def dedupe_mechanism_cards(cards: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    clusters: Dict[str, List[Mapping[str, Any]]] = {}
    for card in cards:
        key = str(card.get("semantic_key") or mechanism_semantic_key(str(card.get("statement", ""))))
        clusters.setdefault(key, []).append(card)
    unique = []
    duplicates = []
    for key, group in clusters.items():
        unique.append(group[0])
        if len(group) > 1:
            duplicates.append({
                "semantic_key": key,
                "canonical_mechanism_id": group[0].get("mechanism_id"),
                "duplicate_ids": [g.get("mechanism_id") for g in group[1:]],
                "evidence_weight_added_by_duplication": 0,
            })
    return {"unique": unique, "duplicate_clusters": duplicates}


def route_book_use(
    *,
    domain: str,
    task: str,
    source_passports: Sequence[Mapping[str, Any]],
    max_sources: int = 5,
) -> Dict[str, Any]:
    domain = domain.upper()
    if domain not in DOMAIN_ADAPTERS:
        domain = "GENERAL"
    eligible = []
    for p in source_passports:
        if validate_source_passport(p):
            continue
        if lifecycle_rank(str(p.get("lifecycle_stage"))) < lifecycle_rank("STRUCTURE_MAPPED"):
            continue
        targets = {str(x).upper() for x in p.get("domain_targets", ["GENERAL"])}
        score = 2 if domain in targets else 1 if "GENERAL" in targets else 0
        if score:
            eligible.append((score, lifecycle_rank(str(p["lifecycle_stage"])), p))
    eligible.sort(key=lambda x: (x[0], x[1]), reverse=True)
    selected = [x[2]["source_id"] for x in eligible[:max_sources]]
    return {
        "domain": domain,
        "task": task,
        "selected_source_ids": selected,
        "retrieval_policy": "MECHANISM_FIRST_THEN_TARGETED_SOURCE_READ",
        "max_sources": max_sources,
        "requires_fresh_full_read": False if selected else True,
        "output_contract": [
            "claims_with_locators",
            "mechanism_cards",
            "failure_modes",
            "contradictions",
            "adapter_packet",
            "promotion_state",
        ],
    }


def build_adapter_packet(
    *,
    domain: str,
    task: str,
    mechanism_cards: Sequence[Mapping[str, Any]],
    source_passports: Mapping[str, Mapping[str, Any]],
    max_mechanisms: int = 3,
) -> Dict[str, Any]:
    domain = domain.upper()
    ranked = []
    for card in mechanism_cards:
        if domain not in card.get("domain_targets", []) and "GENERAL" not in card.get("domain_targets", []):
            continue
        decision = promotion_decision(card, source_passports)
        rank = {
            "PROMOTABLE": 5,
            "PILOT_READY": 4,
            "LOCAL_TEST": 3,
            "REFERENCE_ONLY": 2,
            "HOLD": 1,
            "REJECT": 0,
        }.get(decision["disposition"], 0)
        if rank <= 1:
            continue
        ranked.append((rank, card, decision))
    ranked.sort(key=lambda x: x[0], reverse=True)
    chosen = ranked[:max_mechanisms]
    return {
        "domain": domain,
        "task": task,
        "mechanisms": [
            {
                "mechanism_id": c.get("mechanism_id"),
                "statement": c.get("statement"),
                "disposition": d["disposition"],
                "evidence_locators": c.get("evidence_locators", []),
                "failure_modes": c.get("failure_modes", []),
            }
            for _, c, d in chosen
        ],
        "constraints": [
            "NO_SOURCE_EXPRESSION_COPY",
            "NO_REFERENCE_AS_CANON",
            "NO_LOCKED_PROJECT_REOPEN_WITHOUT_NEW_FAILURE_EVIDENCE",
            "MAX_3_MECHANISMS_PER_LOCAL_APPLICATION_UNLESS_EXPLICITLY_JUSTIFIED",
        ],
    }


def audit_library(passports: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    invalid = []
    stage_counts = {s: 0 for s in SOURCE_STAGES}
    rights_counts = {s: 0 for s in RIGHTS_STATUSES}
    for p in passports:
        errs = validate_source_passport(p)
        if errs:
            invalid.append({"source_id": p.get("source_id"), "errors": errs})
        stage = p.get("lifecycle_stage")
        if stage in stage_counts:
            stage_counts[stage] += 1
        rights = p.get("rights_status")
        if rights in rights_counts:
            rights_counts[rights] += 1
    return {
        "total": len(passports),
        "valid": len(passports) - len(invalid),
        "invalid": invalid,
        "stage_counts": stage_counts,
        "rights_counts": rights_counts,
    }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="IVDIVO Book Intelligence Engine v1.0")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_audit = sub.add_parser("audit-passports")
    p_audit.add_argument("json_path")

    p_dec = sub.add_parser("promotion-decision")
    p_dec.add_argument("card_json")
    p_dec.add_argument("passports_json")

    args = parser.parse_args()
    if args.cmd == "audit-passports":
        with open(args.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        passports = data["sources"] if isinstance(data, dict) and "sources" in data else data
        print(json.dumps(audit_library(passports), ensure_ascii=False, indent=2))
    elif args.cmd == "promotion-decision":
        with open(args.card_json, "r", encoding="utf-8") as f:
            card = json.load(f)
        with open(args.passports_json, "r", encoding="utf-8") as f:
            p = json.load(f)
        passports = p.get("sources", p)
        if isinstance(passports, list):
            passports = {x["source_id"]: x for x in passports}
        print(json.dumps(promotion_decision(card, passports), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
