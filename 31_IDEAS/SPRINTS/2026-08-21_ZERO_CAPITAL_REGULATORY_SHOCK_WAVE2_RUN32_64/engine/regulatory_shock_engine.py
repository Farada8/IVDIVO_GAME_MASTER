from dataclasses import dataclass
from enum import IntEnum

class Evidence(IntEnum):
    E0_HYPOTHESIS = 0
    E1_AUTHORITY_SIGNAL = 1
    E2_MARKET_OBSERVATION = 2
    E3_BUYER_ENGAGEMENT = 3
    E4_PAYMENT_OR_PO = 4
    E5_REPEAT_PAID = 5
    E6_RETENTION_BANKABLE = 6
    E7_SCALE = 7

@dataclass(frozen=True)
class Opportunity:
    name: str
    founder_cash_preproof: float
    official_source: bool
    manual_v0: bool
    legal_or_certification_claim: bool = False
    qualified_contacts: int = 0
    e3_events: int = 0
    e4_events: int = 0

def zero_cash_gate(o: Opportunity) -> bool:
    return o.founder_cash_preproof == 0 and o.manual_v0

def authority_gate(o: Opportunity) -> bool:
    return o.official_source

def liability_gate(o: Opportunity) -> bool:
    return not o.legal_or_certification_claim

def market_state(o: Opportunity) -> Evidence:
    if o.e4_events >= 3:
        return Evidence.E5_REPEAT_PAID
    if o.e4_events >= 1:
        return Evidence.E4_PAYMENT_OR_PO
    if o.e3_events >= 1:
        return Evidence.E3_BUYER_ENGAGEMENT
    if o.official_source:
        return Evidence.E1_AUTHORITY_SIGNAL
    return Evidence.E0_HYPOTHESIS

def governor(o: Opportunity) -> str:
    if not authority_gate(o):
        return "HOLD_SOURCE"
    if not zero_cash_gate(o):
        return "REJECT_ZERO_CASH"
    if not liability_gate(o):
        return "ESCALATE_SPECIALIST"
    if o.qualified_contacts >= 20 and o.e3_events < 2 and o.e4_events == 0:
        return "KILL_OR_MATERIAL_PIVOT"
    if o.e4_events >= 3:
        return "PRODUCTISE_AND_MEASURE_RETENTION"
    if o.e4_events >= 1:
        return "DELIVER_PAID_PILOT_AND_MEASURE"
    if o.e3_events >= 1:
        return "DISCOVERY_AND_PRICE_TEST"
    return "TARGETED_OUTREACH_MAX_5"

def may_build_software(o: Opportunity) -> bool:
    return market_state(o) >= Evidence.E3_BUYER_ENGAGEMENT

def may_seek_acceleration_finance(o: Opportunity) -> bool:
    return market_state(o) >= Evidence.E4_PAYMENT_OR_PO
