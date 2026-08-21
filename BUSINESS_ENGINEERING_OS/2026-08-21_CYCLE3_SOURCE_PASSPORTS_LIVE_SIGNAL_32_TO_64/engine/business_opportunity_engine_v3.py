from dataclasses import dataclass
from typing import Optional, List, Dict

K_ORDER={f"K{i}":i for i in range(6)}
S_ORDER={f"S{i}":i for i in range(5)}
E_ORDER={"E0":0,"E1":1,"E2":2,"E2+":2.5,"E3":3,"E4":4,"E5":5,"E6":6,"E7":7}

@dataclass
class LiveSignal:
    authoritative: bool
    fresh: bool
    corroborated: bool=False
    public_buyer_mapping: bool=False
    def grade(self)->str:
        if not self.authoritative: return "S0"
        if not self.fresh: return "S1"
        if not self.corroborated: return "S2"
        if not self.public_buyer_mapping: return "S3"
        return "S4"

@dataclass
class Experiment:
    name: str
    cash_cost_eur: float
    information_value: float
    reversible: bool=True
    evidence_strength: float=1.0
    @property
    def decision_value(self):
        penalty=1.0 if self.reversible else 0.5
        return (self.information_value*self.evidence_strength*penalty)/(1+self.cash_cost_eur)

def select_experiment(experiments:List[Experiment], founder_cash_limit_eur:float=0.0)->Optional[Experiment]:
    eligible=[e for e in experiments if e.cash_cost_eur<=founder_cash_limit_eur]
    return max(eligible,key=lambda e:e.decision_value) if eligible else None

def public_evidence_ceiling(no_outreach:bool=True)->str:
    return "E2+" if no_outreach else "E3_POSSIBLE_NOT_PROVEN"

def market_grade_from_public_signal(signal_grade:str,no_outreach:bool=True)->str:
    if signal_grade not in S_ORDER: raise ValueError('bad signal grade')
    if S_ORDER[signal_grade]>=1:
        return "E2+" if S_ORDER[signal_grade]>=4 and no_outreach else "E1"
    return "E0"

def cash_gap(inflows:List[float],outflows:List[float])->float:
    if len(inflows)!=len(outflows): raise ValueError('timeline mismatch')
    cumulative=0.0; min_cum=0.0
    for i,o in zip(inflows,outflows):
        cumulative += i-o
        min_cum=min(min_cum,cumulative)
    return -min_cum

def zero_founder_cash_gate(gap:Optional[float], external_bridge:bool)->str:
    if gap is None: return "HOLD_UNKNOWN"
    if gap<=0: return "PASS"
    return "PASS_EXTERNAL_BRIDGE_REQUIRED" if external_bridge else "FAIL_ZERO_FOUNDER_CASH"

def micro_market_gate(segment:Optional[str],benefit:Optional[str],access:Optional[str])->str:
    return "PASS" if all([segment,benefit,access]) else "KILL_OR_RESHAPE"

def strategic_power_gate(benefit:bool,barrier:bool)->str:
    return "POWER_CANDIDATE" if benefit and barrier else "UNPROVEN"

def v3_candidate_gate(global_authority_effect:bool, real_pilot_net_gain:bool)->str:
    if global_authority_effect and not real_pilot_net_gain: return "FAIL_CLOSED"
    return "CANDIDATE_ONLY" if not real_pilot_net_gain else "ELIGIBLE_FOR_PROMOTION_REVIEW"

def validate_opportunity(obj:Dict,no_outreach:bool=True)->List[str]:
    errors=[]
    proof=obj.get('proof',{})
    if no_outreach and E_ORDER.get(proof.get('E_grade','E0'),99)>E_ORDER['E2+']:
        errors.append('PUBLIC_EVIDENCE_CANNOT_PROMOTE_E3')
    if obj.get('buyer_workload',{}).get('willingness_to_pay') is not None and no_outreach:
        errors.append('WTP_MUST_BE_NULL_WITHOUT_BUYER_EVIDENCE')
    if obj.get('capital_topology',{}).get('founder_cash_eur',0)>0:
        errors.append('FOUNDER_CASH_CONSTRAINT_BREACH')
    mm=obj.get('micro_market',{})
    if micro_market_gate(mm.get('segment'),mm.get('benefit'),mm.get('access'))!='PASS':
        errors.append('MICRO_MARKET_INCOMPLETE')
    return errors

def route_vector(create:Dict,broker:Dict,acquire:Dict)->Dict[str,Dict]:
    # intentionally no total score; preserve vectors
    return {'CREATE':create,'BROKER':broker,'ACQUIRE':acquire}
