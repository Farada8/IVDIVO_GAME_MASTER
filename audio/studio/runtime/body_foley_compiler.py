#!/usr/bin/env python3
"""Compile causal body-state and Foley plans from an IVDIVO Scene State Graph.

Provider-independent. It never invents story actions; it only converts body/object
state already present in the graph into production cues and rejects implausible
speech/body combinations.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def dump(path, data): Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")


def compile_body_foley(graph):
    cues=[]; issues=[]; mouth=[]
    for beat in graph.get("beats",[]):
        bid=beat.get("beat_id")
        for turn in beat.get("turns",[]):
            tid=turn.get("turn_id"); speaker=turn.get("speaker_id"); body=turn.get("body") or {}
            mstate=str(body.get("mouth_state","CLEAR")).upper()
            if mstate not in {"", "NONE", "CLEAR"}:
                rec={"speaker_id":speaker,"beat_id":bid,"turn_id":tid,"mouth_state":mstate,
                     "speech_allowed":body.get("speech_allowed",True),
                     "speech_impairment":body.get("speech_impairment","NONE"),
                     "swallow_before_line":bool(body.get("swallow_before_line",False)),
                     "breath_reset":body.get("breath_reset","NONE"),"utensil_state":body.get("utensil_state","NONE")}
                mouth.append(rec)
                if rec["speech_allowed"] and rec["speech_impairment"] in {None,"","NONE"} and not rec["swallow_before_line"]:
                    issues.append({"severity":"MAJOR","code":"IMPOSSIBLE_CLEAN_SPEECH_WITH_MOUTH_STATE","turn_id":tid})

            actions=body.get("audible_actions") or body.get("actions") or []
            if isinstance(actions, dict): actions=[actions]
            for i,a in enumerate(actions):
                if isinstance(a,str): a={"action":a}
                if not isinstance(a,dict) or not a.get("action"): continue
                if a.get("audible") is False: continue
                story_function=a.get("story_function") or body.get("story_function")
                if not story_function:
                    # evocative-detail gate: no function, no cue
                    continue
                cues.append({
                    "cue_id":a.get("cue_id") or f"{tid}_FOLEY_{i+1:02d}",
                    "beat_id":bid,"turn_id":tid,"character_or_source":speaker,
                    "action":a.get("action"),"object":a.get("object"),"material":a.get("material"),
                    "cause":a.get("cause") or "CHARACTER_ACTION","story_function":story_function,
                    "performer_intent":a.get("performer_intent") or body.get("physical_intent"),
                    "character_weight":a.get("character_weight") or body.get("weight"),
                    "action_tempo":a.get("action_tempo") or body.get("action_tempo"),
                    "contact_force":a.get("contact_force"),"audibility":a.get("audibility","SUBTLE"),
                    "proximity":a.get("proximity") or (turn.get("space") or {}).get("distance"),
                    "sync_tolerance":a.get("sync_tolerance","SEMANTIC_ANCHOR"),
                    "repulsion_risk":a.get("repulsion_risk","LOW"),"fatigue_risk":a.get("fatigue_risk","LOW"),
                    "repetition_limit":a.get("repetition_limit",1),"asset_policy":a.get("asset_policy","FOLEY_OR_LIBRARY"),
                    "semantic_anchor":a.get("semantic_anchor") or tid,
                })

    gate="PASS" if not any(i["severity"] in {"FATAL","MAJOR"} for i in issues) else "FAIL"
    return {"schema":"IVDIVO_BODY_FOLEY_PLAN_v1","project_id":graph.get("project_id"),"scene_id":graph.get("scene_id"),
            "gate":gate,"mouth_body_states":mouth,"foley_cues":cues,"issues":issues,
            "laws":["CAUSAL_ONLY","EVOCATIVE_DETAIL_GATE","NO_CONTINUOUS_CHEWING_BY_DEFAULT","HEADPHONE_SALIENCE_GUARD"]}


def main():
    p=argparse.ArgumentParser(); p.add_argument("graph"); p.add_argument("--output",required=True); a=p.parse_args()
    out=compile_body_foley(load(a.graph)); dump(a.output,out); print(f"{out['gate']} cues={len(out['foley_cues'])} mouth_states={len(out['mouth_body_states'])}")
    raise SystemExit(0 if out["gate"]=="PASS" else 2)

if __name__=="__main__": main()
