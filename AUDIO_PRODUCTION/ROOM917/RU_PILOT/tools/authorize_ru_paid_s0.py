#!/usr/bin/env python3
"""Create final ROOM917 RU S0 paid-canary bindings from an approved candidate.

IMPORTANT: this program makes no ElevenLabs/provider calls and spends no credits.
It only emits the authorization artifact consumed later by the separately
manual-dispatched paid S0 workflow.

The caller must supply all explicit confirmation inputs. No implicit or default
spend authorization exists.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
SCOPE_PHRASE = "ROOM917_RU_S0_CANARY_ONLY"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit("FAIL_PAID_S0_AUTHORIZATION: " + message)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bindings-candidate", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--confirm-spend", required=True, help="must be exactly YES")
    ap.add_argument("--scope", required=True, help=f"must be exactly {SCOPE_PHRASE}")
    ap.add_argument("--max-blocks", type=int, required=True, choices=(4, 6))
    ap.add_argument("--authorization-note", required=True)
    args = ap.parse_args()

    if not args.bindings_candidate.exists():
        fail(f"bindings candidate missing: {args.bindings_candidate}")
    if args.confirm_spend != "YES":
        fail("--confirm-spend must be exactly YES")
    if args.scope != SCOPE_PHRASE:
        fail(f"--scope must be exactly {SCOPE_PHRASE}")
    if not args.authorization_note.strip():
        fail("--authorization-note must be non-empty")

    candidate = load(args.bindings_candidate)
    if candidate.get("status") != "READY_FOR_PAID_CANARY_AUTHORIZATION":
        fail("bindings candidate status must be READY_FOR_PAID_CANARY_AUTHORIZATION")
    if candidate.get("founder_paid_canary_authorized") is not False:
        fail("input candidate must not already contain founder paid authorization")
    if candidate.get("paid_s0_authorized") is not False:
        fail("input candidate must not already claim paid S0 authorization")
    if candidate.get("cast_lock") is not False:
        fail("input candidate must not claim CAST LOCK")
    if candidate.get("full_episode_render_allowed") is not False:
        fail("input candidate must not allow full episode render")
    if candidate.get("all_pair_tests") != "PASS":
        fail("all_pair_tests must PASS")
    if candidate.get("pronunciation_gate") != "PASS":
        fail("pronunciation_gate must PASS")
    if candidate.get("founder_credibility_gate") != "PASS":
        fail("founder_credibility_gate must PASS")

    roles = candidate.get("roles") or {}
    if set(roles) != set(ROLES):
        fail("bindings candidate must contain exactly ELENA/JULIAN/MINA/CATE")
    voice_ids: list[str] = []
    for role in ROLES:
        row = roles.get(role) or {}
        voice_id = str(row.get("voice_id") or "")
        if not voice_id:
            fail(f"{role}: voice_id missing")
        if row.get("preview_listen") != "PASS":
            fail(f"{role}: preview_listen must PASS")
        if row.get("provider_identity_check") != "PASS":
            fail(f"{role}: provider_identity_check must PASS")
        voice_ids.append(voice_id)
    if len(set(voice_ids)) != len(ROLES):
        fail("voice IDs must be unique across four roles")

    out = dict(candidate)
    out["schema_version"] = "ivdivo.room917_ru_s0_native_bindings/1.2"
    out["status"] = "PAID_S0_AUTHORIZED"
    out["authorization"] = {
        "authorized_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_bindings_candidate_path": str(args.bindings_candidate),
        "source_bindings_candidate_sha256": sha256(args.bindings_candidate),
        "scope": SCOPE_PHRASE,
        "max_blocks": args.max_blocks,
        "authorization_note": args.authorization_note.strip(),
        "provider_call_made": False,
        "provider_spend_made": False,
        "workflow_auto_dispatched": False,
    }
    out["founder_paid_canary_authorized"] = True
    out["paid_s0_authorized"] = True
    out["authorized_max_blocks"] = args.max_blocks
    out["cast_lock"] = False
    out["full_episode_render_allowed"] = False
    out["next"] = "MANUAL_DISPATCH_ROOM917_RU_S0_CANARY_WITH_confirm_spend_YES_AND_AUTHORIZED_max_blocks"
    out["hard_rules"] = [
        "AUTHORIZATION_ARTIFACT_DOES_NOT_ITSELF_SPEND_CREDITS",
        "PAID_WORKFLOW_MUST_STILL_BE_MANUALLY_DISPATCHED",
        "WORKFLOW_max_blocks_MUST_NOT_EXCEED_authorized_max_blocks",
        "CAST_LOCK_REMAINS_FALSE",
        "FULL_E01_REMAINS_FORBIDDEN",
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "authorized_max_blocks": args.max_blocks,
        "provider_call_made": False,
        "provider_spend_made": False,
        "workflow_auto_dispatched": False,
        "cast_lock": False,
        "full_episode_render_allowed": False,
        "out": str(args.out),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
