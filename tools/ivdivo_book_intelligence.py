#!/usr/bin/env python3
"""IVDIVO Book Intelligence Engine v1.1.

Universal reference gateway with orthogonal source state, evidence-class-aware
promotion, bidirectional traceability audit, and change-impact analysis.
Raw source access is supplied by the calling environment.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Dict, Iterable, List, Mapping, Sequence

LEGACY_SOURCE_STAGES = (
    "REGISTERED", "INTEGRITY_VERIFIED", "STRUCTURE_MAPPED", "FULL_READ",
    "CLAIMS_EXTRACTED", "MECHANISMS_EXTRACTED", "FAILURE_MODES_MAPPED",
    "CROSS_SOURCE_COMPARED", "OPERATIONALIZED", "PROJECT_VALIDATED", "SYNTHESIZED",
)
INTEGRITY_STATUSES = {"UNKNOWN", "VERIFIED", "FAILED", "QUARANTINED"}
READ_COVERAGE = {"NONE", "STRUCTURE_ONLY", "PARTIAL_TARGETED", "FULL_READ"}
EXTRACTION_STAGES = {
    "NONE", "CLAIMS_EXTRACTED", "MECHANISMS_EXTRACTED", "FAILURE_MODES_MAPPED",
    "CROSS_SOURCE_COMPARED", "OPERATIONALIZED", "PROJECT_VALIDATED", "SYNTHESIZED",
}
EXTRACTION_RANK = {
    "NONE": 0, "CLAIMS_EXTRACTED": 1, "MECHANISMS_EXTRACTED": 2,
    "FAILURE_MODES_MAPPED": 3, "CROSS_SOURCE_COMPARED": 4, "OPERATIONALIZED": 5,
    "PROJECT_VALIDATED": 6, "SYNTHESIZED": 7,
}
RIGHTS_STATUSES = {"USER_PROVIDED", "OPEN_LICENSE", "PUBLIC_DOMAIN", "ACCESS_ONLY", "UNKNOWN"}
DOMAIN_ADAPTERS = {"STORY", "AUDIO", "BUSINESS", "SELF_IMPROVEMENT", "RESEARCH", "GAME", "VISUAL", "OPERATIONS", "GENERAL"}

EVIDENCE_CLASSES = {
    "ENGINEERING_VERIFICATION", "REAL_PROJECT_VALIDATION", "HUMAN_VALIDATION",
    "PROVIDER_VALIDATION", "MARKET_VALIDATION", "FACTUAL_SPECIALIST_VALIDATION",
    "LEGACY_UNCLASSIFIED",
}
REAL_VALIDATION_CLASSES = EVIDENCE_CLASSES - {"ENGINEERING_VERIFICATION", "LEGACY_UNCLASSIFIED"}

TRACE_NODE_TYPES = {
    "SOURCE", "SECTION", "CLAIM", "MECHANISM", "ADAPTER", "PROJECT_APPLICATION",
    "TEST", "RESULT", "LEARNING", "ENGINE_RULE",
}
TRACE_RELATIONS = {
    "SOURCE_HAS_SECTION": ("SOURCE", "SECTION"),
    "SECTION_SUPPORTS_CLAIM": ("SECTION", "CLAIM"),
    "CLAIM_ABSTRACTS_TO_MECHANISM": ("CLAIM", "MECHANISM"),
    "MECHANISM_PACKED_FOR_DOMAIN": ("MECHANISM", "ADAPTER"),
    "ADAPTER_APPLIED_TO_PROJECT": ("ADAPTER", "PROJECT_APPLICATION"),
    "PROJECT_APPLICATION_TESTED_BY": ("PROJECT_APPLICATION", "TEST"),
    "TEST_PRODUCED_RESULT": ("TEST", "RESULT"),
    "RESULT_PROMOTED_TO_LEARNING": ("RESULT", "LEARNING"),
    "LEARNING_CHANGED_ENGINE_RULE": ("LEARNING", "ENGINE_RULE"),
}


def _norm_text(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"\s+", " ", value)
    return re.sub(r"[^a-z0-9а-яё _-]+", "", value, flags=re.IGNORECASE)


def mechanism_semantic_key(statement: str) -> str:
    return hashlib.sha256(_norm_text(statement).encode("utf-8")).hexdigest()[:16]


def migrate_source_state(passport: Mapping[str, Any]) -> Dict[str, str]:
    """Return orthogonal v1.1 source state without inventing FULL_READ."""
    if all(passport.get(k) for k in ("integrity_status", "read_coverage", "extraction_stage")):
        return {
            "integrity_status": str(passport["integrity_status"]),
            "read_coverage": str(passport["read_coverage"]),
            "extraction_stage": str(passport["extraction_stage"]),
        }
    legacy = str(passport.get("lifecycle_stage", "REGISTERED"))
    if legacy == "REGISTERED":
        return {"integrity_status": "UNKNOWN", "read_coverage": "NONE", "extraction_stage": "NONE"}
    if legacy == "INTEGRITY_VERIFIED":
        return {"integrity_status": "VERIFIED", "read_coverage": "NONE", "extraction_stage": "NONE"}
    if legacy == "STRUCTURE_MAPPED":
        return {"integrity_status": "VERIFIED", "read_coverage": "STRUCTURE_ONLY", "extraction_stage": "NONE"}
    if legacy == "FULL_READ":
        return {"integrity_status": "VERIFIED", "read_coverage": "FULL_READ", "extraction_stage": "NONE"}
    if legacy in EXTRACTION_STAGES:
        return {"integrity_status": "VERIFIED", "read_coverage": "FULL_READ", "extraction_stage": legacy}
    return {"integrity_status": "UNKNOWN", "read_coverage": "NONE", "extraction_stage": "NONE"}


def validate_source_passport(passport: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    for key in ("source_id", "title", "provenance", "rights_status", "independent_source_group"):
        if not passport.get(key):
            errors.append(f"missing:{key}")
    if passport.get("rights_status") not in RIGHTS_STATUSES:
        errors.append("invalid:rights_status")
    state = migrate_source_state(passport)
    if state["integrity_status"] not in INTEGRITY_STATUSES:
        errors.append("invalid:integrity_status")
    if state["read_coverage"] not in READ_COVERAGE:
        errors.append("invalid:read_coverage")
    if state["extraction_stage"] not in EXTRACTION_STAGES:
        errors.append("invalid:extraction_stage")
    if state["integrity_status"] in {"FAILED", "QUARANTINED"} and state["extraction_stage"] != "NONE":
        errors.append("invalid:extraction_from_failed_or_quarantined_source")
    if EXTRACTION_RANK[state["extraction_stage"]] >= EXTRACTION_RANK["CLAIMS_EXTRACTED"]:
        if state["read_coverage"] not in {"PARTIAL_TARGETED", "FULL_READ"}:
            errors.append("insufficient:read_coverage_for_extraction")
        if not passport.get("content_locator"):
            errors.append("missing:content_locator_for_extraction")
    return errors


def source_can_support_mechanism(passport: Mapping[str, Any]) -> bool:
    if validate_source_passport(passport):
        return False
    state = migrate_source_state(passport)
    return (
        state["integrity_status"] == "VERIFIED"
        and EXTRACTION_RANK[state["extraction_stage"]] >= EXTRACTION_RANK["MECHANISMS_EXTRACTED"]
    )


def can_redistribute_source(passport: Mapping[str, Any]) -> bool:
    return passport.get("rights_status") in {"OPEN_LICENSE", "PUBLIC_DOMAIN"}


def build_mechanism_card(
    *, mechanism_id: str, statement: str, source_ids: Sequence[str],
    failure_modes: Sequence[str], domain_targets: Sequence[str],
    evidence_locators: Sequence[str], abstraction_level: str = "PROJECT_NEUTRAL",
) -> Dict[str, Any]:
    if not statement.strip():
        raise ValueError("statement is required")
    if not source_ids:
        raise ValueError("source_ids required")
    if not evidence_locators:
        raise ValueError("evidence_locators required")
    targets = [d for d in domain_targets if d in DOMAIN_ADAPTERS]
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
    if not card.get("source_ids"):
        errors.append("no_sources")
    return errors


def independent_evidence_groups(
    card: Mapping[str, Any], source_passports: Mapping[str, Mapping[str, Any]]
) -> int:
    groups = set()
    for sid in card.get("source_ids", []):
        passport = source_passports.get(sid)
        if passport and source_can_support_mechanism(passport):
            group = passport.get("independent_source_group")
            if group:
                groups.add(str(group))
    return len(groups)


def project_pilot_summary(card: Mapping[str, Any]) -> Dict[str, Any]:
    pilots = [p for p in card.get("pilot_evidence", []) if isinstance(p, Mapping)]
    real_passes = [
        p for p in pilots
        if p.get("status") == "PASS" and p.get("evidence_class") in REAL_VALIDATION_CLASSES
    ]
    engineering_passes = [
        p for p in pilots
        if p.get("status") == "PASS" and p.get("evidence_class") == "ENGINEERING_VERIFICATION"
    ]
    legacy_passes = [
        p for p in pilots
        if p.get("status") == "PASS" and p.get("evidence_class") in (None, "LEGACY_UNCLASSIFIED")
    ]
    projects = {p.get("project_id") for p in real_passes if p.get("project_id")}
    regressions = [
        p for p in pilots
        if p.get("severity") in {"FATAL", "MAJOR"} or p.get("status") == "REGRESSION"
    ]
    return {
        "real_validation_pass_count": len(real_passes),
        "distinct_real_validation_projects": len(projects),
        "engineering_verification_pass_count": len(engineering_passes),
        "legacy_unclassified_pass_count": len(legacy_passes),
        "fatal_major_regressions": len(regressions),
        "measurable_gain": any(bool(p.get("measurable_gain")) for p in real_passes),
    }


def promotion_decision(
    card: Mapping[str, Any], source_passports: Mapping[str, Mapping[str, Any]]
) -> Dict[str, Any]:
    orig = originality_gate(card)
    if orig:
        return {"disposition": "HOLD", "reasons": orig}
    supportable = [
        sid for sid in card.get("source_ids", [])
        if sid in source_passports and source_can_support_mechanism(source_passports[sid])
    ]
    if not supportable:
        return {"disposition": "HOLD", "reasons": ["no_mechanism_extracted_source"]}
    groups = independent_evidence_groups(card, source_passports)
    pilot = project_pilot_summary(card)
    if pilot["fatal_major_regressions"] > 0:
        return {"disposition": "REJECT", "reasons": ["fatal_or_major_regression"]}
    if pilot["distinct_real_validation_projects"] >= 2 and pilot["measurable_gain"] and groups >= 1:
        return {
            "disposition": "PROMOTABLE",
            "reasons": ["two_real_validation_projects", "measurable_gain", "source_provenance_valid"],
        }
    if pilot["distinct_real_validation_projects"] >= 1:
        reasons = ["needs_second_independent_real_validation_project"]
        if not pilot["measurable_gain"]:
            reasons.append("needs_measurable_gain")
        return {"disposition": "PILOT_READY", "reasons": reasons}
    if pilot["engineering_verification_pass_count"] > 0:
        return {"disposition": "LOCAL_TEST", "reasons": ["engineering_verification_not_real_project_validation"]}
    if pilot["legacy_unclassified_pass_count"] > 0:
        return {"disposition": "LOCAL_TEST", "reasons": ["legacy_pilot_evidence_unclassified"]}
    return {
        "disposition": "LOCAL_TEST",
        "reasons": [
            "cross_source_support_present" if groups >= 2 else "single_source_mechanism",
            "real_project_validation_missing",
        ],
    }


def dedupe_mechanism_cards(cards: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    clusters: Dict[str, List[Mapping[str, Any]]] = {}
    for card in cards:
        key = str(card.get("semantic_key") or mechanism_semantic_key(str(card.get("statement", ""))))
        clusters.setdefault(key, []).append(card)
    unique, duplicates = [], []
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


def audit_traceability_bundle(bundle: Mapping[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    nodes = bundle.get("nodes", [])
    edges = bundle.get("edges", [])
    node_types: Dict[str, str] = {}
    for node in nodes:
        node_id = node.get("id")
        node_type = node.get("type")
        if not node_id:
            errors.append("node_missing_id")
            continue
        if node_id in node_types:
            errors.append(f"duplicate_node:{node_id}")
        if node_type not in TRACE_NODE_TYPES:
            errors.append(f"invalid_node_type:{node_id}:{node_type}")
        node_types[str(node_id)] = str(node_type)

    adjacency = {node_id: set() for node_id in node_types}
    for edge in edges:
        source, target, relation = edge.get("from_id"), edge.get("to_id"), edge.get("relation")
        if source not in node_types or target not in node_types:
            errors.append(f"edge_orphan:{source}->{target}")
            continue
        if relation not in TRACE_RELATIONS:
            errors.append(f"invalid_relation:{relation}")
            continue
        expected = TRACE_RELATIONS[str(relation)]
        actual = (node_types[str(source)], node_types[str(target)])
        if actual != expected:
            errors.append(f"relation_type_mismatch:{relation}:{actual[0]}->{actual[1]}")
        adjacency[str(source)].add(str(target))

    if bundle.get("requires_end_to_end", True):
        sources = [node_id for node_id, kind in node_types.items() if kind == "SOURCE"]
        results = [node_id for node_id, kind in node_types.items() if kind == "RESULT"]
        if not sources:
            errors.append("missing_source_node")
        if not results:
            errors.append("missing_result_node")

        def reachable(start: str, target: str) -> bool:
            seen, stack = {start}, [start]
            while stack:
                current = stack.pop()
                if current == target:
                    return True
                for nxt in adjacency.get(current, set()):
                    if nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
            return False

        for result in results:
            if not any(reachable(source, result) for source in sources):
                errors.append(f"result_not_traceable_to_source:{result}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "node_count": len(node_types),
        "edge_count": len(edges),
    }


def change_impact_set(bundle: Mapping[str, Any], changed_ids: Sequence[str]) -> List[str]:
    nodes = {str(n["id"]): n for n in bundle.get("nodes", []) if n.get("id")}
    adjacency = {node_id: set() for node_id in nodes}
    for edge in bundle.get("edges", []):
        source, target = str(edge.get("from_id")), str(edge.get("to_id"))
        if source in nodes and target in nodes:
            adjacency[source].add(target)
    changed = {str(x) for x in changed_ids if str(x) in nodes}
    impacted, stack = set(), list(changed)
    while stack:
        current = stack.pop()
        for nxt in adjacency.get(current, set()):
            if nxt not in changed and nxt not in impacted:
                impacted.add(nxt)
                stack.append(nxt)
    return sorted(impacted)


def route_book_use(
    *, domain: str, task: str, source_passports: Sequence[Mapping[str, Any]], max_sources: int = 5
) -> Dict[str, Any]:
    domain = domain.upper()
    if domain not in DOMAIN_ADAPTERS:
        domain = "GENERAL"
    eligible = []
    for passport in source_passports:
        if validate_source_passport(passport):
            continue
        state = migrate_source_state(passport)
        if state["read_coverage"] == "NONE":
            continue
        targets = {str(x).upper() for x in passport.get("domain_targets", ["GENERAL"])}
        domain_score = 2 if domain in targets else 1 if "GENERAL" in targets else 0
        if domain_score:
            extraction_score = EXTRACTION_RANK[state["extraction_stage"]]
            coverage_score = {"NONE": 0, "STRUCTURE_ONLY": 1, "PARTIAL_TARGETED": 2, "FULL_READ": 3}[state["read_coverage"]]
            eligible.append((domain_score, extraction_score, coverage_score, passport))
    eligible.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    selected = [item[3]["source_id"] for item in eligible[:max_sources]]
    return {
        "domain": domain,
        "task": task,
        "selected_source_ids": selected,
        "retrieval_policy": "MECHANISM_FIRST_THEN_TARGETED_SOURCE_READ",
        "max_sources": max_sources,
        "requires_fresh_source_read": False if selected else True,
        "output_contract": [
            "claims_with_locators", "mechanism_cards", "failure_modes", "contradictions",
            "adapter_packet", "traceability_bundle", "promotion_state",
        ],
    }


def build_adapter_packet(
    *, domain: str, task: str, mechanism_cards: Sequence[Mapping[str, Any]],
    source_passports: Mapping[str, Mapping[str, Any]], max_mechanisms: int = 3,
) -> Dict[str, Any]:
    domain = domain.upper()
    ranked = []
    for card in mechanism_cards:
        if domain not in card.get("domain_targets", []) and "GENERAL" not in card.get("domain_targets", []):
            continue
        decision = promotion_decision(card, source_passports)
        rank = {"PROMOTABLE": 5, "PILOT_READY": 4, "LOCAL_TEST": 3, "REFERENCE_ONLY": 2, "HOLD": 1, "REJECT": 0}.get(decision["disposition"], 0)
        if rank <= 1:
            continue
        ranked.append((rank, card, decision))
    ranked.sort(key=lambda x: x[0], reverse=True)
    chosen = ranked[:max_mechanisms]
    return {
        "domain": domain,
        "task": task,
        "mechanisms": [{
            "mechanism_id": card.get("mechanism_id"),
            "statement": card.get("statement"),
            "disposition": decision["disposition"],
            "evidence_locators": card.get("evidence_locators", []),
            "failure_modes": card.get("failure_modes", []),
        } for _, card, decision in chosen],
        "constraints": [
            "NO_SOURCE_EXPRESSION_COPY",
            "NO_REFERENCE_AS_CANON",
            "NO_LOCKED_PROJECT_REOPEN_WITHOUT_NEW_FAILURE_EVIDENCE",
            "MAX_3_MECHANISMS_PER_LOCAL_APPLICATION_UNLESS_EXPLICITLY_JUSTIFIED",
            "BIDIRECTIONAL_TRACEABILITY_REQUIRED_FOR_PROMOTION",
            "ENGINEERING_VERIFICATION_NEQ_REAL_PROJECT_VALIDATION",
        ],
    }


def audit_library(passports: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    invalid = []
    integrity_counts = {s: 0 for s in INTEGRITY_STATUSES}
    read_counts = {s: 0 for s in READ_COVERAGE}
    extraction_counts = {s: 0 for s in EXTRACTION_STAGES}
    rights_counts = {s: 0 for s in RIGHTS_STATUSES}
    for passport in passports:
        errors = validate_source_passport(passport)
        if errors:
            invalid.append({"source_id": passport.get("source_id"), "errors": errors})
        state = migrate_source_state(passport)
        if state["integrity_status"] in integrity_counts:
            integrity_counts[state["integrity_status"]] += 1
        if state["read_coverage"] in read_counts:
            read_counts[state["read_coverage"]] += 1
        if state["extraction_stage"] in extraction_counts:
            extraction_counts[state["extraction_stage"]] += 1
        rights = passport.get("rights_status")
        if rights in rights_counts:
            rights_counts[rights] += 1
    return {
        "total": len(passports),
        "valid": len(passports) - len(invalid),
        "invalid": invalid,
        "integrity_counts": integrity_counts,
        "read_coverage_counts": read_counts,
        "extraction_counts": extraction_counts,
        "rights_counts": rights_counts,
    }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="IVDIVO Book Intelligence Engine v1.1")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_audit = sub.add_parser("audit-passports")
    p_audit.add_argument("json_path")

    p_dec = sub.add_parser("promotion-decision")
    p_dec.add_argument("card_json")
    p_dec.add_argument("passports_json")

    p_trace = sub.add_parser("audit-traceability")
    p_trace.add_argument("bundle_json")

    p_impact = sub.add_parser("impact")
    p_impact.add_argument("bundle_json")
    p_impact.add_argument("changed_ids", nargs="+")

    args = parser.parse_args()
    if args.cmd == "audit-passports":
        with open(args.json_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        passports = data["sources"] if isinstance(data, dict) and "sources" in data else data
        print(json.dumps(audit_library(passports), ensure_ascii=False, indent=2))
    elif args.cmd == "promotion-decision":
        with open(args.card_json, "r", encoding="utf-8") as handle:
            card = json.load(handle)
        with open(args.passports_json, "r", encoding="utf-8") as handle:
            p_data = json.load(handle)
        passports = p_data.get("sources", p_data)
        if isinstance(passports, list):
            passports = {x["source_id"]: x for x in passports}
        print(json.dumps(promotion_decision(card, passports), ensure_ascii=False, indent=2))
    elif args.cmd == "audit-traceability":
        with open(args.bundle_json, "r", encoding="utf-8") as handle:
            print(json.dumps(audit_traceability_bundle(json.load(handle)), ensure_ascii=False, indent=2))
    elif args.cmd == "impact":
        with open(args.bundle_json, "r", encoding="utf-8") as handle:
            print(json.dumps(change_impact_set(json.load(handle), args.changed_ids), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
