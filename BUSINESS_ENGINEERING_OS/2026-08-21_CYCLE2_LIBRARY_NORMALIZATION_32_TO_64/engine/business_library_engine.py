from dataclasses import dataclass
from typing import Optional, Literal
EvidenceGrade = Literal["E0","E1","E2","E2+","E3","E4","E5","E6","E7"]

@dataclass(frozen=True)
class Source:
    integrity: str
    duplicate_group: Optional[str]=None
    canonical_identity: str="UNRESOLVED"

@dataclass(frozen=True)
class Opportunity:
    micro_market_benefit: bool
    differentiated: bool
    why_now: bool
    evidence_grade: EvidenceGrade="E0"
    founder_cash_gap: Optional[float]=None
    customer_funded: bool=False
    current_constraint: Optional[str]=None

@dataclass(frozen=True)
class Power:
    benefit: bool
    barrier: bool

def source_weight(source: Source) -> int:
    return 0 if source.integrity == "BROKEN" else 1

def micro_market_gate(o: Opportunity) -> str:
    return "PASS" if o.micro_market_benefit and o.differentiated else "KILL_OR_RESHAPE"

def why_now_gate(o: Opportunity) -> str:
    return "PASS" if o.why_now else "HOLD"

def market_proof_ceiling(no_outreach: bool, grade: EvidenceGrade) -> EvidenceGrade:
    order=["E0","E1","E2","E2+","E3","E4","E5","E6","E7"]
    if no_outreach and order.index(grade) > order.index("E2+"):
        return "E2+"
    return grade

def zero_founder_cash_gate(o: Opportunity) -> str:
    if o.founder_cash_gap is None:
        return "UNKNOWN"
    if o.founder_cash_gap <= 0:
        return "PASS"
    if o.customer_funded:
        return "PASS_WITH_CUSTOMER_FUNDING"
    return "FAIL_ZERO_CASH"

def constraint_gate(o: Opportunity) -> str:
    return "PASS" if o.current_constraint else "HOLD_IDENTIFY_CONSTRAINT"

def power_gate(p: Power) -> str:
    return "POWER_POSSIBLE" if p.benefit and p.barrier else "NO_DURABLE_POWER_PROVEN"

def create_broker_acquire_routes():
    return ("CREATE","BROKER_ORCHESTRATE","ACQUIRE")

def acquisition_target_metric(sde: Optional[float]) -> str:
    return "SDE_CASHFLOW_REQUIRED" if sde is None else "SDE_AVAILABLE"

def premature_scale(grade: EvidenceGrade) -> str:
    return "BLOCK" if grade in ("E0","E1","E2","E2+") else "REVIEW"
