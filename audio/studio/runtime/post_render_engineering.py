#!/usr/bin/env python3
"""Universal post-render engineering control plane.

The project pilots own project data. This module owns evidence semantics, immutable
patch lifecycle, artifact verification and project-neutral regression ranges.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable
import json

from production_control import canonical_hash
from post_render_contracts import canonical_interval

ARTIFACT_PASS_STATES = {
    "PASS", "AUTHORIZED", "REGRESSION_PASS", "HUMAN_PASS", "PASS_EVIDENCE_COMPLETE",
}
PATCH_STATES = {
    "PLANNED", "AUTHORIZED", "RENDERED", "REGRESSION_PASS", "HUMAN_PASS", "REJECTED", "QUARANTINED",
}
TERMINAL_PATCH_STATES = {"HUMAN_PASS", "REJECTED"}


def file_sha256(path: str | Path) -> str:
    h = sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verify_json_artifact(
    path: str | Path,
    *,
    expected_schema_prefix: str | None = None,
    expected_sha256: str | None = None,
    require_status: bool = True,
) -> dict[str, Any]:
    """File existence is not evidence. Verify bytes, schema and semantic status."""
    p = Path(path)
    if not p.is_file():
        return {"status": "BLOCKED_MISSING", "path": str(p), "verified": False}
    actual_sha = file_sha256(p)
    if expected_sha256 and actual_sha.lower() != expected_sha256.lower():
        return {
            "status": "FAIL_HASH_DRIFT", "path": str(p), "verified": False,
            "actual_sha256": actual_sha, "expected_sha256": expected_sha256.lower(),
        }
    try:
        obj = read_json(p)
    except Exception as exc:
        return {"status": "FAIL_JSON_PARSE", "path": str(p), "verified": False, "error_type": type(exc).__name__}
    schema = obj.get("schema_version") or obj.get("schema")
    if expected_schema_prefix and (not isinstance(schema, str) or not schema.startswith(expected_schema_prefix)):
        return {
            "status": "FAIL_SCHEMA", "path": str(p), "verified": False,
            "schema": schema, "expected_schema_prefix": expected_schema_prefix,
        }
    semantic_status = obj.get("status")
    if require_status and semantic_status not in ARTIFACT_PASS_STATES:
        return {
            "status": "HOLD_SEMANTIC_STATUS", "path": str(p), "verified": False,
            "artifact_status": semantic_status, "sha256": actual_sha, "schema": schema,
        }
    return {
        "status": "PASS", "verified": True, "path": str(p), "sha256": actual_sha,
        "schema": schema, "artifact_status": semantic_status, "artifact": obj,
    }


@dataclass
class PatchAttempt:
    patch_id: str
    authorization_hash: str
    source_master_sha256: str
    state: str = "PLANNED"
    rendered_sha256: str | None = None
    regression_sha256: str | None = None
    human_evidence_sha256: str | None = None


class PatchLedger:
    """Restart-safe patch lineage; accepted work may not be silently rewritten."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.attempts: dict[str, PatchAttempt] = {}
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.attempts = {key: PatchAttempt(**value) for key, value in raw.items()}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {key: asdict(value) for key, value in sorted(self.attempts.items())}
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def plan(self, *, patch_id: str, authorization_hash: str, source_master_sha256: str) -> str:
        current = self.attempts.get(patch_id)
        if current:
            if current.authorization_hash != authorization_hash or current.source_master_sha256 != source_master_sha256:
                return "HOLD_IDENTITY_DRIFT"
            if current.state in {"REGRESSION_PASS", "HUMAN_PASS"}:
                return f"REUSE_{current.state}"
            if current.state == "QUARANTINED":
                return "RECONCILIATION_REQUIRED"
            return f"EXISTS_{current.state}"
        self.attempts[patch_id] = PatchAttempt(
            patch_id=patch_id,
            authorization_hash=authorization_hash,
            source_master_sha256=source_master_sha256,
        )
        self._save()
        return "PLANNED"

    def transition(
        self,
        patch_id: str,
        state: str,
        *,
        rendered_sha256: str | None = None,
        regression_sha256: str | None = None,
        human_evidence_sha256: str | None = None,
    ) -> None:
        if state not in PATCH_STATES:
            raise ValueError("PATCH_STATE_INVALID")
        if patch_id not in self.attempts:
            raise KeyError(patch_id)
        current = self.attempts[patch_id]
        if current.state in TERMINAL_PATCH_STATES and state != current.state:
            raise ValueError("TERMINAL_PATCH_ATTEMPT_IMMUTABLE")
        allowed = {
            "PLANNED": {"AUTHORIZED", "REJECTED", "QUARANTINED"},
            "AUTHORIZED": {"RENDERED", "REJECTED", "QUARANTINED"},
            "RENDERED": {"REGRESSION_PASS", "REJECTED", "QUARANTINED"},
            "REGRESSION_PASS": {"HUMAN_PASS", "REJECTED", "QUARANTINED", "REGRESSION_PASS"},
            "HUMAN_PASS": {"HUMAN_PASS"},
            "REJECTED": {"REJECTED"},
            "QUARANTINED": {"AUTHORIZED", "REJECTED", "QUARANTINED"},
        }
        if state not in allowed[current.state]:
            raise ValueError(f"PATCH_TRANSITION_INVALID:{current.state}->{state}")
        current.state = state
        if rendered_sha256 is not None:
            current.rendered_sha256 = rendered_sha256
        if regression_sha256 is not None:
            current.regression_sha256 = regression_sha256
        if human_evidence_sha256 is not None:
            current.human_evidence_sha256 = human_evidence_sha256
        self._save()

    def snapshot(self) -> dict[str, Any]:
        return {key: asdict(value) for key, value in self.attempts.items()}


def validate_patch_plan(plan: dict[str, Any]) -> dict[str, Any]:
    patches = plan.get("patches")
    if not isinstance(patches, list):
        raise ValueError("PATCH_PLAN_PATCHES_MISSING")
    seen: set[str] = set()
    for patch in patches:
        pid = patch.get("patch_id")
        if not pid or pid in seen:
            raise ValueError("PATCH_ID_MISSING_OR_DUPLICATE")
        seen.add(str(pid))
        canonical_interval({
            "start_seconds": patch.get("interval_start_seconds"),
            "end_seconds": patch.get("interval_end_seconds"),
        })
        if not patch.get("source_master_sha256"):
            raise ValueError(f"PATCH_MASTER_SHA_MISSING:{pid}")
        if not patch.get("authorization_hash"):
            raise ValueError(f"PATCH_AUTHORIZATION_HASH_MISSING:{pid}")
    return {"status": "PASS", "patch_count": len(patches), "plan_hash": canonical_hash(plan)}


def validate_regression_ranges(
    before_sha256: str,
    after_sha256: str,
    *,
    authorized_ranges: Iterable[dict[str, Any]],
    protected_ranges: Iterable[dict[str, Any]],
    changed_ranges: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Project-neutral logical regression contract over measured changed ranges.

    Byte-comparison implementations may produce changed_ranges. This validator has no
    hard-coded Scene3 time and rejects any changed range not inside an authorized range
    or intersecting a protected range.
    """
    if before_sha256 == after_sha256:
        return {"status": "FAIL_NO_CHANGE", "pass": False}
    auth = [canonical_interval(row) for row in authorized_ranges]
    protected = [canonical_interval(row) for row in protected_ranges]
    changed = [canonical_interval(row) for row in changed_ranges]
    violations: list[dict[str, Any]] = []
    for item in changed:
        inside = any(
            item["start_seconds"] >= a["start_seconds"] and item["end_seconds"] <= a["end_seconds"]
            for a in auth
        )
        if not inside:
            violations.append({"type": "UNAUTHORIZED_CHANGE", "interval": item})
        for p in protected:
            if max(item["start_seconds"], p["start_seconds"]) < min(item["end_seconds"], p["end_seconds"]):
                violations.append({"type": "PROTECTED_RANGE_CHANGED", "interval": item, "protected": p})
    return {
        "status": "PASS" if not violations else "FAIL",
        "pass": not violations,
        "violations": violations,
        "authorized_range_count": len(auth),
        "protected_range_count": len(protected),
        "changed_range_count": len(changed),
    }


def stage_router(evidence: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Route by verified evidence, never by filename existence alone."""
    order = [
        ("MASTER_BYTE_ESCROW", "master"),
        ("CUE_LINEAGE", "lineage"),
        ("ACCEPTED_TIMING", "timing"),
        ("INTERVAL_ANALYSIS", "intervals"),
        ("INTERVAL_CLASSIFICATION", "classification"),
        ("PATCH_AUTHORIZATION", "authorization"),
        ("PATCH_RENDER", "render"),
        ("REGRESSION_GATE", "regression"),
        ("HUMAN_LISTEN", "human"),
    ]
    stages: list[dict[str, Any]] = []
    blocked = False
    next_stage: str | None = None
    for stage, key in order:
        item = evidence.get(key) or {}
        verified = bool(item.get("verified")) and item.get("status") in ARTIFACT_PASS_STATES | {"PASS"}
        if blocked:
            stages.append({"stage": stage, "status": "BLOCKED_UPSTREAM"})
            continue
        if verified:
            stages.append({"stage": stage, "status": "PASS", "evidence_sha256": item.get("sha256")})
        else:
            stages.append({"stage": stage, "status": "READY_OR_HOLD", "reason": item.get("status") or "EVIDENCE_MISSING"})
            blocked = True
            next_stage = stage
    return {
        "status": "COMPLETE_TO_HUMAN" if next_stage is None else "HOLD",
        "next_stage": next_stage,
        "stages": stages,
        "router_law": "Verified bytes/schema/status, not path existence, advance the state machine.",
    }
