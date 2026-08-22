#!/usr/bin/env python3
"""Plan controlled ROOM917 RU E01 editorial dialogue blocks from immutable units.

Zero-spend planner. It preserves unit order, never crosses scenes, isolates
protected clue/performance units, and uses reference duration estimates only for
initial 30–80 second grouping. It does not call ElevenLabs or authorize spend.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load(path: Path) -> dict[str, Any]:
    data=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data,dict):
        raise ValueError(f"Expected object in {path}")
    return data


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


def unit_duration(unit: dict[str, Any]) -> float:
    value=unit.get("estimated_seconds_reference_only")
    require(isinstance(value,(int,float)) and not isinstance(value,bool), f"unit {unit.get('unit_id')}: missing estimated duration")
    require(float(value)>0, f"unit {unit.get('unit_id')}: nonpositive estimated duration")
    return float(value)


def is_protected(unit: dict[str, Any], protected_texts: set[str]) -> bool:
    return str(unit.get("text") or "") in protected_texts


def make_block(scene: int, ordinal: int, units: list[dict[str, Any]], protected: bool, target_min: float, target_max: float) -> dict[str, Any]:
    duration=round(sum(unit_duration(u) for u in units),3)
    chars=[]
    for u in units:
        c=str(u.get("character") or "")
        if c and c not in chars:
            chars.append(c)
    text_hashes=[str(u.get("text_sha256") or "") for u in units]
    require(all(len(h)==64 for h in text_hashes), "invalid dialogue unit hash in block")
    status="TARGET_RANGE"
    if protected and duration < target_min:
        status="PROTECTED_SHORT_BLOCK"
    elif duration < target_min:
        status="SHORT_EDGE_BLOCK"
    elif duration > target_max:
        raise ValueError(f"block scene {scene} ordinal {ordinal} exceeds max duration: {duration}")
    render_mode="ISOLATED_TTS_BLOCK_ALLOWED_AFTER_CAST_LOCK" if len(chars)==1 else "MULTI_CHARACTER_EDITORIAL_BLOCK_SPLIT_TO_ORDERED_REQUESTS"
    return {
        "block_id": f"RU_E01_BLOCK_S{scene:02d}_{ordinal:03d}",
        "scene": scene,
        "scene_title": units[0].get("scene_title"),
        "status": status,
        "protected": protected,
        "unit_ids": [u["unit_id"] for u in units],
        "unit_text_sha256": text_hashes,
        "characters": chars,
        "estimated_seconds_reference_only": duration,
        "render_mode": render_mode,
        "provider_call_authorized": False,
        "paid_synthesis_authorized": False,
    }


def plan_blocks(units_doc: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    require(units_doc.get("status")=="COMPILED_FROM_AUTHORITATIVE_SCRIPT", "dialogue-unit manifest status invalid")
    require(units_doc.get("story_or_dialogue_changed") is False, "dialogue-unit manifest claims text change")
    duration_policy=policy.get("duration_reference") or {}
    target_min=float(duration_policy.get("target_seconds_min",30.0))
    target_max=float(duration_policy.get("target_seconds_max",80.0))
    require(0<target_min<target_max, "invalid duration target")
    protected_texts=set(policy.get("protected_exact_text_units") or [])

    units=units_doc.get("units") or []
    require(isinstance(units,list) and units, "units missing")
    global_ord=[u.get("global_dialogue_ordinal") for u in units]
    require(global_ord==list(range(1,len(units)+1)), "global dialogue order is not contiguous")

    blocks=[]
    current=[]
    current_scene=None
    scene_block_ord={}

    def flush(protected=False):
        nonlocal current,current_scene
        if not current:
            return
        scene=int(current_scene)
        scene_block_ord[scene]=scene_block_ord.get(scene,0)+1
        blocks.append(make_block(scene,scene_block_ord[scene],current,protected,target_min,target_max))
        current=[]

    for unit in units:
        scene=int(unit.get("scene"))
        protected=is_protected(unit,protected_texts)
        if current_scene is None:
            current_scene=scene
        if scene!=current_scene:
            flush(False)
            current_scene=scene
        if protected:
            flush(False)
            current=[unit]
            flush(True)
            continue
        if not current:
            current=[unit]
            continue
        candidate_duration=sum(unit_duration(u) for u in current)+unit_duration(unit)
        if candidate_duration>target_max:
            flush(False)
            current=[unit]
        else:
            current.append(unit)
            if candidate_duration>=target_min:
                flush(False)
    flush(False)

    flattened=[uid for b in blocks for uid in b["unit_ids"]]
    expected=[u["unit_id"] for u in units]
    require(flattened==expected, "planned blocks lost or reordered dialogue units")
    for b in blocks:
        require(len(set(b["characters"]))>=1, f"{b['block_id']}: no character")
        if b["protected"]:
            require(len(b["unit_ids"])==1, f"{b['block_id']}: protected block must contain exactly one unit")

    return {
        "schema_version":"ivdivo.room917_ru_e01_controlled_block_plan/1.0",
        "generated_at":utc_now(),
        "project_id":"ROOM917",
        "episode":"E01",
        "locale":"ru-RU",
        "story_status":"LOCKED",
        "status":"PLANNED_ZERO_SPEND_PRE_RENDER",
        "source_script_sha256":units_doc.get("source_script_sha256"),
        "dialogue_unit_count":len(units),
        "block_count":len(blocks),
        "target_seconds":[target_min,target_max],
        "estimated_seconds_are_authority":False,
        "provider_calls":0,
        "paid_synthesis_calls":0,
        "story_or_dialogue_changed":False,
        "full_episode_single_pass_allowed":False,
        "blocks":blocks,
        "next":"AFTER_CAST_LOCK_MAP_BLOCK_UNITS_TO_APPROVED_VOICE_IDS_AND_VALIDATE_RENDER_REQUESTS"
    }


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--units",type=Path,required=True)
    ap.add_argument("--policy",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    units=load(args.units); policy=load(args.policy)
    result=plan_blocks(units,policy)
    result["dialogue_units_file_sha256"]=sha256_file(args.units)
    result["boundary_policy_file_sha256"]=sha256_file(args.policy)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"dialogue_units":result["dialogue_unit_count"],"blocks":result["block_count"],"out":str(args.out)},ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
