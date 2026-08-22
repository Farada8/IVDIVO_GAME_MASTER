#!/usr/bin/env python3
"""Guarded ElevenLabs Sound Effects canary renderer for ROOM917 E01 A01/A02.

This is intentionally NOT a production binder. It produces source candidates and
an evidence manifest only. Production binding remains downstream of normalization,
audition, loop/false-clue checks and sound_asset_binding_gate.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

API_KEY_ENV = "ELEVENLABS_API_KEY"
ENDPOINT = "https://api.elevenlabs.io/v1/sound-generation"
ALLOWED_COUNTS = {2, 4}
BALANCED_TWO = {"ROOM917_E01_A01_C01", "ROOM917_E01_A02_C01"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def select_requests(rows: list[dict], max_requests: int) -> list[dict]:
    if max_requests == 4:
        if len(rows) < 4:
            raise SystemExit("Plan has fewer than four requests")
        return rows[:4]
    chosen = [row for row in rows if row.get("request_id") in BALANCED_TWO]
    if len(chosen) != 2:
        raise SystemExit("Balanced two-request canary IDs are missing from plan")
    return chosen


def post_sound(key: str, row: dict, output_format: str) -> tuple[bytes, dict[str, str]]:
    query = urllib.parse.urlencode({"output_format": output_format})
    body = json.dumps(
        {
            "text": row["text"],
            "loop": bool(row.get("loop", True)),
            "duration_seconds": float(row["duration_seconds"]),
            "prompt_influence": float(row.get("prompt_influence", 0.55)),
            "model_id": "eleven_text_to_sound_v2",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT + "?" + query,
        data=body,
        method="POST",
        headers={
            "xi-api-key": key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            audio = response.read()
            headers = {k.lower(): v for k, v in response.headers.items()}
            return audio, headers
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ElevenLabs sound-generation HTTP {exc.code}: {detail}") from exc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--max-requests", type=int, choices=sorted(ALLOWED_COUNTS), required=True)
    ap.add_argument("--confirm-spend", required=True)
    ap.add_argument("--output-format", default="mp3_44100_128")
    args = ap.parse_args()

    if args.confirm_spend != "YES":
        raise SystemExit("Paid sound canary blocked: --confirm-spend must be exactly YES")
    key = os.getenv(API_KEY_ENV)
    if not key:
        raise SystemExit(f"Paid sound canary blocked: {API_KEY_ENV} is absent")

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan.get("status") != "DRY_PLAN_ONLY__NO_PROVIDER_DISPATCH_AUTHORIZED":
        raise SystemExit("Unexpected plan status; refuse to dispatch")
    provider = plan.get("provider") or {}
    if provider.get("model_id") != "eleven_text_to_sound_v2":
        raise SystemExit("Unexpected sound model")
    if provider.get("loop") is not True or float(provider.get("duration_seconds", 0)) != 30.0:
        raise SystemExit("This canary is hard-bound to 30-second looping candidates")

    rows = plan.get("requests") or []
    selected = select_requests(rows, args.max_requests)
    args.outdir.mkdir(parents=True, exist_ok=True)

    evidence = {
        "schema_version": "ivdivo.room917_sfx_canary_evidence/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "provider": "ElevenLabs",
        "model_id": "eleven_text_to_sound_v2",
        "output_format": args.output_format,
        "requested_count": len(selected),
        "paid_dispatch": True,
        "secret_persisted": False,
        "production_binding_authorized": False,
        "candidates": [],
    }

    for row in selected:
        audio, headers = post_sound(key, row, args.output_format)
        if len(audio) < 1024:
            raise RuntimeError(f"Suspiciously small audio response for {row['request_id']}: {len(audio)} bytes")
        filename = f"{row['candidate_id']}_{args.output_format}.mp3"
        path = args.outdir / filename
        path.write_bytes(audio)
        evidence["candidates"].append(
            {
                "request_id": row["request_id"],
                "asset_id": row["asset_id"],
                "candidate_id": row["candidate_id"],
                "provider_source_filename": filename,
                "provider_source_sha256": sha256_bytes(audio),
                "provider_source_size_bytes": len(audio),
                "duration_seconds_requested": row["duration_seconds"],
                "loop_requested": row["loop"],
                "prompt_influence": row.get("prompt_influence"),
                "text_sha256": hashlib.sha256(row["text"].encode("utf-8")).hexdigest(),
                "provider_character_cost_header": headers.get("character-cost"),
                "provider_request_id_header": headers.get("request-id") or headers.get("x-request-id"),
                "audition_status": "HOLD_PENDING_LISTEN",
                "normalization_status": "NOT_RUN",
                "loop_seam_status": "HOLD",
                "false_clue_audit_status": "HOLD",
                "mono_status": "HOLD",
                "phone_proxy_status": "HOLD",
                "production_binding_authorized": False,
            }
        )

    evidence_path = args.outdir / "ROOM917_E01_A01_A02_SFX_CANARY_EVIDENCE.json"
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "CANDIDATES_RENDERED_NOT_BOUND", "count": len(selected), "evidence": str(evidence_path)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
