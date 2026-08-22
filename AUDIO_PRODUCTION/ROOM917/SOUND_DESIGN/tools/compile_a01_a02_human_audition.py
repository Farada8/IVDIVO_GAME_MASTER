#!/usr/bin/env python3
"""Compile explicit human A01/A02 audition decisions into binding-gate input.

This tool never performs provider generation, never infers artistic PASS, and never
creates renderer bindings. It only validates explicit human decisions against the
machine-prepared pending candidate set. The output is atomic: if every requested
asset does not have exactly one fully-passed selected candidate, `candidates` is
empty and the existing sound_asset_binding_gate must not be called successfully.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_GATES = (
    "ROOM_IDENTITY",
    "LOOP_SEAM",
    "FALSE_CLUE_AUDIT",
    "MONO_TRANSLATION",
    "PHONE_PROXY_TRANSLATION",
    "DIALOGUE_UNDERLAY",
)
ALLOWED_GATE_STATUS = {"PASS", "HOLD", "REJECT"}
ALLOWED_DECISION = {"SELECT", "HOLD", "REJECT_ALL"}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"JSON root must be an object: {path}")
    return value


def numeric_gain(value) -> float:
    if isinstance(value, bool):
        raise ValueError("gain_db must be numeric, not boolean")
    gain = float(value)
    if not math.isfinite(gain):
        raise ValueError("gain_db must be finite")
    return gain


def candidate_index(rows: list[dict], asset_id: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise SystemExit(f"Pending candidate row is not an object for {asset_id}")
        if row.get("asset_id") != asset_id:
            raise SystemExit(f"Pending candidate asset mismatch for {asset_id}")
        cid = str(row.get("candidate_id") or "")
        if not cid:
            raise SystemExit(f"Pending candidate missing candidate_id for {asset_id}")
        if cid in out:
            raise SystemExit(f"Duplicate candidate_id for {asset_id}: {cid}")
        out[cid] = row
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Fail-closed ROOM917 A01/A02 human audition compiler")
    ap.add_argument("--pending", required=True, type=Path)
    ap.add_argument("--review", required=True, type=Path)
    ap.add_argument("--out-candidates", required=True, type=Path)
    ap.add_argument("--report", required=True, type=Path)
    args = ap.parse_args()

    pending = load(args.pending)
    review = load(args.review)
    pending_by_asset = pending.get("candidates_by_asset")
    if not isinstance(pending_by_asset, dict) or not pending_by_asset:
        raise SystemExit("Pending candidate set is empty or malformed")

    requested_assets = sorted(pending_by_asset)
    review_assets = review.get("assets")
    if not isinstance(review_assets, dict):
        raise SystemExit("Review must contain an assets object")
    if sorted(review_assets) != requested_assets:
        raise SystemExit("Review asset set must exactly match pending requested asset set")

    fixture_only = bool(review.get("fixture_only", False))
    attested = review.get("human_review_attested") is True
    reviewer = str(review.get("reviewer") or "").strip()
    reviewed_at = str(review.get("reviewed_at") or "").strip()

    global_errors: list[str] = []
    if not fixture_only:
        if not attested:
            global_errors.append("HUMAN_REVIEW_NOT_ATTESTED")
        if not reviewer:
            global_errors.append("REVIEWER_MISSING")
        if not reviewed_at:
            global_errors.append("REVIEWED_AT_MISSING")

    compiled: dict[str, dict] = {}
    rows: list[dict] = []

    for asset_id in requested_assets:
        decision = review_assets[asset_id]
        errors: list[str] = []
        if not isinstance(decision, dict):
            rows.append({"asset_id": asset_id, "status": "HOLD", "errors": ["REVIEW_ROW_NOT_OBJECT"]})
            continue

        action = decision.get("decision")
        if action not in ALLOWED_DECISION:
            errors.append("INVALID_DECISION")

        index = candidate_index(pending_by_asset[asset_id], asset_id)
        selected = None
        if action == "SELECT":
            cid = str(decision.get("selected_candidate_id") or "")
            selected = index.get(cid)
            if selected is None:
                errors.append("SELECTED_CANDIDATE_NOT_IN_PENDING_SET")

            declared_sha = str(decision.get("selected_sha256") or "").lower()
            if not SHA_RE.match(declared_sha):
                errors.append("SELECTED_SHA256_INVALID")
            elif selected is not None and declared_sha != str(selected.get("sha256") or "").lower():
                errors.append("SELECTED_SHA256_MISMATCH")

            gates = decision.get("gates")
            if not isinstance(gates, dict):
                errors.append("GATES_MISSING")
                gates = {}
            if set(gates) != set(REQUIRED_GATES):
                errors.append("GATE_SET_MISMATCH")
            for gate in REQUIRED_GATES:
                status = gates.get(gate)
                if status not in ALLOWED_GATE_STATUS:
                    errors.append(f"INVALID_GATE_STATUS:{gate}")
                elif status != "PASS":
                    errors.append(f"GATE_NOT_PASS:{gate}:{status}")

            try:
                gain_db = numeric_gain(decision.get("gain_db"))
            except (TypeError, ValueError) as exc:
                errors.append("GAIN_DB_NOT_EXPLICIT_NUMERIC:" + str(exc))
                gain_db = None

            if selected is not None:
                if selected.get("binding_status") != "FORBIDDEN_PENDING_HUMAN_AND_CONTEXT_GATES":
                    errors.append("UNEXPECTED_PENDING_BINDING_STATUS")
                if selected.get("audition_status") != "HOLD":
                    errors.append("PENDING_AUDITION_STATUS_NOT_HOLD")
                for key in (
                    "asset_id", "candidate_id", "path", "sha256", "size_bytes",
                    "sample_rate_hz", "bit_depth", "channels",
                ):
                    if key not in selected:
                        errors.append("PENDING_FIELD_MISSING:" + key)

            if not errors and selected is not None and gain_db is not None:
                compiled[asset_id] = {
                    "asset_id": asset_id,
                    "candidate_id": selected["candidate_id"],
                    "path": selected["path"],
                    "sha256": str(selected["sha256"]).lower(),
                    "size_bytes": selected["size_bytes"],
                    "sample_rate_hz": selected["sample_rate_hz"],
                    "bit_depth": selected["bit_depth"],
                    "channels": selected["channels"],
                    "gain_db": gain_db,
                    "audition_status": "PASS",
                    "mono_status": "PASS",
                    "phone_proxy_status": "PASS",
                    "loop_seam_status": "PASS",
                    "false_clue_audit_status": "PASS",
                    "human_review": {
                        "reviewer": reviewer or "CI_SYNTHETIC_FIXTURE",
                        "reviewed_at": reviewed_at or "FIXTURE_ONLY",
                        "gates": {gate: "PASS" for gate in REQUIRED_GATES},
                    },
                }
        else:
            errors.append("ASSET_NOT_SELECTED")

        rows.append({
            "asset_id": asset_id,
            "decision": action,
            "candidate_id": decision.get("selected_candidate_id"),
            "status": "PASS" if not errors else "HOLD",
            "errors": errors,
        })

    all_rows_pass = bool(rows) and all(r["status"] == "PASS" for r in rows)
    atomic_ready = all_rows_pass and not global_errors and len(compiled) == len(requested_assets)
    atomic_candidates = compiled if atomic_ready else {}

    output = {
        "schema_version": "room917.e01_a01_a02_binding_gate_input/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "status": "READY_FOR_EXISTING_SOUND_ASSET_BINDING_GATE" if atomic_ready else "HOLD_NOT_BINDABLE",
        "fixture_only": fixture_only,
        "production_binding_authorized": False,
        "requested_asset_ids": requested_assets,
        "candidates": atomic_candidates,
        "law": "This file is binding-gate input only, never a renderer binding. Candidate output is atomic across the reviewed asset set; any HOLD suppresses all candidates. Existing sound_asset_binding_gate must still verify actual bytes, SHA, format, contract and shared identity rules.",
    }
    report = {
        "schema_version": "room917.e01_a01_a02_human_audition_compile_report/1.0",
        "status": output["status"],
        "fixture_only": fixture_only,
        "human_review_attested": attested,
        "reviewer": reviewer,
        "reviewed_at": reviewed_at,
        "requested_asset_ids": requested_assets,
        "global_errors": global_errors,
        "rows": rows,
        "compiled_candidate_ids": {k: v["candidate_id"] for k, v in atomic_candidates.items()},
        "renderer_binding_emitted": False,
        "provider_calls": 0,
    }

    args.out_candidates.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.out_candidates.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": output["status"], "candidate_count": len(atomic_candidates), "fixture_only": fixture_only}))
    return 0 if atomic_ready else 4


if __name__ == "__main__":
    raise SystemExit(main())
