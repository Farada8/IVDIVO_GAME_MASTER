#!/usr/bin/env python3
"""IVDIVO Self-Improvement Engine registry utility.

Stdlib-only helper for the canonical live registry:
31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json

This tool does not promote canon by itself. It enforces lifecycle hygiene,
anti-loss invariants, explicit next actions, provenance and verification state.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

DEFAULT_REGISTRY = Path("31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json")

TERMINAL = {
    "VERIFIED_CURRENT",
    "HOLD_WITH_TRIGGER",
    "REJECTED_WITH_REASON",
    "SUPERSEDED",
    "ROLLED_BACK",
}

ACTIVE = {
    "DISCOVERED",
    "CAPTURED",
    "DEDUPING",
    "DEVELOPING",
    "READY_FOR_PILOT",
    "PILOTING",
    "PILOT_PASS",
    "PILOT_FAIL",
    "PROMOTION_REVIEW",
    "PROMOTED_PROJECT",
    "PROMOTED_DOMAIN",
    "PROMOTED_UNIVERSAL",
    "APPLYING",
    "APPLIED_UNVERIFIED",
}

ALL_STATES = TERMINAL | ACTIVE

CANDIDATE_TYPES = {
    "STORY_IDEA",
    "STORY_ENGINE",
    "CHARACTER_OR_RELATIONSHIP_MECHANISM",
    "WORLD_OR_SYSTEM_MECHANISM",
    "CRAFT_MECHANISM",
    "PROMPT",
    "PROGRAM_OR_CODE",
    "PROCESS_OR_ROUTER_RULE",
    "REPAIR_MECHANISM",
    "REFERENCE_INSIGHT",
    "EXTERNAL_MODEL_FINDING",
    "HUMAN_OR_MARKET_SIGNAL",
    "AUDIO_VISUAL_PRODUCTION_MECHANISM",
    "BUG_OR_FAILURE_PATTERN",
    "TOOLING_OR_AUTOMATION",
    "OTHER_IMPROVEMENT",
}

SCOPES = {
    "PROJECT_ONLY",
    "BOOK_OR_SERIES",
    "GENRE_OR_DOMAIN",
    "UNIVERSAL_IVDIVO",
    "REFERENCE_ONLY",
}

PROMOTED = {"PROMOTED_PROJECT", "PROMOTED_DOMAIN", "PROMOTED_UNIVERSAL"}


def load_registry(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not isinstance(data.get("candidates"), list):
        raise ValueError("registry must contain a candidates[] array")
    return data


def save_registry(path: Path, data: dict[str, Any]) -> None:
    data["updated"] = date.today().isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(path)


def candidate_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for c in data["candidates"]:
        cid = c.get("candidate_id")
        if isinstance(cid, str):
            out[cid] = c
    return out


def next_id(data: dict[str, Any]) -> str:
    nums = []
    for c in data["candidates"]:
        cid = str(c.get("candidate_id", ""))
        if cid.startswith("SI-") and cid[3:].isdigit():
            nums.append(int(cid[3:]))
    return f"SI-{(max(nums) + 1 if nums else 1):04d}"


def audit(data: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    seen: set[str] = set()

    for idx, c in enumerate(data["candidates"]):
        cid = str(c.get("candidate_id") or f"INDEX-{idx}")
        status = c.get("status")

        if cid in seen:
            issues.append({"severity": "FAIL", "candidate_id": cid, "code": "DUPLICATE_ID", "message": "candidate_id is not unique"})
        seen.add(cid)

        if status not in ALL_STATES:
            issues.append({"severity": "FAIL", "candidate_id": cid, "code": "INVALID_STATUS", "message": f"unknown status: {status}"})

        required = [
            "title",
            "candidate_type",
            "scope",
            "problem_or_opportunity",
            "proposed_mechanism",
            "owner_role",
            "last_movement",
        ]
        for field in required:
            if not c.get(field):
                issues.append({"severity": "FAIL", "candidate_id": cid, "code": "MISSING_REQUIRED", "message": f"missing {field}"})

        if c.get("candidate_type") not in CANDIDATE_TYPES:
            issues.append({"severity": "FAIL", "candidate_id": cid, "code": "INVALID_TYPE", "message": f"unknown candidate_type: {c.get('candidate_type')}"})

        if c.get("scope") not in SCOPES:
            issues.append({"severity": "FAIL", "candidate_id": cid, "code": "INVALID_SCOPE", "message": f"unknown scope: {c.get('scope')}"})

        prov = c.get("source_provenance")
        if not isinstance(prov, list) or len(prov) == 0:
            issues.append({"severity": "FAIL", "candidate_id": cid, "code": "NO_PROVENANCE", "message": "candidate has no persisted source provenance"})
        else:
            for p in prov:
                if not isinstance(p, dict) or not p.get("source_type") or not p.get("locator"):
                    issues.append({"severity": "FAIL", "candidate_id": cid, "code": "BAD_PROVENANCE", "message": "source provenance requires source_type and locator"})

        if status not in TERMINAL:
            if not c.get("next_action"):
                issues.append({"severity": "FAIL", "candidate_id": cid, "code": "ORPHAN_NO_NEXT_ACTION", "message": "active candidate has no next_action"})
            if not c.get("next_gate"):
                issues.append({"severity": "FAIL", "candidate_id": cid, "code": "ORPHAN_NO_NEXT_GATE", "message": "active candidate has no next_gate"})

        if status == "HOLD_WITH_TRIGGER" and not c.get("hold_trigger"):
            issues.append({"severity": "FAIL", "candidate_id": cid, "code": "HOLD_WITHOUT_TRIGGER", "message": "HOLD_WITH_TRIGGER requires hold_trigger"})

        if status in {"REJECTED_WITH_REASON", "SUPERSEDED", "ROLLED_BACK"} and not c.get("terminal_reason"):
            issues.append({"severity": "FAIL", "candidate_id": cid, "code": "TERMINAL_WITHOUT_REASON", "message": f"{status} requires terminal_reason"})

        if status in PROMOTED | {"APPLYING", "APPLIED_UNVERIFIED", "VERIFIED_CURRENT"}:
            targets = c.get("application_targets")
            if not isinstance(targets, list) or not targets:
                issues.append({"severity": "FAIL", "candidate_id": cid, "code": "PROMOTED_WITHOUT_TARGET", "message": "promoted/applied candidate has no application_targets"})

        if status == "VERIFIED_CURRENT":
            evidence = c.get("verification_evidence")
            if not isinstance(evidence, list) or not evidence:
                issues.append({"severity": "FAIL", "candidate_id": cid, "code": "VERIFIED_WITHOUT_EVIDENCE", "message": "VERIFIED_CURRENT requires verification_evidence"})

        # Detect the classic failure: promotion declaration without actual application.
        if status in PROMOTED and not c.get("next_action"):
            issues.append({"severity": "FAIL", "candidate_id": cid, "code": "PROMOTION_STALLED", "message": "promotion must advance to application with explicit next_action"})

    return issues


def cmd_audit(args: argparse.Namespace) -> int:
    data = load_registry(Path(args.registry))
    issues = audit(data)
    failures = [x for x in issues if x["severity"] == "FAIL"]
    if args.json:
        print(json.dumps({"ok": not failures, "issues": issues}, ensure_ascii=False, indent=2))
    else:
        if not issues:
            print(f"PASS: {len(data['candidates'])} candidates; anti-loss and promotion-integrity checks green")
        else:
            for x in issues:
                print(f"{x['severity']} {x['candidate_id']} {x['code']}: {x['message']}")
            print(f"RESULT: {'FAIL' if failures else 'PASS_WITH_WARNINGS'}; issues={len(issues)}")
    return 1 if failures else 0


def cmd_list(args: argparse.Namespace) -> int:
    data = load_registry(Path(args.registry))
    rows = data["candidates"]
    if args.status:
        rows = [c for c in rows if c.get("status") == args.status]
    if args.scope:
        rows = [c for c in rows if c.get("scope") == args.scope]
    for c in rows:
        print(f"{c.get('candidate_id')}\t{c.get('status')}\t{c.get('scope')}\t{c.get('title')}\tNEXT={c.get('next_action')}")
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    path = Path(args.registry)
    data = load_registry(path)
    cid = next_id(data)
    candidate = {
        "candidate_id": cid,
        "title": args.title,
        "candidate_type": args.type,
        "status": "CAPTURED",
        "scope": args.scope,
        "source_provenance": [{
            "source_type": args.source_type,
            "locator": args.source,
            "version": None,
            "hash": None,
            "date": date.today().isoformat(),
            "notes": args.source_note,
        }],
        "problem_or_opportunity": args.problem,
        "proposed_mechanism": args.mechanism,
        "dedupe_relation": "NEW",
        "related_candidates": [],
        "expected_benefit": args.benefit,
        "evidence_state": "HYPOTHESIS",
        "priority_vector": {
            "impact": args.impact,
            "recurrence": args.recurrence,
            "effort": args.effort,
            "regression_risk": args.risk,
            "reversibility": args.reversibility,
            "urgency": args.urgency,
            "affected_surface": args.surface,
        },
        "development_contract": None,
        "pilot_evidence": [],
        "red_team_findings": [],
        "promotion_level": "NONE",
        "application_targets": [],
        "verification_evidence": [],
        "protected_authorities": args.protect or [],
        "owner_role": args.owner,
        "next_action": args.next_action or "Run dedupe/classification and write development contract.",
        "next_gate": args.next_gate or "DEDUPE_AND_DEVELOPMENT_GATE",
        "hold_trigger": None,
        "terminal_reason": None,
        "last_movement": date.today().isoformat(),
        "notes": args.notes,
    }
    data["candidates"].append(candidate)
    save_registry(path, data)
    print(cid)
    return 0


def cmd_advance(args: argparse.Namespace) -> int:
    path = Path(args.registry)
    data = load_registry(path)
    cmap = candidate_map(data)
    if args.id not in cmap:
        print(f"unknown candidate: {args.id}", file=sys.stderr)
        return 2
    c = cmap[args.id]
    if args.status not in ALL_STATES:
        print(f"invalid status: {args.status}", file=sys.stderr)
        return 2
    c["status"] = args.status
    if args.next_action is not None:
        c["next_action"] = args.next_action
    if args.next_gate is not None:
        c["next_gate"] = args.next_gate
    if args.evidence:
        c.setdefault("verification_evidence", []).append(args.evidence)
    if args.hold_trigger is not None:
        c["hold_trigger"] = args.hold_trigger
    if args.reason is not None:
        c["terminal_reason"] = args.reason
    c["last_movement"] = date.today().isoformat()

    issues = [i for i in audit(data) if i["candidate_id"] == args.id and i["severity"] == "FAIL"]
    if issues and not args.force:
        for i in issues:
            print(f"BLOCK {i['code']}: {i['message']}", file=sys.stderr)
        print("candidate not saved; use the required fields instead of forcing an invalid lifecycle", file=sys.stderr)
        return 1

    save_registry(path, data)
    print(f"{args.id} -> {args.status}")
    return 0


def cmd_relevant(args: argparse.Namespace) -> int:
    data = load_registry(Path(args.registry))
    q = args.query.casefold()
    scored: list[tuple[int, dict[str, Any]]] = []
    for c in data["candidates"]:
        hay = " ".join(str(c.get(k, "")) for k in ["title", "problem_or_opportunity", "proposed_mechanism", "scope", "candidate_type", "notes"]).casefold()
        score = sum(1 for token in q.split() if token in hay)
        if score:
            scored.append((score, c))
    scored.sort(key=lambda x: (-x[0], x[1].get("candidate_id", "")))
    for score, c in scored[: args.limit]:
        print(f"{score}\t{c.get('candidate_id')}\t{c.get('status')}\t{c.get('title')}\tNEXT={c.get('next_action')}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="IVDIVO Self-Improvement Engine registry utility")
    p.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("audit", help="run anti-loss and promotion-integrity audit")
    a.add_argument("--json", action="store_true")
    a.set_defaults(func=cmd_audit)

    l = sub.add_parser("list", help="list candidates")
    l.add_argument("--status")
    l.add_argument("--scope")
    l.set_defaults(func=cmd_list)

    c = sub.add_parser("capture", help="capture a new improvement candidate")
    c.add_argument("--title", required=True)
    c.add_argument("--type", required=True, choices=sorted(CANDIDATE_TYPES))
    c.add_argument("--scope", required=True, choices=sorted(SCOPES))
    c.add_argument("--source-type", required=True)
    c.add_argument("--source", required=True)
    c.add_argument("--source-note")
    c.add_argument("--problem", required=True)
    c.add_argument("--mechanism", required=True)
    c.add_argument("--benefit")
    c.add_argument("--owner", default="A00 Router / Improvement Reconciler")
    c.add_argument("--next-action")
    c.add_argument("--next-gate")
    c.add_argument("--protect", action="append")
    c.add_argument("--notes")
    c.add_argument("--impact", default="MEDIUM", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    c.add_argument("--recurrence", default="RECURRING", choices=["ONE_OFF", "RECURRING", "SYSTEMIC"])
    c.add_argument("--effort", default="MEDIUM", choices=["LOW", "MEDIUM", "HIGH"])
    c.add_argument("--risk", default="MEDIUM", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    c.add_argument("--reversibility", default="EASY", choices=["EASY", "MODERATE", "HARD", "IRREVERSIBLE"])
    c.add_argument("--urgency", default="MEDIUM", choices=["LOW", "MEDIUM", "HIGH"])
    c.add_argument("--surface", default="DOMAIN", choices=["LOCAL", "DOMAIN", "PORTFOLIO"])
    c.set_defaults(func=cmd_capture)

    adv = sub.add_parser("advance", help="advance one candidate through the lifecycle")
    adv.add_argument("id")
    adv.add_argument("--status", required=True, choices=sorted(ALL_STATES))
    adv.add_argument("--next-action")
    adv.add_argument("--next-gate")
    adv.add_argument("--evidence")
    adv.add_argument("--hold-trigger")
    adv.add_argument("--reason")
    adv.add_argument("--force", action="store_true", help="emergency only; bypass lifecycle audit")
    adv.set_defaults(func=cmd_advance)

    r = sub.add_parser("relevant", help="surface candidates relevant to an active task")
    r.add_argument("query")
    r.add_argument("--limit", type=int, default=10)
    r.set_defaults(func=cmd_relevant)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except FileNotFoundError as e:
        print(f"registry not found: {e}", file=sys.stderr)
        return 2
    except (ValueError, json.JSONDecodeError) as e:
        print(f"registry error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
