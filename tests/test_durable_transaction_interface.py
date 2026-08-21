from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

from tools.ivdivo_durable_transaction_interface import (
    EXCLUDED_CONTROLLED,
    EXCLUDED_SYNTHETIC,
    QUALIFIED_REAL,
    UNVERIFIED_REAL_CLAIM,
    adapt_si0012_bytes_transaction,
    qualify_interruption_event,
    reconcile_si0014,
    summarize_qualified_records,
    verify_si0012_readback,
)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _event(event_id="E1", project_id="P1", *, real=True, false_resume=False, false_stop=False):
    return {
        "event_id": event_id,
        "project_id": project_id,
        "work_unit": "WU",
        "recovery_decision": "RECOVER_VOLATILE_FIRST",
        "real_interruption": real,
        "false_resume": false_resume,
        "false_stop": false_stop,
        "duplicate_work_units_avoided": 1,
        "writes_reconciled": 1,
        "checkpoint_bytes": 128,
        "checkpoint_tool_calls": 1,
        "recovery_tool_calls": 1,
        "notes": [],
    }


def _real_evidence(tag="1"):
    return {
        "controlled": False,
        "synthetic": False,
        "unplanned": True,
        "interruption_origin": "UNPLANNED_UI_SESSION_LOSS",
        "restart_observed": True,
        "pre_interrupt_checkpoint_id": f"CP-{tag}",
        "post_restart_authority_readback": True,
        "recovery_readback_verified": True,
        "project_state_before": f"state-before-{tag}",
        "project_state_after": f"state-after-{tag}",
        "source_evidence_refs": [f"github:{tag}", f"drive:{tag}"],
    }


def _load_si0012_runtime():
    path = Path("SELF_IMPROVEMENT_STUDIO/SI0012_MIN_COMPAT_RUNTIME_v0.1/si0012_runtime_v0_1.py")
    module_name = "si0012_runtime_v0_1"
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def test_si0012_adapter_stale_rejected():
    out = adapt_si0012_bytes_transaction(b"old", b"new", "bad")
    assert out["decision"] == "STOP"
    assert out["reason"] == "STALE_REJECTED"


def test_si0012_adapter_no_effect_rejected():
    old = b"same"
    out = adapt_si0012_bytes_transaction(old, old, _sha(old))
    assert out["decision"] == "STOP"
    assert out["reason"] == "NO_EFFECT_REJECTED"


def test_si0012_adapter_ready_maps_to_safe_action():
    old, new = b"old", b"new"
    out = adapt_si0012_bytes_transaction(old, new, _sha(old))
    assert out["decision"] == "EXECUTE_MISSING_SAFE_ACTIONS"
    assert out["action_ids"] == ["SI0012_SINGLE_STORE_WRITE"]
    assert out["new_hash"] == _sha(new)


def test_si0012_readback_mismatch_stops():
    out = verify_si0012_readback(b"new", b"different")
    assert out["decision"] == "STOP"
    assert out["reason"] == "READBACK_MISMATCH"


def test_si0012_readback_match_completes():
    out = verify_si0012_readback(b"new", b"new")
    assert out["decision"] == "TRANSACTION_COMPLETE"


def test_si0012_adapter_parity_with_existing_runtime():
    runtime = _load_si0012_runtime()
    old, new = b"old", b"new"
    legacy = runtime.plan_transaction(old, new, _sha(old))
    unified = adapt_si0012_bytes_transaction(old, new, _sha(old))
    assert legacy["status"] == "READY"
    assert unified["decision"] == "EXECUTE_MISSING_SAFE_ACTIONS"
    assert legacy["old_hash"] == unified["old_hash"]
    assert legacy["new_hash"] == unified["new_hash"]
    assert runtime.verify_readback(new, new)["status"] == "COMMITTED_VERIFIED"
    assert verify_si0012_readback(new, new)["decision"] == "TRANSACTION_COMPLETE"


def _tx_plan(state="NOT_STARTED"):
    return {
        "transaction_id": "TX-1",
        "project_id": "P1",
        "work_unit": "WU",
        "authority_snapshot": {"repo_main_sha": "MAIN", "state_revision": "STATE"},
        "actions": [
            {
                "action_id": "A1",
                "artifact_id": "ART",
                "store": "GITHUB",
                "operation": "create-file",
                "effect_class": "REVERSIBLE_WRITE",
                "side_effect_state": state,
                "readback_verified": state == "RECONCILED",
                "intended_identity": {},
                "observed_identity": {},
            }
        ],
    }


def test_si0014_delegate_preserves_missing_safe_action_decision():
    out = reconcile_si0014(_tx_plan(), current_repo_main_sha="MAIN", current_state_revision="STATE")
    assert out["source_runtime"] == "SI-0014"
    assert out["decision"] == "EXECUTE_MISSING_SAFE_ACTIONS"
    assert out["action_ids"] == ["A1"]


def test_si0014_delegate_preserves_rebase_first_on_drift():
    out = reconcile_si0014(_tx_plan(), current_repo_main_sha="NEW_MAIN", current_state_revision="STATE")
    assert out["decision"] == "REBASE_FIRST"
    assert out["reason"] == "AUTHORITY_OR_STATE_DRIFT"


def test_controlled_event_never_counts_as_real_even_if_raw_flag_true():
    evidence = _real_evidence()
    evidence["controlled"] = True
    out = qualify_interruption_event(_event(real=True), evidence)
    assert out["qualification"] == EXCLUDED_CONTROLLED
    assert out["normalized_event"]["real_interruption"] is False


def test_synthetic_event_never_counts_as_real_even_if_raw_flag_true():
    evidence = _real_evidence()
    evidence["synthetic"] = True
    out = qualify_interruption_event(_event(real=True), evidence)
    assert out["qualification"] == EXCLUDED_SYNTHETIC
    assert out["normalized_event"]["real_interruption"] is False


def test_unverified_raw_real_claim_is_downgraded():
    out = qualify_interruption_event(_event(real=True), {"controlled": False, "synthetic": False})
    assert out["qualification"] == UNVERIFIED_REAL_CLAIM
    assert out["normalized_event"]["real_interruption"] is False


def test_complete_unplanned_restart_packet_qualifies():
    out = qualify_interruption_event(_event(real=False), _real_evidence())
    assert out["qualification"] == QUALIFIED_REAL
    assert out["normalized_event"]["real_interruption"] is True


def test_unknown_origin_does_not_qualify():
    evidence = _real_evidence()
    evidence["interruption_origin"] = "UNKNOWN"
    out = qualify_interruption_event(_event(), evidence)
    assert out["qualification"] == UNVERIFIED_REAL_CLAIM


def test_no_restart_does_not_qualify():
    evidence = _real_evidence()
    evidence["restart_observed"] = False
    out = qualify_interruption_event(_event(), evidence)
    assert out["qualification"] == UNVERIFIED_REAL_CLAIM


def test_three_real_across_two_projects_reaches_review_only():
    records = [
        {"event": _event("E1", "P1"), "evidence": _real_evidence("1")},
        {"event": _event("E2", "P1"), "evidence": _real_evidence("2")},
        {"event": _event("E3", "P2"), "evidence": _real_evidence("3")},
    ]
    out = summarize_qualified_records(records)
    assert out["promotion_recommendation"] == "ELIGIBLE_FOR_PROMOTION_REVIEW"
    assert out["decision"] == "ADVISORY_ONLY"
    assert out["metrics"]["real_interruption_count"] == 3
    assert out["metrics"]["real_project_count"] == 2


def test_controlled_event_cannot_inflate_three_event_threshold():
    controlled = _real_evidence("3")
    controlled["controlled"] = True
    records = [
        {"event": _event("E1", "P1"), "evidence": _real_evidence("1")},
        {"event": _event("E2", "P2"), "evidence": _real_evidence("2")},
        {"event": _event("E3", "P3"), "evidence": controlled},
    ]
    out = summarize_qualified_records(records)
    assert out["promotion_recommendation"] == "CONTINUE_PILOT"
    assert out["metrics"]["real_interruption_count"] == 2


def test_false_resume_blocks_even_when_packet_is_real():
    records = [
        {"event": _event("E1", "P1", false_resume=True), "evidence": _real_evidence("1")},
        {"event": _event("E2", "P1"), "evidence": _real_evidence("2")},
        {"event": _event("E3", "P2"), "evidence": _real_evidence("3")},
    ]
    out = summarize_qualified_records(records)
    assert out["promotion_recommendation"] == "HOLD"
    assert out["reason"] == "FALSE_RESUME_PRESENT"
