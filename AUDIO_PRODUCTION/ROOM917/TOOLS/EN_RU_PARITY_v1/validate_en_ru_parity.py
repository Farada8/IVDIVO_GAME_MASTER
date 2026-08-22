#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(report: dict[str, Any], code: str, detail: str) -> None:
    report["failures"].append({"code": code, "detail": detail})


def main() -> int:
    ap = argparse.ArgumentParser(description="ROOM917 E01 English/Russian production parity gate")
    ap.add_argument("--control", required=True)
    ap.add_argument("--en-contract", required=True)
    ap.add_argument("--ru-contract", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    control = load(Path(args.control))
    en = load(Path(args.en_contract))
    ru = load(Path(args.ru_contract))

    report: dict[str, Any] = {
        "schema_version": "ivdivo.room917_en_ru_parity_report/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "status": "FAIL",
        "checks": [],
        "failures": [],
    }

    if control.get("story_status") != "LOCKED" or en.get("story_status") != "LOCKED":
        fail(report, "STORY_LOCK", "EN/control must remain story-locked")
    else:
        report["checks"].append("STORY_LOCK_PASS")

    control_buses = control.get("mix_and_master_parity", {}).get("buses") or []
    en_buses = en.get("critical_mix_buses") or []
    ru_buses = ru.get("buses") or []
    if control_buses != en_buses or control_buses != ru_buses:
        fail(report, "BUS_PARITY", f"control={control_buses} en={en_buses} ru={ru_buses}")
    else:
        report["checks"].append("BUS_PARITY_PASS")

    shared = control.get("shared_language_neutral_story_sounds") or []
    ru_shared = ru.get("shared_language_neutral_assets") or []
    missing_ru = sorted(set(shared) - set(ru_shared))
    extra_ru = sorted(set(ru_shared) - set(shared))
    if missing_ru or extra_ru:
        fail(report, "SHARED_ASSET_IDENTITY", f"missing_ru={missing_ru} extra_ru={extra_ru}")
    else:
        report["checks"].append("SHARED_ASSET_IDENTITY_PASS")

    en_clue = en.get("clue_safe_law", {})
    mix = control.get("mix_and_master_parity", {})
    required_true = {
        "clue_bus_never_ducked_by_music_or_ambience": True,
        "mono_survival_required": True,
    }
    for key, expected in required_true.items():
        if en_clue.get(key) is not expected or mix.get(key) is not expected:
            fail(report, "CLUE_SAFE_PARITY", f"{key} must be true in EN and shared control")
    if not any(f["code"] == "CLUE_SAFE_PARITY" for f in report["failures"]):
        report["checks"].append("CLUE_SAFE_PARITY_PASS")

    if not ru.get("mix_qc", {}).get("must_pass"):
        fail(report, "RU_MIX_QC", "RU mix_qc.must_pass must be present")
    else:
        report["checks"].append("RU_MIX_QC_PRESENT_PASS")

    if en.get("master", {}).get("rerender_forbidden") is not True:
        fail(report, "EN_RERENDER_GUARD", "Existing EN E01 master must not be globally rerendered by default")
    else:
        report["checks"].append("EN_RERENDER_GUARD_PASS")

    if ru.get("dialogue", {}).get("full_episode_single_pass_forbidden") is not True:
        fail(report, "RU_FULL_PASS_GUARD", "RU full-episode single-pass render must remain forbidden")
    else:
        report["checks"].append("RU_FULL_PASS_GUARD_PASS")

    if ru.get("dialogue", {}).get("selective_regeneration_only") is not True:
        fail(report, "RU_SELECTIVE_REGEN", "RU dialogue repair must remain selective")
    else:
        report["checks"].append("RU_SELECTIVE_REGEN_PASS")

    if en.get("preserve", {}).get("no_blanket_silence_fill") is not True:
        fail(report, "EN_SILENCE_GUARD", "EN blanket silence fill must remain forbidden")
    else:
        report["checks"].append("EN_SILENCE_GUARD_PASS")

    if control.get("shared_scene_rules", {}).get("scene_1", {}).get("music") != "NONE":
        fail(report, "SCENE1_MUSIC", "Scene 1 must stay unscored in shared parity control")
    if control.get("shared_scene_rules", {}).get("scene_2", {}).get("music") != "NONE":
        fail(report, "SCENE2_MUSIC", "Scene 2 must stay unscored in shared parity control")
    if ru.get("scene_contracts", {}).get("SCENE_1", {}).get("music") != "NONE":
        fail(report, "RU_SCENE1_MUSIC", "RU Scene 1 must remain unscored")
    if ru.get("scene_contracts", {}).get("SCENE_2", {}).get("music") != "NONE":
        fail(report, "RU_SCENE2_MUSIC", "RU Scene 2 must remain unscored")
    if not any(f["code"] in {"SCENE1_MUSIC", "SCENE2_MUSIC", "RU_SCENE1_MUSIC", "RU_SCENE2_MUSIC"} for f in report["failures"]):
        report["checks"].append("EARLY_MUSIC_EXCLUSION_PASS")

    evidence_order = control.get("shared_scene_rules", {}).get("scene_3", {}).get("required_evidence_order") or []
    ru_order = ru.get("scene_contracts", {}).get("SCENE_3", {}).get("locked_evidence_order") or []
    if evidence_order != ru_order:
        fail(report, "SCENE3_CAUSAL_ORDER", "RU Scene 3 evidence order drifted from shared bilingual control")
    else:
        report["checks"].append("SCENE3_CAUSAL_ORDER_PASS")

    if control.get("shared_sound_policy", {}).get("pitch_or_signature_drift_for_locale") is not False:
        fail(report, "LOCALE_SOUND_DRIFT", "Language-neutral clue signature drift must remain forbidden")
    else:
        report["checks"].append("LOCALE_SOUND_DRIFT_GUARD_PASS")

    if control.get("current_execution", {}).get("paid_ru_s0_not_authorized_by_this_control_file") is not True:
        fail(report, "SPEND_BOUNDARY", "Parity control must not authorize paid RU synthesis")
    else:
        report["checks"].append("SPEND_BOUNDARY_PASS")

    report["status"] = "PASS" if not report["failures"] else "FAIL"
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["status"])
    if report["failures"]:
        for item in report["failures"]:
            print(f"{item['code']}: {item['detail']}")
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
