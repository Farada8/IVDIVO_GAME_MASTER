#!/usr/bin/env python3
"""ROOM917 E01 recovery intake gate.

Fail-closed router for recovered evidence. It does not recover bytes, infer timing,
classify defects, authorize patches, or simulate human review.

Accepted evidence classes:
1. Exact immutable E01 full-master WAV bytes -> P003A2 may run.
2. Complete accepted/live block timing for the current semantic lineage -> lineage
   timing may resolve, but P003A2 still requires master bytes unless exact signal
   intervals are also recovered.
3. Exact P003A2 signal interval output from the same immutable master plus a trusted
   provenance sidecar -> interval classification may run without reacquiring WAV.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import wave
from pathlib import Path
from typing import Any

EXPECTED_MASTER = {
    "sha256": "231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8",
    "size_bytes": 189_558_764,
    "sample_rate_hz": 48_000,
    "sample_width_bytes": 3,
    "channels": 2,
    "frames": 31_593_120,
    "duration_seconds": 658.190,
}
PRE_SCENE3_END = 444.980
ALLOWED_TIMING_GRADES = {"ACCEPTED_ALIGNMENT", "LIVE_TIMELINE"}
ALLOWED_INTERVAL_PROVENANCE = {
    "P003A2_ORIGINAL_OUTPUT",
    "FOUNDER_LOCKED_EXACT_SIGNAL_ANALYSIS",
}
REQUIRED_THRESHOLDS = {-85.0, -50.0, -45.0}


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def _close(a: float, b: float, tol: float = 1e-6) -> bool:
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)


def validate_master(path: Path, spec: dict[str, Any] = EXPECTED_MASTER) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    if not path.is_file():
        return {"status": "FAIL", "checks": [{"id": "FILE_EXISTS", "pass": False}]}
    size = path.stat().st_size
    digest = sha256_file(path)
    checks.append({"id": "SIZE", "pass": size == spec["size_bytes"], "actual": size})
    checks.append({"id": "SHA256", "pass": digest == spec["sha256"], "actual": digest})
    try:
        with wave.open(str(path), "rb") as w:
            meta = {
                "sample_rate_hz": w.getframerate(),
                "sample_width_bytes": w.getsampwidth(),
                "channels": w.getnchannels(),
                "frames": w.getnframes(),
                "duration_seconds": w.getnframes() / w.getframerate(),
                "compression": w.getcomptype(),
            }
    except (wave.Error, EOFError) as exc:
        checks.append({"id": "WAV_PARSE", "pass": False, "error": str(exc)})
        return {"status": "FAIL", "checks": checks}
    checks.extend([
        {"id": "PCM", "pass": meta["compression"] == "NONE", "actual": meta["compression"]},
        {"id": "SAMPLE_RATE", "pass": meta["sample_rate_hz"] == spec["sample_rate_hz"], "actual": meta["sample_rate_hz"]},
        {"id": "SAMPLE_WIDTH", "pass": meta["sample_width_bytes"] == spec["sample_width_bytes"], "actual": meta["sample_width_bytes"]},
        {"id": "CHANNELS", "pass": meta["channels"] == spec["channels"], "actual": meta["channels"]},
        {"id": "FRAMES", "pass": meta["frames"] == spec["frames"], "actual": meta["frames"]},
        {"id": "DURATION", "pass": _close(meta["duration_seconds"], spec["duration_seconds"]), "actual": meta["duration_seconds"]},
    ])
    return {"status": "PASS" if all(c["pass"] for c in checks) else "FAIL", "checks": checks, "metadata": meta}


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return data


def _lineage_block_ids(lineage: dict[str, Any]) -> list[str]:
    ids = [str(b.get("block_id")) for b in lineage.get("blocks", []) if b.get("block_id")]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Semantic lineage must contain unique non-empty block_id values")
    return ids


def validate_timing_map(path: Path, semantic_lineage: Path, master_sha: str = EXPECTED_MASTER["sha256"]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    try:
        tm = _load_json(path)
        lineage = _load_json(semantic_lineage)
        expected_ids = _lineage_block_ids(lineage)
    except Exception as exc:
        return {"status": "FAIL", "checks": [{"id": "JSON_AND_LINEAGE_PARSE", "pass": False, "error": str(exc)}]}

    src_sha = str(tm.get("source_master_sha256", "")).lower()
    checks.append({"id": "SOURCE_MASTER_SHA", "pass": src_sha == master_sha, "actual": src_sha})
    blocks = tm.get("blocks")
    if not isinstance(blocks, list):
        return {"status": "FAIL", "checks": checks + [{"id": "BLOCKS_LIST", "pass": False}]}

    by_id: dict[str, dict[str, Any]] = {}
    duplicate = False
    for b in blocks:
        bid = str(b.get("block_id", ""))
        if bid in by_id:
            duplicate = True
        by_id[bid] = b
    checks.append({"id": "NO_DUPLICATE_BLOCK_IDS", "pass": not duplicate})
    checks.append({"id": "EXACT_BLOCK_SET", "pass": set(by_id) == set(expected_ids), "expected_count": len(expected_ids), "actual_count": len(by_id)})

    ranges: list[tuple[float, float, str]] = []
    detail_errors: list[str] = []
    for bid in expected_ids:
        b = by_id.get(bid)
        if not b:
            continue
        grade = b.get("evidence_grade")
        source = b.get("source") or b.get("source_ref")
        s, e = b.get("start_seconds"), b.get("end_seconds")
        if grade not in ALLOWED_TIMING_GRADES:
            detail_errors.append(f"{bid}: untrusted evidence_grade={grade!r}")
            continue
        if not source:
            detail_errors.append(f"{bid}: source/source_ref required")
            continue
        if s is None or e is None:
            detail_errors.append(f"{bid}: null timing")
            continue
        try:
            s = float(s); e = float(e)
        except (TypeError, ValueError):
            detail_errors.append(f"{bid}: non-numeric timing")
            continue
        if not (0.0 <= s < e <= PRE_SCENE3_END + 1e-6):
            detail_errors.append(f"{bid}: out-of-range or invalid [{s}, {e}]")
            continue
        ranges.append((s, e, bid))

    ranges.sort()
    for (s0, e0, b0), (s1, e1, b1) in zip(ranges, ranges[1:]):
        if s1 < e0 - 1e-9:
            detail_errors.append(f"overlap: {b0} [{s0},{e0}] with {b1} [{s1},{e1}]")
    checks.append({"id": "TRUSTED_COMPLETE_TIMING", "pass": not detail_errors and len(ranges) == len(expected_ids), "errors": detail_errors})
    return {"status": "PASS" if all(c["pass"] for c in checks) else "FAIL", "checks": checks, "resolved_block_count": len(ranges)}


def validate_interval_map(path: Path, provenance_path: Path, master_spec: dict[str, Any] = EXPECTED_MASTER) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    try:
        data = _load_json(path)
        prov = _load_json(provenance_path)
    except Exception as exc:
        return {"status": "FAIL", "checks": [{"id": "JSON_PARSE", "pass": False, "error": str(exc)}]}

    checks.append({"id": "SCHEMA", "pass": data.get("schema_version") == "ivdivo.room917.p003a2_interval_analysis/1.0", "actual": data.get("schema_version")})
    src = data.get("source") or {}
    checks.append({"id": "SOURCE_SHA", "pass": str(src.get("sha256", "")).lower() == master_spec["sha256"], "actual": src.get("sha256")})
    checks.append({"id": "SOURCE_SIZE", "pass": src.get("size_bytes") == master_spec["size_bytes"], "actual": src.get("size_bytes")})
    basis = data.get("analysis_basis") or {}
    thresholds = {float(x) for x in basis.get("thresholds_dbfs", [])}
    checks.extend([
        {"id": "SEGMENT_START", "pass": _close(basis.get("segment_start_seconds", -1), 0.0), "actual": basis.get("segment_start_seconds")},
        {"id": "SEGMENT_END", "pass": _close(basis.get("segment_end_seconds", -1), PRE_SCENE3_END), "actual": basis.get("segment_end_seconds")},
        {"id": "WINDOW_MS", "pass": _close(basis.get("window_ms", -1), 100.0), "actual": basis.get("window_ms")},
        {"id": "THRESHOLDS", "pass": REQUIRED_THRESHOLDS.issubset(thresholds), "actual": sorted(thresholds)},
    ])

    intervals = data.get("intervals")
    interval_errors: list[str] = []
    if not isinstance(intervals, list):
        interval_errors.append("intervals must be a list")
        intervals = []
    for i, iv in enumerate(intervals):
        try:
            s = float(iv["start_seconds"]); e = float(iv["end_seconds"]); t = float(iv["threshold_dbfs"])
        except (KeyError, TypeError, ValueError):
            interval_errors.append(f"interval[{i}] missing/non-numeric required fields")
            continue
        if not (0.0 <= s < e <= PRE_SCENE3_END + 1e-6):
            interval_errors.append(f"interval[{i}] invalid bounds [{s},{e}]")
        if t not in REQUIRED_THRESHOLDS:
            interval_errors.append(f"interval[{i}] unexpected threshold {t}")
    checks.append({"id": "INTERVAL_BOUNDS_AND_THRESHOLDS", "pass": not interval_errors, "errors": interval_errors})

    prov_grade = prov.get("evidence_grade")
    prov_sha = str(prov.get("source_master_sha256", "")).lower()
    prov_ref = prov.get("source_ref")
    immutable = prov.get("immutable_source") is True
    checks.extend([
        {"id": "PROVENANCE_GRADE", "pass": prov_grade in ALLOWED_INTERVAL_PROVENANCE, "actual": prov_grade},
        {"id": "PROVENANCE_SHA", "pass": prov_sha == master_spec["sha256"], "actual": prov_sha},
        {"id": "PROVENANCE_REF", "pass": bool(prov_ref)},
        {"id": "IMMUTABLE_SOURCE", "pass": immutable, "actual": prov.get("immutable_source")},
    ])
    return {"status": "PASS" if all(c["pass"] for c in checks) else "FAIL", "checks": checks, "interval_count": len(intervals)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--master", type=Path)
    ap.add_argument("--semantic-lineage", type=Path)
    ap.add_argument("--timing-map", type=Path)
    ap.add_argument("--interval-map", type=Path)
    ap.add_argument("--interval-provenance", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    results: dict[str, Any] = {}
    if args.master:
        results["master_bytes"] = validate_master(args.master)
    if args.timing_map:
        if not args.semantic_lineage:
            results["accepted_timing"] = {"status": "FAIL", "checks": [{"id": "SEMANTIC_LINEAGE_REQUIRED", "pass": False}]}
        else:
            results["accepted_timing"] = validate_timing_map(args.timing_map, args.semantic_lineage)
    if args.interval_map:
        if not args.interval_provenance:
            results["signal_intervals"] = {"status": "FAIL", "checks": [{"id": "INTERVAL_PROVENANCE_REQUIRED", "pass": False}]}
        else:
            results["signal_intervals"] = validate_interval_map(args.interval_map, args.interval_provenance)

    master_pass = results.get("master_bytes", {}).get("status") == "PASS"
    timing_pass = results.get("accepted_timing", {}).get("status") == "PASS"
    intervals_pass = results.get("signal_intervals", {}).get("status") == "PASS"

    if intervals_pass:
        route = "EVIDENCE_CLASSIFICATION"
    elif master_pass:
        route = "P003A2_SIGNAL_INTERVALS"
    elif timing_pass:
        route = "LINEAGE_TIMING_RESOLUTION__P003A2_STILL_WAITS_FOR_MASTER_BYTES"
    else:
        route = "HOLD_RECOVERY__CONTINUE_INDEPENDENT_SAFE_FRONTIER"

    status = "PASS" if (master_pass or timing_pass or intervals_pass) else "HOLD"
    out = {
        "schema_version": "room917.recovery_intake_gate/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "status": status,
        "results": results,
        "route": route,
        "patch_authorized": False,
        "human_pass_claimed": False,
        "inference_used": False,
        "law": "Recovered evidence is validated only. No missing timing, bytes, interval, asset approval, patch authorization, or human evidence may be inferred.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "route": route}, indent=2))
    return 0 if status == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
