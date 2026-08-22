from __future__ import annotations

from dataclasses import dataclass, asdict


ROUTES = {
    "M0_INTERNAL_PROOF_REQUIRED",
    "M0_BUYER_ROLE_REQUIRED",
    "M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN",
    "M2_PAID_DIAGNOSTIC_PROVEN_IMPLEMENTATION_NOT_PROVEN",
    "M3_IMPLEMENTATION_PROVEN_RECURRING_NOT_PROVEN",
    "M4_RECURRING_VALIDATED_SOFTWARE_NOT_PROVEN",
    "M5_SOFTWARE_CANDIDATE_NOT_SAAS_PROVEN",
}


@dataclass(frozen=True)
class MonetizationEvidence:
    opportunity_id: str
    technical_artifact: bool = False
    nontrivial_delta: bool = False
    buyer_role_plausible: bool = False
    paid_diagnostic_transactions: int = 0
    paid_implementation_transactions: int = 0
    paid_recurring_cycles: int = 0
    independent_customer_contexts_same_workflow: int = 0
    external_action_authorized: bool = False


class EvidenceError(ValueError):
    pass


def validate(e: MonetizationEvidence) -> None:
    for name in (
        "paid_diagnostic_transactions",
        "paid_implementation_transactions",
        "paid_recurring_cycles",
        "independent_customer_contexts_same_workflow",
    ):
        if getattr(e, name) < 0:
            raise EvidenceError(f"{name} cannot be negative")

    if e.nontrivial_delta and not e.technical_artifact:
        raise EvidenceError("nontrivial_delta requires technical_artifact")
    if e.paid_implementation_transactions and not e.paid_diagnostic_transactions:
        raise EvidenceError("implementation proof cannot precede paid diagnostic evidence in this ladder")
    if e.paid_recurring_cycles and not e.paid_implementation_transactions:
        raise EvidenceError("recurring proof cannot precede implementation evidence")
    if e.independent_customer_contexts_same_workflow and not e.paid_recurring_cycles:
        raise EvidenceError("software repetition evidence cannot precede recurring evidence")


def route(e: MonetizationEvidence) -> dict:
    validate(e)

    if not e.technical_artifact or not e.nontrivial_delta:
        disposition = "M0_INTERNAL_PROOF_REQUIRED"
    elif not e.buyer_role_plausible:
        disposition = "M0_BUYER_ROLE_REQUIRED"
    elif e.paid_diagnostic_transactions < 1:
        disposition = "M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN"
    elif e.paid_implementation_transactions < 1:
        disposition = "M2_PAID_DIAGNOSTIC_PROVEN_IMPLEMENTATION_NOT_PROVEN"
    elif e.paid_recurring_cycles < 2:
        disposition = "M3_IMPLEMENTATION_PROVEN_RECURRING_NOT_PROVEN"
    elif e.independent_customer_contexts_same_workflow < 3:
        disposition = "M4_RECURRING_VALIDATED_SOFTWARE_NOT_PROVEN"
    else:
        disposition = "M5_SOFTWARE_CANDIDATE_NOT_SAAS_PROVEN"

    return {
        "schema": "ivdivo.business.monetization_ladder/1.0",
        "opportunity_id": e.opportunity_id,
        "disposition": disposition,
        "evidence": asdict(e),
        "proof_boundary": {
            "external_action_authorized": e.external_action_authorized,
            "software_candidate_is_saas_proven": False,
            "price_is_wtp_without_transaction": False,
            "technical_artifact_is_market_proof": False,
        },
    }
