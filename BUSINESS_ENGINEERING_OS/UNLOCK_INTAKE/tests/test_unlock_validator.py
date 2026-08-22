import importlib.util
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
        mod.pack.FileRecord(
            filename="01_instructions.pdf",
            sha256="a" * 64,
            size=100,
            media_type="application/pdf",
            source_ref="official-export://8872468/01",
        ),
        mod.pack.FileRecord(
            filename="02_pricing.xlsx",
            sha256="b" * 64,
            size=200,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            source_ref="official-export://8872468/02",
        ),
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
    assert r["admissible_for_ingest"] is True
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
    expected = ["01_instructions.pdf", "02_pricing.xlsx"]
    r = mod.validate_p225_input(
        receipt=receipt(), files=files(), authoritative_expected_ids=expected,
        authoritative_completeness_evidence=True,
    )
    assert r["status"] == "P225_INPUT_ADMISSIBLE_COMPLETE_BY_AUTHORITY_GATE"
    assert r["inventory"]["authoritatively_complete"] is True


def test_p235_test_fixture_never_unlocks():
    r = mod.validate_p235_input(designation(mode="TEST_FIXTURE_ONLY"))
    assert r["status"] == "TEST_FIXTURE_ONLY_NOT_BIDDER"
    assert r["admissible_for_authority_review"] is False


def test_p235_incomplete_designation_holds():
    r = mod.validate_p235_input(designation(authorized_designator=None))
    assert r["status"] == "HOLD_INCOMPLETE_EXPLICIT_DESIGNATION"


def test_p235_wrong_resource_holds():
    r = mod.validate_p235_input(designation(resource_id="8176962"))
    assert r["status"] == "HOLD_P235_RESOURCE_MISMATCH"


def test_p235_wrong_entity_holds():
    r = mod.validate_p235_input(designation(legal_entity="OTHER LIMITED"))
    assert r["status"] == "HOLD_P235_LEGAL_ENTITY_MISMATCH"


def test_p235_scope_widening_holds():
    r = mod.validate_p235_input(designation(scope="SUBMIT_TENDER_AND_ACCEPT_CONTRACT"))
    assert r["status"] == "HOLD_P235_SCOPE_NOT_INTERNAL_ONLY"
    assert r["admissible_for_authority_review"] is False


def test_p235_valid_internal_designation_is_candidate_only():
    r = mod.validate_p235_input(designation())
    assert r["status"] == "P235_INPUT_ADMISSIBLE_FOR_AUTHORITY_REVIEW"
    assert r["admissible_for_authority_review"] is True
    assert r["root_authority_mutated"] is False


def test_both_valid_candidates_still_do_not_mutate_authority():
    p225 = mod.validate_p225_input(receipt=receipt(), files=files())
    p235 = mod.validate_p235_input(designation())
    r = mod.unlock_readiness(p225_result=p225, p235_result=p235)
    assert r["both_candidate_inputs_ready"] is True
    assert r["authority_mutation"] is False
    assert r["proof_promotion"] is False
    assert r["external_action_authorized"] is False
