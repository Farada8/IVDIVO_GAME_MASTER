#!/usr/bin/env python3
"""IVDIVO Audio Novel Studio — provider-independent performance compiler.

Consumes a validated Scene State Graph and emits:
- ACTOR_DIRECTOR_SCORE.json
- RHYTHM_PAUSE_BREATH_PLAN.json
- PROVIDER_CONTEXT_PACKETS_DRY_RUN.json

Core rule: internal psychology never goes directly to a provider. The compiler
passes observable/playable behavior, current partner/world context and exact text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def canonical_hash(obj: Any) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def flatten_turns(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for beat in graph.get("beats", []):
        for turn in beat.get("turns", []):
            t = dict(turn)
            t["_beat_id"] = beat.get("beat_id")
            t["_beat_listener"] = beat.get("listener") or {}
            t["_beat_world"] = beat.get("world") or {}
            t["_sound_policy"] = beat.get("sound_policy") or {}
            out.append(t)
    return out


def _provider_safe_behavior(turn: Dict[str, Any]) -> Dict[str, Any]:
    perf = turn.get("performance") or {}
    react = turn.get("reactivity") or {}
    body = turn.get("body") or {}
    space = turn.get("space") or {}
    emotion = turn.get("emotion") or {}

    leakage = emotion.get("leakage") or []
    playable = perf.get("playable_behavior") or []
    if isinstance(playable, str):
        playable = [playable]
    if isinstance(leakage, str):
        leakage = [leakage]

    return {
        "reply_speed": perf.get("entry_timing") or react.get("class"),
        "reply_mode": perf.get("reply_mode") or react.get("class"),
        "tempo": perf.get("tempo"),
        "projection": perf.get("projection"),
        "phrase_ending": perf.get("phrase_ending"),
        "breath": perf.get("breath"),
        "hesitation": perf.get("hesitation"),
        "emphasis": perf.get("emphasis") or [],
        "interruptibility": perf.get("interruptibility"),
        "restraint": perf.get("restraint"),
        "playable_behavior": playable + leakage,
        "body_state": {
            "posture": body.get("posture"),
            "physical_occupation": body.get("physical_occupation"),
            "mouth_state": body.get("mouth_state"),
            "speech_impairment": body.get("speech_impairment"),
            "breath_reset": body.get("breath_reset"),
        },
        "proximity": {
            "distance_to_partner": space.get("distance_to_partner"),
            "distance_to_mic": space.get("distance_to_mic"),
            "head_orientation": space.get("head_orientation"),
            "orientation": space.get("orientation"),
        },
    }


def _context_packet(turn: Dict[str, Any], prev_turn: Dict[str, Any] | None, next_turn: Dict[str, Any] | None, graph: Dict[str, Any]) -> Dict[str, Any]:
    react = turn.get("reactivity") or {}
    relationship = turn.get("relationship") or {}
    status = turn.get("status") or {}
    body = turn.get("body") or {}
    world = turn.get("_beat_world") or {}
    listener = turn.get("_beat_listener") or {}
    return {
        "scene_id": graph.get("scene_id"),
        "scene_objective": graph.get("scene_objective"),
        "immediately_previous_event": react.get("heard_event") or (prev_turn or {}).get("exact_text"),
        "what_speaker_just_heard": react.get("heard_event"),
        "partner_action": react.get("partner_action"),
        "relationship_state": relationship,
        "status_state": status,
        "physical_body_state": body,
        "world_now": {
            "location_id": world.get("location_id"),
            "imagined_scene": world.get("imagined_scene"),
            "listener_focus": listener.get("focus_owner"),
            "active_actions": world.get("active_actions") or [],
        },
        "expected_next_interaction": (next_turn or {}).get("speaker_id"),
        "forbidden_future_knowledge": True,
    }


def _rhythm_event(turn: Dict[str, Any]) -> Dict[str, Any]:
    react = turn.get("reactivity") or {}
    perf = turn.get("performance") or {}
    rhythm = turn.get("rhythm") or {}
    body = turn.get("body") or {}
    return {
        "turn_id": turn.get("turn_id"),
        "beat_id": turn.get("_beat_id"),
        "speaker_id": turn.get("speaker_id"),
        "reply_mode": perf.get("reply_mode") or react.get("class"),
        "entry_trigger": react.get("entry_trigger"),
        "pause_before": rhythm.get("pause_before"),
        "pause_after": rhythm.get("pause_after"),
        "pause_function": rhythm.get("pause_function"),
        "pause_range_ms": rhythm.get("pause_range_ms"),
        "overlap_policy": rhythm.get("overlap_policy"),
        "breath_function": perf.get("breath"),
        "body_action_before_reply": body.get("action_before_reply"),
        "protected_silence": bool(rhythm.get("protected_silence", False)),
    }


def compile_scene(graph: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    turns = flatten_turns(graph)
    actor_score: List[Dict[str, Any]] = []
    rhythm_plan: List[Dict[str, Any]] = []
    packets: List[Dict[str, Any]] = []

    for i, turn in enumerate(turns):
        prev_turn = turns[i - 1] if i > 0 else None
        next_turn = turns[i + 1] if i + 1 < len(turns) else None
        safe_behavior = _provider_safe_behavior(turn)
        context = _context_packet(turn, prev_turn, next_turn, graph)
        role = str(turn.get("speaker_role", "CHARACTER")).upper()
        react = turn.get("reactivity") or {}

        actor_score.append({
            "turn_id": turn.get("turn_id"),
            "beat_id": turn.get("_beat_id"),
            "speaker_id": turn.get("speaker_id"),
            "speaker_role": role,
            "exact_text": turn.get("exact_text"),
            "state_in": turn.get("state_in"),
            "heard_event": react.get("heard_event"),
            "response_impulse": react.get("response_impulse"),
            "entry_trigger": react.get("entry_trigger"),
            "want": turn.get("want"),
            "tactic": turn.get("tactic"),
            "subtext_internal": turn.get("subtext"),
            "emotion_internal": turn.get("emotion"),
            "relationship_state": turn.get("relationship"),
            "status_state": turn.get("status"),
            "listening_state": turn.get("listening"),
            "playable_behavior": safe_behavior,
            "forbidden_performance": turn.get("forbidden_performance") or [],
            "state_out": turn.get("state_out"),
            "render_block_id": turn.get("render_block_id"),
        })

        rhythm_plan.append(_rhythm_event(turn))

        request_basis = {
            "turn_id": turn.get("turn_id"),
            "speaker_id": turn.get("speaker_id"),
            "exact_text": turn.get("exact_text"),
            "scene_context_packet": context,
            "heard_event": react.get("heard_event"),
            "objective": turn.get("want"),
            "tactic": turn.get("tactic"),
            "response_impulse": react.get("response_impulse"),
            "playable_behavior": safe_behavior,
            "pronunciation_refs": turn.get("pronunciation_refs") or [],
            "take_hypothesis": turn.get("take_hypothesis") or "baseline",
            "render_block_id": turn.get("render_block_id"),
            "selective_regeneration_boundary": turn.get("selective_regeneration_boundary", True),
        }
        packets.append({
            **request_basis,
            "request_hash": canonical_hash(request_basis),
            "provider": None,
            "provider_status": "DRY_RUN_PROVIDER_AGNOSTIC",
        })

    source_turn_ids = [t.get("turn_id") for t in turns]
    common = {
        "schema_version": "1.0",
        "project_id": graph.get("project_id"),
        "scene_id": graph.get("scene_id"),
        "source_hash": graph.get("source_hash"),
        "turn_count": len(turns),
        "source_turn_ids": source_turn_ids,
    }

    return {
        "ACTOR_DIRECTOR_SCORE": {**common, "turns": actor_score},
        "RHYTHM_PAUSE_BREATH_PLAN": {**common, "events": rhythm_plan},
        "PROVIDER_CONTEXT_PACKETS_DRY_RUN": {**common, "packets": packets},
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Compile IVDIVO Scene State Graph into performance artifacts")
    p.add_argument("graph")
    p.add_argument("out_dir")
    args = p.parse_args()

    graph = load_json(Path(args.graph))
    outputs = compile_scene(graph)
    out = Path(args.out_dir)
    for name, obj in outputs.items():
        write_json(out / f"{name}.json", obj)
        print(out / f"{name}.json")


if __name__ == "__main__":
    main()
