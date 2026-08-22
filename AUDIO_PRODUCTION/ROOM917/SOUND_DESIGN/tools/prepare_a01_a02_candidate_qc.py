#!/usr/bin/env python3
"""Normalize ROOM917 A01/A02 provider candidates and build listening/QC derivatives.

Machine preparation never awards artistic PASS. It creates reproducible bytes and
preview surfaces for the required human/Founder audition and existing binding gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
import wave


HUMAN_GATES = (
    "ROOM_IDENTITY",
    "LOOP_SEAM",
    "FALSE_CLUE_AUDIT",
    "MONO_TRANSLATION",
    "PHONE_PROXY_TRANSLATION",
    "DIALOGUE_UNDERLAY",
)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def wav_meta(path: Path) -> dict:
    with wave.open(str(path), "rb") as w:
        return {
            "sample_rate_hz": w.getframerate(),
            "bit_depth": w.getsampwidth() * 8,
            "channels": w.getnchannels(),
            "frames": w.getnframes(),
            "duration_seconds": w.getnframes() / w.getframerate(),
            "compression": w.getcomptype(),
        }


def ffmpeg() -> str:
    p = shutil.which("ffmpeg")
    if not p:
        raise SystemExit("ffmpeg is required for candidate QC preparation")
    return p


def normalize(source: Path, out: Path) -> None:
    run([
        ffmpeg(), "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source),
        "-map_metadata", "-1",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le",
        str(out),
    ])


def mono_preview(source: Path, out: Path) -> None:
    run([
        ffmpeg(), "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source),
        "-map_metadata", "-1",
        "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le",
        str(out),
    ])


def phone_preview(source: Path, out: Path) -> None:
    run([
        ffmpeg(), "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source),
        "-map_metadata", "-1",
        "-af", "highpass=f=180,lowpass=f=7000",
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        str(out),
    ])


def seam_preview(source: Path, out: Path, duration: float, window: float = 0.75) -> None:
    if duration <= window * 2:
        raise RuntimeError(f"Candidate too short for seam preview: {duration:.3f}s")
    start = max(0.0, duration - window)
    filt=(
        f"[0:a]atrim=start={start:.6f}:end={duration:.6f},asetpts=PTS-STARTPTS[tail];"
        f"[0:a]atrim=start=0:end={window:.6f},asetpts=PTS-STARTPTS[head];"
        "[tail][head]concat=n=2:v=0:a=1[out]"
    )
    run([
        ffmpeg(), "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source),
        "-filter_complex", filt,
        "-map", "[out]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le",
        str(out),
    ])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()

    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    if evidence.get("production_binding_authorized") is not False:
        raise SystemExit("Source evidence unexpectedly authorizes production binding")
    candidates = evidence.get("candidates") or []
    if not candidates:
        raise SystemExit("No provider candidates found in evidence")

    args.outdir.mkdir(parents=True, exist_ok=True)
    rows=[]
    pending_by_asset: dict[str, list[dict]] = {}

    for cand in candidates:
        source = args.evidence.parent / cand["provider_source_filename"]
        if not source.is_file():
            raise SystemExit(f"Missing provider source candidate: {source}")
        if sha256_file(source) != cand["provider_source_sha256"]:
            raise SystemExit(f"Provider source SHA mismatch: {source.name}")

        cid=cand["candidate_id"]
        normalized=args.outdir / f"{cid}_48K24_STEREO.wav"
        mono=args.outdir / f"{cid}_MONO_QC.wav"
        phone=args.outdir / f"{cid}_PHONE_QC.wav"
        seam=args.outdir / f"{cid}_SEAM_QC.wav"

        normalize(source, normalized)
        meta=wav_meta(normalized)
        if meta["compression"] != "NONE":
            raise RuntimeError("Normalized candidate is not PCM")
        if meta["sample_rate_hz"] != 48000 or meta["bit_depth"] != 24 or meta["channels"] != 2:
            raise RuntimeError(f"Normalization target failed for {cid}: {meta}")

        mono_preview(normalized, mono)
        phone_preview(normalized, phone)
        seam_preview(normalized, seam, meta["duration_seconds"])

        machine={
            "asset_id": cand["asset_id"],
            "candidate_id": cid,
            "provider_source": {
                "filename": cand["provider_source_filename"],
                "sha256": cand["provider_source_sha256"],
                "size_bytes": cand["provider_source_size_bytes"],
            },
            "normalized": {
                "path": str(normalized),
                "sha256": sha256_file(normalized),
                "size_bytes": normalized.stat().st_size,
                **meta,
            },
            "previews": {
                "seam": {"path": str(seam), "sha256": sha256_file(seam)},
                "mono": {"path": str(mono), "sha256": sha256_file(mono)},
                "phone": {"path": str(phone), "sha256": sha256_file(phone)},
            },
            "machine_status": "PREPARED_FOR_HUMAN_AUDITION",
            "human_required": list(HUMAN_GATES),
            "production_binding_authorized": False,
        }
        rows.append(machine)

        pending={
            "asset_id": cand["asset_id"],
            "candidate_id": cid,
            "path": str(normalized),
            "sha256": machine["normalized"]["sha256"],
            "size_bytes": machine["normalized"]["size_bytes"],
            "sample_rate_hz": 48000,
            "bit_depth": 24,
            "channels": 2,
            "gain_db": None,
            "audition_status": "HOLD",
            "mono_status": "HOLD",
            "phone_proxy_status": "HOLD",
            "loop_seam_status": "HOLD",
            "false_clue_audit_status": "HOLD",
            "qc_previews": machine["previews"],
            "binding_status": "FORBIDDEN_PENDING_HUMAN_AND_CONTEXT_GATES",
        }
        pending_by_asset.setdefault(cand["asset_id"], []).append(pending)

    report={
        "schema_version": "ivdivo.room917_a01_a02_machine_qc/1.1",
        "project": "ROOM917",
        "episode": "E01",
        "status": "PREPARED_FOR_HUMAN_AUDITION_NOT_BOUND",
        "candidate_count": len(rows),
        "rows": rows,
        "machine_may_award_artistic_pass": False,
        "production_binding_authorized": False,
        "next": "HUMAN_BLIND_AUDITION_FORM_THEN_FAIL_CLOSED_COMPILER_THEN_EXISTING_SOUND_ASSET_BINDING_GATE",
    }
    (args.outdir / "ROOM917_E01_A01_A02_MACHINE_QC.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")

    pending={
        "schema_version":"room917.e01_sound_asset_candidates_pending_human/1.0",
        "status":"MULTIPLE_CANDIDATES_PENDING_HUMAN_SELECTION_NOT_BINDABLE",
        "candidates_by_asset":pending_by_asset,
        "law":"Do not pass this multi-candidate file directly to sound_asset_binding_gate. Human review must select at most one candidate per asset and fill PASS/HOLD/REJECT plus explicit gain before compiling the binding input.",
    }
    (args.outdir / "ROOM917_E01_A01_A02_PENDING_HUMAN_CANDIDATES.json").write_text(json.dumps(pending, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")

    # Pre-populated review packet: the human reviewer changes only decisions,
    # selected candidate id/SHA, explicit tested gain and gate statuses. The
    # structure itself is generated from the actual candidate evidence.
    review_assets = {}
    for asset_id, asset_candidates in pending_by_asset.items():
        review_assets[asset_id] = {
            "decision": "HOLD",
            "selected_candidate_id": None,
            "selected_sha256": None,
            "gain_db": None,
            "gates": {gate: "HOLD" for gate in HUMAN_GATES},
            "candidate_reference": [
                {
                    "candidate_id": c["candidate_id"],
                    "sha256": c["sha256"],
                    "normalized_path": c["path"],
                    "qc_previews": c["qc_previews"],
                }
                for c in asset_candidates
            ],
            "notes": "",
        }
    review_form = {
        "schema_version": "room917.e01_a01_a02_human_audition_review/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "fixture_only": False,
        "human_review_attested": False,
        "reviewer": "",
        "reviewed_at": "",
        "assets": review_assets,
        "instructions": [
            "Blind-listen candidate sources/previews before selecting.",
            "For SELECT, copy one candidate_id and sha256 from candidate_reference exactly.",
            "Set an explicit gain_db only after dialogue-underlay audition.",
            "Every required gate must be PASS for a selected candidate; any HOLD suppresses the entire A01/A02 binding input.",
            "Set human_review_attested=true only after the actual human listen. Machine preparation cannot do this.",
        ],
    }
    (args.outdir / "ROOM917_E01_A01_A02_HUMAN_AUDITION_REVIEW.json").write_text(json.dumps(review_form, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")

    print(json.dumps({"status":report["status"],"candidate_count":len(rows),"outdir":str(args.outdir),"human_review_form":"ROOM917_E01_A01_A02_HUMAN_AUDITION_REVIEW.json"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
