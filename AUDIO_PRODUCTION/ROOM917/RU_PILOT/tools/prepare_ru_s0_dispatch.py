#!/usr/bin/env python3
"""Compile ROOM917 RU S0 bundle into canonical Audio Studio dispatch blocks.

No provider call. No secret access. Produces exact identity manifest + fixture and
individual block JSON files consumed by audio/studio/controlled_provider_dispatch.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_BUNDLE = HERE.parent / "ROOM917_RU_S0_CANARY_BLOCK_BUNDLE_v1.0.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_text(block: dict) -> str:
    if block.get("block_type") == "TTD_BLOCK":
        return "\n".join(str(t.get("exact_text") or "") for t in block.get("turns", []))
    return str(block.get("exact_text") or block.get("performance_text") or "")


def collect_voice_ids(block: dict) -> list[str]:
    if block.get("block_type") == "TTD_BLOCK":
        return sorted({str(t["voice_id"]) for t in block.get("turns", []) if t.get("voice_id")})
    return [str(block["voice_id"])] if block.get("voice_id") else []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
    blocks = bundle["blocks"]
    args.out.mkdir(parents=True, exist_ok=True)
    block_dir = args.out / "blocks"
    block_dir.mkdir(exist_ok=True)

    manifest_blocks: dict[str, dict] = {}
    expected_blocks: dict[str, dict] = {}
    block_paths: list[str] = []

    for block in blocks:
        bid = block["block_id"]
        path = block_dir / f"{bid}.json"
        path.write_text(json.dumps(block, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        block_paths.append(str(path))
        fingerprint = {
            "block_type": block["block_type"],
            "model_id": block.get("model_id"),
            "language_code": block.get("language_code"),
            "voice_ids": collect_voice_ids(block),
            "exact_text_sha256": sha256_text(canonical_text(block)),
            "output_format": block.get("output_format"),
        }
        manifest_blocks[bid] = dict(fingerprint)
        expected_blocks[bid] = dict(fingerprint)

    manifest = {
        "schema_version": "ivdivo.room917_ru_s0_identity_manifest/1.0",
        "project_id": bundle["project_id"],
        "locale": bundle["locale"],
        "model_id": bundle["model_id"],
        "stage": "RU_S0_PUBLIC_CANARY",
        "blocks": manifest_blocks,
    }
    fixture = {
        "schema_version": "ivdivo.identity_fixture/1.0",
        "scalar_fields": {
            "project_id": bundle["project_id"],
            "locale": bundle["locale"],
            "model_id": bundle["model_id"],
            "stage": "RU_S0_PUBLIC_CANARY"
        },
        "blocks": expected_blocks,
    }

    manifest_path = args.out / "ROOM917_RU_S0_IDENTITY_MANIFEST.json"
    fixture_path = args.out / "ROOM917_RU_S0_IDENTITY_FIXTURE.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fixture_path.write_text(json.dumps(fixture, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    index = {
        "status": "PASS",
        "project_id": bundle["project_id"],
        "locale": bundle["locale"],
        "stage": "RU_S0_PUBLIC_CANARY",
        "block_count": len(blocks),
        "blocks": block_paths,
        "identity_manifest": str(manifest_path),
        "identity_fixture": str(fixture_path),
        "next_gate": "FRESH_AUTHENTICATED_PROVIDER_SNAPSHOT_THEN_BOUNDED_LIVE_DISPATCH"
    }
    (args.out / "ROOM917_RU_S0_DISPATCH_INDEX.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(index, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
