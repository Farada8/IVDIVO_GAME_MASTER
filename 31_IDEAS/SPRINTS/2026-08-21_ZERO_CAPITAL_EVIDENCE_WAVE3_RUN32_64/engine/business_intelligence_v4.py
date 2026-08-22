from dataclasses import dataclass, field
from typing import Dict, List, Optional


class BusinessIntelligenceGateError(RuntimeError):
    pass


@dataclass(frozen=True)
class Signal:
    source: str
    observed_date: str
    event_date: Optional[str]
    signal_type: str
    entity: str
    confidence: float
    contradicted: bool = False


@dataclass(frozen=True)
class OpportunityThesis:
    what_changed: str
    why_now: str
    affected_actor: str
    trigger: str
    payer: str
    falsifier: str
    zero_cash_deliverable: bool
    liability_boundary_ok: bool
    components: Dict[str, float] = field(default_factory=dict)


REQUIRED_COMPONENTS = (
    "signal_strength",
    "source_quality",
    "urgency",
    "buyer_specificity",
    "zero_cash_deliverability",
    "competition_pressure",
    "liability",
    "channel_leverage",
    "repeatability",
)


def signal_provenance_gate(signal: Signal) -> bool:
    if not signal.source.strip():
        raise BusinessIntelligenceGateError("signal source is required")
    if not signal.observed_date.strip():
        raise BusinessIntelligenceGateError("observation date is required")
    if not 0.0 <= signal.confidence <= 1.0:
        raise BusinessIntelligenceGateError("signal confidence must be in [0,1]")
    return True


def why_now_gate(thesis: OpportunityThesis) -> bool:
    required = (
        thesis.what_changed,
        thesis.why_now,
        thesis.affected_actor,
        thesis.trigger,
        thesis.payer,
        thesis.falsifier,
    )
    if any(not item.strip() for item in required):
        raise BusinessIntelligenceGateError("why-now thesis is incomplete")
    if not thesis.zero_cash_deliverable:
        raise BusinessIntelligenceGateError("candidate fails zero-cash deliverability")
    if not thesis.liability_boundary_ok:
        raise BusinessIntelligenceGateError("candidate crosses liability boundary")
    return True


def decomposed_score(thesis: OpportunityThesis) -> Dict[str, object]:
    missing = [key for key in REQUIRED_COMPONENTS if key not in thesis.components]
    if missing:
        raise BusinessIntelligenceGateError(f"missing score components: {','.join(missing)}")
    for key in REQUIRED_COMPONENTS:
        value = thesis.components[key]
        if not 0.0 <= value <= 1.0:
            raise BusinessIntelligenceGateError(f"component {key} must be in [0,1]")

    positive = (
        thesis.components["signal_strength"] * 0.16
        + thesis.components["source_quality"] * 0.14
        + thesis.components["urgency"] * 0.16
        + thesis.components["buyer_specificity"] * 0.12
        + thesis.components["zero_cash_deliverability"] * 0.12
        + thesis.components["channel_leverage"] * 0.08
        + thesis.components["repeatability"] * 0.12
    )
    penalties = (
        thesis.components["competition_pressure"] * 0.05
        + thesis.components["liability"] * 0.05
    )
    value = max(0.0, min(1.0, positive - penalties))
    return {
        "score": round(value * 100.0, 1),
        "components": dict(thesis.components),
        "authority": "ROUTING_ONLY_E2_PLUS_CEILING",
    }


def public_evidence_ceiling(requested_proof: str) -> str:
    order = {"E0": 0, "E1": 1, "E2": 2, "E2_PLUS": 2.5, "E3": 3, "E4": 4, "E5": 5, "E6": 6, "E7": 7}
    if requested_proof not in order:
        raise BusinessIntelligenceGateError("unknown proof level")
    return requested_proof if order[requested_proof] <= order["E2_PLUS"] else "E2_PLUS"


def decision_lineage(evidence_refs: List[str], interpretation: str, competing_hypothesis: str,
                     decision: str, expected_consequence: str) -> Dict[str, object]:
    if not evidence_refs:
        raise BusinessIntelligenceGateError("decision lineage requires evidence refs")
    fields = [interpretation, competing_hypothesis, decision, expected_consequence]
    if any(not item.strip() for item in fields):
        raise BusinessIntelligenceGateError("decision lineage is incomplete")
    return {
        "evidence_refs": list(evidence_refs),
        "interpretation": interpretation,
        "competing_hypothesis": competing_hypothesis,
        "decision": decision,
        "expected_consequence": expected_consequence,
        "actual_consequence": None,
    }
