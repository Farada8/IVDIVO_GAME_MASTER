#!/usr/bin/env python3
"""IVDIVO Audio Studio provider-neutral production control v1.0 candidate.

This is intentionally narrow. It complements the existing provider adapter,
provider preflight, alignment normalizer and scene/runtime compilers. It owns
request idempotency, spend-state persistence, ambiguous-response quarantine,
error classification, capability drift, dependency invalidation and release
control evidence. It performs no provider dispatch and no artistic judgment.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable, Mapping
import json

LEDGER_STATES = {"PLANNED", "SENT", "AMBIGUOUS", "ACCEPTED", "REJECTED"}
TERMINAL_STATES = {"ACCEPTED", "REJECTED"}


def canonical_hash(obj: Any) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def request_identity(compiled_request: Mapping[str, Any]) -> str:
    """Return existing adapter request_hash or derive a stable sanitized identity."""
    existing = compiled_request.get("request_hash")
    if existing:
        return str(existing)
    basis = {
        k: compiled_request.get(k)
        for k in ("provider", "endpoint_profile", "path", "query", "body", "block_id")
        if k in compiled_request
    }
    return canonical_hash(basis)


@dataclass
class Attempt:
    request_hash: str
    block_id: str
    state: str = "PLANNED"
    provider_request_id: str | None = None
    response_hash: str | None = None
    cost: float | None = None
    note: str | None = None


class SpendLedger:
    """Persistent request ledger preventing blind duplicate paid dispatch."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.attempts: dict[str, Attempt] = {}
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise ValueError("LEDGER_FORMAT_INVALID")
            self.attempts = {key: Attempt(**value) for key, value in raw.items()}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {key: asdict(value) for key, value in sorted(self.attempts.items())}
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def get(self, request_hash: str) -> Attempt | None:
        return self.attempts.get(request_hash)

    def plan(self, request_hash: str, block_id: str) -> str:
        current = self.attempts.get(request_hash)
        if current:
            if current.block_id != block_id:
                raise ValueError("REQUEST_HASH_BLOCK_COLLISION")
            if current.state == "ACCEPTED":
                return "REUSED_ACCEPTED"
            if current.state == "AMBIGUOUS":
                return "RECONCILE_REQUIRED"
            return f"EXISTS_{current.state}"
        self.attempts[request_hash] = Attempt(request_hash=request_hash, block_id=block_id)
        self._save()
        return "PLANNED"

    def transition(
        self,
        request_hash: str,
        state: str,
        *,
        provider_request_id: str | None = None,
        response_hash: str | None = None,
        cost: float | None = None,
        note: str | None = None,
    ) -> Attempt:
        if state not in LEDGER_STATES:
            raise ValueError("INVALID_LEDGER_STATE")
        current = self.attempts.get(request_hash)
        if current is None:
            raise KeyError(request_hash)
        if current.state == "ACCEPTED" and state != "ACCEPTED":
            raise ValueError("ACCEPTED_ATTEMPT_IMMUTABLE")
        if current.state == "AMBIGUOUS" and state == "SENT":
            raise ValueError("AMBIGUOUS_REQUIRES_RECONCILIATION")
        if state == "ACCEPTED" and not (response_hash or current.response_hash):
            raise ValueError("ACCEPTED_REQUIRES_RESPONSE_HASH")
        if cost is not None and cost < 0:
            raise ValueError("NEGATIVE_COST_INVALID")
        current.state = state
        if provider_request_id is not None:
            current.provider_request_id = provider_request_id
        if response_hash is not None:
            current.response_hash = response_hash
        if cost is not None:
            current.cost = float(cost)
        if note is not None:
            current.note = note
        self._save()
        return current

    def snapshot(self) -> dict[str, Any]:
        return {key: asdict(value) for key, value in sorted(self.attempts.items())}

    def accepted_cost(self) -> float:
        return round(sum(float(a.cost or 0.0) for a in self.attempts.values() if a.state == "ACCEPTED"), 6)


def dispatch_gate(compiled_request: Mapping[str, Any], ledger: SpendLedger) -> dict[str, Any]:
    rid = request_identity(compiled_request)
    block_id = str(compiled_request.get("block_id") or "")
    if not block_id:
        raise ValueError("BLOCK_ID_REQUIRED")
    status = ledger.plan(rid, block_id)
    if status == "REUSED_ACCEPTED":
        return {"status": "REUSE", "request_hash": rid, "dispatch_allowed": False}
    if status == "RECONCILE_REQUIRED":
        return {"status": "HOLD_AMBIGUOUS", "request_hash": rid, "dispatch_allowed": False}
    if status in {"EXISTS_SENT", "EXISTS_PLANNED"}:
        return {"status": "HOLD_EXISTING_ATTEMPT", "request_hash": rid, "dispatch_allowed": False}
    if status == "EXISTS_REJECTED":
        return {"status": "REPLAN_REQUIRED", "request_hash": rid, "dispatch_allowed": False}
    return {"status": "SEND_READY", "request_hash": rid, "dispatch_allowed": True}


def reconcile_ambiguous(
    ledger: SpendLedger,
    request_hash: str,
    *,
    provider_confirmed_charge: bool | None,
    response_hash: str | None = None,
    provider_request_id: str | None = None,
    cost: float | None = None,
) -> dict[str, Any]:
    current = ledger.get(request_hash)
    if current is None or current.state != "AMBIGUOUS":
        raise ValueError("AMBIGUOUS_ATTEMPT_REQUIRED")
    if provider_confirmed_charge is None:
        return {"status": "HOLD", "reason": "PROVIDER_CHARGE_STATUS_UNKNOWN"}
    if provider_confirmed_charge:
        if not response_hash:
            return {"status": "HOLD", "reason": "CHARGE_CONFIRMED_RESPONSE_EVIDENCE_MISSING"}
        ledger.transition(request_hash, "ACCEPTED", provider_request_id=provider_request_id, response_hash=response_hash, cost=cost)
        return {"status": "ACCEPTED_RECONCILED", "dispatch_allowed": False}
    ledger.transition(request_hash, "REJECTED", provider_request_id=provider_request_id, note="provider confirmed no accepted charge/result")
    return {"status": "REJECTED_RECONCILED", "dispatch_allowed": False}


def normalize_provider_error(status: int | None = None, code: str | None = None, message: str = "") -> dict[str, Any]:
    c = (code or "").upper()
    m = (message or "").upper()
    if status in (401, 403) or "AUTH" in c:
        category, retryable = "AUTH", False
    elif "VOICE" in c:
        category, retryable = "VOICE", False
    elif "MODEL" in c:
        category, retryable = "MODEL", False
    elif "ALIGN" in c:
        category, retryable = "ALIGNMENT", False
    elif "FORMAT" in c or "AUDIO_FORMAT" in c:
        category, retryable = "FORMAT", False
    elif "QUOTA" in c or "CREDIT" in c or "CREDIT" in m:
        category, retryable = "QUOTA", False
    elif status == 429 or "RATE" in c:
        category, retryable = "RATE_LIMIT", True
    elif status in (408, 504) or "TIMEOUT" in c:
        category, retryable = "TIMEOUT", True
    elif status in (400, 404, 422) or "INVALID" in c:
        category, retryable = "INVALID_REQUEST", False
    else:
        category, retryable = "PROVIDER", status in (500, 502, 503)
    return {"category": category, "retryable": retryable, "status": status, "code": code}


def retry_decision(error: Mapping[str, Any], *, response_started: bool = False) -> str:
    if response_started:
        return "QUARANTINE_AMBIGUOUS"
    return "BACKOFF_RETRY" if error.get("retryable") else "FAIL_CLOSED"


def capability_drift(expected: Mapping[str, Any], snapshot: Mapping[str, Any]) -> dict[str, Any]:
    voices = snapshot.get("voices", {}) or {}
    models = snapshot.get("models", {}) or {}
    model_ids = set(models) if isinstance(models, dict) else set(models)
    missing_voices = sorted(v for v in expected.get("voice_ids", []) if v not in voices)
    missing_models = sorted(m for m in expected.get("model_ids", []) if m not in model_ids)
    failed_voices = sorted(v for v in expected.get("voice_ids", []) if isinstance(voices, dict) and v in voices and voices[v].get("status") not in (None, "PASS"))
    failed_models = sorted(m for m in expected.get("model_ids", []) if isinstance(models, dict) and m in models and models[m].get("status") not in (None, "PASS"))
    return {
        "status": "PASS" if not (missing_voices or missing_models or failed_voices or failed_models) else "FAIL_DRIFT",
        "missing_voices": missing_voices,
        "missing_models": missing_models,
        "failed_voices": failed_voices,
        "failed_models": failed_models,
        "auto_substitution": False,
    }


def dependency_descendants(graph: Mapping[str, Iterable[str]], changed: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    stack = list(changed)
    while stack:
        node = stack.pop()
        for child in graph.get(node, []):
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return sorted(seen)


def selective_rerender(failed_blocks: Iterable[str], known_blocks: Iterable[str]) -> list[str]:
    known = set(known_blocks)
    failed = list(failed_blocks)
    unknown = sorted(set(failed) - known)
    if unknown:
        raise ValueError("UNKNOWN_BLOCKS:" + ",".join(unknown))
    return sorted(set(failed))


def release_control_gate(evidence: Mapping[str, bool]) -> dict[str, Any]:
    required = (
        "provider_preflight",
        "idempotency",
        "ambiguous_recovery",
        "alignment",
        "human_review",
        "measured_economics",
        "durable_provenance",
    )
    missing = [name for name in required if not evidence.get(name)]
    return {
        "status": "PASS_CONTROL_LAYER" if not missing else "HOLD",
        "missing": missing,
        "production_ready": False,
        "law": "Control-layer PASS never substitutes for artistic/provider/release authority.",
    }
