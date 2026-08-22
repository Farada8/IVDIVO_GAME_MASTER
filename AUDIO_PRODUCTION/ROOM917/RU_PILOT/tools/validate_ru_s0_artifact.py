#!/usr/bin/env python3
"""Validate a ROOM917 RU S0 canary artifact and build a listening index.

This tool is deliberately provider-evidence focused. It does not judge acting and it
cannot lock cast. Human credibility remains the next gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def one(root: Path, pattern: str, label: str) -> Path:
    rows = sorted(root.glob(pattern))
    if len(rows) != 1:
        raise ValueError(f"{root}: expected exactly one {label}, found {len(rows)}")
    return rows[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact_root", type=Path)
    args = ap.parse_args()
    root = args.artifact_root.resolve()

    plan_path = root / "LIVE_CANARY_PLAN.json"
    receipt_path = root / "CANARY_RECEIPT.json"
    if not plan_path.exists() or not receipt_path.exists():
        raise SystemExit("FAIL_S0_ARTIFACT: missing LIVE_CANARY_PLAN.json or CANARY_RECEIPT.json")

    plan = load_json(plan_path)
    receipt = load_json(receipt_path)
    selected = list(plan.get("selected_block_ids") or [])
    if not selected or len(selected) not in (4, 6):
        raise SystemExit(f"FAIL_S0_ARTIFACT: selected block count must be 4 or 6, got {len(selected)}")
    if plan.get("full_episode_render_forbidden") is not True:
        raise SystemExit("FAIL_S0_ARTIFACT: full_episode_render_forbidden was not true")
    if receipt.get("full_episode_rendered") is not False or receipt.get("cast_locked") is not False:
        raise SystemExit("FAIL_S0_ARTIFACT: receipt violates canary-only boundary")

    receipt_audio = {row["path"]: row for row in receipt.get("audio_files") or []}
    if len(receipt_audio) != len(selected):
        raise SystemExit(
            f"FAIL_S0_ARTIFACT: receipt audio count {len(receipt_audio)} != selected blocks {len(selected)}"
        )

    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    request_hashes: set[str] = set()

    for ordinal, block_id in enumerate(selected, 1):
        candidates = sorted(root.glob(f"*__{block_id}"))
        if len(candidates) != 1:
            failures.append(f"{block_id}: expected one block directory, found {len(candidates)}")
            continue
        block_dir = candidates[0]
        try:
            audio = one(block_dir, "*__audio.*", "audio file")
            req = one(block_dir, "*__request.json", "request evidence")
            resp = one(block_dir, "*__response.json", "response evidence")
            raw_align = one(block_dir, "*__raw_alignment.json", "raw alignment")
            norm_align = one(block_dir, "*__normalized_alignment.json", "normalized alignment")

            if audio.stat().st_size < 2000:
                raise ValueError(f"audio suspiciously small: {audio.stat().st_size} bytes")

            rel_audio = str(audio.relative_to(root))
            rec = receipt_audio.get(rel_audio)
            if not rec:
                raise ValueError(f"audio absent from receipt: {rel_audio}")
            digest = sha256(audio)
            if digest != rec.get("sha256"):
                raise ValueError("audio SHA256 does not match receipt")
            if int(rec.get("bytes", -1)) != audio.stat().st_size:
                raise ValueError("audio byte count does not match receipt")

            req_json = load_json(req)
            resp_json = load_json(resp)
            norm_json = load_json(norm_align)
            request_hash = req_json.get("request_hash")
            if not request_hash:
                raise ValueError("request_hash missing")
            if request_hash in request_hashes:
                raise ValueError("duplicate request_hash")
            request_hashes.add(request_hash)

            serialized = json.dumps(resp_json, ensure_ascii=False).lower()
            if "xi-api-key" in serialized or "elevenlabs_api_key" in serialized:
                raise ValueError("secret-like key name present in persisted response evidence")

            # Alignment shape can differ by endpoint; require non-empty normalized evidence,
            # not a provider-specific internal schema.
            if not norm_json:
                raise ValueError("normalized alignment is empty")

            rows.append(
                {
                    "listen_order": ordinal,
                    "block_id": block_id,
                    "audio": rel_audio,
                    "audio_sha256": digest,
                    "audio_bytes": audio.stat().st_size,
                    "request_hash": request_hash,
                    "request_evidence": str(req.relative_to(root)),
                    "response_evidence": str(resp.relative_to(root)),
                    "raw_alignment": str(raw_align.relative_to(root)),
                    "normalized_alignment": str(norm_align.relative_to(root)),
                    "human_decision": "PENDING",
                    "allowed_decisions": ["PASS", "REPAIR", "RECAST", "STOP"],
                }
            )
        except Exception as exc:  # noqa: BLE001 - aggregate QC failures
            failures.append(f"{block_id}: {exc}")

    report = {
        "schema_version": "ivdivo.room917_ru_s0_artifact_qc/1.0",
        "status": "PASS_MACHINE_QC_HUMAN_LISTEN_REQUIRED" if not failures and len(rows) == len(selected) else "FAIL_MACHINE_QC",
        "selected_blocks": selected,
        "validated_blocks": len(rows),
        "failures": failures,
        "full_episode_promotion_allowed": False,
        "cast_lock_allowed_without_human_listen": False,
        "next_gate": "ROOM917_RU_S0_HUMAN_LISTEN_GATE",
    }
    (root / "S0_QC_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    index = {
        "schema_version": "ivdivo.room917_ru_s0_listening_index/1.0",
        "status": "READY_FOR_HUMAN_LISTEN" if report["status"].startswith("PASS") else "BLOCKED",
        "listen_in_order": rows,
        "founder_fast_questions_ru": [
            "Верю ли я, что это живой человек?",
            "Верю ли я, что он или она реально занят этой работой, а не читает текст?",
            "Слышу ли я типичный голос ИИ?",
            "Хочу ли я слушать этих людей ещё десять минут?",
        ],
        "promotion_rule": "NO_CAST_LOCK_AND_NO_FULL_E01_UNTIL_HUMAN_PASS",
    }
    (root / "S0_LISTENING_INDEX.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if failures or len(rows) != len(selected):
        for f in failures:
            print(f"FAIL: {f}")
        return 2

    print(f"PASS machine QC: {len(rows)} blocks. Human listen is still mandatory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
