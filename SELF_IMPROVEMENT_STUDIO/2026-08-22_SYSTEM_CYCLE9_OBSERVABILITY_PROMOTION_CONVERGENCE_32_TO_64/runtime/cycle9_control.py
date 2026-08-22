#!/usr/bin/env python3
"""Bounded Cycle9 Self-Improvement controls.

This module is deliberately not a new Self-Improvement engine. It compiles
existing v2 lifecycle/evidence/meta-budget laws into small fail-closed helpers.
It cannot mutate CURRENT authority or execute durable multi-store writes.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Iterable, Mapping, Sequence


EVIDENCE_ORDER = {
    "NONE": 0,
    "SOURCE": 1,
    "MACHINE": 2,
    "PROVIDER": 3,
    "HUMAN": 4,
    "FOUNDER": 5,
    "BUYER": 6,
    "PAYMENT": 7,
}


def evidence_family_count(records: Sequence[Mapping]) -> dict:
    """Count independent raw evidence roots, not summaries/models."""
    roots = defaultdict(list)
    for r in records:
        root = r.get("raw_root_id")
        if not root:
            return {"status": "HOLD_MISSING_RAW_ROOT", "independent_families": None}
        roots[str(root)].append(dict(r))
    return {
        "status": "PASS",
        "independent_families": len(roots),
        "families": {k: len(v) for k, v in sorted(roots.items())},
    }


def evidence_class_firewall(*, claimed: str, evidence_class: str) -> dict:
    """Prevent class laundering; exact class or stronger does not imply semantics.

    The ordinal is used only for obvious impossible upward claims. Domain gates
    still decide whether a stronger class is relevant to the claimed fact.
    """
    c = claimed.upper()
    e = evidence_class.upper()
    if c not in EVIDENCE_ORDER or e not in EVIDENCE_ORDER:
        return {"status": "HOLD_UNKNOWN_EVIDENCE_CLASS", "allowed": False}
    if EVIDENCE_ORDER[e] < EVIDENCE_ORDER[c]:
        return {"status": "BLOCK_EVIDENCE_CLASS_LAUNDERING", "allowed": False, "required": c, "observed": e}
    return {"status": "CLASS_CEILING_POSSIBLE_DOMAIN_GATE_STILL_REQUIRED", "allowed": True, "required": c, "observed": e}


def promotion_eligibility(candidate: Mapping) -> dict:
    """Return review eligibility only. Never returns VERIFIED_CURRENT."""
    blockers = []
    required_truthy = [
        "development_contract",
        "pilot_evidence",
        "adversarial_review",
        "regression_evidence",
        "evaluation_matrix_result",
        "scope",
        "application_targets",
        "rollback_plan",
        "readback_plan",
    ]
    for field in required_truthy:
        if not candidate.get(field):
            blockers.append(field)
    if candidate.get("requires_independent_replication") and not candidate.get("independent_replication_evidence"):
        blockers.append("independent_replication_evidence")
    if candidate.get("requires_human") and not candidate.get("human_evidence"):
        blockers.append("human_evidence")
    if candidate.get("requires_provider") and not candidate.get("provider_evidence"):
        blockers.append("provider_evidence")
    if blockers:
        return {"status": "HOLD_PROMOTION_BLOCKERS", "eligible_for_review": False, "blockers": blockers, "auto_promote": False}
    return {"status": "ELIGIBLE_FOR_REVIEW", "eligible_for_review": True, "blockers": [], "auto_promote": False}


def negative_evidence_retention(*, existing_negative_ids: Iterable[str], proposed_retained_ids: Iterable[str], supersession_map: Mapping[str, str | None]) -> dict:
    existing = {str(x) for x in existing_negative_ids}
    retained = {str(x) for x in proposed_retained_ids}
    missing = []
    valid_superseded = []
    for item in sorted(existing - retained):
        replacement = supersession_map.get(item)
        if replacement:
            valid_superseded.append({"negative_id": item, "replacement": replacement})
        else:
            missing.append(item)
    if missing:
        return {"status": "BLOCK_NEGATIVE_EVIDENCE_LOSS", "allowed": False, "missing_unsuperseded": missing, "superseded": valid_superseded}
    return {"status": "PASS_NEGATIVE_EVIDENCE_RETAINED_OR_SUPERSEDED", "allowed": True, "missing_unsuperseded": [], "superseded": valid_superseded}


def engine_worthiness(*, recurrence: bool, stateful_coordination: bool, unique_runtime_contract: bool, current_owner_can_absorb: bool) -> dict:
    if current_owner_can_absorb:
        return {"status": "REUSE_OR_ADAPTER", "new_engine_allowed": False}
    if recurrence and stateful_coordination and unique_runtime_contract:
        return {"status": "ENGINE_REVIEW_CANDIDATE", "new_engine_allowed": False, "requires_review": True}
    return {"status": "RULE_OR_ADAPTER_NOT_ENGINE", "new_engine_allowed": False}


def meta_work_budget_governor(*, founder_selected_meta: bool, meta_direct_prerequisite: bool, higher_priority_product_task_unblocked: bool, active_meta_primary: int, active_meta_pilots: int) -> dict:
    if active_meta_primary > 1 or active_meta_pilots > 2:
        return {"status": "HOLD_META_WIP_OVERFLOW", "route": "REDUCE_META_WIP"}
    if founder_selected_meta:
        return {"status": "PASS_FOUNDER_META_FOCUS", "route": "META"}
    if meta_direct_prerequisite:
        return {"status": "PASS_META_PREREQUISITE", "route": "META"}
    if higher_priority_product_task_unblocked:
        return {"status": "RETURN_TO_PRODUCT", "route": "PRODUCT"}
    return {"status": "META_ALLOWED_BOUNDED", "route": "META"}


def self_reference_guard(*, modifies_self_improvement_gate: bool, waives_required_evidence: bool, externalized_review: bool) -> dict:
    if modifies_self_improvement_gate and waives_required_evidence:
        return {"status": "BLOCK_SELF_REFERENCE_GATE_WEAKENING", "allowed": False}
    if modifies_self_improvement_gate and not externalized_review:
        return {"status": "HOLD_EXTERNALIZED_REVIEW_REQUIRED", "allowed": False}
    return {"status": "PASS_SELF_REFERENCE_GUARD", "allowed": True}
