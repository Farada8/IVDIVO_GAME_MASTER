#!/usr/bin/env python3
"""IVDIVO Audio Novel Studio — Scene State Graph validator.

Provider-independent. It validates the multi-layer dramatic state that connects
story/canon to performance, body, space, sound and listener attention.

It does NOT invent story facts. A reasoning/creative stage must populate the
Scene State Graph from locked source + current authority before this validator runs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ALLOWED_REPLY_MODES = {
    "NONREACTIVE", "NARRATIVE", "IMMEDIATE", "SHORT_BEAT", "THINK", "WITHHOLD",
    "INTERRUPT", "OVERLAP", "STEP_ON_LINE", "FALSE_START", "SELF_CORRECT",
    "WAIT_FOR_PARTNER", "ACTION_BEFORE_REPLY", "BREATH_BEFORE_REPLY", "NO_REPLY",
}

REQUIRED_GRAPH_FIELDS = [
    "schema_version", "project_id", "scene_id", "source_hash", "delivery_mode",
    "scene_objective", "listener_point_of_audition", "world_state", "beats",
]

REQUIRED_BEAT_FIELDS = [
    "beat_id", "source_text_ids", "story_change", "listener", "world", "turns", "sound_policy",
]

REQUIRED_CHARACTER_TURN_FIELDS = [
    "turn_id", "speaker_id", "speaker_role", "exact_text", "reactivity",
    "knowledge", "attention", "want", "tactic", "subtext", "emotion",
    "relationship", "status", "listening", "body", "performance", "space",
    "state_in", "state_out",
]

REQUIRED_NARRATOR_TURN_FIELDS = [
    "turn_id", "speaker_id", "speaker_role", "exact_text", "reactivity",
    "attention", "performance", "space", "state_in", "state_out",
]


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _issue(issues: List[Dict[str, Any]], severity: str, code: str, location: str, message: str) -> None:
    issues.append({
        "severity": severity,
        "code": code,
        "location": location,
        "message": message,
    })


def _missing_fields(obj: Dict[str, Any], fields: Iterable[str]) -> List[str]:
    return [f for f in fields if f not in obj]


def _primary_emotion(turn: Dict[str, Any]) -> Tuple[str | None, float | None]:
    emotion = turn.get("emotion") or {}
    felt = emotion.get("felt") or {}
    primary = felt.get("primary")
    intensity = felt.get("intensity")
    try:
        intensity = float(intensity) if intensity is not None else None
    except (TypeError, ValueError):
        intensity = None
    return primary, intensity


def validate_graph(graph: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []

    missing = _missing_fields(graph, REQUIRED_GRAPH_FIELDS)
    if missing:
        _issue(issues, "FATAL", "GRAPH_FIELDS_MISSING", "$", f"Missing fields: {missing}")

    beats = graph.get("beats")
    if not isinstance(beats, list) or not beats:
        _issue(issues, "FATAL", "NO_BEATS", "$.beats", "Scene State Graph must contain at least one beat")
        beats = []

    seen_beat_ids = set()
    seen_turn_ids = set()
    last_turn_by_speaker: Dict[str, Dict[str, Any]] = {}
    previous_world_location = None

    for bi, beat in enumerate(beats):
        loc = f"$.beats[{bi}]"
        if not isinstance(beat, dict):
            _issue(issues, "FATAL", "BEAT_NOT_OBJECT", loc, "Beat must be an object")
            continue
        missing = _missing_fields(beat, REQUIRED_BEAT_FIELDS)
        if missing:
            _issue(issues, "MAJOR", "BEAT_FIELDS_MISSING", loc, f"Missing fields: {missing}")

        beat_id = beat.get("beat_id")
        if beat_id in seen_beat_ids:
            _issue(issues, "FATAL", "DUPLICATE_BEAT_ID", loc, f"Duplicate beat_id {beat_id}")
        if beat_id:
            seen_beat_ids.add(beat_id)

        source_ids = beat.get("source_text_ids")
        if not isinstance(source_ids, list) or not source_ids:
            _issue(issues, "MAJOR", "BEAT_SOURCE_IDS_EMPTY", loc, "Beat requires source_text_ids")

        listener = beat.get("listener") or {}
        for f in ["must_understand", "may_feel", "must_wait_for", "focus_owner", "suppress"]:
            if f not in listener:
                _issue(issues, "MEDIUM", "LISTENER_FIELD_MISSING", f"{loc}.listener", f"Missing {f}")

        world = beat.get("world") or {}
        world_location = world.get("location_id")
        if previous_world_location and world_location and world_location != previous_world_location:
            if not world.get("transition_from_previous"):
                _issue(
                    issues, "MAJOR", "WORLD_JUMP_WITHOUT_TRANSITION", f"{loc}.world",
                    f"Location changed {previous_world_location!r} -> {world_location!r} without transition_from_previous"
                )
        if world_location:
            previous_world_location = world_location

        turns = beat.get("turns")
        if not isinstance(turns, list):
            _issue(issues, "MAJOR", "TURNS_NOT_LIST", f"{loc}.turns", "turns must be a list")
            continue

        for ti, turn in enumerate(turns):
            tloc = f"{loc}.turns[{ti}]"
            if not isinstance(turn, dict):
                _issue(issues, "FATAL", "TURN_NOT_OBJECT", tloc, "Turn must be an object")
                continue
            role = str(turn.get("speaker_role", "CHARACTER")).upper()
            required = REQUIRED_NARRATOR_TURN_FIELDS if role == "NARRATOR" else REQUIRED_CHARACTER_TURN_FIELDS
            missing = _missing_fields(turn, required)
            if missing:
                _issue(issues, "MAJOR", "TURN_FIELDS_MISSING", tloc, f"Missing fields: {missing}")

            turn_id = turn.get("turn_id")
            if turn_id in seen_turn_ids:
                _issue(issues, "FATAL", "DUPLICATE_TURN_ID", tloc, f"Duplicate turn_id {turn_id}")
            if turn_id:
                seen_turn_ids.add(turn_id)

            if not isinstance(turn.get("exact_text"), str) or not turn.get("exact_text", "").strip():
                _issue(issues, "FATAL", "EMPTY_EXACT_TEXT", tloc, "exact_text must be non-empty")

            reactivity = turn.get("reactivity") or {}
            rclass = str(reactivity.get("class", "")).upper()
            if rclass and rclass not in ALLOWED_REPLY_MODES:
                _issue(issues, "MEDIUM", "UNKNOWN_REPLY_CLASS", f"{tloc}.reactivity", f"Unknown class {rclass}")
            if role != "NARRATOR" and rclass not in {"NONREACTIVE", "NARRATIVE", ""}:
                if not reactivity.get("heard_event"):
                    _issue(issues, "MAJOR", "REACTIVE_TURN_WITHOUT_HEARD_EVENT", f"{tloc}.reactivity", "Reactive character turn requires heard_event")
                if not reactivity.get("response_impulse"):
                    _issue(issues, "MAJOR", "REACTIVE_TURN_WITHOUT_RESPONSE_IMPULSE", f"{tloc}.reactivity", "Reactive character turn requires response_impulse")
                if not reactivity.get("entry_trigger"):
                    _issue(issues, "MEDIUM", "REACTIVE_TURN_WITHOUT_ENTRY_TRIGGER", f"{tloc}.reactivity", "Reactive character turn should define entry_trigger")

            performance = turn.get("performance") or {}
            if role != "NARRATOR":
                for f in ["reply_mode", "tempo", "projection", "phrase_ending", "breath", "playable_behavior"]:
                    if f not in performance:
                        _issue(issues, "MEDIUM", "PERFORMANCE_FIELD_MISSING", f"{tloc}.performance", f"Missing {f}")

            body = turn.get("body") or {}
            mouth_state = str(body.get("mouth_state", "CLEAR")).upper()
            speech_allowed = body.get("speech_allowed", True)
            if role != "NARRATOR" and mouth_state not in {"CLEAR", "NONE", ""} and speech_allowed:
                impairment = str(body.get("speech_impairment", "NONE")).upper()
                swallow_before = bool(body.get("swallow_before_line", False))
                if impairment in {"NONE", ""} and not swallow_before:
                    _issue(
                        issues, "MAJOR", "MOUTH_STATE_SPEECH_INCONSISTENT", f"{tloc}.body",
                        "Audible/non-clear mouth state allows clean speech without impairment or swallow_before_line"
                    )

            space = turn.get("space") or {}
            if space.get("ear_specific") and not space.get("mono_fallback"):
                _issue(issues, "MAJOR", "EAR_SPECIFIC_WITHOUT_MONO_FALLBACK", f"{tloc}.space", "Ear-specific staging requires mono_fallback")

            speaker = turn.get("speaker_id")
            if speaker:
                prev = last_turn_by_speaker.get(speaker)
                if prev and role != "NARRATOR":
                    prev_primary, prev_intensity = _primary_emotion(prev)
                    cur_primary, cur_intensity = _primary_emotion(turn)
                    transition = (turn.get("emotion") or {}).get("transition_cause")
                    large_change = (
                        prev_primary and cur_primary and prev_primary != cur_primary and
                        prev_intensity is not None and cur_intensity is not None and
                        max(prev_intensity, cur_intensity) >= 5
                    )
                    intensity_jump = (
                        prev_intensity is not None and cur_intensity is not None and
                        abs(cur_intensity - prev_intensity) >= 3
                    )
                    if (large_change or intensity_jump) and not transition:
                        _issue(
                            issues, "MEDIUM", "EMOTION_CHANGE_WITHOUT_CAUSE", f"{tloc}.emotion",
                            "Large emotional transition should name transition_cause"
                        )

                    prev_out = prev.get("state_out")
                    cur_in = turn.get("state_in")
                    if prev_out and cur_in and prev_out != cur_in:
                        bridge = reactivity.get("heard_event") or (turn.get("emotion") or {}).get("transition_cause")
                        if not bridge:
                            _issue(
                                issues, "MEDIUM", "STATE_CONTINUITY_UNEXPLAINED", tloc,
                                f"state_in {cur_in!r} differs from previous state_out {prev_out!r} without bridge"
                            )
                last_turn_by_speaker[speaker] = turn

    severities = {s: 0 for s in ["FATAL", "MAJOR", "MEDIUM", "POLISH"]}
    for issue in issues:
        severities[issue["severity"]] = severities.get(issue["severity"], 0) + 1

    gate = "PASS" if severities["FATAL"] == 0 and severities["MAJOR"] == 0 else "FAIL"
    return {
        "schema": "IVDIVO_SCENE_STATE_GRAPH_VALIDATION_v1",
        "project_id": graph.get("project_id"),
        "scene_id": graph.get("scene_id"),
        "gate": gate,
        "counts": {
            "beats": len(beats),
            "turns": len(seen_turn_ids),
            "issues": len(issues),
            **{f"{k.lower()}_issues": v for k, v in severities.items()},
        },
        "issues": issues,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Validate IVDIVO Scene State Graph")
    p.add_argument("graph")
    p.add_argument("--output")
    args = p.parse_args()

    graph_path = Path(args.graph)
    report = validate_graph(load_json(graph_path))
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    raise SystemExit(0 if report["gate"] == "PASS" else 2)


if __name__ == "__main__":
    main()
