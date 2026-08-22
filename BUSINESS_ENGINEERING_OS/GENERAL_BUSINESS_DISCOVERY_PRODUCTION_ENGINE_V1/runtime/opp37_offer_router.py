from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


REQUIRED_ARTIFACT_COMPONENTS = (
    "ORDINARY_CONTROL_SUMMARY",
    "CANONICAL_FACT_LEDGER",
    "DIRECT_BOOKING_SURFACE_MAP",
    "PRIORITIZED_REPAIR_QUEUE",
    "NEGATIVE_FINDINGS",
    "ANSWERABILITY_VERIFICATION_SET",
    "IMPLEMENTATION_HANDOFF_CHECKLIST",
)

ALLOWED_ARCHITECTURES = (
    "PRODUCTIZED_ONE_SITE_DECISION_PACK",
    "IMPLEMENTATION_COORDINATOR_CONDITIONAL",
    "SAAS_TOOL_HOLD",
)

WAVE_STAGES = (
    "PRE_WAVE", "EMERGING", "EARLY_COMMERCIAL", "EXPANDING", "CROWDED", "LATE_COMMODITIZED"
)


@dataclass(frozen=True)
class OfferEvidence:
    test37_internal_pass: bool
    artifact_components: Sequence[str]
    source_provenance_required: bool = True
    ordinary_control_separated: bool = True
    negative_findings_allowed: bool = True
    claims_revenue_uplift: bool = False
    claims_wtp: bool = False
    claims_profitability: bool = False
    external_action_authorized: bool = False


def founder_profile_gate(*, remote_first: bool, founder_cash_at_risk_eur: float, founder_physical_load: str,
                         test_before_build_spend: bool, wave_stage: str) -> Mapping[str, object]:
    if wave_stage not in WAVE_STAGES:
        return {"status": "HOLD_UNKNOWN_WAVE_STAGE", "deep_dive_allowed": False}
    if not remote_first:
        return {"status": "OUT_OF_PROFILE_REMOTE", "deep_dive_allowed": False}
    if founder_cash_at_risk_eur > 3000:
        return {"status": "OUT_OF_PROFILE_CAPITAL", "deep_dive_allowed": False}
    if founder_physical_load not in ("NONE", "LOW"):
        return {"status": "OUT_OF_PROFILE_PHYSICAL", "deep_dive_allowed": False}
    if not test_before_build_spend:
        return {"status": "HOLD_TEST_BEFORE_BUILD_REQUIRED", "deep_dive_allowed": False}

    early = wave_stage in ("PRE_WAVE", "EMERGING", "EARLY_COMMERCIAL")
    return {
        "status": "FOUNDER_PROFILE_PASS",
        "deep_dive_allowed": True,
        "remote_first": True,
        "cash_within_default_ceiling": True,
        "early_wave_priority_eligible": early,
        "normal_cashflow_candidate": not early,
        "demand_proof": False,
        "proof_promotion": False,
    }


def _normalize_offer_name(name: str) -> str:
    normalized = name.upper().replace("-", "_").replace("/", "_")
    normalized = "_".join(normalized.split())
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized


def validate_offer(evidence: OfferEvidence, *, offer_name: str) -> Mapping[str, object]:
    if not evidence.test37_internal_pass:
        return {"status": "HOLD_TEST37_NOT_PASSED", "testable": False, "proof_promotion": False}
    if "GENERIC_AI_SEO_AUDIT" in _normalize_offer_name(offer_name):
        return {"status": "KILL_GENERIC_COMMODITY_CORE", "testable": False, "proof_promotion": False}

    missing = [x for x in REQUIRED_ARTIFACT_COMPONENTS if x not in set(evidence.artifact_components)]
    if missing:
        return {"status": "HOLD_INCOMPLETE_DECISION_ARTIFACT", "testable": False, "missing": missing, "proof_promotion": False}
    if not evidence.source_provenance_required:
        return {"status": "HOLD_PROVENANCE_REQUIRED", "testable": False, "proof_promotion": False}
    if not evidence.ordinary_control_separated:
        return {"status": "HOLD_NO_ORDINARY_CONTROL", "testable": False, "proof_promotion": False}
    if not evidence.negative_findings_allowed:
        return {"status": "HOLD_UPSELL_BIAS_NEGATIVE_CONTROL_REQUIRED", "testable": False, "proof_promotion": False}
    if evidence.claims_revenue_uplift or evidence.claims_wtp or evidence.claims_profitability:
        return {"status": "HOLD_UNPROVEN_MARKET_OR_ECONOMIC_CLAIM", "testable": False, "proof_promotion": False}

    return {
        "status": "INTERNAL_OFFER_TESTABLE_NO_MARKET_PROOF",
        "testable": True,
        "external_action_authorized": evidence.external_action_authorized,
        "buyer_behavior": False,
        "willingness_to_pay": None,
        "profitability": None,
        "proof_promotion": False,
    }


def pricing_hypothesis(*, delivery_cost_measured: bool = False, buyer_wtp_proven: bool = False) -> Mapping[str, object]:
    return {
        "currency": "EUR",
        "test_points_ex_vat": (249, 349, 490),
        "central_hypothesis": 349,
        "delivery_cost_measured": delivery_cost_measured,
        "buyer_wtp_proven": buyer_wtp_proven,
        "minimum_viable_price": None if not delivery_cost_measured else "REQUIRES_P33_P40_MODEL",
        "willingness_to_pay": None if not buyer_wtp_proven else "REQUIRES_REAL_BUYER_EVIDENCE",
        "profitability": None,
    }


def internal_decision_test(*, specific_decisions: int, protected_negative_controls: int, sample: int = 3) -> Mapping[str, object]:
    if sample != 3:
        return {"status": "HOLD_EXACT_THREE_SITE_FIXTURE_REQUIRED", "pass": False, "buyer_value_proven": False}
    passed = specific_decisions >= 2 and protected_negative_controls >= 1
    return {
        "status": "PASS_INTERNAL_DECISION_DISCRIMINATION" if passed else "FAIL_INTERNAL_DECISION_DISCRIMINATION",
        "pass": passed,
        "specific_decisions": specific_decisions,
        "protected_negative_controls": protected_negative_controls,
        "buyer_value_proven": False,
        "proof_promotion": False,
    }


def architecture_route(architecture: str, *, repeated_manual_need: bool = False, buyer_behavior: bool = False) -> Mapping[str, object]:
    if architecture not in ALLOWED_ARCHITECTURES:
        return {"status": "HOLD_UNKNOWN_ARCHITECTURE", "build": False}
    if architecture == "PRODUCTIZED_ONE_SITE_DECISION_PACK":
        return {"status": "INTERNAL_TESTABLE_EXTERNAL_USE_GATED", "build": True, "external_use": False}
    if architecture == "IMPLEMENTATION_COORDINATOR_CONDITIONAL":
        return {"status": "READY_ONLY_AFTER_BUYER_BEHAVIOR" if buyer_behavior else "HOLD_BUYER_BEHAVIOR_REQUIRED", "build": False}
    return {"status": "READY_ONLY_AFTER_REPEATED_MANUAL_NEED" if repeated_manual_need else "HOLD_REPEATED_MANUAL_NEED_REQUIRED", "build": False}


def next_route(*, founder_profile_pass: bool, p25_p32_complete: bool, ci_verified: bool) -> Mapping[str, object]:
    if not founder_profile_pass:
        return {"state": "HOLD_FOUNDER_PROFILE_RESREEN_REQUIRED", "next": "APPLY_FOUNDER_PROFILE", "external_action": False}
    if not p25_p32_complete:
        return {"state": "S3_FATAL_TEST_READY_WITH_INTERNAL_DIFFERENTIAL", "next": "COMPLETE_P25_P32", "external_action": False}
    if not ci_verified:
        return {"state": "S5_OFFER_TESTABLE_INTERNAL_ONLY_PENDING_CI", "next": "RUN_REGRESSION", "external_action": False}
    return {
        "state": "S5_OFFER_TESTABLE_INTERNAL_ONLY",
        "executed_next64": 32,
        "remaining_next64": 32,
        "next": "P33-P40_OPP37_NULL_SAFE_ECONOMICS_AND_MANUAL_DELIVERY_TIMING",
        "portfolio_disposition": "NORMAL_CASHFLOW_CANDIDATE",
        "early_wave_priority": False,
        "buyer_behavior": False,
        "willingness_to_pay": None,
        "transaction": None,
        "unit_economics": None,
        "external_action": False,
        "proof_promotion": False,
    }
