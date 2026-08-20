#!/usr/bin/env python3
"""Compile listener point of audition, spatial staging, ambience and sound cues.

The graph is treated as the scene reality. This module does not invent extra plot
sounds. It turns declared world/space state into an audible geography and rejects
stereo-only causality.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def dump(path,data): Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")


def compile_spatial_sound(graph):
    issues=[]; positions=[]; moves=[]; sound_cues=[]; ambience=[]
    lpoa=graph.get("listener_point_of_audition") or {}
    if not lpoa.get("listener_position"):
        issues.append({"severity":"MAJOR","code":"LISTENER_POSITION_MISSING"})
    if "mono_safe" not in lpoa:
        issues.append({"severity":"MAJOR","code":"MONO_POLICY_MISSING"})

    last_pos={}
    for beat in graph.get("beats",[]):
        bid=beat.get("beat_id"); world=beat.get("world") or {}; policy=beat.get("sound_policy") or {}
        layer=world.get("ambience") or policy.get("ambience")
        if layer:
            ambience.append({"beat_id":bid,"location_id":world.get("location_id"),"layers":layer,
                             "focus_policy":policy.get("focus_policy") or "RETREAT_BEHIND_DIALOGUE",
                             "suppress_windows":policy.get("suppress_windows",[]),
                             "no_obvious_loop":True})
        events=world.get("audible_events") or policy.get("sound_events") or []
        if isinstance(events,dict): events=[events]
        for i,e in enumerate(events):
            if isinstance(e,str): e={"event":e}
            if not isinstance(e,dict) or not e.get("event"): continue
            if not e.get("story_function"):
                continue
            sound_cues.append({"cue_id":e.get("cue_id") or f"{bid}_SFX_{i+1:02d}","beat_id":bid,
                "event":e.get("event"),"physical_class":e.get("physical_class","BACKGROUND_OR_EVENT"),
                "cause":e.get("cause"),"material":e.get("material"),"story_function":e.get("story_function"),
                "literal_meaning":e.get("literal_meaning") or e.get("event"),
                "possible_extended_meaning":e.get("possible_extended_meaning",[]),
                "forbidden_implications":e.get("forbidden_implications",[]),
                "asset_strategy":e.get("asset_strategy","LIBRARY_OR_GENERATED"),"semantic_anchor":e.get("semantic_anchor") or bid})

        for turn in beat.get("turns",[]):
            tid=turn.get("turn_id"); sid=turn.get("speaker_id"); space=turn.get("space") or {}
            pos={"beat_id":bid,"turn_id":tid,"source_id":sid,"azimuth":space.get("azimuth"),
                 "elevation":space.get("elevation"),"distance":space.get("distance"),
                 "head_orientation":space.get("head_orientation"),"occlusion":space.get("occlusion"),
                 "mic_distance":space.get("mic_distance"),"acoustic_distance":space.get("acoustic_distance"),
                 "ear_specific":bool(space.get("ear_specific",False)),"mono_fallback":space.get("mono_fallback")}
            positions.append(pos)
            if pos["ear_specific"] and not pos["mono_fallback"]:
                issues.append({"severity":"MAJOR","code":"EAR_SPECIFIC_WITHOUT_MONO_FALLBACK","turn_id":tid})
            prev=last_pos.get(sid)
            if prev and any(pos.get(k)!=prev.get(k) for k in ("azimuth","distance","head_orientation","occlusion")):
                moves.append({"source_id":sid,"from_turn":prev.get("turn_id"),"to_turn":tid,
                              "from":{"azimuth":prev.get("azimuth"),"distance":prev.get("distance"),"head_orientation":prev.get("head_orientation")},
                              "to":{"azimuth":pos.get("azimuth"),"distance":pos.get("distance"),"head_orientation":pos.get("head_orientation")},
                              "automation_domains":["STEREO","DEPTH","SPECTRAL","DIRECT_REVERB_RATIO"]})
            last_pos[sid]=pos

    gate="PASS" if not any(i["severity"] in {"FATAL","MAJOR"} for i in issues) else "FAIL"
    return {"schema":"IVDIVO_SPATIAL_SOUND_WORLD_PLAN_v1","project_id":graph.get("project_id"),"scene_id":graph.get("scene_id"),
            "gate":gate,"listener_point_of_audition":lpoa,"positions":positions,"movement_automation":moves,
            "ambience_architecture":ambience,"sound_cues":sound_cues,"issues":issues,
            "laws":["DISTANCE_IS_NOT_PAN","STORY_SOUND_ONLY","SPACE_ACOUSTICALLY_COHERENT","CRITICAL_MEANING_MONO_SAFE"]}


def main():
    p=argparse.ArgumentParser(); p.add_argument("graph"); p.add_argument("--output",required=True); a=p.parse_args()
    out=compile_spatial_sound(load(a.graph)); dump(a.output,out); print(f"{out['gate']} positions={len(out['positions'])} moves={len(out['movement_automation'])} cues={len(out['sound_cues'])}")
    raise SystemExit(0 if out["gate"]=="PASS" else 2)

if __name__=="__main__": main()
