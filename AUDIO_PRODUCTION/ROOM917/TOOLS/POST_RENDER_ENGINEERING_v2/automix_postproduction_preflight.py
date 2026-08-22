#!/usr/bin/env python3
"""Fail-closed production preflight for ROOM917 E01 AutoMix/postproduction.

This gate does not render, approve assets, invent timing, or grant release authority.
It verifies that already-approved production evidence is structurally compatible
with the actual upstream ROOM917 gates before handoff to selective post-render work.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

PASS = "PASS_AUTOMIX_EXECUTION_READY"
HOLD = "HOLD_AUTOMIX_EXECUTION"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
BINDING_REPORT_SCHEMA = "room917.sound_asset_binding_gate/1.1"
SEMANTIC_TIMING_SCHEMA = "room917.e01_sound_asset_resolved_timing/1.1"


def _gate(name: str, ok: bool, reasons: List[str]) -> Dict[str, Any]:
    return {"gate": name, "status": "PASS" if ok else "HOLD", "reasons": reasons}


def _as_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _exact_set(value: Any, expected: List[str]) -> bool:
    return isinstance(value, list) and len(value) == len(expected) and set(value) == set(expected)


def evaluate(contract: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
    gates: List[Dict[str, Any]] = []

    locale = candidate.get("locale")
    locale_policy = contract.get("locale_policy", {}).get(locale, {}) if locale else {}
    locale_reasons: List[str] = []
    if not locale_policy:
        locale_reasons.append("locale_missing_or_not_authorized")
    elif locale_policy.get("automix_allowed_when_all_gates_pass") is not True:
        locale_reasons.append(f"locale_{locale}_automix_not_authorized_by_current_policy")
    gates.append(_gate("LOCALE_AUTHORITY", not locale_reasons, locale_reasons))

    mode_reasons: List[str] = []
    if candidate.get("mode") != "POST_RENDER_PATCH":
        mode_reasons.append("unsupported_or_missing_mode__expected_POST_RENDER_PATCH")
    gates.append(_gate("MODE", not mode_reasons, mode_reasons))

    voice = candidate.get("voice_manifest") if isinstance(candidate.get("voice_manifest"), dict) else {}
    voice_contract = contract.get("voice_gate", {})
    voice_reasons: List[str] = []
    allowed_manifest = set(_as_list(voice_contract.get("manifest_status_allowed")))
    allowed_source = set(_as_list(voice_contract.get("source_status_allowed")))
    if voice.get("status") not in allowed_manifest:
        voice_reasons.append("voice_manifest_not_PASS_or_LOCKED")
    if voice.get("fixture_only") is not False:
        voice_reasons.append("voice_manifest_fixture_or_unproven")
    if voice.get("production_sources") is not True:
        voice_reasons.append("voice_manifest_not_declared_production_sources")
    sources = _as_list(voice.get("sources"))
    if not sources:
        voice_reasons.append("voice_sources_missing")
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            voice_reasons.append(f"voice_source_{index}_invalid")
            continue
        if source.get("approval_status") not in allowed_source:
            voice_reasons.append(f"voice_source_{index}_not_PASS_or_LOCKED")
        if voice_contract.get("sha256_required_per_source") is True and not SHA256_RE.match(str(source.get("sha256", ""))):
            voice_reasons.append(f"voice_source_{index}_sha256_missing_or_invalid")
    gates.append(_gate("VOICE_PROVENANCE", not voice_reasons, voice_reasons))

    # Require the real upstream binder report shape, not a manually summarized list.
    sound = candidate.get("sound_binding_report") if isinstance(candidate.get("sound_binding_report"), dict) else {}
    sound_contract = contract.get("sound_asset_gate", {})
    sound_reasons: List[str] = []
    if sound.get("schema_version") != BINDING_REPORT_SCHEMA:
        sound_reasons.append("sound_binding_report_schema_not_current_binder")
    if sound.get("status") != sound_contract.get("binding_report_status_required", "PASS"):
        sound_reasons.append("sound_binding_report_not_PASS")
    if sound.get("renderer_bindings_atomic") is not True:
        sound_reasons.append("sound_binding_report_not_atomic")
    if sound.get("renderer_bindings_complete_for_requested_set") is not True:
        sound_reasons.append("sound_binding_requested_set_not_complete")
    if sound.get("renderer_bindings_suppressed_on_hold") is not False:
        sound_reasons.append("sound_binding_report_indicates_hold_or_suppression")
    if sound.get("request_set_errors") not in ([], None):
        sound_reasons.append("sound_binding_request_set_errors_present")

    requested = _as_list(sound.get("requested_asset_ids"))
    emitted = _as_list(sound.get("renderer_bindings_emitted"))
    if not requested or len(requested) != len(set(requested)):
        sound_reasons.append("sound_requested_asset_ids_missing_or_duplicated")
    if not _exact_set(emitted, requested):
        sound_reasons.append("sound_renderer_emitted_set_not_exact_requested_set")
    required_current = set(_as_list(sound_contract.get("required_asset_ids_for_current_patch")))
    if required_current and not required_current.issubset(set(requested)):
        sound_reasons.append("sound_current_patch_required_assets_missing")

    rows = _as_list(sound.get("rows"))
    row_ids = []
    if not rows:
        sound_reasons.append("sound_binding_rows_missing")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            sound_reasons.append(f"sound_binding_row_{index}_invalid")
            continue
        row_ids.append(row.get("asset_id"))
        if row.get("status") != sound_contract.get("every_requested_binding_status_required", "PASS"):
            sound_reasons.append(f"sound_binding_row_{index}_not_PASS")
    if rows and not _exact_set(row_ids, requested):
        sound_reasons.append("sound_binding_rows_do_not_exactly_cover_requested_set")
    gates.append(_gate("SOUND_ASSET_BINDING", not sound_reasons, sound_reasons))

    # Production timing must come from the atomic semantic resolver output.
    timing = candidate.get("timing") if isinstance(candidate.get("timing"), dict) else {}
    timing_contract = contract.get("timing_gate", {})
    timing_reasons: List[str] = []
    if timing.get("schema_version") != SEMANTIC_TIMING_SCHEMA:
        timing_reasons.append("timing_schema_not_current_semantic_resolver")
    if timing.get("status") != "PASS" or timing.get("production_timing_ready") is not True:
        timing_reasons.append("semantic_timing_not_complete_PASS")
    if timing.get("holds") not in ([], None):
        timing_reasons.append("semantic_timing_holds_present")
    if timing.get("errors") not in ([], None):
        timing_reasons.append("semantic_timing_errors_present")
    timing_requested = _as_list(timing.get("requested_asset_ids"))
    production_resolved = timing.get("production_resolved") if isinstance(timing.get("production_resolved"), dict) else {}
    if not timing_requested or len(timing_requested) != len(set(timing_requested)):
        timing_reasons.append("semantic_timing_requested_set_missing_or_duplicated")
    if set(production_resolved) != set(timing_requested):
        timing_reasons.append("semantic_timing_production_set_not_complete")
    allowed_timing_sources = set(_as_list(timing_contract.get("allowed_grades")))
    for aid, row in production_resolved.items():
        events = _as_list(row.get("events")) if isinstance(row, dict) else []
        if not events:
            timing_reasons.append(f"semantic_timing_{aid}_events_missing")
        for event in events:
            if not isinstance(event, dict) or event.get("source_status") not in allowed_timing_sources:
                timing_reasons.append(f"semantic_timing_{aid}_source_not_allowed")
    gates.append(_gate("LIVE_TIMING", not timing_reasons, timing_reasons))

    silence = candidate.get("protected_silence") if isinstance(candidate.get("protected_silence"), dict) else {}
    silence_reasons: List[str] = []
    if silence.get("resolved_from_same_live_timing") is not True:
        silence_reasons.append("protected_silence_not_resolved_from_same_live_timing")
    if silence.get("post_fx_sample_exact_mask") is not True:
        silence_reasons.append("post_fx_sample_exact_mask_missing")
    if silence.get("silence_removal") is not False:
        silence_reasons.append("silence_removal_enabled_or_unknown")
    if silence.get("reverb_tail_invasion") is not False:
        silence_reasons.append("reverb_tail_invasion_enabled_or_unknown")
    gates.append(_gate("PROTECTED_SILENCE", not silence_reasons, silence_reasons))

    bus_contract = contract.get("buses", {})
    expected_buses = _as_list(bus_contract.get("required_exact_set"))
    bus_reasons: List[str] = []
    if not _exact_set(candidate.get("buses"), expected_buses):
        bus_reasons.append("bus_set_does_not_match_required_exact_set")
    gates.append(_gate("BUS_TOPOLOGY", not bus_reasons, bus_reasons))

    duck = candidate.get("ducking") if isinstance(candidate.get("ducking"), dict) else {}
    duck_contract = contract.get("ducking", {})
    duck_reasons: List[str] = []
    if not _exact_set(duck.get("targets"), _as_list(duck_contract.get("allowed_targets_exact"))):
        duck_reasons.append("duck_targets_must_be_exactly_AMBIENCE_and_MUSIC")
    if not _exact_set(duck.get("immune"), _as_list(duck_contract.get("immune_required"))):
        duck_reasons.append("duck_immune_set_must_be_exactly_DIALOGUE_and_CLUE_SFX")
    if duck.get("event_aware") is not True:
        duck_reasons.append("ducking_not_event_aware")
    gates.append(_gate("DUCKING", not duck_reasons, duck_reasons))

    tel_contract = contract.get("cate_telephone_chain", {})
    telephone_events = _as_list(candidate.get("telephone_events"))
    tel_reasons: List[str] = []
    if not telephone_events:
        tel_reasons.append("cate_telephone_event_missing_for_E01")
    required_tel = {
        "speaker": tel_contract.get("speaker_exact"),
        "clean_human_source": tel_contract.get("clean_human_source_required"),
        "hpf_hz": tel_contract.get("hpf_hz"),
        "lpf_hz": tel_contract.get("lpf_hz"),
        "reverb": tel_contract.get("reverb"),
        "mono_core": tel_contract.get("mono_core"),
        "pitch_shift": tel_contract.get("pitch_shift"),
        "stereo_widening": tel_contract.get("stereo_widening"),
        "ghost_processing": tel_contract.get("ghost_processing"),
    }
    for index, event in enumerate(telephone_events):
        if not isinstance(event, dict):
            tel_reasons.append(f"telephone_event_{index}_invalid")
            continue
        for key, expected in required_tel.items():
            if event.get(key) != expected:
                tel_reasons.append(f"telephone_event_{index}_{key}_mismatch")
    gates.append(_gate("CATE_TELEPHONE_CHAIN", not tel_reasons, tel_reasons))

    master_contract = contract.get("post_render_patch_mode", {})
    master = candidate.get("master") if isinstance(candidate.get("master"), dict) else {}
    master_reasons: List[str] = []
    if master_contract.get("verified_master_bytes_required") is True and master.get("verified_bytes") is not True:
        master_reasons.append("exact_master_bytes_not_verified")
    expected_master_sha = str(master_contract.get("expected_master_sha256", ""))
    if not SHA256_RE.match(str(master.get("sha256", ""))):
        master_reasons.append("master_sha256_missing_or_invalid")
    elif expected_master_sha and master.get("sha256") != expected_master_sha:
        master_reasons.append("master_sha256_does_not_match_current_authority")
    gates.append(_gate("MASTER_IDENTITY", not master_reasons, master_reasons))

    failures = [g for g in gates if g["status"] != "PASS"]
    return {
        "schema_version": "ivdivo.room917_automix_preflight_result/1.1",
        "project": contract.get("project", "ROOM917"),
        "episode": contract.get("episode", "E01"),
        "status": PASS if not failures else HOLD,
        "release_authority": False,
        "render_authorized": not failures,
        "gates": gates,
        "failed_gates": [g["gate"] for g in failures],
        "reasons": [reason for g in failures for reason in g["reasons"]],
        "next": (
            "HAND_OFF_TO_EXISTING_SELECTIVE_POST_RENDER_CHAIN__HUMAN_P003B_STILL_REQUIRED"
            if not failures
            else "REPAIR_OR_SUPPLY_ONLY_THE_FAILED_EVIDENCE_LAYER__DO_NOT_RENDER"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    candidate = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = evaluate(contract, candidate)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(result["status"])
    if result["reasons"]:
        for reason in result["reasons"]:
            print(f"- {reason}")
    return 0 if result["status"] == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
