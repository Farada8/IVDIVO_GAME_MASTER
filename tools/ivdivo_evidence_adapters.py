#!/usr/bin/env python3
"""IVDIVO evidence/approval adapters for Production Proof Chain.

Candidate utility. Converts explicit Founder, human-listener, provider and model-review
observations into bounded proof-chain evidence objects. It does not create evidence,
perform provider calls, or infer approvals.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

MODEL_TYPES = {"MODEL_REVIEW", "EXTERNAL_AI", "INFERENCE"}
HUMAN_TYPES = {"HUMAN_NATIVE", "PRACTITIONER", "BLIND_LISTENER"}


def _nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _stable_hash(obj: Any) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def founder_evidence(*, evidence_id: str, project_id: str, frontier: str,
                     gate_id: str, decision: str, locator: str,
                     explicit: bool) -> dict[str, Any]:
    for name, value in {
        "evidence_id": evidence_id, "project_id": project_id, "frontier": frontier,
        "gate_id": gate_id, "decision": decision, "locator": locator,
    }.items():
        _nonempty(value, name)
    if not explicit:
        return {
            "evidence_id": evidence_id,
            "source_type": "FOUNDER",
            "authority_weight": 100,
            "status": "HOLD",
            "scope": {"project_id": project_id, "frontier": frontier, "gate_id": gate_id},
            "locator": locator,
            "reason": "EXPLICIT_FOUNDER_DECISION_REQUIRED",
        }
    return {
        "evidence_id": evidence_id,
        "source_type": "FOUNDER",
        "authority_weight": 100,
        "status": "PASS" if decision.upper() in {"APPROVE", "LOCK", "PASS", "GO"} else "FAIL",
        "scope": {"project_id": project_id, "frontier": frontier, "gate_id": gate_id},
        "locator": locator,
        "decision": decision.upper(),
    }


def human_listener_evidence(*, evidence_id: str, project_id: str, artifact_id: str,
                            reviewer_id: str, locator: str, verdict: str,
                            blind: bool = True, model_generated: bool = False) -> dict[str, Any]:
    for name, value in {
        "evidence_id": evidence_id, "project_id": project_id, "artifact_id": artifact_id,
        "reviewer_id": reviewer_id, "locator": locator, "verdict": verdict,
    }.items():
        _nonempty(value, name)
    if model_generated:
        raise ValueError("MODEL_OUTPUT_CANNOT_BE_ADAPTED_AS_HUMAN_SIGNAL")
    return {
        "evidence_id": evidence_id,
        "source_type": "BLIND_LISTENER" if blind else "HUMAN_NATIVE",
        "authority_weight": 80,
        "status": verdict.upper(),
        "project_id": project_id,
        "artifact_id": artifact_id,
        "reviewer_id": reviewer_id,
        "locator": locator,
        "blind": bool(blind),
    }


def provider_response_evidence(*, evidence_id: str, project_id: str, provider: str,
                               request_id: str, response_locator: str | None,
                               artifact_id: str | None, verdict: str,
                               live: bool) -> dict[str, Any]:
    for name, value in {
        "evidence_id": evidence_id, "project_id": project_id, "provider": provider,
        "request_id": request_id, "verdict": verdict,
    }.items():
        _nonempty(value, name)
    if not live:
        return {
            "evidence_id": evidence_id,
            "source_type": "MACHINE_TEST",
            "authority_weight": 40,
            "status": "PASS" if verdict.upper() == "PASS" else verdict.upper(),
            "project_id": project_id,
            "provider": provider,
            "request_id": request_id,
            "artifact_id": artifact_id,
            "response_locator": response_locator,
            "live": False,
            "cannot_prove": ["LIVE_PROVIDER_EXECUTION"],
        }
    if not response_locator:
        return {
            "evidence_id": evidence_id,
            "source_type": "PROVIDER_RESPONSE",
            "authority_weight": 85,
            "status": "HOLD",
            "project_id": project_id,
            "provider": provider,
            "request_id": request_id,
            "artifact_id": artifact_id,
            "live": True,
            "reason": "LIVE_RESPONSE_LOCATOR_REQUIRED",
        }
    return {
        "evidence_id": evidence_id,
        "source_type": "PROVIDER_RESPONSE",
        "authority_weight": 85,
        "status": verdict.upper(),
        "project_id": project_id,
        "provider": provider,
        "request_id": request_id,
        "response_locator": response_locator,
        "artifact_id": artifact_id,
        "live": True,
    }


def model_review_evidence(*, evidence_id: str, project_id: str, locator: str,
                          verdict: str, authority_weight: int = 30) -> dict[str, Any]:
    _nonempty(evidence_id, "evidence_id")
    _nonempty(project_id, "project_id")
    _nonempty(locator, "locator")
    if authority_weight > 40:
        raise ValueError("MODEL_REVIEW_AUTHORITY_CEILING_EXCEEDED")
    return {
        "evidence_id": evidence_id,
        "source_type": "EXTERNAL_AI",
        "authority_weight": int(authority_weight),
        "status": verdict.upper(),
        "project_id": project_id,
        "locator": locator,
        "cannot_prove": ["FOUNDER_APPROVAL", "HUMAN_SIGNAL", "LIVE_PROVIDER_RESULT"],
    }


def make_approval_token(*, project_id: str, frontier: str, gate_id: str,
                        evidence_id: str) -> dict[str, str]:
    scope = {
        "project_id": _nonempty(project_id, "project_id"),
        "frontier": _nonempty(frontier, "frontier"),
        "gate_id": _nonempty(gate_id, "gate_id"),
        "evidence_id": _nonempty(evidence_id, "evidence_id"),
    }
    return {**scope, "token": "ivdappr:" + _stable_hash(scope)}


def approval_token_matches(token: dict[str, Any], *, project_id: str,
                           frontier: str, gate_id: str,
                           evidence_id: str) -> bool:
    if not isinstance(token, dict):
        return False
    expected = make_approval_token(project_id=project_id, frontier=frontier,
                                   gate_id=gate_id, evidence_id=evidence_id)
    return token == expected


def resolve_conflicting_evidence(evidence: list[dict[str, Any]]) -> dict[str, Any]:
    if not evidence:
        return {"status": "HOLD", "reason": "NO_EVIDENCE"}
    passes = [e for e in evidence if e.get("status") == "PASS"]
    fails = [e for e in evidence if e.get("status") in {"FAIL", "REJECTED"}]
    if passes and fails:
        return {
            "status": "UNRESOLVED_CONFLICT",
            "reason": "PASS_AND_FAIL_EVIDENCE_COEXIST",
            "pass_ids": [e.get("evidence_id") for e in passes],
            "fail_ids": [e.get("evidence_id") for e in fails],
            "disposition_required": "RECONCILE_PROVENANCE_SCOPE_OR_REPAIR_BEFORE_GATE",
        }
    if fails:
        return {"status": "FAIL", "evidence_ids": [e.get("evidence_id") for e in fails]}
    if passes:
        return {"status": "PASS", "evidence_ids": [e.get("evidence_id") for e in passes]}
    return {"status": "HOLD", "reason": "NO_TERMINAL_PASS_FAIL_EVIDENCE"}


def artifact_readback_evidence(*, evidence_id: str, artifact_id: str,
                               expected_sha256: str, readback_sha256: str) -> dict[str, Any]:
    for name, value in {
        "evidence_id": evidence_id, "artifact_id": artifact_id,
        "expected_sha256": expected_sha256, "readback_sha256": readback_sha256,
    }.items():
        _nonempty(value, name)
    matched = expected_sha256 == readback_sha256
    return {
        "evidence_id": evidence_id,
        "source_type": "MACHINE_TEST",
        "authority_weight": 70,
        "status": "PASS" if matched else "FAIL",
        "artifact_id": artifact_id,
        "expected_sha256": expected_sha256,
        "readback_sha256": readback_sha256,
        "matched": matched,
    }
