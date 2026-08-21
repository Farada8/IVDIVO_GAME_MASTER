from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import IntEnum
from typing import Dict, List

class EvidenceGrade(IntEnum):
    E0_HYPOTHESIS = 0
    E1_AUTHORITATIVE_SIGNAL = 1
    E2_OBSERVED_BUYER_PAIN = 2
    E3_BUYER_INTEREST_OR_LOI = 3
    E4_PAID_PILOT_DEPOSIT_OR_PO = 4
    E5_REPEATED_PAID_DELIVERY = 5
    E6_FINANCE_READY = 6
    E7_SCALE_PROVEN = 7

WEIGHTS: Dict[str, float] = {
    "cashless_start": 0.22,
    "buyer_before_build": 0.18,
    "speed_to_first_revenue": 0.15,
    "demand_signal": 0.15,
    "repeatability": 0.10,
    "financing_ladder": 0.10,
    "gross_margin_potential": 0.10,
}

@dataclass(frozen=True)
class OpportunityCandidate:
    name: str
    cashless_start: int
    buyer_before_build: int
    speed_to_first_revenue: int
    demand_signal: int
    repeatability: int
    financing_ladder: int
    gross_margin_potential: int
    regulation_complexity: int = 0
    long_cycle_risk: int = 0
    founder_cash_pre_proof_eur: float = 0.0
    irreversible_commitment_pre_payment: bool = False
    evidence_grade: EvidenceGrade = EvidenceGrade.E0_HYPOTHESIS

    def validate(self) -> None:
        for field in WEIGHTS:
            v = getattr(self, field)
            if not 0 <= v <= 5:
                raise ValueError(f"{field} must be 0..5")
        for field in ("regulation_complexity", "long_cycle_risk"):
            v = getattr(self, field)
            if not 0 <= v <= 5:
                raise ValueError(f"{field} must be 0..5")
        if self.founder_cash_pre_proof_eur < 0:
            raise ValueError("founder cash cannot be negative")

def zero_cash_gate(c: OpportunityCandidate) -> bool:
    """PASS only when no new irreversible founder cash-out is required before external payment proof."""
    c.validate()
    return c.founder_cash_pre_proof_eur == 0 and not c.irreversible_commitment_pre_payment

def score(c: OpportunityCandidate) -> int:
    c.validate()
    base = sum(getattr(c, k) / 5 * w for k, w in WEIGHTS.items()) * 100
    penalty = c.regulation_complexity * 1.4 + c.long_cycle_risk * 1.4
    return max(0, min(100, round(base - penalty)))

def next_action(c: OpportunityCandidate) -> str:
    if not zero_cash_gate(c):
        return "RESTRUCTURE_OR_KILL_PRE_PROOF_CASH_REQUIREMENT"
    if c.evidence_grade < EvidenceGrade.E1_AUTHORITATIVE_SIGNAL:
        return "GROUND_WITH_AUTHORITATIVE_SIGNAL"
    if c.evidence_grade < EvidenceGrade.E3_BUYER_INTEREST_OR_LOI:
        return "RUN_ZERO_COST_BUYER_DISCOVERY"
    if c.evidence_grade < EvidenceGrade.E4_PAID_PILOT_DEPOSIT_OR_PO:
        return "SELL_MANUAL_PAID_PILOT_BEFORE_BUILD"
    if c.evidence_grade < EvidenceGrade.E5_REPEATED_PAID_DELIVERY:
        return "DELIVER_MANUALLY_AND_CAPTURE_UNIT_ECONOMICS"
    if c.evidence_grade < EvidenceGrade.E6_FINANCE_READY:
        return "STANDARDISE_AND_PREPARE_FINANCE_PACKAGE"
    if c.evidence_grade < EvidenceGrade.E7_SCALE_PROVEN:
        return "AUTOMATE_AND_SCALE_WITH_EXTERNAL_CAPITAL"
    return "SCALE_WITH_REGRESSION_MONITORING"

def proof_ladder() -> List[str]:
    return [
        "P0 SOURCE_PROOF — authoritative external signal exists",
        "P1 PROBLEM_PROOF — specific buyer pain observed",
        "P2 INTEREST_PROOF — buyer asks for proposal/LOI/call",
        "P3 PAYMENT_PROOF — paid pilot/deposit/PO/commission trigger",
        "P4 DELIVERY_PROOF — delivered outcome with actual cost/time",
        "P5 REPEATABILITY_PROOF — repeated paid delivery to >=3 buyers",
        "P6 FINANCEABILITY_PROOF — bank/grant/invoice finance or investor can underwrite evidence",
        "P7 SCALE_PROOF — acquisition + delivery + margin survive increased volume",
    ]

def serialize(c: OpportunityCandidate) -> dict:
    d = asdict(c)
    d["evidence_grade"] = c.evidence_grade.name
    d["zero_cash_gate"] = zero_cash_gate(c)
    d["score"] = score(c)
    d["next_action"] = next_action(c)
    return d
