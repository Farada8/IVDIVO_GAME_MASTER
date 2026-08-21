#!/usr/bin/env python3
"""Scene/block delete-and-adjacency-swap diagnostic.

Input is a JSON architecture list. Each scene declares provides[] state/evidence changes
and requires[] dependencies. Optional structure_kind=PARALLEL_OR_MONTAGE prevents the
swap heuristic from treating intentionally reorderable parallel units as automatic defects.
This is a diagnostic, not an automatic rewrite authority.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any


def audit(data: dict[str,Any]) -> dict[str,Any]:
    scenes=data.get("scenes",[])
    issues=[]; delete_tests=[]; swap_tests=[]
    produced_initial=set(data.get("initial_state",[]))
    for i,s in enumerate(scenes):
        sid=s.get("scene_id",f"S{i}")
        provides=set(s.get("provides",[]))
        broken=[]
        for later in scenes[i+1:]:
            req=set(later.get("requires",[]))
            lost=(req & provides)
            # only count if no other earlier scene also supplies it
            for x in list(lost):
                supplied_elsewhere=x in produced_initial or any(x in set(p.get("provides",[])) for p in scenes[:i]) or any(x in set(p.get("provides",[])) for p in scenes[i+1:scenes.index(later)])
                if supplied_elsewhere: lost.discard(x)
            if lost: broken.append({"consumer":later.get("scene_id"),"missing":sorted(lost)})
        delete_tests.append({"scene_id":sid,"essential_by_declared_dependency":bool(broken),"broken_dependencies":broken})
    for i in range(len(scenes)-1):
        a,b=scenes[i],scenes[i+1]
        if a.get("structure_kind")=="PARALLEL_OR_MONTAGE" and b.get("structure_kind")=="PARALLEL_OR_MONTAGE":
            verdict="LEGITIMATELY_REORDERABLE_PARALLEL"
        else:
            a_prov=set(a.get("provides",[])); b_req=set(b.get("requires",[]))
            b_prov=set(b.get("provides",[])); a_req=set(a.get("requires",[]))
            if a_prov & b_req or b_prov & a_req: verdict="SWAP_BREAKS_DECLARED_CAUSALITY"
            else: verdict="SWAP_PASSES_DIAGNOSTIC_REVIEW_CAUSALITY_OR_ESCALATION"
        swap_tests.append({"a":a.get("scene_id"),"b":b.get("scene_id"),"verdict":verdict})
    if scenes and all(not t["essential_by_declared_dependency"] for t in delete_tests): issues.append("NO_SCENE_HAS_DECLARED_DOWNSTREAM_DEPENDENCY")
    return {"status":"REVIEW" if issues or any(t["verdict"].startswith("SWAP_PASSES") for t in swap_tests) else "PASS","delete_tests":delete_tests,"swap_tests":swap_tests,"issues":issues}

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("architecture",type=Path); a=p.parse_args()
    try:r=audit(json.loads(a.architecture.read_text(encoding="utf-8")))
    except Exception as exc:r={"status":"FAIL","issues":[str(exc)]}
    print(json.dumps(r,ensure_ascii=False,indent=2)); return 1 if r["status"]=="FAIL" else 0
if __name__=="__main__":raise SystemExit(main())
