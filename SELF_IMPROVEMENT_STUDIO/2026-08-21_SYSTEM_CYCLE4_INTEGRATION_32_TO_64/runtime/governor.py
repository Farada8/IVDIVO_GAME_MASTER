from __future__ import annotations
PRIORITY={"P0":0,"P1":1,"P2":2,"P3":3,"P4":4,"P5":5,"P6":6}
def choose(tasks:list[dict],meta_wip:int=0)->dict:
    ready=[t for t in tasks if t.get("ready") is True]
    if not ready:return {"decision":"STOP","reason":"NO_READY_TASK"}
    ready.sort(key=lambda t:(PRIORITY.get(t.get("priority","P6"),9),-float(t.get("information_value",0)),float(t.get("cost",0))))
    best=ready[0]
    if best.get("priority") in {"P4","P5","P6"}:
        prod=[t for t in ready if t.get("priority") in {"P1","P2"}]
        if prod:best=prod[0]
        elif meta_wip>=1:return {"decision":"STOP","reason":"META_WIP_LIMIT"}
    return {"decision":"RUN","task":best}
def next_cycle_gate(results:list[dict],proposed_prompts:list[dict])->dict:
    unresolved_external=any(r.get("status") in {"HOLD_HUMAN","HOLD_PROVIDER","HOLD_MARKET","HOLD_ECONOMICS"} for r in results)
    ready_prod=any(r.get("priority") in {"P1","P2"} and r.get("ready") for r in results)
    if unresolved_external or ready_prod:return {"decision":"DO_NOT_BLINDLY_RUN_ALL_PROMPTS","reason":"REAL_EVIDENCE_OR_PRODUCTION_HAS_HIGHER_INFORMATION_VALUE","selected":[]}
    ranked=sorted(proposed_prompts,key=lambda p:(PRIORITY.get(p.get("priority","P6"),9),-p.get("information_value",0)))
    return {"decision":"SELECT_BOUNDED_SUBSET","selected":[p.get("id") for p in ranked[:4]]}
