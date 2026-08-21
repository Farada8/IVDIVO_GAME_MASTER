#!/usr/bin/env python3
"""Fail-closed causal Story Core validator.

This checks structural causal connectivity, not literary quality. A populated list of
labels is insufficient; required causal paths must exist and the hero must cause the
climax/resolution path.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

REQUIRED_PATHS = [
    ("WHY_NOW", "WANT"),
    ("WANT", "HERO_ACTION"),
    ("HERO_ACTION", "OPPOSITION"),
    ("OPPOSITION", "WRONG_STRATEGY"),
    ("WRONG_STRATEGY", "PRICE"),
    ("PRICE", "MIDPOINT"),
    ("MIDPOINT", "CLIMAX_CHOICE"),
    ("CLIMAX_CHOICE", "RESOLUTION"),
]

def validate(core: dict[str, Any]) -> dict[str, Any]:
    errors=[]
    required_fields=["hero","want","why_now","opposition","wrong_strategy","price","midpoint","climax_choice","resolution","causal_edges"]
    for f in required_fields:
        if core.get(f) in (None,"",[]): errors.append(f"MISSING:{f}")
    edges={(e.get("from"),e.get("to")) for e in core.get("causal_edges",[]) if isinstance(e,dict) and str(e.get("because","")).strip()}
    for edge in REQUIRED_PATHS:
        if edge not in edges: errors.append(f"MISSING_CAUSAL_EDGE:{edge[0]}->{edge[1]}")
    if core.get("climax_caused_by_hero") is not True:
        errors.append("CLIMAX_NOT_CAUSED_BY_HERO")
    if core.get("resolution_closes_main_conflict") is not True:
        errors.append("MAIN_CONFLICT_NOT_CLOSED")
    if core.get("series_hook") and core.get("series_hook_after_resolution") is not True:
        errors.append("SERIES_HOOK_BEFORE_RESOLUTION")
    return {"status":"PASS" if not errors else "FAIL","errors":errors}

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("core",type=Path); a=p.parse_args()
    try: result=validate(json.loads(a.core.read_text(encoding="utf-8")))
    except Exception as exc: result={"status":"FAIL","errors":[f"READ_OR_PARSE:{exc}"]}
    print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result["status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
