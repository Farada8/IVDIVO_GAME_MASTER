from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, Sequence, Tuple
from collections import deque

class IntegrationGateError(RuntimeError):
    pass

PROOF_ORDER={"E0":0,"E1":1,"E2":2,"E2_PLUS":2.5,"E3":3,"E4":4,"E5":5,"E6":6,"E7":7}
EXTERNAL_ACTIONS={"SEND_EMAIL","CALL","DM","CONTACT","PURCHASE","PAID_API","AD_SPEND","SIGN_CONTRACT"}

@dataclass(frozen=True)
class Constraints:
    no_outreach: bool=True
    new_founder_cash_eur: float=0.0
    public_evidence_ceiling: str="E2_PLUS"

@dataclass(frozen=True)
class PublicSignal:
    signal_id:str
    source_url:str
    official_primary:bool
    publication_date:Optional[str]
    event_date:Optional[str]
    application_date:Optional[str]
    jurisdiction:Optional[str]
    superseded:bool=False

def signal_state(s:PublicSignal)->str:
    if not s.source_url.strip(): raise IntegrationGateError("source URL required")
    if not s.official_primary: return "DISCOVERY_ONLY"
    if s.superseded: return "SUPERSEDED_ZERO_CURRENT_WEIGHT"
    if not s.jurisdiction: return "HOLD_JURISDICTION_UNKNOWN"
    return "CURRENT_PRIMARY_SIGNAL"

def date_triad(s:PublicSignal)->Tuple[Optional[str],Optional[str],Optional[str]]:
    return s.publication_date,s.event_date,s.application_date

def cap_market_proof(requested:str,c:Constraints=Constraints(),*,buyer_event:bool=False,payment_event:bool=False)->str:
    if requested not in PROOF_ORDER: raise IntegrationGateError("unknown proof level")
    if payment_event: return "E4"
    if buyer_event: return "E3"
    ceiling=c.public_evidence_ceiling
    return requested if PROOF_ORDER[requested]<=PROOF_ORDER[ceiling] else ceiling

def proof_plane_firewall(*,knowledge_level:str,signal_level:str,requested_market_level:str)->str:
    _=knowledge_level,signal_level
    return cap_market_proof(requested_market_level)

def action_gate(action:str,c:Constraints=Constraints())->bool:
    if c.no_outreach and action.upper() in EXTERNAL_ACTIONS:
        raise IntegrationGateError("external/irreversible action disabled")
    return True

@dataclass(frozen=True)
class CreativeOpportunity:
    opportunity_id:str
    official_source_url:Optional[str]
    source_fresh:bool
    eligibility:Optional[bool]
    deadline:Optional[str]
    total_project_budget_eur:Optional[float]
    artist_fee_eur:Optional[float]

def creative_state(o:CreativeOpportunity)->str:
    if not o.official_source_url: return "DISCOVERY_ONLY"
    if not o.source_fresh: return "HOLD_STALE_SOURCE"
    if o.eligibility is False: return "REJECT_INELIGIBLE"
    if o.eligibility is None: return "HOLD_ELIGIBILITY_UNKNOWN"
    if not o.deadline: return "HOLD_DEADLINE_UNKNOWN"
    if o.total_project_budget_eur is not None and o.artist_fee_eur is not None and o.artist_fee_eur>o.total_project_budget_eur:
        raise IntegrationGateError("artist fee exceeds project budget")
    return "APPLICATION_READY_RESEARCH"

def project_budget_is_artist_income(o:CreativeOpportunity)->bool:
    return bool(o.total_project_budget_eur is not None and o.artist_fee_eur is not None and o.total_project_budget_eur==o.artist_fee_eur)

@dataclass(frozen=True)
class OpportunityObject:
    opportunity_id:str
    buyer:str
    workload:str
    fatal_assumption:Optional[str]
    create_vector:Optional[Mapping[str,object]]=None
    broker_vector:Optional[Mapping[str,object]]=None
    acquire_vector:Optional[Mapping[str,object]]=None
    price_eur:Optional[float]=None
    delivery_cost_eur:Optional[float]=None
    delivery_minutes:Optional[float]=None

def opportunity_gate(o:OpportunityObject)->bool:
    if not o.buyer.strip() or not o.workload.strip(): raise IntegrationGateError("buyer/workload required")
    if not o.fatal_assumption: raise IntegrationGateError("fatal assumption required")
    return True

def observed_economics(o:OpportunityObject)->Optional[dict]:
    if None in (o.price_eur,o.delivery_cost_eur,o.delivery_minutes): return None
    return {"revenue_eur":o.price_eur,"delivery_cost_eur":o.delivery_cost_eur,"delivery_minutes":o.delivery_minutes,"contribution_eur":o.price_eur-o.delivery_cost_eur}

def finance_gate(proof_level:str,path:str)->str:
    if proof_level not in PROOF_ORDER: raise IntegrationGateError("unknown proof level")
    if PROOF_ORDER[proof_level]<PROOF_ORDER["E4"]: return "HOLD_DEMAND_PROOF_REQUIRED"
    return f"READY_TO_ASSESS_{path.upper()}"

@dataclass(frozen=True)
class DecisionLineage:
    evidence_refs:Tuple[str,...]
    interpretation:str
    competing_hypothesis:str
    decision:str
    expected_consequence:str
    actual_consequence:Optional[str]=None

def lineage_gate(d:DecisionLineage)->bool:
    if not d.evidence_refs: raise IntegrationGateError("evidence refs required")
    if any(not x.strip() for x in (d.interpretation,d.competing_hypothesis,d.decision,d.expected_consequence)):
        raise IntegrationGateError("lineage incomplete")
    return True

def selective_invalidation(edges:Mapping[str,Sequence[str]],changed:Iterable[str],locked:Iterable[str]=())->dict:
    dirty=set(changed); blocked=set(); locks=set(locked); q=deque(changed)
    while q:
        n=q.popleft()
        for nxt in edges.get(n,()):
            if nxt in locks: blocked.add(nxt); continue
            if nxt not in dirty: dirty.add(nxt); q.append(nxt)
    return {"dirty":tuple(sorted(dirty)),"blocked_locked":tuple(sorted(blocked))}

def shared_mechanism_disposition(*,semantic_duplicate:bool,current_sufficient:bool,new_decision_delta:bool)->str:
    if semantic_duplicate and current_sufficient: return "REUSE_CURRENT"
    if semantic_duplicate and not current_sufficient: return "MERGE_DELTA"
    if not new_decision_delta: return "NO_OP"
    return "KEEP_NEW_BOUNDED"

def self_improvement_gate(*,observed_defect:bool,regression_pass:bool,provenance_bound:bool,readback_pass:bool)->str:
    if not observed_defect: return "PROTECT_NO_CHANGE"
    if regression_pass and provenance_bound and readback_pass: return "READY_FOR_BOUNDED_PROMOTION"
    return "HOLD_EVIDENCE_INCOMPLETE"

def protected_project_gate(lock_state:str,mutation_scope:str)->bool:
    if lock_state.upper()=="FOUNDER_LOCKED" and mutation_scope.upper() not in {"EVIDENCE_ONLY","METADATA_ONLY"}:
        raise IntegrationGateError("Founder lock blocks mutation")
    return True

def cross_store_identity(expected_sha256:str,observed_sha256:str,expected_size:int,observed_size:int)->str:
    return "BINARY_EXTERNAL_PARITY" if expected_sha256==observed_sha256 and expected_size==observed_size else "IDENTITY_MISMATCH"

def business_profile(name:str)->Tuple[str,...]:
    profiles={
      "ZERO_CAPITAL":("ZERO_NEW_FOUNDER_CASH","BUYER_BEFORE_BUILD","FINANCE_AFTER_PROOF"),
      "REGULATORY_SHOCK":("OFFICIAL_SOURCE","DATE_SEMANTICS","LIABILITY_BOUNDARY","PUBLIC_EVIDENCE_CEILING"),
      "CREATIVE_OPPORTUNITY":("OFFICIAL_SOURCE_FRESHNESS","ELIGIBILITY_GATE","BUDGET_NEQ_INCOME","APPLICATION_OBJECT"),
      "PUBLIC_ART":("SITE_CONSTRAINT","FEE_VS_PRODUCTION_BUDGET","INSURANCE_HUMAN_HANDOFF","INSTALLATION_CASH_TIMING"),
      "HOSPITALITY":("BUYER_WORKFLOW","CAPEX_VS_SERVICE_SPLIT","OUTCOME_PROXY_GUARD","MANUAL_V0"),
      "CONSTRUCTION":("TENDER_SIGNAL","SCOPE_LIABILITY","QUOTE_JOB_DOC_WORKFLOW","CASH_CONVERSION"),
    }
    key=name.upper()
    if key not in profiles: raise IntegrationGateError("unknown profile")
    return profiles[key]
