from dataclasses import dataclass

PROOF_ORDER = {"E0":0,"E1":1,"E2":2,"E2_PLUS":2.5,"E3":3,"E4":4,"E5":5,"E6":6,"E7":7}

class GateError(RuntimeError):
    pass

@dataclass(frozen=True)
class Constraints:
    outreach_enabled: bool = False
    new_founder_cash_eur: float = 0.0
    public_evidence_ceiling: str = "E2_PLUS"

@dataclass(frozen=True)
class Opportunity:
    mandatory:int
    urgency:int
    evidence:int
    manual:int
    data:int
    repeat:int
    channel:int
    liability:int
    commodity:int
    complexity:int
    official_source:bool=True
    founder_cash_eur:float=0.0
    legal_or_assurance_claim:bool=False


def score(o: Opportunity) -> float:
    raw=(4*o.mandatory+3*o.urgency+3*o.evidence+3*o.manual+2*o.data+2*o.repeat+o.channel-2*o.liability-2*o.commodity-o.complexity)
    return round(max(0.0,min(100.0,raw/90.0*100.0)),1)


def zero_cash_gate(o: Opportunity, c: Constraints) -> bool:
    if c.new_founder_cash_eur != 0:
        raise GateError("cycle constraint requires zero new founder cash")
    if o.founder_cash_eur > 0:
        raise GateError("candidate requires founder cash before proof")
    return True


def official_source_gate(o: Opportunity) -> bool:
    if not o.official_source:
        raise GateError("material regulatory claim lacks first-party authority")
    return True


def liability_gate(o: Opportunity) -> bool:
    if o.legal_or_assurance_claim:
        raise GateError("legal/certification/security/emissions assurance must be specialist-routed")
    return True


def action_gate(action: str, c: Constraints) -> bool:
    external={"SEND_EMAIL","CALL","DM","CONTACT","PURCHASE","PAID_API","AD_SPEND"}
    if action in external and not c.outreach_enabled:
        raise GateError("external/outreach action disabled by user constraint")
    return True


def cap_proof(requested: str, c: Constraints, external_buyer_event: bool=False, payment_event: bool=False) -> str:
    if payment_event:
        return "E4"
    if external_buyer_event:
        return "E3"
    ceiling=c.public_evidence_ceiling
    return requested if PROOF_ORDER[requested] <= PROOF_ORDER[ceiling] else ceiling


def disposition(o: Opportunity) -> str:
    s=score(o)
    if o.founder_cash_eur > 0 or o.legal_or_assurance_claim:
        return "KILL_OR_MUTATE"
    if s >= 75:
        return "KEEP_RESEARCH"
    if s >= 60:
        return "WATCH_MUTATE"
    return "BACKLOG"
