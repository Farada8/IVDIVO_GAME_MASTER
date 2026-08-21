#!/usr/bin/env python3
"""Global candidate identity / namespace auditor for IVDIVO Self-Improvement.

This tool is intentionally NOT a promotion engine. It proves whether candidate
identifiers are globally coherent across configured candidate-bearing roots.

Statuses:
- PASS: no active identity collision and no index debt.
- PASS_WITH_TRACKED_DEBT: only explicitly tracked migration/index debt remains.
- FAIL: untracked ID collision, malformed record, dangling redirect, or namespace
  inconsistency.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

CID_RE = re.compile(r"^SI-\d{4}$")
DEFAULT_BASE = "31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json"
DEFAULT_EXT = "31_IDEAS/REGISTRY_EXTENSIONS"
DEFAULT_PENDING = "31_IDEAS/PENDING"
DEFAULT_FAMILY = "31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY_FAMILY.json"
DEFAULT_DEBT = "31_IDEAS/CANDIDATE_IDENTITY_MIGRATION_DEBT.json"

SEMANTIC_FIELDS = (
    "title",
    "candidate_type",
    "scope",
    "problem_or_opportunity",
    "proposed_mechanism",
    "dedupe_relation",
)


@dataclass(frozen=True)
class CandidateRecord:
    candidate_id: str
    source_path: str
    semantic_sha256: str
    title: str
    candidate_type: str
    status: str


@dataclass(frozen=True)
class RedirectRecord:
    old_candidate_id: str
    new_candidate_id: str
    source_path: str
    reason: str


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def semantic_payload(item: dict[str, Any]) -> dict[str, Any]:
    return {k: item.get(k) for k in SEMANTIC_FIELDS}


def semantic_sha256(item: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(semantic_payload(item))).hexdigest()


def validate_candidate(item: dict[str, Any], source_path: str) -> list[str]:
    errors: list[str] = []
    cid = item.get("candidate_id")
    if not isinstance(cid, str) or not CID_RE.fullmatch(cid):
        errors.append(f"INVALID_CANDIDATE_ID:{source_path}:{cid!r}")
    for field in ("title", "candidate_type", "status"):
        if not item.get(field):
            errors.append(f"MISSING_FIELD:{source_path}:{field}")
    if not item.get("problem_or_opportunity"):
        errors.append(f"MISSING_FIELD:{source_path}:problem_or_opportunity")
    if not item.get("proposed_mechanism"):
        errors.append(f"MISSING_FIELD:{source_path}:proposed_mechanism")
    return errors


def parse_record(item: dict[str, Any], source_path: str):
    if item.get("record_type") == "CANDIDATE_ID_REDIRECT":
        old = item.get("old_candidate_id")
        new = item.get("new_candidate_id")
        errors = []
        if not isinstance(old, str) or not CID_RE.fullmatch(old):
            errors.append(f"INVALID_REDIRECT_OLD:{source_path}:{old!r}")
        if not isinstance(new, str) or not CID_RE.fullmatch(new):
            errors.append(f"INVALID_REDIRECT_NEW:{source_path}:{new!r}")
        if old == new:
            errors.append(f"SELF_REDIRECT:{source_path}:{old}")
        if not item.get("reason"):
            errors.append(f"REDIRECT_WITHOUT_REASON:{source_path}")
        if errors:
            return None, errors
        return RedirectRecord(str(old), str(new), source_path, str(item["reason"])), []

    if "candidate_id" not in item:
        return None, []
    errors = validate_candidate(item, source_path)
    if errors:
        return None, errors
    return CandidateRecord(
        candidate_id=str(item["candidate_id"]),
        source_path=source_path,
        semantic_sha256=semantic_sha256(item),
        title=str(item.get("title", "")),
        candidate_type=str(item.get("candidate_type", "")),
        status=str(item.get("status", "")),
    ), []


def iter_candidate_objects(repo_root: Path, base: Path, directories: Iterable[Path]):
    base_raw = load_json(base)
    for idx, item in enumerate(base_raw.get("candidates", [])):
        if isinstance(item, dict):
            yield item, f"{base.relative_to(repo_root)}#candidates[{idx}]"
    for directory in directories:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.json")):
            raw = load_json(path)
            rel = str(path.relative_to(repo_root)).replace("\\", "/")
            if isinstance(raw, dict):
                yield raw, rel
            elif isinstance(raw, list):
                for idx, item in enumerate(raw):
                    if isinstance(item, dict):
                        yield item, f"{rel}[{idx}]"


def read_tracked_debt(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    raw = load_json(path)
    rows = raw.get("tracked_collisions", [])
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("candidate_id"), str):
            out[row["candidate_id"]] = row
    return out


def debt_matches(cid: str, records: list[CandidateRecord], debt: dict[str, dict[str, Any]]) -> bool:
    row = debt.get(cid)
    if not row:
        return False
    expected_paths = sorted(row.get("expected_source_paths", []))
    actual_paths = sorted(r.source_path for r in records)
    if expected_paths and expected_paths != actual_paths:
        return False
    expected_hashes = sorted(row.get("expected_semantic_sha256", []))
    actual_hashes = sorted(r.semantic_sha256 for r in records)
    if expected_hashes and expected_hashes != actual_hashes:
        return False
    return bool(row.get("repair_locator"))


def next_free_id(used: set[str], reserved: set[str] | None = None, start: int = 1) -> str:
    all_used = set(used)
    if reserved:
        all_used |= set(reserved)
    n = max(1, start)
    while True:
        cid = f"SI-{n:04d}"
        if cid not in all_used:
            return cid
        n += 1


def audit_repo(repo_root: Path, base_path: Path, directories: list[Path], family_path: Path | None = None, debt_path: Path | None = None) -> dict[str, Any]:
    records: list[CandidateRecord] = []
    redirects: list[RedirectRecord] = []
    errors: list[str] = []
    for item, source in iter_candidate_objects(repo_root, base_path, directories):
        record, parse_errors = parse_record(item, source)
        errors.extend(parse_errors)
        if isinstance(record, CandidateRecord):
            records.append(record)
        elif isinstance(record, RedirectRecord):
            redirects.append(record)

    by_id: dict[str, list[CandidateRecord]] = {}
    for record in records:
        by_id.setdefault(record.candidate_id, []).append(record)

    debt = read_tracked_debt(debt_path) if debt_path else {}
    collisions, tracked, duplicate_same = [], [], []
    for cid, rows in sorted(by_id.items()):
        if len(rows) <= 1:
            continue
        hashes = {r.semantic_sha256 for r in rows}
        item = {
            "candidate_id": cid,
            "records": [asdict(r) for r in rows],
            "classification": "ID_COLLISION_DIFFERENT_MECHANISM" if len(hashes) > 1 else "DUPLICATE_SAME_MECHANISM",
        }
        if len(hashes) == 1:
            duplicate_same.append(item)
        elif debt_matches(cid, rows, debt):
            tracked.append(item)
        else:
            collisions.append(item)

    active_ids = set(by_id)
    redirect_old: dict[str, RedirectRecord] = {}
    for redirect in redirects:
        if redirect.old_candidate_id in redirect_old:
            errors.append(f"DUPLICATE_REDIRECT:{redirect.old_candidate_id}")
        redirect_old[redirect.old_candidate_id] = redirect
        if redirect.new_candidate_id not in active_ids:
            errors.append(f"DANGLING_REDIRECT:{redirect.source_path}:{redirect.new_candidate_id}")

    indexed_extensions: set[str] = set()
    unindexed_extensions: list[str] = []
    if family_path and family_path.exists():
        family = load_json(family_path)
        indexed_extensions = set(family.get("known_extensions", []))
        ext_dir = next((d for d in directories if d.name == "REGISTRY_EXTENSIONS"), None)
        if ext_dir and ext_dir.exists():
            actual = {str(p.relative_to(repo_root)).replace("\\", "/") for p in ext_dir.glob("*.json")}
            unindexed_extensions = sorted(actual - indexed_extensions)

    status = "PASS"
    if errors or collisions:
        status = "FAIL"
    elif tracked or duplicate_same or unindexed_extensions:
        status = "PASS_WITH_TRACKED_DEBT"

    return {
        "status": status,
        "candidate_count": len(records),
        "active_candidate_ids": sorted(active_ids),
        "collisions": collisions,
        "tracked_collision_debt": tracked,
        "duplicate_same_mechanism": duplicate_same,
        "redirects": [asdict(r) for r in redirects],
        "unindexed_extensions": unindexed_extensions,
        "errors": sorted(errors),
        "next_free_candidate_id": next_free_id(active_ids),
        "promotion_eligible": status == "PASS",
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Audit global IVDIVO Self-Improvement candidate identity.")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--base", default=DEFAULT_BASE)
    p.add_argument("--extensions", default=DEFAULT_EXT)
    p.add_argument("--pending", default=DEFAULT_PENDING)
    p.add_argument("--family", default=DEFAULT_FAMILY)
    p.add_argument("--debt", default=DEFAULT_DEBT)
    args = p.parse_args()
    root = Path(args.repo_root).resolve()
    result = audit_repo(root, root / args.base, [root / args.extensions, root / args.pending], root / args.family, root / args.debt)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in {"PASS", "PASS_WITH_TRACKED_DEBT"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
