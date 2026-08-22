import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "BUSINESS_ENGINEERING_OS/UNLOCK_INTAKE/engine/unlock_validator.py"
spec = importlib.util.spec_from_file_location("ivdivo_unlock_validator", PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules["ivdivo_unlock_validator"] = mod
spec.loader.exec_module(mod)


def receipt(resource="8872468"):
    return mod.pack.AcquisitionReceipt(
        resource_id=resource,
        channel="USER_PROVIDED_OFFICIAL_EXPORT",
        acquired_at="2026-08-22T06:00:00+01:00",
        actor="AUTHORIZED_USER",
        source_url="official-export://8872468",
        evidence_class="PRIVATE_PRIMARY_OFFICIAL_EXPORT",
    )


def files():
    return [
        mod.pack.FileRecord("01_instructions.pdf", "a" * 64, 100, "application/pdf", "official-export://8872468/01"),
        mod.pack.FileRecord("02_pricing.xlsx", "b" * 64, 200, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "official-export://8872468/02"),
    ]


def designation(**overrides):
    data = dict(
        resource_id="8872468",
        legal_entity="SYNTHESIS-IVDIVO LIMITED",
        authorized_designator="AUTHORIZED_FOUNDER_OR_OFFICER",
        designated_at="2026-08-22T06:00:00+01:00",
        scope=mod.INTERNAL_EVALUATION_SCOPE,
        active=True,
        mode="ACTUAL_BIDDER",
    )
    data.update(overrides)
    return mod.bidder.BidderDesignationV2(**data)


def test_p225_no_files_holds():
    r = mod.validate_p225_input(receipt=receipt(), files=[])
    assert r["status"] == "HOLD_P225_NO_FILES"
    assert r["admissible_for_ingest"] is False


def test_p225_resource_mismatch_holds():
    r = mod.validate_p225_input(receipt=receipt("8176962"), files=files())
    assert r["status"] == "HOLD_P225_INVALID_INPUT"
    assert "resource mismatch" in r["reason"]


def test_p225_credential_metadata_rejected():
    r = mod.validate_p225_input(receipt=receipt(), files=files(), metadata={"session_token": "secret"})
    assert r["status"] == "HOLD_P225_INVALID_INPUT"
    assert "credential-like" in r["reason"]


def test_p225_valid_export_keeps_completeness_separate():
    r = mod.validate_p225_input(receipt=receipt(), files=files())
    assert r["status"] == "P225_INPUT_ADMISSIBLE_COMPLETENESS_UNPROVEN"
    assert r["inventory"]["authoritatively_complete"] is False
    assert r["root_authority_mutated"] is False


def test_p225_partial_authoritative_inventory_is_not_complete():
    r = mod.validate_p225_input(
        receipt=receipt(), files=files(),
        authoritative_expected_ids=["01_instructions.pdf", "02_pricing.xlsx", "03_conditions.pdf"],
        authoritative_completeness_evidence=True,
    )
    assert r["status"] == "P225_INPUT_ADMISSIBLE_PARTIAL_INVENTORY"
    assert r["inventory"]["missing"] == ["03_conditions.pdf"]


def test_p225_complete_only_with_authoritative_completeness_evidence():
    r = mod.validate_p225_input(
        receipt=receipt(), files=files(),
        authoritative_expected_ids=["01_instructions.pdf", "02_pricing.xlsx"],
        authoritative_completeness_evidence=True,
    )
    assert r["status"] == "P225_INPUT_ADMISSIBLE_COMPLETE_BY_AUTHORITY_GATE"
    assert r["inventory"]["authoritatively_complete"] is True


def test_p235_test_fixture_never_unlocks():
    assert mod.validate_p235_input(designation(mode="TEST_FIXTURE_ONLY"))["status"] == "TEST_FIXTURE_ONLY_NOT_BIDDER"


def test_p235_incomplete_designation_holds():
    assert mod.validate_p235_input(designation(authorized_designator=None))["status"] == "HOLD_INCOMPLETE_EXPLICIT_DESIGNATION"


def test_p235_wrong_resource_holds():
    assert mod.validate_p235_input(designation(resource_id="8176962"))["status"] == "HOLD_P235_RESOURCE_MISMATCH"


def test_p235_wrong_entity_holds():
    assert mod.validate_p235_input(designation(legal_entity="OTHER LIMITED"))["status"] == "HOLD_P235_LEGAL_ENTITY_MISMATCH"


def test_p235_scope_widening_holds():
    assert mod.validate_p235_input(designation(scope="SUBMIT_TENDER_AND_ACCEPT_CONTRACT"))["status"] == "HOLD_P235_SCOPE_NOT_INTERNAL_ONLY"


def test_p235_valid_internal_designation_is_candidate_only():
    r = mod.validate_p235_input(designation())
    assert r["status"] == "P235_INPUT_ADMISSIBLE_FOR_AUTHORITY_REVIEW"
    assert r["root_authority_mutated"] is False


def test_both_valid_candidates_still_do_not_mutate_authority():
    p225 = mod.validate_p225_input(receipt=receipt(), files=files())
    p235 = mod.validate_p235_input(designation())
    r = mod.unlock_readiness(p225_result=p225, p235_result=p235)
    assert r["both_candidate_inputs_ready"] is True
    assert r["authority_mutation"] is False
    assert r["proof_promotion"] is False
    assert r["external_action_authorized"] is False


def test_validated_candidates_do_not_bypass_resume_gate_before_authority_commit():
    p225 = mod.validate_p225_input(receipt=receipt(), files=files())
    p235 = mod.validate_p235_input(designation())
    r = mod.unlock_readiness(p225_result=p225, p235_result=p235)
    assert r["current_resume_route_before_authority_commit"] == "PROTECT_NO_CHANGE"


def test_current_public_first_party_status_is_not_p225_pack_event():
    state_path = ROOT / "BUSINESS_ENGINEERING_OS/2026-08-22_P225_PUBLIC_FIRST_PARTY_STATUS_REFRESH/01_MACHINE_STATE.json"
    state = json.loads(state_path.read_text())
    assert state["source"]["class"] == "CURRENT_PUBLIC_FIRST_PARTY_INDEX"
    assert state["source"]["complete_attachment_inventory_observed"] is False
    assert state["source"]["complete_tender_document_bytes_observed"] is False
    assert state["target_pack_acquired"] is False
    assert state["resume_route"] == "PROTECT_NO_CHANGE"
    r = mod.validate_p225_input(receipt=receipt(), files=[])
    assert r["status"] == "HOLD_P225_NO_FILES"
