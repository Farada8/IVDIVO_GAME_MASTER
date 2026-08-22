from __future__ import annotations
from typing import Any, Iterable
import hashlib, re

SI_RE = re.compile(r"\bSI-\d{4}\b")
EVIDENCE_ORDER = {"E0":0,"E1":1,"E2":2,"E3":3,"E4":4,"E5":5}


def extract_si_ids(text: str) -> set[str]:
    return set(SI_RE.findall(text or ""))


def registry_collision_guard(proposed_id: str | None, main_ids: Iterable[str], active_surface_ids: Iterable[str]) -> dict[str, Any]:
    main=set(main_ids); active=set(active_surface_ids); reserved=main|active
    if proposed_id is None:
        return {"verdict":"NO_ALLOCATION", "reserved":sorted(reserved), "collision":False}
    collision=proposed_id in reserved
    return {"verdict":"STOP_COLLISION" if collision else "SAFE_TO_RESERVE_PENDING_RECHECK", "reserved":sorted(reserved), "collision":collision}


def authority_stack_resolver(surfaces: list[dict[str, Any]]) -> dict[str, Any]:
    current=[s for s in surfaces if s.get("status") in {"CURRENT","VERIFIED_CURRENT"}]
    controlling=[s for s in current if s.get("role")=="CONTROLLING"]
    if len(controlling)>1 and len({s.get("priority") for s in controlling}) != len(controlling):
        return {"verdict":"HOLD_AUTHORITY_CONFLICT","ordered":[]}
    order=sorted(surfaces, key=lambda s:(0 if s.get("role")=="CONTROLLING" else 1, s.get("priority",999)))
    return {"verdict":"PASS","ordered":[s.get("id") for s in order]}


def freshness_vector(required: Iterable[str], observed: dict[str, dict[str, Any]]) -> dict[str, Any]:
    required=list(required); stale=[]; missing=[]
    for dim in required:
        item=observed.get(dim)
        if not item: missing.append(dim); continue
        if item.get("state") not in {"CURRENT","FRESH","MATCH"}: stale.append(dim)
    verdict="PASS" if not stale and not missing else "REBASE_OR_REFRESH"
    return {"verdict":verdict,"required":required,"stale":stale,"missing":missing}


def meta_wip_limiter(primary_meta:int, pilots:int, founder_switched:bool=False, prerequisite:bool=False, production_blocked:bool=False) -> dict[str,Any]:
    allowed = founder_switched or prerequisite or production_blocked
    if primary_meta<=1 and pilots<=2:
        return {"verdict":"PASS","exception_used":False}
    return {"verdict":"PASS_FOUNDER_SWITCH" if allowed else "STOP_WIP_LIMIT","exception_used":allowed}


def production_return_guard(target:str|None, founder_switched:bool=False) -> str:
    if target: return "PASS"
    return "PASS_FOUNDER_SWITCH_BOUNDED" if founder_switched else "STOP_NO_RETURN_TARGET"


def prompt_fingerprint(card:dict[str,Any]) -> str:
    fields=[str(card.get(k,"" )).strip().lower() for k in ("consumer","evidence_class","gate","action_semantics","state_mutation")]
    return hashlib.sha256("|".join(fields).encode()).hexdigest()[:20]


def dedupe_prompt_bank(cards:list[dict[str,Any]]) -> dict[str,Any]:
    seen={}; duplicates=[]
    for c in cards:
        fp=prompt_fingerprint(c)
        if fp in seen: duplicates.append((seen[fp],c.get("id")))
        else: seen[fp]=c.get("id")
    return {"unique":len(seen),"total":len(cards),"duplicates":duplicates,"verdict":"PASS" if not duplicates else "MERGE_DUPLICATES"}


def evidence_yield(before_decision:Any, after_decision:Any, evidence_added:list[str]|None=None, blocker_removed:list[str]|None=None, explicit_hold:str|None=None) -> dict[str,Any]:
    evidence_added=evidence_added or []; blocker_removed=blocker_removed or []
    changed=before_decision != after_decision
    useful=changed or bool(evidence_added) or bool(blocker_removed) or bool(explicit_hold)
    return {"verdict":"PASS_YIELD" if useful else "REJECT_NO_EFFECT","decision_changed":changed,"evidence_added":evidence_added,"blocker_removed":blocker_removed,"hold":explicit_hold}


def voi_route(tests:list[dict[str,Any]]) -> dict[str,Any]:
    eligible=[t for t in tests if t.get("decision_consumer")]
    if not eligible: return {"verdict":"HOLD_NO_DECISION_CONSUMER","selected":None}
    def key(t):
        return (int(t.get("decision_flip",0))+int(t.get("evidence_independence",0)), -int(t.get("burden",3)), -int(t.get("risk",3)))
    sel=max(eligible,key=key)
    return {"verdict":"PASS","selected":sel.get("id"),"basis":"ordinal decision-change/evidence-independence before burden/risk"}


def cost_of_delay_band(consequence:str) -> str:
    c=(consequence or "").lower()
    if any(x in c for x in ("data loss","authority corruption","irreversible","payment replay","safety")): return "HIGH"
    if any(x in c for x in ("blocks production","deadline","stale merge","rework")): return "MEDIUM"
    return "LOW"


def proof_claim_classifier(required_class:str, evidence_class:str) -> dict[str,Any]:
    if required_class not in EVIDENCE_ORDER or evidence_class not in EVIDENCE_ORDER: return {"verdict":"HOLD_UNKNOWN_EVIDENCE_CLASS"}
    ok=EVIDENCE_ORDER[evidence_class]>=EVIDENCE_ORDER[required_class]
    return {"verdict":"SUPPORTED" if ok else "NOT_PROVEN_EVIDENCE_CEILING","required":required_class,"observed":evidence_class}


def external_evidence_firewall(claim:str, evidence_type:str) -> str:
    external={"HUMAN_SIGNAL","PROVIDER_LIVE","PAYMENT","MARKET_BEHAVIOR"}
    if claim in external and evidence_type in {"MODEL_REVIEW","AUTOMATED_TEST","SOURCE_INSPECTION","SELF_PRODUCED_ARTIFACT"}:
        return "STOP_EVIDENCE_SUBSTITUTION"
    return "PASS"


def fail_closed_router(issue:str) -> str:
    routes={
        "AUTHORITY_CONFLICT":"HOLD_AFFECTED_ACTION",
        "STALE_REQUIRED_SURFACE":"REFRESH_OR_REBASE",
        "REGISTRY_ID_COLLISION_RISK":"NO_ID_ALLOCATION",
        "EVIDENCE_CLASS_MISMATCH":"HOLD_CLAIM",
        "NO_DECISION_RELEVANCE":"REJECT_META_STEP",
        "WIP_LIMIT":"QUEUE_META_WORK",
        "EXTERNAL_EVIDENCE_REQUIRED":"HOLD_UNTIL_EXTERNAL",
        "IRREVERSIBLE_APPROVAL_REQUIRED":"STOP_FOR_EXPLICIT_APPROVAL",
        "TOOL_LIMITATION":"PRESERVE_STATE_AND_ROUTE_AROUND",
    }
    return routes.get(issue,"HOLD_UNKNOWN_FAILURE_CLASS")


def observability(events:list[dict[str,Any]]) -> dict[str,int]:
    keys=["prompt_executed","decision_changed","evidence_gap_closed","duplicate_build_avoided","stale_surface_detected","blocker_removed","write_readback","rollback","production_returned","no_effect"]
    return {k:sum(1 for e in events if e.get("type")==k) for k in keys}


def knowledge_compactor(cards:list[dict[str,Any]]) -> dict[str,Any]:
    groups={}
    for c in cards:
        groups.setdefault(prompt_fingerprint(c),[]).append(c.get("id"))
    actions=[]
    for ids in groups.values(): actions.append({"ids":ids,"action":"KEEP" if len(ids)==1 else "MERGE"})
    return {"actions":actions,"protected_history":True}


def rollback_plan(changed:str, dependency_graph:dict[str,list[str]], locked:set[str]|None=None) -> dict[str,Any]:
    locked=locked or set(); affected=[]; stack=list(dependency_graph.get(changed,[])); seen=set()
    while stack:
        n=stack.pop()
        if n in seen or n in locked: continue
        seen.add(n); affected.append(n); stack.extend(dependency_graph.get(n,[]))
    return {"changed":changed,"revalidate":affected,"locked_preserved":sorted(locked),"verdict":"PASS_SELECTIVE"}


def promotion_disposition(*, prospective_cross_project:bool, registry_race_guard:bool, application_readback:bool, evidence_ceiling:str) -> dict[str,Any]:
    if not registry_race_guard: return {"verdict":"HOLD_REGISTRY_RACE"}
    if not prospective_cross_project: return {"verdict":"HOLD_LOCAL_PILOT"}
    if not application_readback: return {"verdict":"HOLD_NO_APPLICATION_READBACK"}
    if EVIDENCE_ORDER.get(evidence_ceiling,0)<2: return {"verdict":"HOLD_WEAK_EVIDENCE"}
    return {"verdict":"READY_FOR_NORMAL_V2_PROMOTION_REVIEW"}


def next64_compile(gaps:list[dict[str,str]], n:int=64) -> list[dict[str,str]]:
    if not gaps: return []
    out=[]
    for i in range(n):
        g=gaps[i % len(gaps)]
        out.append({"id":f"D{33+i:02d}","gap":g["gap"],"dependency":g["dependency"],"stopping_rule":g["stopping_rule"],"status":"DESIGNED_NOT_EXECUTED"})
    return out


def validate_input_asset_registry(items:list[dict[str,Any]]) -> dict[str,Any]:
    bad=[]
    for x in items:
        if not x.get("filename") or not re.fullmatch(r"[0-9a-f]{64}",x.get("sha256", "")) or x.get("size_bytes",0)<0 or not x.get("role"):
            bad.append(x.get("filename"))
    return {"verdict":"PASS" if not bad else "FAIL","count":len(items),"bad":bad}
