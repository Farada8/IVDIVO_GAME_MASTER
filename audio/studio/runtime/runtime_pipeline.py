#!/usr/bin/env python3
"""IVDIVO Audio Novel Studio runtime scene compiler.

One Scene State Graph -> validated mental-scene/performance/body/space/sound/music
machine artifacts. Pre-live only: no provider dispatch, real alignment or master.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from scene_state_graph import validate_graph
from auditory_mise_en_scene import compile_mise_en_scene
from performance_compiler import compile_scene
from body_foley_compiler import compile_body_foley
from spatial_sound_compiler import compile_spatial_sound
from music_mix_compiler import compile_music_mix


def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def write(p,d):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")


def run(graph,out_dir):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    reports={}
    reports["scene_validation"]=validate_graph(graph)
    write(out/"SCENE_STATE_VALIDATION.json",reports["scene_validation"])
    if reports["scene_validation"]["gate"]!="PASS":
        return {"gate":"FAIL","failed_stage":"SCENE_STATE_VALIDATION","reports":reports}

    mise=compile_mise_en_scene(graph); reports["mise_en_scene"]=mise; write(out/"AUDITORY_MISE_EN_SCENE.json",mise)
    perf=compile_scene(graph); reports["performance"]=perf
    for name,obj in perf.items(): write(out/f"{name}.json",obj)
    body=compile_body_foley(graph); reports["body_foley"]=body; write(out/"BODY_FOLEY_PLAN.json",body)
    spatial=compile_spatial_sound(graph); reports["spatial_sound"]=spatial; write(out/"SPATIAL_SOUND_WORLD_PLAN.json",spatial)
    music=compile_music_mix(graph); reports["music_mix"]=music; write(out/"MUSIC_MIX_INTENT.json",music)

    failed=[name for name,r in (("MISE_EN_SCENE",mise),("BODY_FOLEY",body),("SPATIAL_SOUND",spatial),("MUSIC_MIX",music)) if r.get("gate")!="PASS"]
    artifacts=["SCENE_STATE_VALIDATION.json","AUDITORY_MISE_EN_SCENE.json",* [f"{n}.json" for n in perf],"BODY_FOLEY_PLAN.json","SPATIAL_SOUND_WORLD_PLAN.json","MUSIC_MIX_INTENT.json"]
    manifest={"schema":"IVDIVO_AUDIO_NOVEL_RUNTIME_COMPILE_v1","project_id":graph.get("project_id"),"scene_id":graph.get("scene_id"),
              "gate":"FAIL" if failed else "PASS","failed_stages":failed,"artifacts":artifacts,
              "next_if_pass":"PROVIDER_SAFE_RENDER_BLOCK_COMPILATION_AND_DRY_RUN",
              "explicitly_not_done":["LIVE_PROVIDER_CALL","ABSOLUTE_TIMELINE","FINAL_AUTOMIX","MASTER"]}
    write(out/"RUNTIME_COMPILE_MANIFEST.json",manifest)
    return manifest


def main():
    p=argparse.ArgumentParser(); p.add_argument("graph"); p.add_argument("--out-dir",required=True); a=p.parse_args()
    result=run(load(a.graph),a.out_dir); print(json.dumps(result,indent=2,ensure_ascii=False)); raise SystemExit(0 if result.get("gate")=="PASS" else 2)

if __name__=="__main__": main()
