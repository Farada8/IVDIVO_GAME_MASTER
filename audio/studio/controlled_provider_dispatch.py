#!/usr/bin/env python3
"""IVDIVO Audio Studio — controlled paid-provider dispatch wrapper.

Connects the existing provider adapter to provider-neutral production-control
contracts without changing story text or provider payload semantics.

Safety properties:
- compile/dry-run is default; live requires explicit --live;
- accepted request hashes are reused after restart rather than resent;
- any *new* live dispatch requires an identity manifest+fixture AND a PASS
  authenticated capability snapshot;
- immutable request/spend ledger prevents blind duplicate payment;
- transport/provider uncertainty after POST is quarantined as AMBIGUOUS;
- accepted provider evidence is persisted through the existing adapter;
- provider acceptance is distinct from production-asset acceptance;
- canonical 48 kHz WAV ingest is attempted only when the returned source format
  can be validated without guessing or silent transcoding.

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
from audio_asset_ingest import persist_ingest
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


def _canonical_asset_gate(compiled: dict[str, Any], evidence: dict[str, Any], out: Path) -> dict[str, Any]:
    """Promote provider bytes to canonical 48 kHz evidence only when provable.

    The current strict ingest accepts 48 kHz PCM WAV or raw PCM16 with explicit
    metadata. The provider adapter may return MP3 or PCM without channel metadata;
    those bytes remain durable provider evidence but are HOLD for production
    timeline/take use until an explicit upstream conversion/metadata step exists.
    """
    audio_path = Path(str(evidence.get("audio_artifact") or ""))
    if not audio_path.exists():
        return {"status": "HOLD_AUDIO_ARTIFACT_MISSING"}

    output_format = str((compiled.get("query") or {}).get("output_format") or "")
    if output_format.startswith("wav_"):
        canonical_path = out / f"{compiled['block_id']}__canonical_48k.wav"
        try:
            ingest = persist_ingest(audio_path, canonical_path, source_format="WAV")
        except ValueError as exc:
            return {
                "status": "HOLD_CANONICAL_INGEST_FAILED",
                "reason": str(exc),
                "provider_audio_artifact": str(audio_path),
            }
        return {"status": "PASS", "ingest": ingest}

    if output_format.startswith("pcm_"):
        return {
            "status": "HOLD_RAW_PCM_METADATA_REQUIRED",
            "provider_audio_artifact": str(audio_path),
            "reason": "channel/sample metadata must be explicit before canonical wrapping",
        }

    return {
        "status": "HOLD_EXPLICIT_UPSTREAM_CONVERSION_REQUIRED",
        "provider_audio_artifact": str(audio_path),
        "source_output_format": output_format or "UNKNOWN",
        "reason": "provider bytes are spend/provenance evidence but not canonical timeline/take evidence",
    }


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

    # New paid dispatch is fail-closed unless both identity and authenticated
    # capability evidence are explicit. Reusing an already accepted hash above
    # does not require re-proving these because no provider call will occur.
    missing_live_gates: list[str] = []
    if ig.get("status") != "PASS":
        missing_live_gates.append("IDENTITY_FIXTURE")
    if cap.get("status") != "PASS":
        missing_live_gates.append("AUTHENTICATED_CAPABILITY_SNAPSHOT")
    if missing_live_gates:
        return {
            "status": "NO_DISPATCH_LIVE_GATES",
            "dispatch": False,
            "request_hash": compiled["request_hash"],
            "missing": missing_live_gates,
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
    # ACCEPTED here means the paid provider request/evidence is accepted into the
    # spend/provenance ledger. It does NOT mean artistic/production take lock.
    ledger.transition(
        compiled["request_hash"],
        "ACCEPTED",
        provider_request_id=meta.get("provider_request_id"),
        response_hash=evidence.get("audio_sha256"),
    )
    asset_gate = _canonical_asset_gate(compiled, evidence, out)
    return {
        "status": "LIVE_PROVIDER_ACCEPTED",
        "dispatch": True,
        "request_hash": compiled["request_hash"],
        "evidence": evidence,
        "production_asset_gate": asset_gate,
        "take_lock": False,
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
