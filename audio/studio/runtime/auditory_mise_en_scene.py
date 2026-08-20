#!/usr/bin/env python3
"""Compile the listener's evolving mental scene from Scene State Graph.

This is not visual prose generation. It is an audio-directing abstraction: what the
listener should mentally locate now, which depth plane owns attention, what enters or
recedes, and what event causes the transition. It may only use facts already present
in the Scene State Graph.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def dump(p,d): Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")


def compile_mise_en_scene(graph):
    frames=[]; issues=[]; previous=None
    for beat in graph.get("beats",[]):
        bid=beat.get("beat_id"); world=beat.get("world") or {}; listener=beat.get("listener") or {}; policy=beat.get("sound_policy") or {}
        scene_image=world.get("imagined_scene") or world.get("mental_scene")
        planes=world.get("depth_planes") or {
            "near": world.get("near_plane",[]),
            "mid": world.get("mid_plane",[]),
            "far": world.get("far_plane",[]),
        }
        if not scene_image:
            # descriptive mental image is optional; spatial facts still form a frame
            scene_image={"location_id":world.get("location_id"),"focus_owner":listener.get("focus_owner")}
        transition=world.get("transition_from_previous") or policy.get("attention_transition")
        if previous is not None and not transition:
            prev_focus=previous.get("focus_owner"); cur_focus=listener.get("focus_owner")
            prev_loc=previous.get("location_id"); cur_loc=world.get("location_id")
            if prev_focus!=cur_focus or prev_loc!=cur_loc:
                issues.append({"severity":"MEDIUM","code":"MENTAL_FRAME_CHANGE_WITHOUT_CAUSE","beat_id":bid,
                               "message":"Focus/location changed but no transition cause was declared."})
        frame={
            "frame_id":f"{bid}_MENTAL_FRAME",
            "beat_id":bid,
            "location_id":world.get("location_id"),
            "mental_scene":scene_image,
            "focus_owner":listener.get("focus_owner"),
            "listener_must_understand":listener.get("must_understand",[]),
            "listener_may_feel":listener.get("may_feel",[]),
            "depth_planes":planes,
            "foreground_action":world.get("active_actions",[]),
            "what_enters_attention":policy.get("reveal",[]) or world.get("attention_entries",[]),
            "what_recedes":policy.get("suppress",[]) or listener.get("suppress",[]),
            "transition_from_previous":transition,
            "silence_role":policy.get("silence_role"),
            "auditory_camera":{
                "position":(graph.get("listener_point_of_audition") or {}).get("listener_position"),
                "orientation":(graph.get("listener_point_of_audition") or {}).get("listener_orientation"),
                "move":world.get("listener_move") or policy.get("listener_move"),
                "focus_change":policy.get("focus_change"),
                "depth_change":policy.get("depth_change"),
            },
            "forbidden_new_facts":True,
        }
        frames.append(frame); previous={"focus_owner":frame["focus_owner"],"location_id":frame["location_id"]}
    gate="PASS" if not any(i["severity"] in {"FATAL","MAJOR"} for i in issues) else "FAIL"
    return {"schema":"IVDIVO_AUDITORY_MISE_EN_SCENE_v1","project_id":graph.get("project_id"),"scene_id":graph.get("scene_id"),
            "gate":gate,"frames":frames,"issues":issues,
            "law":"The listener should experience changing coherent scenes, not a pile of simultaneous audio assets."}


def main():
    p=argparse.ArgumentParser(); p.add_argument("graph"); p.add_argument("--output",required=True); a=p.parse_args()
    out=compile_mise_en_scene(load(a.graph)); dump(a.output,out); print(f"{out['gate']} frames={len(out['frames'])}")
    raise SystemExit(0 if out["gate"]=="PASS" else 2)

if __name__=="__main__": main()
