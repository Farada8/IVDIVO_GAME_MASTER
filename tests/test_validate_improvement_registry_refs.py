import json
from pathlib import Path

from tools.validate_improvement_registry_refs import audit


def write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj), encoding="utf-8")


def base_candidate(cid="SI-0007", status="VERIFIED_CURRENT"):
    return {
        "candidate_id": cid,
        "title": "x",
        "candidate_type": "PROGRAM_OR_CODE",
        "status": status,
        "scope": "UNIVERSAL_IVDIVO",
        "source_provenance": [{"source_type":"TEST"}],
        "owner_role": "tester",
        "next_action": "next",
        "next_gate": "gate",
        "application_targets": ["x"],
        "verification_evidence": ["test"] if status == "VERIFIED_CURRENT" else [],
        "hold_trigger": "trigger" if status == "HOLD_WITH_TRIGGER" else None,
        "terminal_reason": "reason" if status in {"REJECTED","SUPERSEDED","ROLLED_BACK"} else None,
    }


def test_state_reference_can_be_satisfied_by_extension(tmp_path):
    state = {"current_candidate":"SI-0007", "promotion_status":{"registry_candidate_record":"SI-0008_WRITE_THROUGH_PENDING_SELF_REFERENCE_HYGIENE"}}
    write(tmp_path / "state.json", state)
    write(tmp_path / "registry.json", {"candidates":[base_candidate("SI-0007")]})
    write(tmp_path / "extensions" / "si8.json", base_candidate("SI-0008"))
    result = audit(tmp_path / "state.json", tmp_path / "registry.json", tmp_path / "extensions")
    assert result["status"] == "PASS"
    assert result["referenced_candidate_ids"] == ["SI-0007", "SI-0008"]


def test_missing_referenced_candidate_fails(tmp_path):
    write(tmp_path / "state.json", {"current_candidate":"SI-0008"})
    write(tmp_path / "registry.json", {"candidates":[base_candidate("SI-0007")]})
    result = audit(tmp_path / "state.json", tmp_path / "registry.json", None)
    assert result["status"] == "FAIL"
    assert any(e["error"] == "STATE_REFERENCE_NOT_REGISTERED" for e in result["errors"])


def test_verified_without_evidence_fails(tmp_path):
    item = base_candidate("SI-0008")
    item["verification_evidence"] = []
    write(tmp_path / "state.json", {"current_candidate":"SI-0008"})
    write(tmp_path / "registry.json", {"candidates":[item]})
    result = audit(tmp_path / "state.json", tmp_path / "registry.json", None)
    assert result["status"] == "FAIL"
    assert any("verification_evidence" in e["error"] for e in result["errors"])


def test_duplicate_id_across_base_and_extensions_raises(tmp_path):
    write(tmp_path / "state.json", {"current_candidate":"SI-0007"})
    write(tmp_path / "registry.json", {"candidates":[base_candidate("SI-0007")]})
    write(tmp_path / "extensions" / "dup.json", base_candidate("SI-0007"))
    import pytest
    with pytest.raises(ValueError):
        audit(tmp_path / "state.json", tmp_path / "registry.json", tmp_path / "extensions")
