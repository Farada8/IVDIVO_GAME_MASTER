#!/usr/bin/env python3
"""Compile ROOM917 RU Listener-QC defects into smallest-scope repair actions.

Zero-spend planner only. It does not call ElevenLabs, modify scripts, edit audio,
or authorize paid rendering. It converts evidence-backed defect records into a
machine-readable repair queue while failing closed on unknown/overbroad scope.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any

ALLOWED_LAYERS = {"PERFORMANCE", "EDIT", "MIX", "SOUND_ASSET", "UNKNOWN"}
ALLOWED_STATUS = {"KEEP", "REPAIR", "HOLD"}
ALLOWED_SEVERITY = {"FATAL", "MAJOR", "MEDIUM", "POLISH"}
LOCAL_SCOPE_WORDS = {
    "TOKEN", "WORD", "PHRASE", "LINE", "LOCAL_BLOCK", "BLOCK", "CUE", "CLIP",
    "INTERVAL", "EVENT", "CROSSFADE", "STEM", "BUS", "ASSET"
}
FORBIDDEN_SCOPE_WORDS = {"EPISODE", "FULL_EPISODE", "WHOLE_EPISODE", "BOOK", "SEASON"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def tokens(value: object) -> set[str]:
    text = str(value or "").upper().replace("-", "_")
    return set(re.findall(r"[A-Z0-9_]+", text))


def is_overbroad_scope(scope: object) -> bool:
    t = tokens(scope)
    return bool(t & FORBIDDEN_SCOPE_WORDS)


def has_local_scope(scope: object) -> bool:
    t = tokens(scope)
    return bool(t & LOCAL_SCOPE_WORDS)


def text_blob(defect: dict[str, Any]) -> str:
    return " ".join(
        str(defect.get(k) or "")
        for k in ("heard", "scene_failure", "smallest_repair_scope", "minimal_fix", "do_not_touch")
    ).casefold()


def detect_performance_subtype(defect: dict[str, Any]) -> str:
    text = text_blob(defect)
    if any(key in text for key in ("pronunc", "произнош", "лени-бёрд", "грейхейвен", "эшкрофт")):
        return "PRONUNCIATION"
    if any(key in text for key in ("ai", "synthetic", "robot", "искусствен", "ии слыш")):
        return "AI_ARTIFACT_OR_SYNTHETIC_DELIVERY"
    if any(key in text for key in ("overplay", "melodram", "trailer", "переиг", "слишком драм")):
        return "EMOTION_OVERPLAY"
    if any(key in text for key in ("flat", "dead", "underplay", "плоск", "мертв", "недоигр")):
        return "EMOTION_UNDERPLAY"
    if any(key in text for key in ("drift", "identity", "другой голос", "тембр")):
        return "VOICE_IDENTITY_DRIFT"
    if any(key in text for key in ("diction", "слова неразбор", "неразборчив")):
        return "DICTION"
    return "PERFORMANCE_GENERAL"


def compile_defect(defect: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    defect_id = str(defect.get("defect_id") or "").strip()
    layer = str(defect.get("failure_layer") or "").strip().upper()
    severity = str(defect.get("severity") or "").strip().upper()
    status = str(defect.get("status") or "").strip().upper()
    scope = str(defect.get("smallest_repair_scope") or "").strip()

    if not defect_id:
        errors.append("DEFECT_ID_MISSING")
    if layer not in ALLOWED_LAYERS:
        errors.append(f"INVALID_FAILURE_LAYER:{layer or '<empty>'}")
    if severity not in ALLOWED_SEVERITY:
        errors.append(f"INVALID_SEVERITY:{severity or '<empty>'}")
    if status not in ALLOWED_STATUS:
        errors.append(f"INVALID_STATUS:{status or '<empty>'}")

    start = defect.get("start_seconds")
    end = defect.get("end_seconds")
    if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or float(end) <= float(start):
        errors.append("INVALID_TIME_RANGE")

    if status == "KEEP":
        return None, errors
    if status == "HOLD":
        return {
            "repair_id": f"REPAIR_{defect_id}",
            "defect_id": defect_id,
            "status": "HOLD",
            "reason": "SOURCE_DEFECT_STATUS_HOLD",
            "provider_call_allowed": False,
            "paid_synthesis_allowed": False,
            "story_or_dialogue_change_allowed": False,
        }, errors

    if is_overbroad_scope(scope):
        errors.append("OVERBROAD_REPAIR_SCOPE_FORBIDDEN")
    if not scope:
        errors.append("SMALLEST_REPAIR_SCOPE_MISSING")

    base = {
        "repair_id": f"REPAIR_{defect_id}",
        "defect_id": defect_id,
        "severity": severity,
        "question_class": defect.get("question_class"),
        "failure_layer": layer,
        "start_seconds": start,
        "end_seconds": end,
        "requested_scope": scope,
        "minimal_fix_source": defect.get("minimal_fix"),
        "do_not_touch": defect.get("do_not_touch"),
        "regression_tests": defect.get("regression_tests") or [],
        "story_or_dialogue_change_allowed": False,
        "whole_episode_rerender_allowed": False,
        "provider_call_allowed": False,
        "paid_synthesis_allowed": False,
        "execution_status": "PLANNED_NOT_EXECUTED",
    }

    if layer == "UNKNOWN":
        base.update({
            "status": "HOLD",
            "action": "EVIDENCE_CLASSIFICATION_REQUIRED",
            "reason": "UNKNOWN_FAILURE_LAYER_CANNOT_BE_PATCHED",
        })
        return base, errors

    if layer == "PERFORMANCE":
        subtype = detect_performance_subtype(defect)
        if not has_local_scope(scope):
            errors.append("PERFORMANCE_REPAIR_REQUIRES_LOCAL_SCOPE")
        action = "SELECTIVE_DIALOGUE_RERENDER"
        if subtype == "PRONUNCIATION":
            action = "PRONUNCIATION_RULE_OR_MINIMUM_PHRASE_RERENDER"
        base.update({
            "status": "READY_AFTER_MAPPING_AND_SPEND_GATE",
            "action": action,
            "performance_issue": subtype,
            "requires_exact_source_unit_mapping": True,
            "requires_same_locked_source_text_hash": True,
            "requires_current_approved_voice_id": True,
            "requires_eleven_v3": True,
            "requires_pronunciation_contract": subtype == "PRONUNCIATION",
            "requires_render_request_validator_pass": True,
            "requires_separate_paid_canary_or_repair_authorization": True,
            "preferred_scope_order": ["TOKEN", "MINIMUM_PHRASE", "LINE", "LOCAL_BLOCK"],
            "post_splice_qc_required": True,
        })
    elif layer == "EDIT":
        base.update({
            "status": "READY_FOR_EDIT_ONLY",
            "action": "LOCAL_EDIT_OR_ALIGNMENT_REPAIR",
            "requires_new_tts": False,
            "preserve_selected_take_if_possible": True,
            "requires_local_crossfade_or_timing_qc": True,
        })
    elif layer == "MIX":
        base.update({
            "status": "READY_FOR_MIX_PATCH_ONLY",
            "action": "LOCAL_MIX_OR_AUTOMATION_PATCH",
            "requires_new_tts": False,
            "dialogue_rerender_forbidden": True,
            "requires_stereo_mono_mobile_regression": True,
        })
    elif layer == "SOUND_ASSET":
        base.update({
            "status": "READY_FOR_ASSET_REPAIR_ONLY_AFTER_ASSET_FAILURE_PROOF",
            "action": "REPLACE_OR_REPAIR_FAILED_SOUND_ASSET",
            "requires_new_tts": False,
            "dialogue_rerender_forbidden": True,
            "new_asset_requires_blind_selection_and_identity_lock": True,
            "shared_en_ru_asset_check_required": True,
        })

    return base, errors


def compile_plan(result: dict[str, Any]) -> dict[str, Any]:
    defects = result.get("defects") or []
    errors: list[dict[str, Any]] = []
    repairs: list[dict[str, Any]] = []

    if not isinstance(defects, list):
        errors.append({"defect_id": None, "errors": ["DEFECTS_NOT_LIST"]})
        defects = []

    source_identity = result.get("source_identity") or {}
    identity_status = str(source_identity.get("identity_status") or "UNVERIFIED").upper()
    blind = result.get("blind_listen") or {}
    pass_a_frozen = bool(blind.get("pass_a_notes_frozen"))

    for defect in defects:
        if not isinstance(defect, dict):
            errors.append({"defect_id": None, "errors": ["DEFECT_NOT_OBJECT"]})
            continue
        repair, defect_errors = compile_defect(defect)
        if defect_errors:
            errors.append({"defect_id": defect.get("defect_id"), "errors": defect_errors})
        if repair is not None:
            repairs.append(repair)

    hard_hold_reasons: list[str] = []
    if identity_status not in {"VERIFIED", "PASS", "MATCH", "PROVENANCE_VERIFIED"}:
        hard_hold_reasons.append("AUDIO_IDENTITY_NOT_VERIFIED")
    if not pass_a_frozen and any(r.get("status") != "HOLD" for r in repairs):
        hard_hold_reasons.append("PASS_A_NOT_FROZEN")

    status = "FAIL_CLOSED" if errors else "PASS_PLAN_COMPILED"
    executable = status == "PASS_PLAN_COMPILED" and not hard_hold_reasons
    if not executable and status == "PASS_PLAN_COMPILED":
        status = "HOLD_EVIDENCE_GATE"

    return {
        "schema_version": "ivdivo.room917_ru_selective_repair_plan/1.0",
        "generated_at": utc_now(),
        "project": "ROOM917",
        "episode": result.get("episode", "E01"),
        "locale": result.get("locale", "ru-RU"),
        "status": status,
        "executable_now": executable,
        "provider_calls_made": 0,
        "paid_synthesis_calls_made": 0,
        "story_or_dialogue_changed": False,
        "whole_episode_rerender_allowed": False,
        "source_identity_status": identity_status,
        "pass_a_notes_frozen": pass_a_frozen,
        "hard_hold_reasons": hard_hold_reasons,
        "errors": errors,
        "repair_count": len(repairs),
        "repairs": repairs,
        "routing_law": {
            "PERFORMANCE": "SELECTIVE_TTS_ONLY_AFTER_MAPPING_VALIDATION_AND_SEPARATE_SPEND_GATE",
            "EDIT": "EDIT_ONLY_FIRST",
            "MIX": "MIX_PATCH_ONLY_FIRST",
            "SOUND_ASSET": "ASSET_LAYER_ONLY_FIRST",
            "UNKNOWN": "HOLD_AND_CLASSIFY",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    plan = compile_plan(load(args.result))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(plan["status"])
    return 2 if plan["status"] == "FAIL_CLOSED" else 0


if __name__ == "__main__":
    sys.exit(main())
