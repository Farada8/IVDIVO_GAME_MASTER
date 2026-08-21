#!/usr/bin/env python3
"""IVDIVO SI-0012 minimum compatibility runtime v0.1.

WORKING/PILOT candidate. This module is a compatibility/execution layer under
CURRENT Self-Improvement v2 + machine-execution authority. It is not story
canon and does not issue Founder locks, spend provider credits, or fabricate
human/provider/market evidence.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any
import hashlib, time, uuid

RANK={"VERIFIED_CURRENT":60,"MERGED_MAIN":60,"LOCKED":60,"APPROVED":55,"WORKING_SYNC_PENDING":40,"WORKING":35,"DISCOVERY_ONLY":10,"REFERENCE_ONLY":5,"SUPERSEDED":0}
DOMAINS={"BOOK","AUDIO","ENGINE","RESEARCH","OPERATIONS","META"}
GRADES={"SOURCE_EXPLICIT","CONTINUITY_REQUIRED","DERIVED_INFERENCE","DESIGN_CHOICE","UNSUPPORTED"}

@dataclass
class SourceRef:
    kind:str; locator:str; status:str; revision:str|None=None; updated:str|None=None; authority:bool=False

@dataclass
class NormalizedState:
    project_id:str; title:str; domain:str; authority_source:SourceRef; work_frontier_source:SourceRef; status:str
    phase:str|None=None; next_obligation:str|None=None; stop_reason:str|None=None
    blockers:list[str]=field(default_factory=list); protected_facts:list[dict[str,Any]]=field(default_factory=list)
    prohibited_actions:list[str]=field(default_factory=list); parallel_safe_branches:list[str]=field(default_factory=list)
    evidence_boundaries:list[str]=field(default_factory=list); raw_refs:list[str]=field(default_factory=list)
    def to_dict(self): return asdict(self)


def select_sources(sources:list[SourceRef]):
    if not sources: raise ValueError("NO_SOURCES")
    auth=[s for s in sources if s.authority and RANK.get(s.status,-1)>=50]
    if not auth: raise ValueError("AUTHORITY_UNRESOLVED")
    authority=max(auth,key=lambda s:(RANK.get(s.status,-1),s.updated or ""))
    usable=[s for s in sources if RANK.get(s.status,-1)>0]
    frontier=max(usable,key=lambda s:((s.updated or ""),RANK.get(s.status,-1)))
    return authority,frontier


def make_fact(fact_id,value,grade,source_refs,consumers=None,protected=False):
    if grade not in GRADES: raise ValueError("INVALID_ASSERTION_GRADE")
    if grade!="UNSUPPORTED" and not source_refs: raise ValueError("SUPPORTED_FACT_REQUIRES_SOURCE")
    return {"fact_id":fact_id,"value":value,"assertion_grade":grade,"source_refs":list(source_refs),"consumers":list(consumers or []),"protected":bool(protected)}


def adapt_project(bundle:dict[str,Any])->NormalizedState:
    domain=bundle["domain"].upper()
    if domain not in DOMAINS: raise ValueError(f"UNSUPPORTED_DOMAIN:{domain}")
    sources=[SourceRef(**s) for s in bundle["sources"]]
    authority,frontier=select_sources(sources)
    main=bundle.get("state",{}); working=bundle.get("working_state") or {}
    state=working if frontier.locator==bundle.get("working_state_locator") else main
    project_id=str(state.get("project_id") or state.get("project") or bundle.get("project_id") or "UNKNOWN")
    title=str(state.get("title") or state.get("project") or bundle.get("title") or project_id)
    status=str(state.get("status") or state.get("current_phase") or state.get("mode") or "UNKNOWN")
    phase=state.get("current_production_phase") or state.get("current_phase") or state.get("scope")
    next_obligation=(state.get("highest_unblocked_obligation") or state.get("next_unblocked_obligation") or (state.get("next_action") or {}).get("stage") or state.get("next_queue"))
    stop_reason="FOUNDER_DECISION_REQUIRED" if ("FOUNDER" in status.upper() or "FOUNDER" in str(state.get("mode","")).upper()) else None
    blockers=[]; prohibited=[]; parallel=[]; boundaries=[]; facts=[]
    blocker=state.get("current_blocker")
    if blocker:
        blockers.append(str(blocker.get("type") if isinstance(blocker,dict) else blocker))
        if (state.get("next_action") or {}).get("tool_executable_here") is False: stop_reason="TOOL_RUNTIME_LIMITATION"
    if state.get("founder_lock_required") is True and state.get("founder_locked") is not True: stop_reason="FOUNDER_DECISION_REQUIRED"
    if domain=="AUDIO":
        prohibited.extend(state.get("prohibited_actions") or state.get("hard_stops") or [])
        parallel.extend(state.get("parallel_safe_branches") or [])
        for i,p in enumerate(state.get("protected_audio_facts") or [],1):
            facts.append(make_fact(f"AUDIO_PROTECTED_{i}",p,"CONTINUITY_REQUIRED",[authority.locator],["AUDIO_PIPELINE"],True))
        if state.get("live_audio_status") in {"NOT_CLAIMED_NOT_YET_PROVEN","NOT_CLAIMED"}: boundaries.append("LIVE_PROVIDER_EVIDENCE_NOT_PRESENT")
        if "HUMAN_SIGNAL_REMAINS_EXTERNAL_EVIDENCE" in prohibited: boundaries.append("HUMAN_SIGNAL_EXTERNAL")
    else: prohibited.extend(state.get("prohibited") or state.get("prohibited_actions") or [])
    boundaries.extend(str(x) for x in (state.get("unrun_external_gates") or []))
    return NormalizedState(project_id,title,domain,authority,frontier,status,phase,next_obligation,stop_reason,blockers,facts,prohibited,parallel,boundaries,[s.locator for s in sources])


def obligation_dag(n:NormalizedState):
    root=n.next_obligation or "NO_NEXT_OBLIGATION"
    if n.stop_reason: return [{"id":"N1","obligation":root,"deps":[],"status":"STOP","reason":n.stop_reason}]
    out=[{"id":"N1","obligation":root,"deps":[],"status":"READY","reason":None}]
    for i,b in enumerate(n.parallel_safe_branches,2): out.append({"id":f"N{i}","obligation":b,"deps":[],"status":"PARALLEL","reason":None})
    return out


def compile_ir(n:NormalizedState,dag):
    p=dag[0]; stop=p["status"]=="STOP"
    return {"task_id":f"{n.project_id}:{p['id']}","project_id":n.project_id,"domain":n.domain,
      "authority_refs":[n.authority_source.locator],"work_frontier_ref":n.work_frontier_source.locator,
      "task_delta":p["obligation"],"inputs":n.raw_refs,"protected_facts":n.protected_facts,
      "forbidden_changes":n.prohibited_actions,"outputs":["EXECUTION_RESULT","TELEMETRY_EVENT","UPDATED_STATE_IF_AUTHORIZED"],
      "gate":p.get("reason") if stop else "VERIFY_AND_PERSIST","evidence_requirement":n.evidence_boundaries,
      "downstream_consumer":"CURRENT_PROJECT_STATE","execution_mode":"STOP" if stop else "PLAN_ONLY"}


def guard(n:NormalizedState,ir:dict,context=None):
    context=context or {}
    if n.stop_reason: return {"decision":"STOP","reason":n.stop_reason}
    text=str(ir.get("task_delta","")).upper()
    if "LIVE" in text and "PROVIDER" in text and not context.get("provider_authorized"): return {"decision":"STOP","reason":"EXTERNAL_PROVIDER_REQUIRED"}
    if context.get("mutating_locked_story") and not context.get("reopen_authorized"): return {"decision":"STOP","reason":"LOCKED_LAYER_REOPEN_NOT_AUTHORIZED"}
    if context.get("irreversible") and not context.get("approval_present"): return {"decision":"STOP","reason":"IRREVERSIBLE_APPROVAL_REQUIRED"}
    return {"decision":"PLAN","reason":"BOUNDED_NON_MUTATING_PLAN_ALLOWED"}


def telemetry(n:NormalizedState,decision:dict):
    return {"event_id":str(uuid.uuid4()),"ts":time.time(),"kind":"ROUTING_DECISION","project_id":n.project_id,"domain":n.domain,
      "decision":decision["decision"],"reason":decision["reason"],"evidence_class":"PERSISTED_STATE_EVIDENCE",
      "authority":n.authority_source.locator,"frontier":n.work_frontier_source.locator,"obligation":n.next_obligation}


def plan(bundle:dict[str,Any],context=None):
    n=adapt_project(bundle); dag=obligation_dag(n); ir=compile_ir(n,dag); d=guard(n,ir,context)
    return {"normalized_state":n.to_dict(),"dag":dag,"task_ir":ir,"decision":d,"telemetry_event":telemetry(n,d)}


def digest_bytes(data:bytes): return hashlib.sha256(data).hexdigest()
def plan_transaction(old_bytes:bytes,new_bytes:bytes,expected_hash:str):
    actual=digest_bytes(old_bytes)
    if actual!=expected_hash: return {"status":"STALE_REJECTED","actual_hash":actual}
    if old_bytes==new_bytes: return {"status":"NO_EFFECT_REJECTED","actual_hash":actual}
    return {"status":"READY","old_hash":actual,"new_hash":digest_bytes(new_bytes)}
def verify_readback(expected_new:bytes,readback:bytes):
    if expected_new!=readback: return {"status":"REPAIR_REQUIRED","expected":digest_bytes(expected_new),"readback":digest_bytes(readback)}
    return {"status":"COMMITTED_VERIFIED","hash":digest_bytes(readback)}
