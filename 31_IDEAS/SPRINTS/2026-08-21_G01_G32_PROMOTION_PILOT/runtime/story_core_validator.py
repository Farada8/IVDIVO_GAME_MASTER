#!/usr/bin/env python3
import json, sys

REQ=["hero","want","why_now","action","opposition","wrong_strategy","price","midpoint","climax_choice","resolution"]
EDGES=[("want","action"),("why_now","action"),("action","opposition"),("wrong_strategy","price"),("price","midpoint"),("midpoint","climax_choice"),("climax_choice","resolution")]

def validate(core):
    errors=[]
    for k in REQ:
        if not str(core.get(k,"" )).strip():
            errors.append("MISSING_"+k.upper())
    if core.get("hero_agency") in (False,None): errors.append("PASSIVE_OR_UNPROVEN_HERO_AGENCY")
    if not core.get("climax_choice_changes_outcome",False): errors.append("NO_CAUSAL_CLIMAX_CHOICE")
    if core.get("external_rescue_solves_main_conflict",False): errors.append("EXTERNAL_RESCUE_SOLVES_MAIN_CONFLICT")
    if not core.get("midpoint_changes_objective_or_model",False): errors.append("WEAK_MIDPOINT")
    if not core.get("price_paid",False): errors.append("PRICE_NOT_PAID")
    edges=set(tuple(x) for x in core.get("causal_edges",[]))
    for edge in EDGES:
        if edge not in edges: errors.append("MISSING_EDGE_"+edge[0].upper()+"_"+edge[1].upper())
    if core.get("permutable_core",False): errors.append("PERMUTABLE_LABEL_ONLY_CORE")
    return sorted(set(errors))

if __name__=="__main__":
    fixtures=json.load(open(sys.argv[1],encoding="utf-8"))
    failed=0
    for row in fixtures:
        errors=validate(row["core"])
        actual_pass=not errors
        ok=(actual_pass==row["expected_pass"])
        print(row["id"],"PASS" if ok else "FAIL",errors)
        failed += int(not ok)
    raise SystemExit(1 if failed else 0)
