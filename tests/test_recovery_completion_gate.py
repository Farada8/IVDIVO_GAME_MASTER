from copy import deepcopy

from tools.ivdivo_recovery_completion_gate import evaluate


SOURCE_HASH = "a" * 64


def valid_state():
    return {
        "schema_version": "2.0",
        "recovery_id": "REC-TEST-001",
        "recovery_status": "INGESTION_COMPLETE",
        "source": {
            "sha256": SOURCE_HASH,
            "bytes": 1000,
            "completeness": "UNKNOWN_COMPLETENESS",
            "completeness_basis": "complete supplied paste parsed; original chat completeness not independently proven",
            "input_tail_processed": True,
            "source_completeness_proven": False,
            "first_turn_signature": "u1",
            "last_turn_signature": "a9",
            "truncation_indicators": [],
            "chunks": [
                {
                    "chunk_id": "C001",
                    "source_sha256": SOURCE_HASH,
                    "range_kind": "BYTE",
                    "start": 0,
                    "end": 1000,
                    "overlap_hash": None,
                    "findings_hash": "findings-1",
                    "processed_at": "2026-08-21T15:00:00Z",
                    "input_tail_in_chunk": True,
                }
            ],
        },
        "authority": {
            "direct_founder_directives": [],
            "paraphrased_directive_claims": [],
            "authority_unambiguous": True,
            "authority_resolution_note": "no material conflict",
        },
        "project_partitions": [
            {
                "partition_id": "P1",
                "project_key": "TEST_PROJECT",
                "project_id": None,
                "branch_or_line": None,
                "artifact_claims": [],
                "chat_only_candidates": [],
                "frontier": {
                    "last_verified_completed_artifact": "A1",
                    "current_authority": ["AUTH1"],
                    "open_gates": [],
                    "blockers": [],
                    "do_not_repeat": [],
                    "next_legal_action": "continue",
                    "fresh": True,
                },
                "material_items_dispositioned": True,
            }
        ],
        "verification_tasks": [
            {
                "task_id": "V1",
                "claim_type": "SAVED",
                "store": "GITHUB",
                "reference": "path/file.md",
                "expected_identity": None,
                "required_action": "readback",
                "result": "VERIFIED",
                "evidence_ref": "github:path/file.md@sha",
                "checked_at": "2026-08-21T15:01:00Z",
                "superseded_by": None,
                "notes": None,
            }
        ],
        "unknowns": [],
        "conflicts": [],
        "writes": [
            {
                "write_id": "W1",
                "recovery_id": "REC-TEST-001",
                "target": "github:path/file.md",
                "content_fingerprint": "fp1",
                "previous_pointer": None,
                "status": "WRITTEN",
                "result_ref": "sha1",
                "readback_status": "PASS",
                "notes": None,
            }
        ],
        "system_improvement_candidates": [],
        "completion_gate": {
            "all_material_items_dispositioned": True,
            "all_accepted_writes_read_back": True,
            "authority_unambiguous": True,
            "frontier_fresh": True,
            "no_material_conflicts": True,
            "secrets_persisted": False,
            "input_tail_processed": True,
            "ingestion_complete": True,
            "can_auto_continue": True,
            "reason": "all recovery checks green",
        },
        "next_action": {
            "action": "continue",
            "requires_new_founder_choice": False,
            "requires_human_evidence": False,
            "requires_external_provider": False,
            "executable_here": True,
            "do_not_repeat": [],
        },
    }


def test_valid_state_passes_to_next_action_resolver():
    out = evaluate(valid_state())
    assert out["decision"] == "RECOVERY_COMPLETE"
    assert out["handoff_to_next_action_resolver"] is True
    assert out["can_auto_continue_after_normal_action_gates"] is True


def test_extracted_unverified_fails_closed():
    state = valid_state()
    state["recovery_status"] = "EXTRACTED_UNVERIFIED"
    out = evaluate(state)
    assert out["decision"] == "STOP"
    assert out["reason"] == "RECOVERY_NOT_COMPLETE"


def test_unprocessed_tail_blocks_completion():
    state = valid_state()
    state["source"]["input_tail_processed"] = False
    out = evaluate(state)
    assert out["reason"] == "INPUT_TAIL_NOT_PROCESSED"


def test_material_unknown_blocks_completion():
    state = valid_state()
    state["unknowns"] = [
        {"unknown_id": "U1", "category": "MISSING_EXACT_DETAIL", "description": "missing Founder branch choice", "material": True}
    ]
    out = evaluate(state)
    assert out["reason"] == "MATERIAL_UNKNOWNS_REMAIN"


def test_open_material_conflict_blocks_completion():
    state = valid_state()
    state["conflicts"] = [
        {"conflict_id": "C1", "left_ref": "A", "right_ref": "B", "material": True, "status": "OPEN", "resolution": None}
    ]
    out = evaluate(state)
    assert out["reason"] == "MATERIAL_CONFLICTS_REMAIN"


def test_unchecked_verification_task_blocks_completion():
    state = valid_state()
    state["verification_tasks"][0]["result"] = "UNCHECKED"
    state["verification_tasks"][0]["evidence_ref"] = None
    out = evaluate(state)
    assert out["reason"] == "VERIFICATION_TASK_NOT_TERMINAL"


def test_verified_task_requires_evidence_ref():
    state = valid_state()
    state["verification_tasks"][0]["evidence_ref"] = None
    out = evaluate(state)
    assert out["reason"] == "VERIFICATION_EVIDENCE_MISSING"


def test_written_record_requires_readback_pass():
    state = valid_state()
    state["writes"][0]["readback_status"] = "PENDING"
    out = evaluate(state)
    assert out["reason"] == "WRITE_READBACK_NOT_PASS"


def test_secret_firewall_must_be_green():
    state = valid_state()
    state["completion_gate"]["secrets_persisted"] = True
    out = evaluate(state)
    assert out["reason"] == "SECRET_FIREWALL_NOT_GREEN"


def test_auto_continue_cannot_hide_founder_decision_gate():
    state = valid_state()
    state["next_action"]["requires_new_founder_choice"] = True
    out = evaluate(state)
    assert out["reason"] == "AUTO_CONTINUE_CONTRADICTS_FOUNDER_DECISION_GATE"


def test_recovery_can_complete_without_auto_continue():
    state = valid_state()
    state["completion_gate"]["can_auto_continue"] = False
    state["next_action"]["requires_human_evidence"] = True
    state["next_action"]["executable_here"] = False
    out = evaluate(state)
    assert out["decision"] == "RECOVERY_COMPLETE"
    assert out["can_auto_continue_after_normal_action_gates"] is False
