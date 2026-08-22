#!/usr/bin/env python3
"""Compile ROOM917 RU S0 runtime canary bundle from authorized pre-canary bindings.

The checked-in S0 text bundle is TEXT/TEST GEOMETRY ONLY. Historical public
voice IDs are diagnostic and may never reach paid production. The bindings
artifact is explicitly canary-only and must not claim acting evidence or CAST LOCK.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
DIAGNOSTIC_IDS = {
    "21m00Tcm4TlvDq8ikWAM": "ELENA",
    "pNInz6obpgDQGcFmaJgB": "JULIAN",
    "XrExE9yKIg1WjnnlVkGX": "MINA",
    "EXAVITQu4vr4xnSDxMaL": "CATE",
}
S0_ALLOWED_OUTPUT_FORMATS = {"mp3_44100_128", "mp3_44100_192"}
S0_DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL_NATIVE_BINDING_GATE: " + message)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template-bundle", type=Path, required=True)
    ap.add_argument("--bindings", type=Path, required=True)
    ap.add_argument("--provider-snapshot", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    for path in (args.template_bundle, args.bindings, args.provider_snapshot):
        require(path.exists(), f"missing required file: {path}")

    template = load(args.template_bundle)
    bindings = load(args.bindings)
    snapshot = load(args.provider_snapshot)

    require(template.get("model_id") == "eleven_v3", "template model must be eleven_v3")
    require(bindings.get("status") == "PAID_S0_AUTHORIZED", "bindings status must be PAID_S0_AUTHORIZED")
    require(bindings.get("founder_paid_canary_authorized") is True, "founder_paid_canary_authorized must be true")
    require(bindings.get("paid_s0_authorized") is True, "paid_s0_authorized must be true")
    require(bindings.get("pre_canary_binding_gate") == "PASS", "pre_canary_binding_gate must PASS")
    require(bindings.get("canary_binding_only") is True, "bindings must be canary_binding_only=true")
    require(bindings.get("acting_evidence_complete") is False, "S0 bindings must not claim acting evidence complete")
    require(bindings.get("cast_lock") is False, "S0 bindings must not claim CAST LOCK")
    require(bindings.get("full_episode_render_allowed") is False, "S0 bindings must not allow full episode render")
    require(bindings.get("provider_snapshot_sha256") == digest(args.provider_snapshot), "binding snapshot hash mismatch")

    query = snapshot.get("query_policy") or {}
    require(query.get("language") == "ru", "provider snapshot is not language=ru")
    require(query.get("category") == "professional", "provider snapshot is not category=professional")
    require(int(query.get("min_notice_period_days") or 0) >= 365, "provider snapshot notice period policy <365 days")

    candidates = {str(v.get("voice_id")): v for v in snapshot.get("candidates") or [] if v.get("voice_id")}
    require(bool(candidates), "provider snapshot contains no native RU candidates")

    bound: dict[str, str] = {}
    role_rows = bindings.get("roles") or {}
    for role in ROLES:
        row = role_rows.get(role) or {}
        voice_id = str(row.get("voice_id") or "")
        require(bool(voice_id), f"{role}: voice_id missing")
        require(voice_id not in DIAGNOSTIC_IDS, f"{role}: diagnostic legacy/default ID forbidden")
        require(row.get("preview_listen") == "PASS", f"{role}: preview_listen must be PASS")
        require(row.get("provider_identity_check") == "PASS", f"{role}: provider_identity_check must be PASS")
        require(row.get("provider_durability_check") == "PASS", f"{role}: provider_durability_check must be PASS")
        require(row.get("plausible_for_canary") == "PASS", f"{role}: plausible_for_canary must be PASS")
        require(row.get("canary_binding_only") is True, f"{role}: role binding must be canary-only")
        cand = candidates.get(voice_id)
        require(cand is not None, f"{role}: voice_id absent from sealed native provider snapshot")
        require(cand.get("ru_verified") is True, f"{role}: provider candidate is not ru_verified")
        disable = cand.get("disable_at_unix")
        require(disable in (None, 0, "", "0"), f"{role}: provider candidate has disable_at_unix={disable}")
        bound[role] = voice_id

    runtime = json.loads(json.dumps(template, ensure_ascii=False))
    runtime["schema_version"] = "ivdivo.room917_ru_s0_native_runtime_bundle/2.0"
    runtime["status"] = "NATIVE_RU_BOUND_PAID_S0_RUNTIME"
    runtime["cast_source"] = str(args.bindings)
    runtime["canary_binding_only"] = True
    runtime["acting_evidence_complete"] = False
    runtime["cast_lock"] = False
    runtime["provider_snapshot"] = {
        "path": str(args.provider_snapshot),
        "sha256": digest(args.provider_snapshot),
        "query_policy": query,
    }

    for block in runtime.get("blocks") or []:
        fmt = str(block.get("output_format") or S0_DEFAULT_OUTPUT_FORMAT)
        require(fmt in S0_ALLOWED_OUTPUT_FORMATS, f"{block.get('block_id')}: unsupported S0 audition output_format={fmt}")
        block["output_format"] = fmt

        if block.get("voice_id"):
            old = str(block["voice_id"])
            role = DIAGNOSTIC_IDS.get(old)
            require(role is not None, f"{block.get('block_id')}: unknown template voice ID {old}")
            block["voice_id"] = bound[role]
        for turn in block.get("turns") or []:
            old = str(turn.get("voice_id") or "")
            role = DIAGNOSTIC_IDS.get(old)
            require(role is not None, f"{block.get('block_id')}: unknown turn template voice ID {old}")
            turn["voice_id"] = bound[role]

        if isinstance(block.get("voice_settings"), dict):
            vs = block["voice_settings"]
            vs.pop("similarity_boost", None)
            vs.pop("use_speaker_boost", None)
            vs.pop("speed", None)
            if "style" in vs:
                vs["style"] = 0.0

    runtime["runtime_voice_bindings"] = bound
    runtime["eleven_v3_setting_policy"] = {
        "allowed_for_this_canary": ["stability", "style"],
        "style_fixed": 0.0,
        "removed_as_unavailable_for_v3": ["similarity_boost", "use_speaker_boost", "speed"],
        "comparison_rule": "same meaningful settings within each A/B/C round"
    }
    runtime["audition_output_policy"] = {
        "allowed_formats": sorted(S0_ALLOWED_OUTPUT_FORMATS),
        "default": S0_DEFAULT_OUTPUT_FORMAT,
        "final_master_format_is_separate": True,
        "final_master_target": "48K_24BIT_WAV_AFTER_CAST_LOCK_AND_ASSEMBLY"
    }
    runtime["hard_rules"] = list(runtime.get("hard_rules") or []) + [
        "NATIVE_RU_PROVIDER_SNAPSHOT_MATCH_REQUIRED",
        "DIAGNOSTIC_PUBLIC_IDS_FORBIDDEN",
        "S0_AUDITION_OUTPUT_FORMAT_ALLOWLIST_REQUIRED",
        "ELEVEN_V3_UNAVAILABLE_SETTINGS_STRIPPED",
        "PRE_CANARY_BINDING_IS_NOT_CAST_LOCK",
        "HUMAN_LISTEN_REQUIRED_AFTER_AUDIO_EXISTS",
        "FULL_E01_RENDER_FORBIDDEN_AT_S0"
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(runtime, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS_NATIVE_BINDING_GATE",
        "out": str(args.out),
        "roles": bound,
        "provider_snapshot_sha256": runtime["provider_snapshot"]["sha256"],
        "canary_binding_only": True,
        "cast_lock": False,
        "audition_formats": sorted(S0_ALLOWED_OUTPUT_FORMATS),
        "v3_removed_settings": runtime["eleven_v3_setting_policy"]["removed_as_unavailable_for_v3"]
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
