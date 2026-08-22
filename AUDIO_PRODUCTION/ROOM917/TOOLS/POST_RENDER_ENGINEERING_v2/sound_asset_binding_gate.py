#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, wave
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(block_size), b""):
            h.update(b)
    return h.hexdigest()


def wav_meta(path: Path) -> dict:
    with wave.open(str(path), "rb") as w:
        if w.getcomptype() != "NONE":
            raise ValueError("only uncompressed PCM WAV is production-bindable")
        return {
            "sample_rate_hz": w.getframerate(),
            "bit_depth": w.getsampwidth() * 8,
            "channels": w.getnchannels(),
            "frames": w.getnframes(),
            "duration_seconds": w.getnframes() / w.getframerate(),
        }


def evaluate_candidate(asset_id: str, spec: dict, candidate: dict, contract: dict) -> dict:
    errors = []
    required = contract["binding_acceptance"]["required_candidate_fields"]
    missing = [k for k in required if k not in candidate]
    if missing:
        errors.append("MISSING_FIELDS:" + ",".join(missing))

    if candidate.get("asset_id") != asset_id:
        errors.append("ASSET_ID_MISMATCH")
    if candidate.get("audition_status") != "PASS":
        errors.append("AUDITION_NOT_PASS")

    if spec.get("story_critical"):
        if candidate.get("mono_status") != "PASS":
            errors.append("MONO_NOT_PASS")
        if candidate.get("phone_proxy_status") != "PASS":
            errors.append("PHONE_PROXY_NOT_PASS")

    if spec.get("class") == "AMBIENCE_BED":
        if candidate.get("loop_seam_status") != "PASS":
            errors.append("LOOP_SEAM_NOT_PASS")
        if candidate.get("false_clue_audit_status") != "PASS":
            errors.append("FALSE_CLUE_AUDIT_NOT_PASS")

    p = Path(str(candidate.get("path") or ""))
    observed = {}
    if not p.is_file():
        errors.append("ASSET_BYTES_NOT_FOUND")
    else:
        expected_sha = str(candidate.get("sha256") or "").lower()
        if not SHA_RE.match(expected_sha):
            errors.append("INVALID_DECLARED_SHA256")
        else:
            observed_sha = sha256_file(p)
            observed["sha256"] = observed_sha
            if observed_sha != expected_sha:
                errors.append("SHA256_MISMATCH")
        observed["size_bytes"] = p.stat().st_size
        if candidate.get("size_bytes") != p.stat().st_size:
            errors.append("SIZE_MISMATCH")
        try:
            m = wav_meta(p)
            observed["wav"] = m
            target = contract["delivery_normalization_target"]
            if m["sample_rate_hz"] != target["sample_rate_hz"]:
                errors.append("SAMPLE_RATE_MISMATCH")
            if m["bit_depth"] != target["bit_depth"]:
                errors.append("BIT_DEPTH_MISMATCH")
            if m["channels"] != target["channels"]:
                errors.append("CHANNEL_COUNT_MISMATCH")
            for k in ("sample_rate_hz", "bit_depth", "channels"):
                if candidate.get(k) != m[k]:
                    errors.append("DECLARED_METADATA_MISMATCH:" + k)
        except Exception as e:
            errors.append("WAV_METADATA_ERROR:" + str(e))

    try:
        float(candidate.get("gain_db"))
    except (TypeError, ValueError):
        errors.append("GAIN_DB_NOT_EXPLICIT_NUMERIC")

    return {
        "asset_id": asset_id,
        "candidate_id": candidate.get("candidate_id"),
        "status": "PASS" if not errors else "HOLD",
        "errors": errors,
        "observed": observed,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Fail-closed ROOM917 E01 sound asset identity/binding gate")
    ap.add_argument("--contract", required=True, type=Path)
    ap.add_argument("--candidates", required=True, type=Path)
    ap.add_argument("--out-bindings", required=True, type=Path)
    ap.add_argument("--report", required=True, type=Path)
    args = ap.parse_args()

    contract = load(args.contract)
    payload = load(args.candidates)
    candidates = payload.get("candidates", payload)
    if not isinstance(candidates, dict):
        raise SystemExit("candidates must be an object keyed by asset_id")

    specs = contract.get("assets", {})
    report_rows = []
    bindings = {}
    for asset_id, cand in candidates.items():
        spec = specs.get(asset_id)
        if spec is None:
            report_rows.append({"asset_id": asset_id, "status": "HOLD", "errors": ["ASSET_NOT_IN_CURRENT_BRANCH_CONTRACT"]})
            continue
        r = evaluate_candidate(asset_id, spec, cand, contract)
        report_rows.append(r)
        if r["status"] == "PASS":
            bindings[asset_id] = {
                "path": str(Path(cand["path"]).resolve()),
                "gain_db": float(cand["gain_db"]),
                "candidate_id": cand["candidate_id"],
                "sha256": cand["sha256"].lower(),
                "identity_gate": "PASS"
            }

    args.out_bindings.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.out_bindings.write_text(json.dumps(bindings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    overall = "PASS" if report_rows and all(r["status"] == "PASS" for r in report_rows) else "HOLD"
    report = {
        "schema_version": "room917.sound_asset_binding_gate/1.0",
        "status": overall,
        "contract": str(args.contract),
        "rows": report_rows,
        "renderer_bindings_emitted": sorted(bindings),
        "law": "Renderer bindings exist only after byte identity, format, audition and translation gates pass. No filename-only binding."
    }
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{overall} passed={len(bindings)} total={len(report_rows)}")
    return 0 if overall == "PASS" else 4


if __name__ == "__main__":
    raise SystemExit(main())
