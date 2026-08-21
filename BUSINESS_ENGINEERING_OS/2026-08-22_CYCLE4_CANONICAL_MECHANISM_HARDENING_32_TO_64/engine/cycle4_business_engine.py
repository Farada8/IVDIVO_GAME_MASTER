from dataclasses import dataclass
from typing import Optional, Sequence, Mapping, Any

@dataclass(frozen=True)
class SourceAlias:
    file_id: str
    canonical_work_id: Optional[str]
    byte_hash: Optional[str] = None
    broken: bool = False
    replacement_file_id: Optional[str] = None

@dataclass(frozen=True)
class Contradiction:
    left_claim: str
    right_claim: str
    scope: str
    resolution: str

@dataclass(frozen=True)
class Measurement:
    decision: str
    uncertainty_reduction: float
    decision_value: float
    cost: float

@dataclass(frozen=True)
class WorkItem:
    id: str
    priority: int
    ready: bool = True

def canonical_evidence_family(aliases: Sequence[SourceAlias]) -> dict[str,list[str]]:
    families={}
    for a in aliases:
        if a.broken: continue
        key=a.byte_hash or a.canonical_work_id or f"UNRESOLVED:{a.file_id}"
        families.setdefault(key,[]).append(a.file_id)
    return families

def resolve_broken_alias(alias: SourceAlias, valid_file_ids:set[str]) -> str:
    if not alias.broken: return "VALID"
    if alias.replacement_file_id and alias.replacement_file_id in valid_file_ids:
        return "REPLACED_BY_VALID_ALIAS"
    return "ZERO_EVIDENCE_HOLD"

def k5_fixture(source_present:bool, deterministic_fixture_passed:bool, overclaim:bool=False)->str:
    if overclaim or not source_present: return "HOLD"
    return "K5" if deterministic_fixture_passed else "K4"

def route_framework(*,question:str,irreversible_cost:float,uncertainty:str)->str:
    q=question.lower()
    if "fatal" in q or "seven domain" in q: return "ROAD_TEST"
    if "job" in q or "circumstance" in q or "progress" in q: return "JTBD"
    if "position" in q or "category" in q: return "POSITIONING"
    if "pains" in q or "gains" in q or "value map" in q: return "VPC"
    if "experiment" in q or "evidence" in q: return "TBI"
    if "mvp" in q or "pivot" in q or "validated learning" in q: return "LEAN"
    if irreversible_cost>0 and uncertainty=="HIGH": return "ROAD_TEST_THEN_TBI"
    return "CONDITIONAL_ROUTING_REQUIRED"

def route_contradiction(left:Mapping[str,Any],right:Mapping[str,Any])->Contradiction:
    scope=left.get("scope") if left.get("scope")==right.get("scope") else "SCOPE_MISMATCH"
    return Contradiction(str(left.get("claim")),str(right.get("claim")),scope,"PRESERVE_AND_TEST")

def format_uncertainty(kind:str,value:Any=None,low:float|None=None,high:float|None=None,scenarios:Mapping[str,float]|None=None)->dict:
    if kind=="binary":
        if value not in (True,False,None): raise ValueError("binary must be true/false/null")
        return {"kind":"binary","value":value}
    if kind=="interval":
        if low is None or high is None or low>high: raise ValueError("valid interval required")
        return {"kind":"interval","low":low,"high":high}
    if kind=="scenario":
        if not scenarios: raise ValueError("scenarios required")
        return {"kind":"scenario","scenarios":dict(scenarios)}
    raise ValueError("unsupported uncertainty kind")

def voi(m:Measurement)->dict:
    if m.cost<0: raise ValueError("cost cannot be negative")
    ev=max(0.0,m.decision_value*m.uncertainty_reduction)
    return {"decision":m.decision,"expected_information_value":ev,"cost":m.cost,"run":ev>m.cost}

def wip_select(items:Sequence[WorkItem],primary_limit:int=1,pilot_limit:int=2)->dict:
    ready=sorted((i for i in items if i.ready),key=lambda x:(x.priority,x.id))
    p=ready[:primary_limit]; pilots=ready[primary_limit:primary_limit+pilot_limit]; held=ready[primary_limit+pilot_limit:]
    return {"primary":[x.id for x in p],"pilots":[x.id for x in pilots],"held":[x.id for x in held]}

def quick_stop(*,learning_milestone:bool,customer_milestone:bool,irreversible_spend:bool)->str:
    if irreversible_spend and not (learning_milestone or customer_milestone): return "STOP_NO_EVIDENCE_MILESTONE"
    if not learning_milestone and not customer_milestone: return "HOLD_REDESIGN_TEST"
    return "CONTINUE"

def human_handoff(*,economics_material_unknown:bool=False,legal_material_unknown:bool=False,provider_required:bool=False)->str:
    if legal_material_unknown: return "STOP_HUMAN_LEGAL_REQUIRED"
    if economics_material_unknown: return "STOP_HUMAN_ECONOMICS_REQUIRED"
    if provider_required: return "STOP_EXTERNAL_PROVIDER_REQUIRED"
    return "AUTOMATION_ALLOWED"

def anti_fake_precision(obj:Mapping[str,Any])->str:
    if {"total_score","magic_score","overall_score"}.intersection(obj): return "REJECT_ADDITIVE_SCORE"
    return "PASS"

def creative_opportunity_state(*,source_is_official:bool,deadline_verified:bool,eligibility_verified:bool,budget_verified:bool)->str:
    if not source_is_official: return "DISCOVERY_ONLY"
    if not deadline_verified: return "HOLD_DEADLINE"
    if not eligibility_verified: return "HOLD_ELIGIBILITY"
    if not budget_verified: return "HOLD_BUDGET"
    return "APPLICATION_READY_FACTS"
