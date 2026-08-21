#!/usr/bin/env python3
"""IVDIVO Audio Studio — ambiguous provider response reconciliation contract.

A transport timeout after a request may mean the provider charged/generated even
when the client did not receive the complete response. This module forbids blind
re-payment. It does not invent provider lookup capabilities: the caller must supply
an authenticated lookup result or explicitly report lookup unsupported/unavailable.
"""
from __future__ import annotations

from typing import Any

VALID_LOOKUP_STATES = {"FOUND_ACCEPTED", "FOUND_FAILED", "NOT_FOUND", "LOOKUP_UNSUPPORTED", "LOOKUP_UNAVAILABLE"}


def reconcile_ambiguous(
    attempt: dict[str, Any],
    lookup_result: dict[str, Any],
) -> dict[str, Any]:
    if attempt.get("state") != "AMBIGUOUS":
        raise ValueError("ATTEMPT_NOT_AMBIGUOUS")
    if not attempt.get("request_hash") or not attempt.get("block_id"):
        raise ValueError("ATTEMPT_IDENTITY_MISSING")

    state = lookup_result.get("state")
    if state not in VALID_LOOKUP_STATES:
        raise ValueError("PROVIDER_LOOKUP_STATE_INVALID")

    if state == "FOUND_ACCEPTED":
        response_hash = lookup_result.get("response_hash")
        provider_request_id = lookup_result.get("provider_request_id")
        if not response_hash or not provider_request_id:
            raise ValueError("PROVIDER_LOOKUP_EVIDENCE_INCOMPLETE")
        return {
            "status": "RECONCILED_ACCEPTED",
            "next_action": "INGEST_EXISTING_RESPONSE",
            "retry_allowed": False,
            "provider_request_id": provider_request_id,
            "response_hash": response_hash,
        }

    if state == "FOUND_FAILED":
        return {
            "status": "RECONCILED_FAILED",
            "next_action": "RETRY_ONLY_IF_FAILURE_POLICY_ALLOWS",
            "retry_allowed": bool(lookup_result.get("retryable", False)),
        }

    if state == "NOT_FOUND":
        # A provider-confirmed NOT_FOUND can release the quarantine, but the caller
        # still applies its ordinary retry/spend policy.
        return {
            "status": "RECONCILED_NOT_FOUND",
            "next_action": "RETRY_POLICY_MAY_EVALUATE",
            "retry_allowed": True,
        }

    return {
        "status": "HOLD_AMBIGUOUS",
        "next_action": "REQUIRE_PROVIDER_OR_HUMAN_RECONCILIATION",
        "retry_allowed": False,
        "reason": state,
    }
