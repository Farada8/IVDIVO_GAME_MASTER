#!/usr/bin/env python3
"""Transactional writer/compactor for the IVDIVO Self-Improvement Registry family.

Writes candidate shards, not story/canon. The family pointer remains the current
machine registry map. Every mutation is snapshot-backed, stale-base checked,
duplicate-ID fail-closed, and rollback-capable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_FAMILY = Path("31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY_FAMILY.json")
ACTIVE_OR_TERMINAL = {
    "DISCOVERED", "CAPTURED", "DEDUPING", "DEVELOPING", "READY_FOR_PILOT", "PILOTING",
    "PILOT_PASS", "PILOT_FAIL", "PROMOTION_REVIEW", "PROMOTED_PROJECT",
    "PROMOTED_DOMAIN", "PROMOTED_UNIVERSAL", "APPLYING", "APPLIED_UNVERIFIED",
    "VERIFIED_CURRENT", "HOLD_WITH_TRIGGER", "REJECTED_WITH_REASON", "REJECTED",
    "SUPERSEDED", "ROLLED_BACK",
}
PROMOTED_OR_APPLIED = {
    "PROMOTED_PROJECT", "PROMOTED_DOMAIN", "PROMOTED_UNIVERSAL",
    "PROMOTED", "APPLYING", "APPLIED_UNVERIFIED", "VERIFIED_CURRENT",
}
TERMINAL = {"REJECTED_WITH_REASON", "REJECTED", "SUPERSEDED", "ROLLED_BACK"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def resolve_repo_path(repo_root: Path, value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else repo_root / p


def valid_candidate_id(value: str) -> bool:
    return len(value) == 7 and value.startswith("SI-") and value[3:].isdigit()


def validate_candidate(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "candidate_id", "title", "candidate_type", "status", "scope",
        "source_provenance", "problem_or_opportunity", "proposed_mechanism",
        "owner_role", "next_action", "next_gate",
    ]
    for field in required:
        if item.get(field) in (None, "", []):
            errors.append("MISSING_" + field.upper())
    cid = str(item.get("candidate_id", ""))
    if not valid_candidate_id(cid):
        errors.append("INVALID_CANDIDATE_ID")
    status = str(item.get("status", ""))
    if status not in ACTIVE_OR_TERMINAL:
        errors.append("INVALID_STATUS")
    prov = item.get("source_provenance")
    if not isinstance(prov, list) or not prov:
        errors.append("NO_PROVENANCE")
    elif any(not isinstance(x, dict) or not x.get("source_type") or not x.get("locator") for x in prov):
        errors.append("BAD_PROVENANCE")
    if status in PROMOTED_OR_APPLIED and not item.get("application_targets"):
        errors.append("PROMOTED_WITHOUT_TARGET")
    if status == "VERIFIED_CURRENT" and not item.get("verification_evidence"):
        errors.append("VERIFIED_WITHOUT_EVIDENCE")
    if status == "HOLD_WITH_TRIGGER" and not item.get("hold_trigger"):
        errors.append("HOLD_WITHOUT_TRIGGER")
    if status in TERMINAL and not item.get("terminal_reason"):
        errors.append("TERMINAL_WITHOUT_REASON")
    return sorted(set(errors))


def candidate_semantic_bytes(item: dict[str, Any]) -> bytes:
    return json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def collect_family(repo_root: Path, family: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, Path]]:
    candidates: dict[str, dict[str, Any]] = {}
    sources: dict[str, Path] = {}
    base = resolve_repo_path(repo_root, family["base_registry"])
    raw = load_json(base)
    for item in raw.get("candidates", []):
        cid = item.get("candidate_id")
        if not cid:
            raise ValueError("BASE_MISSING_CANDIDATE_ID")
        if cid in candidates:
            raise ValueError(f"DUPLICATE_ID:{cid}")
        candidates[cid] = item
        sources[cid] = base
    ext_dir = resolve_repo_path(repo_root, family["extension_directory"])
    if ext_dir.exists():
        for path in sorted(ext_dir.glob("*.json")):
            item = load_json(path)
            cid = item.get("candidate_id")
            if not cid:
                raise ValueError(f"EXTENSION_MISSING_CANDIDATE_ID:{path}")
            if cid in candidates:
                raise ValueError(f"DUPLICATE_ID:{cid}")
            candidates[cid] = item
            sources[cid] = path
    return candidates, sources


class RegistryLock:
    def __init__(self, path: Path):
        self.path = path
        self.fd: int | None = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise RuntimeError(f"REGISTRY_LOCKED:{self.path}") from exc
        os.write(self.fd, f"pid={os.getpid()}\n".encode())
        os.fsync(self.fd)
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.fd is not None:
            os.close(self.fd)
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def snapshot_dir(repo_root: Path, txn_id: str) -> Path:
    return repo_root / "31_IDEAS" / ".registry_txn_snapshots" / txn_id


def make_manifest(repo_root: Path, family_path: Path, shard_path: Path, family_before: bytes,
                  shard_before: bytes | None, txn_id: str) -> tuple[Path, dict[str, Any]]:
    snap = snapshot_dir(repo_root, txn_id)
    snap.mkdir(parents=True, exist_ok=False)
    (snap / "family.before").write_bytes(family_before)
    if shard_before is not None:
        (snap / "shard.before").write_bytes(shard_before)
    manifest = {
        "schema_version": "1.0",
        "txn_id": txn_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "family_path": str(family_path.relative_to(repo_root)),
        "shard_path": str(shard_path.relative_to(repo_root)),
        "family_before_sha256": sha256_bytes(family_before),
        "shard_existed_before": shard_before is not None,
        "shard_before_sha256": sha256_bytes(shard_before) if shard_before is not None else None,
        "status": "PREPARED",
    }
    atomic_write_bytes(snap / "manifest.json", dump_json_bytes(manifest))
    return snap, manifest


def restore_from_snapshot(repo_root: Path, snap: Path) -> dict[str, Any]:
    manifest_path = snap / "manifest.json"
    manifest = load_json(manifest_path)
    family_path = repo_root / manifest["family_path"]
    shard_path = repo_root / manifest["shard_path"]
    atomic_write_bytes(family_path, (snap / "family.before").read_bytes())
    if manifest["shard_existed_before"]:
        atomic_write_bytes(shard_path, (snap / "shard.before").read_bytes())
    else:
        try:
            shard_path.unlink()
        except FileNotFoundError:
            pass
    manifest["status"] = "ROLLED_BACK"
    manifest["rolled_back_at"] = datetime.now(timezone.utc).isoformat()
    atomic_write_bytes(manifest_path, dump_json_bytes(manifest))
    return manifest


def cmd_register(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    family_path = resolve_repo_path(repo_root, args.family).resolve()
    candidate_path = Path(args.candidate).resolve()
    family_before = family_path.read_bytes()
    actual_family_sha = sha256_bytes(family_before)
    if args.expected_family_sha and args.expected_family_sha != actual_family_sha:
        print(json.dumps({"status": "STALE_BASE", "expected": args.expected_family_sha, "actual": actual_family_sha}))
        return 3
    family = json.loads(family_before.decode("utf-8"))
    item = load_json(candidate_path)
    errors = validate_candidate(item)
    if errors:
        print(json.dumps({"status": "INVALID_CANDIDATE", "errors": errors}, ensure_ascii=False))
        return 2
    candidates, sources = collect_family(repo_root, family)
    cid = item["candidate_id"]
    if cid in candidates:
        if candidate_semantic_bytes(candidates[cid]) == candidate_semantic_bytes(item):
            print(json.dumps({"status": "NOOP_EXISTING", "candidate_id": cid, "source": str(sources[cid])}, ensure_ascii=False))
            return 0
        print(json.dumps({"status": "DUPLICATE_ID_CONFLICT", "candidate_id": cid, "existing": str(sources[cid])}, ensure_ascii=False))
        return 4

    ext_dir = resolve_repo_path(repo_root, family["extension_directory"])
    shard_path = ext_dir / f"{cid}.json"
    shard_before = shard_path.read_bytes() if shard_path.exists() else None
    txn_id = args.txn_id or (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:10])
    lock_path = repo_root / "31_IDEAS" / ".registry_family.lock"

    with RegistryLock(lock_path):
        snap, manifest = make_manifest(repo_root, family_path, shard_path, family_before, shard_before, txn_id)
        try:
            atomic_write_bytes(shard_path, dump_json_bytes(item))
            if os.getenv("IVDIVO_REGISTRY_TXN_FAIL_AFTER") == "SHARD":
                raise RuntimeError("INJECTED_FAILURE_AFTER_SHARD")
            rel = str(shard_path.relative_to(repo_root)).replace("\\", "/")
            known = list(family.get("known_extensions", []))
            if rel not in known:
                known.append(rel)
            family["known_extensions"] = sorted(known)
            family["updated"] = datetime.now(timezone.utc).date().isoformat()
            atomic_write_bytes(family_path, dump_json_bytes(family))
            if os.getenv("IVDIVO_REGISTRY_TXN_FAIL_AFTER") == "FAMILY":
                raise RuntimeError("INJECTED_FAILURE_AFTER_FAMILY")
            check_family = load_json(family_path)
            after_candidates, _ = collect_family(repo_root, check_family)
            if cid not in after_candidates:
                raise RuntimeError("READBACK_MISSING_CANDIDATE")
            if candidate_semantic_bytes(after_candidates[cid]) != candidate_semantic_bytes(item):
                raise RuntimeError("READBACK_CANDIDATE_MISMATCH")
            manifest["status"] = "COMMITTED"
            manifest["family_after_sha256"] = sha256_file(family_path)
            manifest["shard_after_sha256"] = sha256_file(shard_path)
            manifest["candidate_id"] = cid
            atomic_write_bytes(snap / "manifest.json", dump_json_bytes(manifest))
        except Exception as exc:
            restore_from_snapshot(repo_root, snap)
            print(json.dumps({"status": "ROLLED_BACK_ON_ERROR", "txn_id": txn_id, "error": str(exc)}, ensure_ascii=False))
            return 5
    print(json.dumps({
        "status": "COMMITTED", "txn_id": txn_id, "candidate_id": cid,
        "family_sha256": sha256_file(family_path), "shard_sha256": sha256_file(shard_path),
    }, ensure_ascii=False))
    return 0


def cmd_rollback(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    snap = snapshot_dir(repo_root, args.txn_id)
    if not snap.exists():
        print(json.dumps({"status": "UNKNOWN_TRANSACTION", "txn_id": args.txn_id}))
        return 2
    with RegistryLock(repo_root / "31_IDEAS" / ".registry_family.lock"):
        manifest = restore_from_snapshot(repo_root, snap)
    print(json.dumps({
        "status": "ROLLED_BACK", "txn_id": args.txn_id,
        "family_sha256": sha256_file(repo_root / manifest["family_path"]),
    }, ensure_ascii=False))
    return 0


def cmd_compact(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    family_path = resolve_repo_path(repo_root, args.family)
    family = load_json(family_path)
    candidates, sources = collect_family(repo_root, family)
    rows = [candidates[cid] for cid in sorted(candidates)]
    output = resolve_repo_path(repo_root, args.output)
    manifest_path = resolve_repo_path(repo_root, args.manifest)
    base_path = resolve_repo_path(repo_root, family["base_registry"])
    ext_files = sorted({p for p in sources.values() if p != base_path})
    compiled = {
        "schema_version": "1.0",
        "build_type": "DETERMINISTIC_REGISTRY_FAMILY_COMPACTION",
        "source_family": str(family_path.relative_to(repo_root)),
        "candidate_count": len(rows),
        "candidates": rows,
    }
    out_bytes = dump_json_bytes(compiled)
    manifest = {
        "schema_version": "1.0",
        "base_registry_sha256": sha256_file(base_path),
        "extension_shas": {str(p.relative_to(repo_root)).replace("\\", "/"): sha256_file(p) for p in ext_files},
        "family_sha256": sha256_file(family_path),
        "candidate_count": len(rows),
        "output_sha256": sha256_bytes(out_bytes),
        "output_path": str(output.relative_to(repo_root)),
        "readback_status": "PENDING",
    }
    atomic_write_bytes(output, out_bytes)
    reread = load_json(output)
    if len(reread.get("candidates", [])) != len(rows):
        raise RuntimeError("COMPACTION_ROUNDTRIP_COUNT_MISMATCH")
    ids = [x.get("candidate_id") for x in reread["candidates"]]
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        raise RuntimeError("COMPACTION_ROUNDTRIP_ID_FAILURE")
    manifest["readback_status"] = "PASS"
    atomic_write_bytes(manifest_path, dump_json_bytes(manifest))
    print(json.dumps({"status": "PASS", "candidate_count": len(rows), "output_sha256": manifest["output_sha256"]}))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Transactional IVDIVO improvement-registry family writer")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--family", default=str(DEFAULT_FAMILY))
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("register-candidate")
    r.add_argument("--candidate", required=True)
    r.add_argument("--expected-family-sha")
    r.add_argument("--txn-id")
    r.set_defaults(func=cmd_register)
    rb = sub.add_parser("rollback")
    rb.add_argument("txn_id")
    rb.set_defaults(func=cmd_rollback)
    c = sub.add_parser("compact")
    c.add_argument("--output", default="31_IDEAS/BUILD/CURRENT_IMPROVEMENT_REGISTRY_COMPACTED.json")
    c.add_argument("--manifest", default="31_IDEAS/BUILD/CURRENT_IMPROVEMENT_REGISTRY_COMPACTION_MANIFEST.json")
    c.set_defaults(func=cmd_compact)
    args = p.parse_args()
    try:
        return int(args.func(args))
    except (ValueError, json.JSONDecodeError, RuntimeError, OSError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
