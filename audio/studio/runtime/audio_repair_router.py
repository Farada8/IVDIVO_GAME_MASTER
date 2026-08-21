#!/usr/bin/env python3
"""IVDIVO Audio Studio — earliest-cause selective repair router.

Audio specialization of the current Targeted Repair / Patch Contract Standard.
It never changes story authority by itself. The router chooses the earliest audio
layer consistent with observed evidence and returns descendants to invalidate.
"""
from __future__ import annotations

from typing import Any

AUDIO_LAYER_ORDER = [
    "SOURCE_TEXT_AUTHORITY",
    "PERFORMANCE_DIRECTION",
    "VOICE_TAKE",
    "EDIT_RHYTHM",
    "BLOCKING_PROXIMITY",
    "FOLEY_OBJECT_CAUSALITY",
    "AMBIENCE_ROOM_IDENTITY",
    "MUSIC_DRAMATURGY",
    "SPATIAL_MIX",
    "MASTERING",
]

LAYER_DESCENDANTS = {
    "SOURCE_TEXT_AUTHORITY": AUDIO_LAYER_ORDER[1:],
    "PERFORMANCE_DIRECTION": AUDIO_LAYER_ORDER[2:],
    "VOICE_TAKE": AUDIO_LAYER_ORDER[3:],
    "EDIT_RHYTHM": AUDIO_LAYER_ORDER[4:],
    "BLOCKING_PROXIMITY": AUDIO_LAYER_ORDER[5:],
    "FOLEY_OBJECT_CAUSALITY": AUDIO_LAYER_ORDER[6:],
    "AMBIENCE_ROOM_IDENTITY": AUDIO_LAYER_ORDER[7:],
    "MUSIC_DRAMATURGY": AUDIO_LAYER_ORDER[8:],
    "SPATIAL_MIX": ["MASTERING"],
    "MASTERING": [],
}

SYMPTOM_ROUTING = {
    "WRONG_WORDS_OR_MEANING": "SOURCE_TEXT_AUTHORITY",
    "WRONG_OBJECTIVE_TACTIC_STATUS": "PERFORMANCE_DIRECTION",
    "VOICE_IDENTITY_OR_ACTING_FAILURE": "VOICE_TAKE",
    "LATENCY_PAUSE_OVERLAP_DRAG": "EDIT_RHYTHM",
    "DISTANCE_OR_MOVEMENT_UNCLEAR": "BLOCKING_PROXIMITY",
    "PHYSICAL_ACTION_NOT_AUDIBLE": "FOLEY_OBJECT_CAUSALITY",
    "ROOM_OR_WEATHER_DROPS_OUT": "AMBIENCE_ROOM_IDENTITY",
    "EMOTIONAL_CONTOUR_NEEDS_SCORE": "MUSIC_DRAMATURGY",
    "PAN_WIDTH_OCCLUSION_REVERB_FAILURE": "SPATIAL_MIX",
    "LOUDNESS_TRUEPEAK_DELIVERY_ONLY": "MASTERING",
}


def route_issue(issue: dict[str, Any]) -> dict[str, Any]:
    """Route one evidenced issue to its earliest repair layer.

    Required evidence fields intentionally separate listener symptom from proposed fix.
    `story_locked=True` prevents SOURCE_TEXT_AUTHORITY from becoming an automatic rewrite.
    """
    required = {"issue_id", "severity", "symptom_class", "evidence_ref"}
    missing = sorted(required - set(issue))
    if missing:
        raise ValueError(f"REPAIR_ISSUE_FIELDS_MISSING:{','.join(missing)}")

    symptom = issue["symptom_class"]
    if symptom not in SYMPTOM_ROUTING:
        return {
            "issue_id": issue["issue_id"],
            "status": "HOLD_UNKNOWN_CAUSE",
            "earliest_layer": None,
            "invalidates": [],
            "automatic_patch_allowed": False,
        }

    layer = SYMPTOM_ROUTING[symptom]
    story_locked = bool(issue.get("story_locked", False))
    if layer == "SOURCE_TEXT_AUTHORITY" and story_locked:
        return {
            "issue_id": issue["issue_id"],
            "status": "ESCALATE_STORY_AUTHORITY",
            "earliest_layer": layer,
            "invalidates": [],
            "automatic_patch_allowed": False,
            "reason": "LOCKED_STORY_REQUIRES_FOUNDER_OR_FATAL_MAJOR_STORY_EVIDENCE",
        }

    protected = list(issue.get("protected_fields") or [])
    return {
        "issue_id": issue["issue_id"],
        "status": "PATCH_ROUTE_READY",
        "earliest_layer": layer,
        "invalidates": list(LAYER_DESCENDANTS[layer]),
        "protected_fields": protected,
        "automatic_patch_allowed": False,
        "preferred_scope": "LOCAL_FIRST",
    }


def choose_edit_vs_regen(issue: dict[str, Any]) -> dict[str, Any]:
    """Distinguish edit-only repair from selective regeneration.

    No whole-scene/episode rerender is returned automatically.
    """
    layer = issue.get("earliest_layer")
    if layer in {"EDIT_RHYTHM", "BLOCKING_PROXIMITY", "FOLEY_OBJECT_CAUSALITY", "AMBIENCE_ROOM_IDENTITY", "MUSIC_DRAMATURGY", "SPATIAL_MIX", "MASTERING"}:
        action = "EDIT_OR_LOCAL_REMIX_FIRST"
    elif layer in {"PERFORMANCE_DIRECTION", "VOICE_TAKE"}:
        action = "SELECTIVE_VOICE_REGEN_OR_RETAKE"
    elif layer == "SOURCE_TEXT_AUTHORITY":
        action = "AUTHORITY_ESCALATION"
    else:
        action = "HOLD"
    return {
        "action": action,
        "whole_episode_rerender": False,
        "requires_acceptance_test": True,
    }
