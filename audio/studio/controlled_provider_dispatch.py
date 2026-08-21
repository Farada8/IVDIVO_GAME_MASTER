#!/usr/bin/env python3
"""IVDIVO Audio Studio — controlled paid-provider dispatch wrapper.

This is the authoritative-integration candidate that connects the existing
ElevenLabs adapter to the Wave3/Wave4 production-control contracts without
changing story or provider payload semantics.

Safety properties:
- compile/dry-run is default; live requires explicit --live;
- optional canary identity fixture may be checked before any dispatch;
- authenticated capability snapshot must PASS when supplied;
- immutable request/spend ledger prevents blind duplicate payment;
- transport/provider uncertainty after POST is quarantined as AMBIGUOUS;
- accepted provider evidence is persisted through the existing adapter;
- accepted request hashes are reused after restart rather than resent.

No API key is persisted or printed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
RUNTIME = HERE / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import elevenlabs_adapter as adapter
from production_control import SpendLedger, capability_drift, validate_identity_fixture


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def capability_gate(compiled: dict[str, Any], block: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    if snapshot.get("status") != "PASS":
        return {"status": "FAIL_SNAPSHOT_NOT_PASS", "auto_substitution": False}
    voice_ids: list[str] = []
    bt = block.get("block_type")
    if bt == "TTD_BLOCK":
        voice_ids = sorted({str(t.get("voice_id")) for t in block.get("turns", []) if t.get("voice_id")})
    elif block.get("voice_id"):
        voice_ids = [str(block["voice_id"])]
    model_id = compiled.get("body", {}).get("model_id")
    expected = {"voice_ids": voice_ids, "model_ids": [model_id] if model_id else []}
    return capability_drift(expected, snapshot)


def identity_gate(manifest_path: str | None, fixture_path: str | None) -> dict[str, Any]:
    if not manifest_path and not fixture_path:
        return {"status": "NOT_REQUESTED"}
    if not manifest_path or not fixture_path:
        raise ValueError("IDENTITY_MANIFEST_AND_FIXTURE_REQUIRED_TOGETHER")
    return validate_identity_fixture(load_json(manifest_path), load_json(fixture_path))


def execute(
    block_path: str,
    out_dir: str,
    ledger_path: str,
    *,
    live: bool = False,
    capability_snapshot_path: str | None = None,
    manifest_path: str | None = None,
    fixture_path: str | None = None,
    timeout: float = 60.0,
) -> dict[str, Any]:
    block = load_json(block_path)
    compiled = adapter.compile_block(block)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    compiled_path = out / f"{compiled['block_id']}__compiled_request.json"
    compiled_path.write_text(json.dumps(compiled, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    ig = identity_gate(manifest_path, fixture_path)
    if ig.get("status") not in {"PASS", "NOT_REQUESTED"}:
        return {"status": "NO_DISPATCH_IDENTITY", "identity_gate": ig, "dispatch": False}

    cap = {"status": "NOT_REQUESTED"}
    if capability_snapshot_path:
        cap = capability_gate(compiled, block, load_json(capability_snapshot_path))
        if cap.get("status") != "PASS":
            return {"status": "NO_DISPATCH_CAPABILITY", "capability_gate": cap, "dispatch": False}

    ledger = SpendLedger(ledger_path)
    plan = ledger.plan(compiled["request_hash"], compiled["block_id"])
    if plan == "REUSED_ACCEPTED":
        return {
            "status": "REUSE_ACCEPTED",
            "dispatch": False,
            "request_hash": compiled["request_hash"],
            "ledger_state": plan,
        }
    if plan == "RECONCILE_REQUIRED":
        return {
            "status": "HOLD_AMBIGUOUS_RECONCILIATION_REQUIRED",
            "dispatch": False,
            "request_hash": compiled["request_hash"],
            "ledger_state": plan,
        }

    if not live:
        return {
            "status": "DRY_PASS",
            "dispatch": False,
            "request_hash": compiled["request_hash"],
            "compiled_request": str(compiled_path),
            "identity_gate": ig,
            "capability_gate": cap,
            "ledger_state": plan,
        }

    if plan not in {"PLANNED", "EXISTS_REJECTED"}:
        return {
            "status": "NO_DISPATCH_LEDGER_STATE",
            "dispatch": False,
            "request_hash": compiled["request_hash"],
            "ledger_state": plan,
        }

    ledger.transition(compiled["request_hash"], "SENT")
    try:
        raw, meta = adapter.dispatch(compiled, timeout)
    except RuntimeError as exc:
        try:
            failure = json.loads(str(exc))
        except json.JSONDecodeError:
            failure = {"failure": "FAIL_PROVIDER_UNKNOWN"}
        category = failure.get("failure")
        if category in {"FAIL_PROVIDER_CONNECTIVITY"} or int(failure.get("http_status") or 0) >= 500:
            ledger.transition(compiled["request_hash"], "AMBIGUOUS")
            return {
                "status": "HOLD_AMBIGUOUS",
                "dispatch": True,
                "request_hash": compiled["request_hash"],
                "failure": failure,
            }
        ledger.transition(compiled["request_hash"], "REJECTED")
        return {
            "status": "PROVIDER_REJECTED",
            "dispatch": True,
            "request_hash": compiled["request_hash"],
            "failure": failure,
        }

    evidence = adapter.persist(compiled, raw, meta, out)
    ledger.transition(
        compiled["request_hash"],
        "ACCEPTED",
        provider_request_id=meta.get("provider_request_id"),
        response_hash=evidence.get("audio_sha256"),
    )
    return {
        "status": "LIVE_ACCEPTED",
        "dispatch": True,
        "request_hash": compiled["request_hash"],
        "evidence": evidence,
    }


def main() -> None:
    p = argparse.ArgumentParser(prog="ivdivo-controlled-provider-dispatch")
    p.add_argument("block_json")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--ledger", required=True)
    p.add_argument("--capability-snapshot")
    p.add_argument("--manifest")
    p.add_argument("--fixture")
    p.add_argument("--timeout", type=float, default=60.0)
    p.add_argument("--live", action="store_true")
    args = p.parse_args()
    result = execute(
        args.block_json,
        args.out_dir,
        args.ledger,
        live=args.live,
        capability_snapshot_path=args.capability_snapshot,
        manifest_path=args.manifest,
        fixture_path=args.fixture,
        timeout=args.timeout,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if result["status"].startswith("NO_DISPATCH") or result["status"].startswith("HOLD_"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
