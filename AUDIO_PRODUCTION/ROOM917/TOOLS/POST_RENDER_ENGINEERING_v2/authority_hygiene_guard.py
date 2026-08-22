#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PASS = "PASS_CURRENT_AUTHORITY"
QUARANTINE = "QUARANTINE_LEGACY_CONFLICT"
HOLD = "HOLD_UNVERIFIED_AUTHORITY"


def _norm(text: str) -> str:
    return " ".join((text or "").lower().split())


def evaluate_authority(candidate: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
    candidate_id = str(candidate.get("drive_id") or "")
    title = str(candidate.get("title") or "")
    content = str(candidate.get("content") or "")
    haystack = _norm(title + "\n" + content)

    reasons: List[str] = []
    stale_hits: List[str] = []
    for marker in rules.get("legacy_conflict_markers", []):
        if _norm(str(marker)) in haystack:
            stale_hits.append(str(marker))

    if stale_hits:
        reasons.append("legacy_conflict_markers=" + json.dumps(stale_hits, ensure_ascii=False))
        return {
            "status": QUARANTINE,
            "candidate_drive_id": candidate_id or None,
            "title": title,
            "reasons": reasons,
        }

    allowed_ids = set(map(str, rules.get("allowed_drive_ids", [])))
    required_markers = list(map(str, rules.get("required_current_markers", [])))

    if candidate_id in allowed_ids:
        missing = [m for m in required_markers if _norm(m) not in haystack]
        if missing:
            reasons.append(
                "allowlisted_id_but_required_markers_missing="
                + json.dumps(missing, ensure_ascii=False)
            )
            return {
                "status": HOLD,
                "candidate_drive_id": candidate_id,
                "title": title,
                "reasons": reasons,
            }
        reasons.append("exact_allowlisted_drive_id")
        reasons.append("required_current_markers_present")
        return {
            "status": PASS,
            "candidate_drive_id": candidate_id,
            "title": title,
            "reasons": reasons,
        }

    reasons.append("candidate_not_allowlisted")
    return {
        "status": HOLD,
        "candidate_drive_id": candidate_id or None,
        "title": title,
        "reasons": reasons,
    }


def load_json(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("--rules", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()

    candidate = load_json(args.candidate)
    rules = load_json(args.rules)
    result = evaluate_authority(candidate, rules)

    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

    if result["status"] == PASS:
        return 0
    if result["status"] == QUARANTINE:
        return 3
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
