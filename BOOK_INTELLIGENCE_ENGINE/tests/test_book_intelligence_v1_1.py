import importlib.util
import json
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[2] / "tools" / "ivdivo_book_intelligence.py"
spec = importlib.util.spec_from_file_location("book_intelligence", RUNTIME)
bi = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(bi)


def nasa_source():
    return {
        "source_id": "OPEN-NASA-SE-HANDBOOK",
        "title": "NASA Systems Engineering Handbook",
        "provenance": "NASA official",
        "rights_status": "PUBLIC_DOMAIN",
        "independent_source_group": "NASA-SE",
        "content_locator": "official:NTRS-20170001761",
        "integrity_status": "VERIFIED",
        "read_coverage": "PARTIAL_TARGETED",
        "extraction_stage": "MECHANISMS_EXTRACTED",
    }


def mechanism_card(pilots=None):
    return {
        "mechanism_id": "M",
        "statement": "Separate verification from validation.",
        "source_ids": ["NASA"],
        "evidence_locators": ["NASA/SP-2016-6105 Rev2 §5.3"],
        "failure_modes": [],
        "domain_targets": ["GENERAL"],
        "abstraction_level": "PROJECT_NEUTRAL",
        "project_specific_expression_removed": True,
        "pilot_evidence": pilots or [],
    }


def trace_bundle():
    return {
        "bundle_id": "fixture",
        "requires_end_to_end": True,
        "nodes": [
            {"id": "s", "type": "SOURCE"},
            {"id": "sec", "type": "SECTION"},
            {"id": "c", "type": "CLAIM"},
            {"id": "m", "type": "MECHANISM"},
            {"id": "a", "type": "ADAPTER"},
            {"id": "p", "type": "PROJECT_APPLICATION"},
            {"id": "t", "type": "TEST"},
            {"id": "r", "type": "RESULT"},
            {"id": "l", "type": "LEARNING"},
            {"id": "e", "type": "ENGINE_RULE"},
        ],
        "edges": [
            {"from_id": "s", "to_id": "sec", "relation": "SOURCE_HAS_SECTION"},
            {"from_id": "sec", "to_id": "c", "relation": "SECTION_SUPPORTS_CLAIM"},
            {"from_id": "c", "to_id": "m", "relation": "CLAIM_ABSTRACTS_TO_MECHANISM"},
            {"from_id": "m", "to_id": "a", "relation": "MECHANISM_PACKED_FOR_DOMAIN"},
            {"from_id": "a", "to_id": "p", "relation": "ADAPTER_APPLIED_TO_PROJECT"},
            {"from_id": "p", "to_id": "t", "relation": "PROJECT_APPLICATION_TESTED_BY"},
            {"from_id": "t", "to_id": "r", "relation": "TEST_PRODUCED_RESULT"},
            {"from_id": "r", "to_id": "l", "relation": "RESULT_PROMOTED_TO_LEARNING"},
            {"from_id": "l", "to_id": "e", "relation": "LEARNING_CHANGED_ENGINE_RULE"},
        ],
    }


def test_partial_targeted_mechanism_does_not_require_full_read():
    source = nasa_source()
    assert bi.validate_source_passport(source) == []
    assert bi.source_can_support_mechanism(source) is True
    assert bi.migrate_source_state(source)["read_coverage"] == "PARTIAL_TARGETED"


def test_legacy_structure_mapped_migrates_without_mechanism_eligibility():
    source = {
        "source_id": "X", "title": "X", "provenance": "drive",
        "rights_status": "ACCESS_ONLY", "independent_source_group": "X",
        "content_locator": "x", "lifecycle_stage": "STRUCTURE_MAPPED",
    }
    assert bi.migrate_source_state(source) == {
        "integrity_status": "VERIFIED", "read_coverage": "STRUCTURE_ONLY", "extraction_stage": "NONE"
    }
    assert bi.source_can_support_mechanism(source) is False


def test_complete_traceability_chain_passes():
    assert bi.audit_traceability_bundle(trace_bundle())["status"] == "PASS"


def test_broken_traceability_chain_fails():
    bundle = json.loads(json.dumps(trace_bundle()))
    bundle["edges"] = [e for e in bundle["edges"] if e["relation"] != "CLAIM_ABSTRACTS_TO_MECHANISM"]
    result = bi.audit_traceability_bundle(bundle)
    assert result["status"] == "FAIL"
    assert any(x.startswith("result_not_traceable_to_source") for x in result["errors"])


def test_change_impact_propagates_to_all_descendants():
    assert bi.change_impact_set(trace_bundle(), ["c"]) == ["a", "e", "l", "m", "p", "r", "t"]


def test_engineering_verification_does_not_promote():
    passports = {"NASA": {**nasa_source(), "source_id": "NASA"}}
    card = mechanism_card([{
        "project_id": "P1", "status": "PASS", "evidence_class": "ENGINEERING_VERIFICATION", "measurable_gain": True
    }])
    assert bi.promotion_decision(card, passports)["disposition"] == "LOCAL_TEST"


def test_one_real_validation_project_is_not_promotable():
    passports = {"NASA": {**nasa_source(), "source_id": "NASA"}}
    card = mechanism_card([{
        "project_id": "P1", "status": "PASS", "evidence_class": "REAL_PROJECT_VALIDATION", "measurable_gain": True
    }])
    assert bi.promotion_decision(card, passports)["disposition"] == "PILOT_READY"


def test_two_real_validation_projects_with_gain_can_promote():
    passports = {"NASA": {**nasa_source(), "source_id": "NASA"}}
    card = mechanism_card([
        {"project_id": "P1", "status": "PASS", "evidence_class": "REAL_PROJECT_VALIDATION", "measurable_gain": True},
        {"project_id": "P2", "status": "PASS", "evidence_class": "REAL_PROJECT_VALIDATION", "measurable_gain": True},
    ])
    assert bi.promotion_decision(card, passports)["disposition"] == "PROMOTABLE"


def test_quarantined_source_cannot_support_extraction():
    source = nasa_source()
    source["integrity_status"] = "QUARANTINED"
    errors = bi.validate_source_passport(source)
    assert "invalid:extraction_from_failed_or_quarantined_source" in errors
    assert bi.source_can_support_mechanism(source) is False
