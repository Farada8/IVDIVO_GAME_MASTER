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


def _exact_authority_match(candidate: Dict[str, Any], allowed: Dict[str, Any]) -> bool:
    for field in ("drive_id", "revision_id", "title"):
        expected = str(allowed.get(field) or "")
        actual = str(candidate.get(field) or "")
        if expected and actual != expected:
            return False
    return bool(str(allowed.get("drive_id") or ""))


def evaluate_authority(candidate: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
    candidate_id = str(candidate.get("drive_id") or "")
    title = str(candidate.get("title") or "")
    content = str(candidate.get("content") or "")
    haystack = _norm(title + "\n" + content)

    stale_hits: List[str] = []
    if content:
        for marker in rules.get("legacy_conflict_markers", []):
            if _norm(str(marker)) in haystack:
                stale_hits.append(str(marker))

    if stale_hits:
        return {
            "status": QUARANTINE,
            "candidate_drive_id": candidate_id or None,
            "candidate_revision_id": candidate.get("revision_id"),
            "title": title,
            "reasons": [
                "legacy_conflict_markers="
                + json.dumps(stale_hits, ensure_ascii=False)
            ],
        }

    exact_match = any(
        _exact_authority_match(candidate, allowed)
        for allowed in rules.get("allowed_authorities", [])
    )

    if exact_match:
        reasons = ["exact_allowlisted_authority_identity"]
        if content:
            required = list(map(str, rules.get("required_current_markers", [])))
            missing = [m for m in required if _norm(m) not in haystack]
            if missing:
                return {
                    "status": HOLD,
                    "candidate_drive_id": candidate_id or None,
                    "candidate_revision_id": candidate.get("revision_id"),
                    "title": title,
                    "reasons": [
                        "allowlisted_identity_but_required_markers_missing="
                        + json.dumps(missing, ensure_ascii=False)
                    ],
                }
            reasons.append("required_current_markers_present")
        else:
            reasons.append("metadata_only_preflight_exact_id_revision_title")
        return {
            "status": PASS,
            "candidate_drive_id": candidate_id or None,
            "candidate_revision_id": candidate.get("revision_id"),
            "title": title,
            "reasons": reasons,
        }

    same_id_known = any(
        candidate_id and candidate_id == str(a.get("drive_id") or "")
        for a in rules.get("allowed_authorities", [])
    )
    reason = (
        "known_drive_id_but_revision_or_title_mismatch"
        if same_id_known
        else "candidate_not_allowlisted"
    )
    return {
        "status": HOLD,
        "candidate_drive_id": candidate_id or None,
        "candidate_revision_id": candidate.get("revision_id"),
        "title": title,
        "reasons": [reason],
    }


def load_json(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("--rules", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()

    result = evaluate_authority(load_json(args.candidate), load_json(args.rules))
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
