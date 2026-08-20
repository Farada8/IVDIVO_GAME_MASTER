#!/usr/bin/env python3
"""IVDIVO Audio Novel Studio — Audio Adaptation Plan validator v0.1.

Validates the missing bridge:
BOOK_INGEST -> AUDIO_ADAPTATION_PLAN -> SCENE_MAP -> SCENE_STATE_GRAPH seeds.

This module does not invent scenes. A reasoning stage/model creates the plan; this
validator makes the plan accountable to source authority and delivery mode.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

DELIVERY_MODES = {"NARRATED", "MULTI_VOICE", "DRAMATIZED", "FULL_AUDIO_DRAMA"}
TEXT_PROTECTION = {"EXACT_SOURCE", "LOCKED_TRANSLATION", "AUTHORIZED_ADAPTATION"}
DECISION_TYPES = {
    "NARRATE",
    "ACTOR_DIALOGUE",
    "NARRATOR_PLUS_ACTOR",
    "SOUND_SUPPORTED_SPOKEN",
    "ADAPT",
    "OMIT",
}


def load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def issue(out: List[Dict[str, Any]], severity: str, code: str, location: str, message: str) -> None:
    out.append({"severity": severity, "code": code, "location": location, "message": message})


def validate(plan: Dict[str, Any], source_units: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    mode = plan.get("delivery_mode")
    protection = plan.get("text_protection")

    if mode not in DELIVERY_MODES:
        issue(issues, "FATAL", "BAD_DELIVERY_MODE", "$", f"Unknown delivery_mode {mode!r}")
    if protection not in TEXT_PROTECTION:
        issue(issues, "FATAL", "BAD_TEXT_PROTECTION", "$", f"Unknown text_protection {protection!r}")

    source_hash = source_units.get("source_hash")
    if not source_hash or plan.get("source_hash") != source_hash:
        issue(issues, "FATAL", "SOURCE_HASH_MISMATCH", "$", "Plan source_hash does not match SOURCE_UNIT_MAP")

    units = source_units.get("units") or []
    valid_units = {u.get("unit_id"): u for u in units if u.get("unit_id")}
    scenes = plan.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        issue(issues, "FATAL", "NO_SCENES", "$.scenes", "Adaptation plan requires at least one scene")
        scenes = []

    seen_scene_ids = set()
    decisions_by_unit: Dict[str, List[Dict[str, Any]]] = {uid: [] for uid in valid_units}
    last_global_ordinal = -1

    for si, scene in enumerate(scenes):
        sloc = f"$.scenes[{si}]"
        scene_id = scene.get("scene_id")
        if not scene_id:
            issue(issues, "MAJOR", "SCENE_ID_MISSING", sloc, "scene_id required")
        elif scene_id in seen_scene_ids:
            issue(issues, "FATAL", "DUPLICATE_SCENE_ID", sloc, f"Duplicate scene_id {scene_id}")
        else:
            seen_scene_ids.add(scene_id)

        for field in ("chapter_id", "scene_objective", "dramatic_function", "listener_contract_seed", "decisions"):
            if field not in scene:
                issue(issues, "MAJOR", "SCENE_FIELD_MISSING", sloc, f"Missing {field}")

        decisions = scene.get("decisions") or []
        if not isinstance(decisions, list) or not decisions:
            issue(issues, "MAJOR", "SCENE_HAS_NO_DECISIONS", f"{sloc}.decisions", "Scene must map source units")
            continue

        for di, decision in enumerate(decisions):
            dloc = f"{sloc}.decisions[{di}]"
            uid = decision.get("source_unit_id")
            dtype = decision.get("decision_type")
            if uid not in valid_units:
                issue(issues, "FATAL", "UNKNOWN_SOURCE_UNIT", dloc, f"Unknown source_unit_id {uid!r}")
                continue
            decisions_by_unit.setdefault(uid, []).append(decision)

            if dtype not in DECISION_TYPES:
                issue(issues, "MAJOR", "BAD_DECISION_TYPE", dloc, f"Unknown decision_type {dtype!r}")

            source_unit = valid_units[uid]
            expected_hash = source_unit.get("text_sha256")
            if decision.get("source_text_sha256") != expected_hash:
                issue(issues, "FATAL", "SOURCE_UNIT_HASH_MISMATCH", dloc, f"Hash mismatch for {uid}")

            ordinal = int(source_unit.get("global_ordinal", 0))
            if ordinal < last_global_ordinal and not decision.get("shared_context", False):
                issue(issues, "MAJOR", "SOURCE_ORDER_REGRESSION", dloc, f"Source unit {uid} moves backwards without shared_context")
            last_global_ordinal = max(last_global_ordinal, ordinal)

            if protection in {"EXACT_SOURCE", "LOCKED_TRANSLATION"} and dtype in {"ADAPT", "OMIT"}:
                issue(issues, "FATAL", "UNAUTHORIZED_TEXT_CHANGE", dloc, f"{dtype} forbidden under {protection}")

            if dtype in {"ADAPT", "OMIT"}:
                diff = decision.get("adaptation_diff")
                if not isinstance(diff, dict) or not diff.get("approved"):
                    issue(issues, "FATAL", "ADAPTATION_DIFF_NOT_APPROVED", dloc, f"{dtype} requires approved adaptation_diff")
                else:
                    for f in ("source", "performance_version", "reason", "meaning_change"):
                        if f not in diff:
                            issue(issues, "MAJOR", "ADAPTATION_DIFF_FIELD_MISSING", dloc, f"adaptation_diff missing {f}")

            if dtype == "ACTOR_DIALOGUE" and not decision.get("speaker_ids"):
                issue(issues, "MAJOR", "ACTOR_DECISION_WITHOUT_SPEAKER", dloc, "ACTOR_DIALOGUE requires speaker_ids")

    for uid, mapped in decisions_by_unit.items():
        if not mapped:
            issue(issues, "FATAL", "SOURCE_UNIT_UNMAPPED", "$.scenes", f"Source unit {uid} has no adaptation decision")
        elif len(mapped) > 1 and not any(bool(d.get("shared_context")) for d in mapped):
            issue(issues, "MAJOR", "SOURCE_UNIT_MULTIMAPPED", "$.scenes", f"Source unit {uid} mapped multiple times without shared_context")

    counts = {"FATAL": 0, "MAJOR": 0, "MEDIUM": 0, "POLISH": 0}
    for x in issues:
        counts[x["severity"]] = counts.get(x["severity"], 0) + 1
    gate = "PASS" if counts["FATAL"] == 0 and counts["MAJOR"] == 0 else "FAIL"

    return {
        "schema": "IVDIVO_AUDIO_ADAPTATION_PLAN_VALIDATION_v1",
        "project_id": plan.get("project_id"),
        "source_hash": plan.get("source_hash"),
        "delivery_mode": mode,
        "text_protection": protection,
        "scene_count": len(scenes),
        "source_unit_count": len(valid_units),
        "mapped_source_unit_count": sum(1 for x in decisions_by_unit.values() if x),
        "gate": gate,
        "counts": counts,
        "issues": issues,
        "next_if_pass": "SCENE_STATE_GRAPH_SEED_COMPILATION",
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Validate IVDIVO Audio Adaptation Plan")
    p.add_argument("plan")
    p.add_argument("source_unit_map")
    p.add_argument("--output")
    a = p.parse_args()

    report = validate(load(Path(a.plan)), load(Path(a.source_unit_map)))
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if a.output:
        Path(a.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    raise SystemExit(0 if report["gate"] == "PASS" else 2)


if __name__ == "__main__":
    main()
