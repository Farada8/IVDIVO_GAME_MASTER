from dataclasses import dataclass, field
from typing import Optional, List, Dict

E_RANK={"E0":0,"E1":1,"E2":2,"E2+":2.5,"E3":3,"E4":4,"E5":5,"E6":6,"E7":7}

@dataclass
class Opportunity:
    name: str
    why_now: Optional[str]=None
    target_segment: Optional[str]=None
    clear_benefit: bool=False
    differentiated: bool=False
    manual_v0: bool=False
    founder_cash_required: float=0.0
    customer_funding_available: bool=False
    external_buyer_interaction: bool=False
    payment_proof: bool=False
    evidence_level: str="E0"
    current_constraint: Optional[str]=None
    economics: Dict[str, Optional[float]]=field(default_factory=dict)
    entry_modes: List[str]=field(default_factory=lambda:["CREATE","BROKER","ACQUIRE"])

def clamp_evidence(o: Opportunity)->str:
    if o.payment_proof:
        return max(o.evidence_level,"E4",key=lambda x:E_RANK[x])
    if o.external_buyer_interaction:
        if E_RANK.get(o.evidence_level,0)>3: return "E3"
        return max(o.evidence_level,"E3",key=lambda x:E_RANK[x])
    return o.evidence_level if E_RANK.get(o.evidence_level,0)<=2.5 else "E2+"

def micro_market_gate(o: Opportunity)->str:
    if not o.target_segment or not o.clear_benefit or not o.differentiated:
        return "KILL_OR_RESHAPE"
    return "PASS"

def zero_cash_gate(o: Opportunity)->str:
    if o.founder_cash_required <= 0: return "PASS"
    if o.customer_funding_available: return "MUTATE_TO_CUSTOMER_FUNDED"
    return "FAIL_ZERO_CASH"

def build_scale_gate(o: Opportunity)->str:
    e=clamp_evidence(o)
    return "ALLOW_EXECUTION_SCALE" if E_RANK[e] >= 4 else "BLOCK_PREMATURE_SCALE"

def economics_gate(o: Opportunity)->str:
    required=("price","gross_margin","conversion","cash_cycle_days")
    if any(o.economics.get(k) is None for k in required):
        return "UNKNOWN_KEEP_NULL"
    return "MEASURED"

def constraint_gate(o: Opportunity)->str:
    return "PASS" if o.current_constraint else "IDENTIFY_CONSTRAINT_FIRST"

def route(o: Opportunity)->dict:
    return {"evidence":clamp_evidence(o),"micro_market":micro_market_gate(o),"zero_cash":zero_cash_gate(o),"scale":build_scale_gate(o),"economics":economics_gate(o),"constraint":constraint_gate(o),"entry_modes":o.entry_modes}
