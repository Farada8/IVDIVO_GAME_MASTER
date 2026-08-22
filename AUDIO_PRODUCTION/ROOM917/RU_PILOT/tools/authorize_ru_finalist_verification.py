#!/usr/bin/env python3
"""Authorize bounded ROOM917 RU finalist verification.

No provider call. No credits spent. The authorization must exactly match the
coverage-minimal finalist plan; silent extra blocks are forbidden.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

SCOPE = "ROOM917_RU_FINALIST_VERIFICATION_ONLY"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(msg: str) -> None:
    raise SystemExit("FAIL_FINALIST_AUTHORIZATION: " + msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--confirm-spend", required=True)
    ap.add_argument("--scope", required=True)
    ap.add_argument("--max-blocks", type=int, required=True, choices=(6, 7, 8))
    ap.add_argument("--authorization-note", required=True)
    args = ap.parse_args()

    if not args.plan.exists():
        fail(f"plan missing: {args.plan}")
    if args.confirm_spend != "YES":
        fail("--confirm-spend must be exactly YES")
    if args.scope != SCOPE:
        fail(f"--scope must be exactly {SCOPE}")
    if not args.authorization_note.strip():
        fail("--authorization-note must be non-empty")

    plan = load(args.plan)
    if plan.get("status") != "READY_FOR_FINALIST_SPEND_AUTHORIZATION":
        fail("plan status must be READY_FOR_FINALIST_SPEND_AUTHORIZATION")
    if plan.get("provider_call_made") is not False or plan.get("provider_spend_made") is not False:
        fail("plan must be zero-provider-call zero-spend")
    if plan.get("cast_lock") is not False or plan.get("full_e01_render_allowed") is not False:
        fail("plan cannot grant CAST LOCK or full E01")
    required = int(plan.get("required_block_count") or 0)
    blocks = plan.get("blocks") or []
    ids = plan.get("selected_block_ids") or []
    if required not in (6, 7, 8):
        fail(f"unexpected required_block_count={required}")
    if len(blocks) != required or len(ids) != required:
        fail("plan block count does not match required_block_count")
    if len(set(ids)) != required:
        fail("plan selected_block_ids contain duplicates")
    if args.max_blocks != required:
        fail(f"authorized max must exactly equal plan requirement {required}; got {args.max_blocks}")

    out = dict(plan)
    out["schema_version"] = "ivdivo.room917_ru_finalist_verification_authorization/1.0"
    out["status"] = "PAID_FINALIST_VERIFICATION_AUTHORIZED"
    out["authorization"] = {
        "authorized_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_plan_path": str(args.plan),
        "source_plan_sha256": digest(args.plan),
        "scope": SCOPE,
        "authorized_block_count": required,
        "authorization_note": args.authorization_note.strip(),
        "provider_call_made": False,
        "provider_spend_made": False,
        "workflow_auto_dispatched": False,
    }
    out["authorized_block_count"] = required
    out["provider_call_made"] = False
    out["provider_spend_made"] = False
    out["cast_lock"] = False
    out["full_e01_render_allowed"] = False
    out["next"] = "MANUAL_DISPATCH_ROOM917_RU_FINALIST_VERIFICATION_WITH_EXACT_AUTHORIZED_PLAN"
    out["hard_rules"] = list(out.get("hard_rules") or []) + [
        "AUTHORIZATION_MUST_EXACTLY_MATCH_MINIMAL_PLAN",
        "NO_SILENT_EXTRA_PAID_BLOCKS",
        "NO_AUTO_DISPATCH",
        "NO_CAST_LOCK_FROM_SPEND_AUTHORIZATION",
        "NO_FULL_E01_RENDER"
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "authorized_block_count": required,
        "provider_call_made": False,
        "provider_spend_made": False,
        "cast_lock": False,
        "out": str(args.out)
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
