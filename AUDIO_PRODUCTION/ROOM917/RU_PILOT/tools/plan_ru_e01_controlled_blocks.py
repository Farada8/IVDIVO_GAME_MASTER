#!/usr/bin/env python3
"""Plan controlled ROOM917 RU E01 editorial dialogue blocks from immutable units.

Zero-spend planner. It preserves unit order, never crosses scenes, isolates
protected clue/performance units, and uses reference duration estimates only for
initial 30–80 second grouping. Noncritical segments are rebalanced so a short
final edge is repaired when possible without exceeding 80 seconds.
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
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected object in {path}")
    return data


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


def unit_duration(unit: dict[str, Any]) -> float:
    value = unit.get("estimated_seconds_reference_only")
    require(isinstance(value, (int, float)) and not isinstance(value, bool), f"unit {unit.get('unit_id')}: missing estimated duration")
    require(float(value) > 0, f"unit {unit.get('unit_id')}: nonpositive estimated duration")
    return float(value)


def group_duration(units: list[dict[str, Any]]) -> float:
    return sum(unit_duration(u) for u in units)


def is_protected(unit: dict[str, Any], protected_texts: set[str]) -> bool:
    return str(unit.get("text") or "") in protected_texts


def make_block(scene: int, ordinal: int, units: list[dict[str, Any]], protected: bool, target_min: float, target_max: float) -> dict[str, Any]:
    duration = round(group_duration(units), 3)
    chars: list[str] = []
    for unit in units:
        char = str(unit.get("character") or "")
        if char and char not in chars:
            chars.append(char)
    text_hashes = [str(unit.get("text_sha256") or "") for unit in units]
    require(all(len(h) == 64 for h in text_hashes), "invalid dialogue unit hash in block")

    status = "TARGET_RANGE"
    if protected and duration < target_min:
        status = "PROTECTED_SHORT_BLOCK"
    elif duration < target_min:
        status = "SHORT_EDGE_BLOCK"
    elif duration > target_max:
        raise ValueError(f"block scene {scene} ordinal {ordinal} exceeds max duration: {duration}")

    render_mode = (
        "ISOLATED_TTS_BLOCK_ALLOWED_AFTER_CAST_LOCK"
        if len(chars) == 1
        else "MULTI_CHARACTER_EDITORIAL_BLOCK_SPLIT_TO_ORDERED_REQUESTS"
    )
    return {
        "block_id": f"RU_E01_BLOCK_S{scene:02d}_{ordinal:03d}",
        "scene": scene,
        "scene_title": units[0].get("scene_title"),
        "status": status,
        "protected": protected,
        "unit_ids": [unit["unit_id"] for unit in units],
        "unit_text_sha256": text_hashes,
        "characters": chars,
        "estimated_seconds_reference_only": duration,
        "render_mode": render_mode,
        "provider_call_authorized": False,
        "paid_synthesis_authorized": False,
    }


def partition_noncritical_segment(segment: list[dict[str, Any]], target_min: float, target_max: float) -> list[list[dict[str, Any]]]:
    """Partition one contiguous noncritical segment while preserving order.

    Fill toward target_max. If the final group is short, merge it with the
    previous group when possible; otherwise move previous tail units into the
    final group while keeping both groups >= target_min when possible.
    """
    if not segment:
        return []

    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for unit in segment:
        if not current:
            current = [unit]
            continue
        if group_duration(current) + unit_duration(unit) > target_max:
            groups.append(current)
            current = [unit]
        else:
            current.append(unit)
    if current:
        groups.append(current)

    if len(groups) >= 2 and group_duration(groups[-1]) < target_min:
        prev = groups[-2]
        last = groups[-1]
        if group_duration(prev) + group_duration(last) <= target_max:
            groups[-2] = prev + last
            groups.pop()
        else:
            # Move a contiguous tail from prev to the front of last, preserving
            # global order and keeping prev >= target_min where possible.
            while len(prev) > 1 and group_duration(last) < target_min:
                candidate = prev[-1]
                if group_duration(last) + unit_duration(candidate) > target_max:
                    break
                if group_duration(prev) - unit_duration(candidate) < target_min:
                    break
                prev.pop()
                last.insert(0, candidate)
            groups[-2] = prev
            groups[-1] = last

    for group in groups:
        require(group_duration(group) <= target_max, "noncritical partition produced >max block")
    return groups


def plan_blocks(units_doc: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    require(units_doc.get("status") == "COMPILED_FROM_AUTHORITATIVE_SCRIPT", "dialogue-unit manifest status invalid")
    require(units_doc.get("story_or_dialogue_changed") is False, "dialogue-unit manifest claims text change")
    duration_policy = policy.get("duration_reference") or {}
    target_min = float(duration_policy.get("target_seconds_min", 30.0))
    target_max = float(duration_policy.get("target_seconds_max", 80.0))
    require(0 < target_min < target_max, "invalid duration target")
    protected_texts = set(policy.get("protected_exact_text_units") or [])

    units = units_doc.get("units") or []
    require(isinstance(units, list) and units, "units missing")
    global_ord = [unit.get("global_dialogue_ordinal") for unit in units]
    require(global_ord == list(range(1, len(units) + 1)), "global dialogue order is not contiguous")

    blocks: list[dict[str, Any]] = []
    scene_block_ord: dict[int, int] = {}
    segment: list[dict[str, Any]] = []
    current_scene: int | None = None

    def append_group(scene: int, group: list[dict[str, Any]], protected: bool) -> None:
        scene_block_ord[scene] = scene_block_ord.get(scene, 0) + 1
        blocks.append(make_block(scene, scene_block_ord[scene], group, protected, target_min, target_max))

    def flush_segment(scene: int | None) -> None:
        nonlocal segment
        if scene is None or not segment:
            segment = []
            return
        for group in partition_noncritical_segment(segment, target_min, target_max):
            append_group(scene, group, False)
        segment = []

    for unit in units:
        scene = int(unit.get("scene"))
        if current_scene is None:
            current_scene = scene
        if scene != current_scene:
            flush_segment(current_scene)
            current_scene = scene
        if is_protected(unit, protected_texts):
            flush_segment(current_scene)
            append_group(scene, [unit], True)
        else:
            segment.append(unit)
    flush_segment(current_scene)

    flattened = [uid for block in blocks for uid in block["unit_ids"]]
    expected = [unit["unit_id"] for unit in units]
    require(flattened == expected, "planned blocks lost or reordered dialogue units")
    for block in blocks:
        require(len(set(block["characters"])) >= 1, f"{block['block_id']}: no character")
        if block["protected"]:
            require(len(block["unit_ids"]) == 1, f"{block['block_id']}: protected block must contain exactly one unit")

    ordinary_short = sum(1 for block in blocks if block["status"] == "SHORT_EDGE_BLOCK")
    return {
        "schema_version": "ivdivo.room917_ru_e01_controlled_block_plan/1.1",
        "generated_at": utc_now(),
        "project_id": "ROOM917",
        "episode": "E01",
        "locale": "ru-RU",
        "story_status": "LOCKED",
        "status": "PLANNED_ZERO_SPEND_PRE_RENDER",
        "source_script_sha256": units_doc.get("source_script_sha256"),
        "dialogue_unit_count": len(units),
        "block_count": len(blocks),
        "ordinary_short_edge_block_count": ordinary_short,
        "target_seconds": [target_min, target_max],
        "estimated_seconds_are_authority": False,
        "provider_calls": 0,
        "paid_synthesis_calls": 0,
        "story_or_dialogue_changed": False,
        "full_episode_single_pass_allowed": False,
        "blocks": blocks,
        "next": "AFTER_CAST_LOCK_MAP_BLOCK_UNITS_TO_APPROVED_VOICE_IDS_AND_VALIDATE_RENDER_REQUESTS",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", type=Path, required=True)
    ap.add_argument("--policy", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    units = load(args.units)
    policy = load(args.policy)
    result = plan_blocks(units, policy)
    result["dialogue_units_file_sha256"] = sha256_file(args.units)
    result["boundary_policy_file_sha256"] = sha256_file(args.policy)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "dialogue_units": result["dialogue_unit_count"], "blocks": result["block_count"], "ordinary_short_edge_blocks": result["ordinary_short_edge_block_count"], "out": str(args.out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
