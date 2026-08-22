#!/usr/bin/env python3
"""Route ROOM917 AutoMix work under the project-wide fail-closed non-stop law."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from IVDIVO_NARRATIVE_OS.tools.local_gate_router import (  # noqa: E402
    GLOBAL_GATE_TYPES,
    LOCAL_GATE_TYPES,
    Obligation,
    route,
)

ALLOWED_STATUS = {"READY", "BLOCKED", "DONE"}


def evaluate(queue: dict) -> dict:
    errors: list[str] = []
    if queue.get("schema_version") != "ivdivo.room917_automix_continuation_queue/1.0":
        errors.append("QUEUE_SCHEMA_INVALID")
    rows = queue.get("obligations")
    if not isinstance(rows, list) or not rows:
        errors.append("OBLIGATIONS_MISSING")
        rows = []

    ids: set[str] = set()
    obligations: list[Obligation] = []
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"ROW_{idx}_NOT_OBJECT")
            continue
        oid = row.get("id")
        if not isinstance(oid, str) or not oid:
            errors.append(f"ROW_{idx}_ID_INVALID")
            continue
        if oid in ids:
            errors.append(f"DUPLICATE_ID:{oid}")
            continue
        ids.add(oid)
        status = row.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"STATUS_INVALID:{oid}")
        gate_type = row.get("gate_type")
        if status == "BLOCKED" and gate_type not in (GLOBAL_GATE_TYPES | LOCAL_GATE_TYPES):
            errors.append(f"BLOCKED_GATE_TYPE_INVALID:{oid}")
        if status != "BLOCKED" and gate_type is not None:
            errors.append(f"NONBLOCKED_GATE_TYPE_MUST_BE_NULL:{oid}")
        priority = row.get("priority")
        if not isinstance(priority, int) or isinstance(priority, bool) or priority < 0:
            errors.append(f"PRIORITY_INVALID:{oid}")
        deps = row.get("dependencies", [])
        if not isinstance(deps, list) or any(not isinstance(x, str) or not x for x in deps):
            errors.append(f"DEPENDENCIES_INVALID:{oid}")
            deps = []
        obligations.append(
            Obligation(
                id=oid,
                priority=priority if isinstance(priority, int) and not isinstance(priority, bool) else 999999,
                status=status if status in ALLOWED_STATUS else "BLOCKED",
                gate_type=gate_type,
                dependencies=tuple(deps),
                scope=str(row.get("scope") or "ROOM917_E01_AUTOMIX"),
            )
        )

    known = {o.id for o in obligations}
    for o in obligations:
        for dep in o.dependencies:
            if dep not in known:
                errors.append(f"UNKNOWN_DEPENDENCY:{o.id}:{dep}")

    if errors:
        return {
            "schema_version": "ivdivo.room917_automix_continuation_decision/1.0",
            "status": "FAIL_QUEUE_INVALID",
            "action": "GLOBAL_STOP",
            "selected_id": None,
            "errors": errors,
            "law": queue.get("law"),
        }

    decision = route(obligations)
    return {
        "schema_version": "ivdivo.room917_automix_continuation_decision/1.0",
        "status": "PASS_ROUTE_DECISION",
        "action": decision.action,
        "selected_id": decision.selected_id,
        "blocked_local": list(decision.blocked_local),
        "blocked_global": list(decision.blocked_global),
        "reason": decision.reason,
        "law": queue.get("law"),
        "non_stop_preserved": decision.action in {"CONTINUE", "LOCAL_GATE_ONLY_NO_READY_SIBLING", "QUEUE_EMPTY"},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    queue = json.loads(args.queue.read_text(encoding="utf-8"))
    result = evaluate(queue)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["action"], result.get("selected_id"))
    return 0 if result.get("status") == "PASS_ROUTE_DECISION" else 4


if __name__ == "__main__":
    raise SystemExit(main())
