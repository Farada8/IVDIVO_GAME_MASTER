import json
from pathlib import Path

from tools.ivdivo_durable_transaction_interface import UNVERIFIED_REAL_CLAIM, qualify_interruption_event


def _event():
    return {
        "event_id": "E-DUP",
        "project_id": "P1",
        "work_unit": "WU",
        "recovery_decision": "RECOVER_VOLATILE_FIRST",
        "real_interruption": True,
        "false_resume": False,
        "false_stop": False,
        "duplicate_work_units_avoided": 1,
        "writes_reconciled": 1,
        "checkpoint_bytes": 128,
        "checkpoint_tool_calls": 1,
        "recovery_tool_calls": 1,
        "notes": [],
    }


def _evidence():
    return {
        "controlled": False,
        "synthetic": False,
        "unplanned": True,
        "interruption_origin": "UNPLANNED_UI_SESSION_LOSS",
        "restart_observed": True,
        "pre_interrupt_checkpoint_id": "CP-1",
        "post_restart_authority_readback": True,
        "recovery_readback_verified": True,
        "project_state_before": "STATE-A",
        "project_state_after": "STATE-B",
        "source_evidence_refs": ["github:same", "github:same"],
    }


def test_evidence_schema_matches_runtime_qualification_minimum():
    schema = json.loads(Path("schemas/IVDIVO_DURABLE_TRANSACTION_INTERFACE_SCHEMA_v1.json").read_text(encoding="utf-8"))
    evidence = schema["properties"]["evidence"]
    required = set(evidence["required"])
    runtime_required = {
        "controlled",
        "synthetic",
        "unplanned",
        "interruption_origin",
        "restart_observed",
        "pre_interrupt_checkpoint_id",
        "post_restart_authority_readback",
        "recovery_readback_verified",
        "project_state_before",
        "project_state_after",
        "source_evidence_refs",
    }
    assert runtime_required <= required
    refs = evidence["properties"]["source_evidence_refs"]
    assert refs["minItems"] >= 2
    assert refs["uniqueItems"] is True


def test_duplicate_evidence_refs_cannot_inflate_genuine_packet():
    out = qualify_interruption_event(_event(), _evidence())
    assert out["qualification"] == UNVERIFIED_REAL_CLAIM
    assert out["qualified_real_interruption"] is False
    assert out["normalized_event"]["real_interruption"] is False
    assert out["evidence_checks"]["source_evidence_refs"] is False
