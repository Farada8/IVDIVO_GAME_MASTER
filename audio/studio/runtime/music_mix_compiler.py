#!/usr/bin/env python3
"""Compile music permissions and pre-alignment mix intentions from Scene State Graph.

Music is allowed only when a story value change is declared. Mix output is semantic
until real timing exists; no absolute timestamps are created here.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def dump(path,data): Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")


def compile_music_mix(graph):
    cues=[]; no_music=[]; mix=[]; issues=[]
    for beat in graph.get("beats",[]):
        bid=beat.get("beat_id"); listener=beat.get("listener") or {}; policy=beat.get("sound_policy") or {}
        music=policy.get("music") or {}
        if music is False or music.get("allowed") is False:
            no_music.append({"beat_id":bid,"reason":music.get("reason") if isinstance(music,dict) else "SCENE_POLICY"})
        elif isinstance(music,dict) and music.get("allowed"):
            value_change=music.get("value_change")
            if not value_change:
                issues.append({"severity":"MAJOR","code":"MUSIC_WITHOUT_VALUE_CHANGE","beat_id":bid})
            else:
                cues.append({"cue_id":music.get("cue_id") or f"{bid}_MUSIC_01","beat_id":bid,
                    "story_function":music.get("story_function"),"value_change":value_change,
                    "entry_anchor":music.get("entry_anchor") or f"AFTER:{bid}:VALUE_CHANGE",
                    "exit_anchor":music.get("exit_anchor"),"theme_id":music.get("theme_id"),
                    "intensity":music.get("intensity","LOW"),"instrument_family":music.get("instrument_family",[]),
                    "rhythmic_density":music.get("rhythmic_density","SPARSE"),"harmonic_role":music.get("harmonic_role"),
                    "diegetic_or_score":music.get("diegetic_or_score","SCORE"),
                    "forbidden_implications":music.get("forbidden_implications",["PREMATURE_ROMANCE","PREMATURE_GUILT","PREMATURE_DANGER"]),
                    "semantic_only_pre_alignment":True})

        mix.append({"beat_id":bid,"focus_owner":listener.get("focus_owner"),
                    "secondary_support":listener.get("secondary_support",[]),
                    "suppress":listener.get("suppress",[]),
                    "time_conflict":policy.get("time_conflict",[]),"frequency_conflict":policy.get("frequency_conflict",[]),
                    "level_conflict":policy.get("level_conflict",[]),"stereo_conflict":policy.get("stereo_conflict",[]),
                    "depth_conflict":policy.get("depth_conflict",[]),
                    "automation_intent":policy.get("automation_intent",[]),
                    "dramatic_reason":policy.get("mix_reason") or "PROTECT_LISTENER_FOCUS",
                    "absolute_timestamps":None})

    gate="PASS" if not any(i["severity"] in {"FATAL","MAJOR"} for i in issues) else "FAIL"
    return {"schema":"IVDIVO_MUSIC_MIX_INTENT_v1","project_id":graph.get("project_id"),"scene_id":graph.get("scene_id"),
            "gate":gate,"music_cues":cues,"no_music_windows":no_music,"mix_action_intents":mix,"issues":issues,
            "laws":["PERFORMANCE_BEFORE_MUSIC","VALUE_CHANGE_REQUIRED","NO_ABSOLUTE_TIMESTAMPS_BEFORE_ALIGNMENT","MUSIC_LOSES_TO_COMPREHENSION"]}


def main():
    p=argparse.ArgumentParser(); p.add_argument("graph"); p.add_argument("--output",required=True); a=p.parse_args()
    out=compile_music_mix(load(a.graph)); dump(a.output,out); print(f"{out['gate']} music={len(out['music_cues'])} no_music={len(out['no_music_windows'])}")
    raise SystemExit(0 if out["gate"]=="PASS" else 2)

if __name__=="__main__": main()
