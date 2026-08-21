#!/usr/bin/env python3
"""IVDIVO Audio Novel Studio production-control CLI.

Provider-neutral checkpoint utility for deterministic dry manifests, resume checks,
identity fixtures and scoped invalidation. It never dispatches paid requests.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from production_control import (
    canonical_hash,
    scoped_invalidation,
    validate_identity_fixture,
)


def _read(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write(path: str | Path, obj: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def freeze_manifest(manifest_path: str, fixture_path: str, checkpoint_path: str) -> dict[str, Any]:
    manifest = _read(manifest_path)
    fixture = _read(fixture_path)
    gate = validate_identity_fixture(manifest, fixture)
    checkpoint = {
        "status": "FROZEN_DRY_CHECKPOINT",
        "dispatch_allowed": False,
        "manifest_hash": canonical_hash(manifest),
        "fixture_hash": canonical_hash(fixture),
        "identity_gate": gate,
        "manifest": manifest,
    }
    _write(checkpoint_path, checkpoint)
    return checkpoint


def resume_checkpoint(checkpoint_path: str, fixture_path: str) -> dict[str, Any]:
    checkpoint = _read(checkpoint_path)
    fixture = _read(fixture_path)
    manifest = checkpoint.get("manifest")
    if not isinstance(manifest, dict):
        raise ValueError("CHECKPOINT_MANIFEST_MISSING")
    gate = validate_identity_fixture(manifest, fixture)
    if canonical_hash(manifest) != checkpoint.get("manifest_hash"):
        raise ValueError("CHECKPOINT_HASH_DRIFT")
    return {
        "status": "RESUME_PASS",
        "dispatch_allowed": False,
        "resent_requests": 0,
        "identity_gate": gate,
    }


def invalidate(dependency_map_path: str, changed: list[str]) -> dict[str, Any]:
    dependency_map = _read(dependency_map_path)
    return {
        "status": "INVALIDATION_PLAN",
        "changed": changed,
        "invalidated": scoped_invalidation(dependency_map, changed),
        "dispatch_allowed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(prog="ivdivo-audio-control")
    sub = parser.add_subparsers(dest="command", required=True)

    freeze = sub.add_parser("freeze")
    freeze.add_argument("--manifest", required=True)
    freeze.add_argument("--fixture", required=True)
    freeze.add_argument("--checkpoint", required=True)

    resume = sub.add_parser("resume")
    resume.add_argument("--checkpoint", required=True)
    resume.add_argument("--fixture", required=True)

    inv = sub.add_parser("invalidate")
    inv.add_argument("--dependency-map", required=True)
    inv.add_argument("--changed", action="append", required=True)

    args = parser.parse_args()
    if args.command == "freeze":
        result = freeze_manifest(args.manifest, args.fixture, args.checkpoint)
    elif args.command == "resume":
        result = resume_checkpoint(args.checkpoint, args.fixture)
    else:
        result = invalidate(args.dependency_map, args.changed)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
