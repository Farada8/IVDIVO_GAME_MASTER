#!/usr/bin/env python3
"""Provider-neutral freshness gate for durable project-state authority snapshots.

This tool never decides canon. It only detects whether a state must be re-read/rebased
before continuation because an observed authority identity/revision/order changed.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime
from pathlib import Path
from typing import Any


def _dt(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def audit(snapshot: dict[str, Any], observations: dict[str, Any]) -> dict[str, Any]:
    errors, stale, review = [], [], []
    base_rows = snapshot.get("sources")
    live_rows = observations.get("sources")
    if not isinstance(base_rows, list) or not base_rows:
        return {"status": "FAIL_CONTRACT", "errors": ["SNAPSHOT_SOURCES_REQUIRED"]}
    if not isinstance(live_rows, list) or not live_rows:
        return {"status": "FAIL_CONTRACT", "errors": ["OBSERVATION_SOURCES_REQUIRED"]}

    base, live = {}, {}
    for row in base_rows:
        key = row.get("source_key")
        if not key or key in base:
            errors.append("SNAPSHOT_DUPLICATE_OR_MISSING_SOURCE_KEY")
        else:
            base[key] = row
    for row in live_rows:
        key = row.get("source_key")
        if not key or key in live:
            errors.append("OBSERVATION_DUPLICATE_OR_MISSING_SOURCE_KEY")
        else:
            live[key] = row

    for key, b in base.items():
        c = live.get(key)
        if not c:
            review.append({"source_key": key, "reason": "SOURCE_NOT_OBSERVED"})
            continue
        if b.get("locator") != c.get("locator"):
            stale.append({"source_key": key, "reason": "LOCATOR_CHANGED"})
        br, cr = b.get("revision"), c.get("revision")
        if br and cr and br != cr:
            stale.append({"source_key": key, "reason": "REVISION_CHANGED", "baseline": br, "current": cr})
        bm, cm = _dt(b.get("modified_at")), _dt(c.get("modified_at"))
        if bm and cm and cm > bm:
            stale.append({"source_key": key, "reason": "MODIFIED_AFTER_SNAPSHOT", "baseline": b.get("modified_at"), "current": c.get("modified_at")})
        if b.get("title") and c.get("title") and b["title"] != c["title"]:
            stale.append({"source_key": key, "reason": "TITLE_CHANGED", "baseline": b["title"], "current": c["title"]})

    baseline_current = [r for r in base_rows if r.get("disposition") == "CURRENT"]
    live_current = [r for r in live_rows if r.get("disposition") == "CURRENT"]
    if len(baseline_current) != 1:
        errors.append("SNAPSHOT_REQUIRES_EXACTLY_ONE_CURRENT")
    if len(live_current) != 1:
        errors.append("OBSERVATION_REQUIRES_EXACTLY_ONE_CURRENT")
    if len(baseline_current) == 1 and len(live_current) == 1:
        bcur, lcur = baseline_current[0], live_current[0]
        if bcur.get("source_key") != lcur.get("source_key"):
            stale.append({"reason": "CURRENT_AUTHORITY_CHANGED", "baseline": bcur.get("source_key"), "current": lcur.get("source_key")})
        if int(lcur.get("authority_rank", 0)) < int(bcur.get("authority_rank", 0)):
            errors.append("AUTHORITY_RANK_REGRESSION")

    if errors:
        status = "FAIL_CONTRACT"
    elif stale:
        status = "STALE_REBASE_REQUIRED"
    elif review:
        status = "REVIEW_REQUIRED"
    else:
        status = "PASS_FRESH"
    return {"status": status, "project_id": snapshot.get("project_id"), "stale": stale, "review": review, "errors": errors}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--snapshot", type=Path, required=True)
    p.add_argument("--observations", type=Path, required=True)
    a = p.parse_args()
    result = audit(json.loads(a.snapshot.read_text(encoding="utf-8")), json.loads(a.observations.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS_FRESH" else (2 if result["status"] == "REVIEW_REQUIRED" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
