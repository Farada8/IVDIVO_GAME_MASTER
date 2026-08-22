#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

QUESTION_CLASSES = {
    "ACTOR_BELIEF",
    "AI_AUDIBLE",
    "DEAD_SCENE",
    "GEOGRAPHY",
    "MYSTERY",
    "SFX_MASKING",
}
FAILURE_LAYERS = {"PERFORMANCE", "EDIT", "MIX", "SOUND_ASSET", "UNKNOWN"}
SEVERITIES = {"FATAL", "MAJOR", "MEDIUM", "POLISH"}
REQUIRED_DEFECT_FIELDS = {
    "defect_id",
    "start_seconds",
    "end_seconds",
    "question_class",
    "severity",
    "confidence",
    "heard",
    "scene_failure",
    "failure_layer",
    "smallest_repair_scope",
    "minimal_fix",
    "do_not_touch",
    "regression_tests",
    "status",
}
ACTION_BY_LAYER = {
    "PERFORMANCE": "SELECTIVE_DIALOGUE_RERENDER",
    "EDIT": "LOCAL_EDIT_TIMING_PATCH",
    "MIX": "LOCAL_MIX_PATCH",
    "SOUND_ASSET": "SELECTIVE_SOUND_ASSET_REPLACEMENT_OR_REGEN",
}
BROAD_SCOPE_TOKENS = (
    "WHOLE EPISODE",
    "FULL EPISODE",
    "ENTIRE EPISODE",
    "WHOLE SCENE",
    "FULL SCENE",
    "ENTIRE SCENE",
    "COMPLETE RERENDER",
    "FULL RERENDER",
    "ALL DIALOGUE",
    "RERENDER EVERYTHING",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def broad_scope(*values: object) -> bool:
    text = " ".join(str(v) for v in values if v is not None).upper().replace("_", " ")
    return any(token in text for token in BROAD_SCOPE_TOKENS)


def source_gate(result: dict) -> list[str]:
    errors: list[str] = []
    source = result.get("source_identity") or {}
    mode = source.get("target_identity_mode")
    allowed = set(source.get("allowed_target_identity_mode") or [])
    if source.get("identity_status") != "VERIFIED":
        errors.append("SOURCE_IDENTITY_NOT_VERIFIED")
    if not mode or mode not in allowed:
        errors.append("TARGET_IDENTITY_MODE_NOT_ALLOWED")
    if not source.get("observed_sha256"):
        errors.append("OBSERVED_SHA256_MISSING")
    blind = result.get("blind_listen") or {}
    if blind.get("pass_a_notes_frozen") is not True:
        errors.append("PASS_A_NOTES_NOT_FROZEN")
    if blind.get("pass_a_story_free") in (None, "NOT_RUN"):
        errors.append("PASS_A_NOT_RUN")
    if blind.get("pass_b_targeted_verification") in (None, "NOT_RUN"):
        errors.append("PASS_B_NOT_RUN")
    return errors


def validate_defect(defect: dict, duration: float) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_DEFECT_FIELDS - set(defect))
    if missing:
        errors.append("MISSING_FIELDS:" + ",".join(missing))
        return errors
    if defect.get("question_class") not in QUESTION_CLASSES:
        errors.append("UNKNOWN_QUESTION_CLASS")
    if defect.get("failure_layer") not in FAILURE_LAYERS:
        errors.append("UNKNOWN_FAILURE_LAYER_VALUE")
    if defect.get("severity") not in SEVERITIES:
        errors.append("UNKNOWN_SEVERITY")
    try:
        start = float(defect.get("start_seconds"))
        end = float(defect.get("end_seconds"))
        if not (0.0 <= start < end <= duration + 1e-6):
            errors.append("INVALID_INTERVAL")
    except (TypeError, ValueError):
        errors.append("INVALID_INTERVAL")
    if not str(defect.get("heard") or "").strip():
        errors.append("HEARD_EVIDENCE_MISSING")
    if not str(defect.get("scene_failure") or "").strip():
        errors.append("SCENE_FAILURE_MISSING")
    if not str(defect.get("minimal_fix") or "").strip():
        errors.append("MINIMAL_FIX_MISSING")
    if not str(defect.get("smallest_repair_scope") or "").strip():
        errors.append("SMALLEST_REPAIR_SCOPE_MISSING")
    if not isinstance(defect.get("do_not_touch"), list):
        errors.append("DO_NOT_TOUCH_MUST_BE_LIST")
    if not isinstance(defect.get("regression_tests"), list) or not defect.get("regression_tests"):
        errors.append("REGRESSION_TESTS_REQUIRED")
    if broad_scope(defect.get("smallest_repair_scope"), defect.get("minimal_fix")):
        errors.append("BROAD_SCOPE_FORBIDDEN")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Compile verified ROOM917 P003B audible defects into smallest-scope selective repairs.")
    ap.add_argument("--result", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    result = load(args.result)
    gate_errors = source_gate(result)
    duration = float((result.get("source_identity") or {}).get("expected_duration_seconds") or 658.190)
    output = {
        "schema_version": "ivdivo.room917_p003b_selective_repair_plan/1.0",
        "project": "ROOM917",
        "episode": result.get("episode"),
        "authority": result.get("authority"),
        "source_identity": {
            "mode": (result.get("source_identity") or {}).get("target_identity_mode"),
            "observed_sha256": (result.get("source_identity") or {}).get("observed_sha256"),
            "identity_status": (result.get("source_identity") or {}).get("identity_status"),
        },
        "status": "HOLD",
        "release_authorized": False,
        "whole_episode_rerender_authorized": False,
        "story_rewrite_authorized": False,
        "repairs": [],
        "holds": [],
        "ignored_keep_defects": [],
        "gate_errors": gate_errors,
        "law": "VERIFIED_AUDIBLE_DEFECT -> EXACT_INTERVAL -> SMALLEST_LAYER_REPAIR -> REGRESSION -> RELISTEN; NO_RELEASE_FROM_COMPILER",
    }

    if gate_errors:
        dump(args.out, output)
        print("HOLD " + ";".join(gate_errors))
        return 4

    for defect in result.get("defects") or []:
        defect_id = defect.get("defect_id", "UNKNOWN")
        status = defect.get("status")
        if status == "KEEP":
            output["ignored_keep_defects"].append(defect_id)
            continue
        errors = validate_defect(defect, duration)
        if status == "HOLD":
            output["holds"].append({"defect_id": defect_id, "reasons": errors or ["DEFECT_STATUS_HOLD"]})
            continue
        if status != "REPAIR":
            output["holds"].append({"defect_id": defect_id, "reasons": errors + ["DEFECT_STATUS_NOT_ALLOWED"]})
            continue
        if defect.get("severity") == "FATAL":
            errors.append("FATAL_REQUIRES_MANUAL_REOPEN_OR_EXPLICIT_REPAIR_AUTHORITY")
        if defect.get("failure_layer") == "UNKNOWN":
            errors.append("UNKNOWN_FAILURE_LAYER_REQUIRES_LISTEN_OR_DIAGNOSIS")
        if errors:
            output["holds"].append({"defect_id": defect_id, "reasons": sorted(set(errors))})
            continue

        layer = defect["failure_layer"]
        repair = {
            "patch_id": "P003B_" + str(defect_id),
            "defect_id": defect_id,
            "question_class": defect["question_class"],
            "severity": defect["severity"],
            "failure_layer": layer,
            "action": ACTION_BY_LAYER[layer],
            "start_seconds": float(defect["start_seconds"]),
            "end_seconds": float(defect["end_seconds"]),
            "smallest_repair_scope": defect["smallest_repair_scope"],
            "minimal_fix": defect["minimal_fix"],
            "do_not_touch": defect["do_not_touch"],
            "regression_tests": defect["regression_tests"],
            "authorization": "SELECTIVE_REPAIR_ONLY",
            "release_effect": "NONE_UNTIL_REGRESSION_AND_HUMAN_RELISTEN",
        }
        output["repairs"].append(repair)

    if output["repairs"] and output["holds"]:
        output["status"] = "REPAIR_PLAN_READY_WITH_HOLDS"
    elif output["repairs"]:
        output["status"] = "REPAIR_PLAN_READY"
    elif output["holds"]:
        output["status"] = "HOLD"
    else:
        output["status"] = "NO_REPAIR_REQUESTED"

    dump(args.out, output)
    print(output["status"] + f" repairs={len(output['repairs'])} holds={len(output['holds'])}")
    return 0 if output["status"] in {"REPAIR_PLAN_READY", "REPAIR_PLAN_READY_WITH_HOLDS", "NO_REPAIR_REQUESTED"} else 4


if __name__ == "__main__":
    raise SystemExit(main())
