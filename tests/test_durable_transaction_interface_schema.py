import json
from pathlib import Path


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
    assert evidence["properties"]["source_evidence_refs"]["minItems"] >= 2
