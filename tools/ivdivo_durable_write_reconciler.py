#!/usr/bin/env python3
"""IVDIVO durable multi-store transaction planner/reconciler.

Pure fail-closed logic. It does not call GitHub, Drive, providers, or spend credits.
It decides what a caller may do next after reading current store/provider evidence.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

SCHEMA_VERSION = "ivdivo.durable_write_transaction/1.0"

FORBIDDEN_KEY_FRAGMENTS = (
    "api_key", "apikey", "access_token", "refresh_token", "password",
    "passwd", "secret_key", "authorization", "bearer_token",
)

EFFECT_CLASSES = {"READ_ONLY", "REVERSIBLE_WRITE", "PAID_WRITE", "IRREVERSIBLE_WRITE"}
SIDE_EFFECT_STATES = {
    "NOT_STARTED", "STARTED_UNKNOWN", "CONFIRMED", "RECONCILED",
    "SUPERSEDED", "FAILED",
}
STORES = {"GITHUB", "DRIVE", "FILE_LIBRARY", "PROVIDER", "LOCAL"}


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def _walk_forbidden(obj: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            low = str(key).lower()
            if any(fragment in low for fragment in FORBIDDEN_KEY_FRAGMENTS):
                hits.append(f"{path}.{key}")
            hits.extend(_walk_forbidden(value, f"{path}.{key}"))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            hits.extend(_walk_forbidden(value, f"{path}[{i}]"))
    return hits


def derive_idempotency_key(
    *, transaction_id: str, action_id: str, store: str, operation: str, artifact_id: str
) -> str:
    material = {
        "transaction_id": transaction_id,
        "action_id": action_id,
        "store": store.upper(),
        "operation": operation,
        "artifact_id": artifact_id,
    }
    return "ivdtx:" + _sha256(material)


def _require_string(obj: dict[str, Any], key: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def _identity_matches(intended: dict[str, Any] | None, observed: dict[str, Any] | None) -> bool:
    intended = intended or {}
    observed = observed or {}
    for key, value in intended.items():
        if value in (None, ""):
            continue
        if observed.get(key) != value:
            return False
    return True


def normalize_transaction(plan: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(plan, dict):
        raise TypeError("plan must be an object")
    hits = _walk_forbidden(plan)
    if hits:
        raise ValueError("forbidden credential-like fields: " + ",".join(hits))

    transaction_id = _require_string(plan, "transaction_id")
    project_id = _require_string(plan, "project_id")
    work_unit = _require_string(plan, "work_unit")
    authority = plan.get("authority_snapshot")
    if not isinstance(authority, dict):
        raise ValueError("authority_snapshot must be an object")
    repo_main_sha = _require_string(authority, "repo_main_sha")
    state_revision = _require_string(authority, "state_revision")

    actions = plan.get("actions")
    if not isinstance(actions, list) or not actions:
        raise ValueError("actions must be a non-empty list")

    seen_action_ids: set[str] = set()
    seen_keys: set[str] = set()
    normalized_actions = []
    for raw in actions:
        if not isinstance(raw, dict):
            raise ValueError("every action must be an object")
        action_id = _require_string(raw, "action_id")
        artifact_id = _require_string(raw, "artifact_id")
        operation = _require_string(raw, "operation")
        if action_id in seen_action_ids:
            raise ValueError(f"duplicate action_id:{action_id}")
        seen_action_ids.add(action_id)

        store = str(raw.get("store", "")).upper()
        if store not in STORES:
            raise ValueError(f"invalid store:{store}")
        effect_class = str(raw.get("effect_class", "")).upper()
        if effect_class not in EFFECT_CLASSES:
            raise ValueError(f"invalid effect_class:{effect_class}")
        side_effect_state = str(raw.get("side_effect_state", "NOT_STARTED")).upper()
        if side_effect_state not in SIDE_EFFECT_STATES:
            raise ValueError(f"invalid side_effect_state:{side_effect_state}")

        key = raw.get("idempotency_key")
        if key in (None, ""):
            key = derive_idempotency_key(
                transaction_id=transaction_id,
                action_id=action_id,
                store=store,
                operation=operation,
                artifact_id=artifact_id,
            )
        if key in seen_keys:
            raise ValueError(f"duplicate idempotency_key:{key}")
        seen_keys.add(key)

        intended = raw.get("intended_identity")
        observed = raw.get("observed_identity")
        if intended is not None and not isinstance(intended, dict):
            raise ValueError("intended_identity must be object/null")
        if observed is not None and not isinstance(observed, dict):
            raise ValueError("observed_identity must be object/null")

        normalized_actions.append({
            "action_id": action_id,
            "artifact_id": artifact_id,
            "store": store,
            "operation": operation,
            "effect_class": effect_class,
            "idempotency_key": key,
            "side_effect_state": side_effect_state,
            "readback_verified": raw.get("readback_verified") is True,
            "intended_identity": deepcopy(intended) if intended else {},
            "observed_identity": deepcopy(observed) if observed else {},
            "external_reference": raw.get("external_reference"),
            "notes": list(raw.get("notes", [])) if isinstance(raw.get("notes", []), list) else [],
        })

    return {
        "schema_version": SCHEMA_VERSION,
        "transaction_id": transaction_id,
        "project_id": project_id,
        "work_unit": work_unit,
        "authority_snapshot": {
            "repo_main_sha": repo_main_sha,
            "state_revision": state_revision,
            "source_hash": authority.get("source_hash"),
        },
        "blockers": list(plan.get("blockers", [])) if isinstance(plan.get("blockers", []), list) else [],
        "actions": normalized_actions,
        "evidence_boundary": list(plan.get("evidence_boundary", [])) if isinstance(plan.get("evidence_boundary", []), list) else [],
    }


def transaction_hash(plan: dict[str, Any]) -> str:
    return _sha256(normalize_transaction(plan))


def reconcile_transaction(
    plan: dict[str, Any],
    *,
    current_repo_main_sha: str,
    current_state_revision: str,
    external_blockers: list[Any] | None = None,
) -> dict[str, Any]:
    tx = normalize_transaction(plan)

    blockers = list(tx.get("blockers", [])) + list(external_blockers or [])
    if blockers:
        return {"decision": "STOP", "reason": "BLOCKERS_PRESENT", "blockers": blockers}

    snap = tx["authority_snapshot"]
    drift: dict[str, Any] = {}
    if str(snap["repo_main_sha"]) != str(current_repo_main_sha):
        drift["repo_main_sha"] = {"transaction": snap["repo_main_sha"], "current": current_repo_main_sha}
    if str(snap["state_revision"]) != str(current_state_revision):
        drift["state_revision"] = {"transaction": snap["state_revision"], "current": current_state_revision}
    if drift:
        return {"decision": "REBASE_FIRST", "reason": "AUTHORITY_OR_STATE_DRIFT", "drift": drift}

    identity_conflicts = []
    for action in tx["actions"]:
        if action["side_effect_state"] in {"CONFIRMED", "RECONCILED"}:
            if not _identity_matches(action["intended_identity"], action["observed_identity"]):
                identity_conflicts.append(action["action_id"])
    if identity_conflicts:
        return {"decision": "STOP", "reason": "IDENTITY_MISMATCH", "action_ids": identity_conflicts}

    ambiguous_high_impact = [
        a["action_id"] for a in tx["actions"]
        if a["side_effect_state"] == "STARTED_UNKNOWN" and a["effect_class"] in {"PAID_WRITE", "IRREVERSIBLE_WRITE"}
    ]
    if ambiguous_high_impact:
        return {
            "decision": "QUARANTINE_EXTERNAL_SIDE_EFFECT",
            "reason": "AMBIGUOUS_PAID_OR_IRREVERSIBLE_EFFECT",
            "action_ids": ambiguous_high_impact,
        }

    ambiguous_reversible = [
        a["action_id"] for a in tx["actions"]
        if a["side_effect_state"] == "STARTED_UNKNOWN" and a["effect_class"] in {"READ_ONLY", "REVERSIBLE_WRITE"}
    ]
    if ambiguous_reversible:
        return {"decision": "VERIFY_STORE_BEFORE_RETRY", "reason": "AMBIGUOUS_REVERSIBLE_EFFECT", "action_ids": ambiguous_reversible}

    readback_pending = [
        a["action_id"] for a in tx["actions"]
        if a["side_effect_state"] in {"CONFIRMED", "RECONCILED"} and not a["readback_verified"]
    ]
    if readback_pending:
        return {"decision": "VERIFY_READBACK", "reason": "CONFIRMED_WITHOUT_READBACK", "action_ids": readback_pending}

    not_started = [a for a in tx["actions"] if a["side_effect_state"] == "NOT_STARTED"]
    if not_started:
        high_impact = [a["action_id"] for a in not_started if a["effect_class"] in {"PAID_WRITE", "IRREVERSIBLE_WRITE"}]
        safe_missing = [a["action_id"] for a in not_started if a["effect_class"] in {"READ_ONLY", "REVERSIBLE_WRITE"}]
        if high_impact:
            return {
                "decision": "REQUIRE_EXPLICIT_DISPATCH_GATE",
                "reason": "UNSTARTED_PAID_OR_IRREVERSIBLE_ACTION",
                "high_impact_action_ids": high_impact,
                "safe_action_ids": safe_missing,
            }
        return {"decision": "EXECUTE_MISSING_SAFE_ACTIONS", "reason": "ONLY_SAFE_ACTIONS_REMAIN", "action_ids": safe_missing}

    failed = [a["action_id"] for a in tx["actions"] if a["side_effect_state"] == "FAILED"]
    if failed:
        return {"decision": "STOP", "reason": "FAILED_ACTIONS_PRESENT", "action_ids": failed}

    return {
        "decision": "TRANSACTION_COMPLETE",
        "reason": "ALL_ACTIONS_TERMINAL_AND_READBACK_VERIFIED",
        "transaction_id": tx["transaction_id"],
        "transaction_sha256": _sha256(tx),
    }
