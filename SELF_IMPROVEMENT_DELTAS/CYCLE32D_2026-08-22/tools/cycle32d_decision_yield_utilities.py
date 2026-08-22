from __future__ import annotations
from typing import Any, Iterable
import hashlib, re

SI_RE = re.compile(r"\bSI-\d{4}\b")
EVIDENCE_ORDER = {"E0":0,"E1":1,"E2":2,"E3":3,"E4":4,"E5":5}

def extract_si_ids(text: str) -> set[str]:
    return set(SI_RE.findall(text or ""))

def registry_collision_guard(proposed_id: str | None, main_ids: Iterable[str], active_surface_ids: Iterable[str]) -> dict[str, Any]:
    """Read-only race canary. This is NOT a transactional reservation service."""
    reserved = set(main_ids) | set(active_surface_ids)
    if proposed_id is None:
        return {"verdict":"NO_ALLOCATION", "reserved":sorted(reserved), "collision":False}
    collision = proposed_id in reserved
    return {"verdict":"STOP_COLLISION" if collision else "SAFE_TO_RESERVE_PENDING_RECHECK", "reserved":sorted(reserved), "collision":collision}

def freshness_vector(required: Iterable[str], observed: dict[str, dict[str, Any]]) -> dict[str, Any]:
    required=list(required); stale=[]; missing=[]
    for dim in required:
        item=observed.get(dim)
        if not item: missing.append(dim)
        elif item.get("state") not in {"CURRENT","FRESH","MATCH"}: stale.append(dim)
    return {"verdict":"PASS" if not stale and not missing else "REBASE_OR_REFRESH", "required":required, "stale":stale, "missing":missing}

def prompt_fingerprint(card: dict[str, Any]) -> str:
    fields=[str(card.get(k,"")).strip().lower() for k in ("consumer","evidence_class","gate","action_semantics","state_mutation")]
    return hashlib.sha256("|".join(fields).encode()).hexdigest()[:20]

def dedupe_prompt_bank(cards: list[dict[str, Any]]) -> dict[str, Any]:
    seen={}; duplicates=[]
    for card in cards:
        fp=prompt_fingerprint(card)
        if fp in seen: duplicates.append((seen[fp], card.get("id")))
        else: seen[fp]=card.get("id")
    return {"unique":len(seen),"total":len(cards),"duplicates":duplicates,"verdict":"PASS" if not duplicates else "MERGE_DUPLICATES"}

def evidence_yield(before_decision: Any, after_decision: Any, *, evidence_added: list[str] | None=None, blocker_removed: list[str] | None=None, explicit_hold: str | None=None) -> dict[str, Any]:
    evidence_added=evidence_added or []; blocker_removed=blocker_removed or []
    changed=before_decision != after_decision
    useful=changed or bool(evidence_added) or bool(blocker_removed) or bool(explicit_hold)
    return {"verdict":"PASS_YIELD" if useful else "REJECT_NO_EFFECT", "decision_changed":changed, "evidence_added":evidence_added, "blocker_removed":blocker_removed, "hold":explicit_hold}

def voi_route(tests: list[dict[str, Any]]) -> dict[str, Any]:
    eligible=[t for t in tests if t.get("decision_consumer")]
    if not eligible: return {"verdict":"HOLD_NO_DECISION_CONSUMER","selected":None}
    def key(t):
        return (int(t.get("decision_flip",0))+int(t.get("evidence_independence",0)),-int(t.get("burden",3)),-int(t.get("risk",3)))
    selected=max(eligible,key=key)
    return {"verdict":"PASS","selected":selected.get("id")}

def proof_claim_classifier(required_class: str, evidence_class: str) -> dict[str, Any]:
    if required_class not in EVIDENCE_ORDER or evidence_class not in EVIDENCE_ORDER:
        return {"verdict":"HOLD_UNKNOWN_EVIDENCE_CLASS"}
    ok=EVIDENCE_ORDER[evidence_class] >= EVIDENCE_ORDER[required_class]
    return {"verdict":"SUPPORTED" if ok else "NOT_PROVEN_EVIDENCE_CEILING", "required":required_class, "observed":evidence_class}

def rollback_plan(changed: str, dependency_graph: dict[str,list[str]], locked: set[str] | None=None) -> dict[str, Any]:
    locked=locked or set(); affected=[]; seen=set(); stack=list(dependency_graph.get(changed,[]))
    while stack:
        node=stack.pop()
        if node in seen or node in locked: continue
        seen.add(node); affected.append(node); stack.extend(dependency_graph.get(node,[]))
    return {"verdict":"PASS_SELECTIVE","changed":changed,"revalidate":affected,"locked_preserved":sorted(locked)}

def validate_input_asset_registry(items: list[dict[str, Any]]) -> dict[str, Any]:
    bad=[]
    for item in items:
        if not item.get("filename") or not re.fullmatch(r"[0-9a-f]{64}",item.get("sha256","")) or item.get("size_bytes",0)<0 or not item.get("role"):
            bad.append(item.get("filename"))
    return {"verdict":"PASS" if not bad else "FAIL","count":len(items),"bad":bad}
