#!/usr/bin/env python3
"""Validate an authority-version chain without deciding story/canon."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any


def audit(data: dict[str, Any]) -> dict[str, Any]:
    rows = data.get("sources")
    errors = []
    if not isinstance(rows, list) or not rows:
        return {"status": "FAIL", "errors": ["SOURCES_REQUIRED"]}
    by_key = {}
    for row in rows:
        key = row.get("source_key")
        if not key or key in by_key:
            errors.append("DUPLICATE_OR_MISSING_SOURCE_KEY")
        else:
            by_key[key] = row
        if not isinstance(row.get("authority_rank"), int):
            errors.append(f"BAD_AUTHORITY_RANK:{key}")
        if row.get("disposition") not in {"CURRENT", "SUPERSEDED", "HISTORICAL", "REFERENCE_ONLY"}:
            errors.append(f"BAD_DISPOSITION:{key}")

    currents = [r for r in rows if r.get("disposition") == "CURRENT"]
    if len(currents) != 1:
        errors.append(f"CURRENT_COUNT:{len(currents)}")
    if currents:
        max_rank = max(int(r.get("authority_rank", -1)) for r in rows)
        if currents[0].get("authority_rank") != max_rank:
            errors.append("CURRENT_NOT_HIGHEST_RANK")

    graph = {k: list(v.get("supersedes") or []) for k, v in by_key.items()}
    for key, targets in graph.items():
        for target in targets:
            if target not in by_key:
                errors.append(f"UNKNOWN_SUPERSEDES_TARGET:{key}:{target}")

    visiting, done = set(), set()
    def visit(key):
        if key in visiting:
            errors.append(f"SUPERSESSION_CYCLE:{key}")
            return
        if key in done:
            return
        visiting.add(key)
        for target in graph.get(key, []):
            if target in by_key:
                visit(target)
        visiting.remove(key)
        done.add(key)
    for key in by_key:
        visit(key)

    reached = set()
    for targets in graph.values():
        reached.update(targets)
    for key, row in by_key.items():
        if row.get("disposition") == "SUPERSEDED" and key not in reached:
            errors.append(f"ORPHAN_SUPERSEDED:{key}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "project_id": data.get("project_id"),
        "current_source_key": currents[0].get("source_key") if len(currents) == 1 else None,
        "errors": sorted(set(errors)),
        "canon_mutation_authorized": False,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("manifest", type=Path)
    a = p.parse_args()
    result = audit(json.loads(a.manifest.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
