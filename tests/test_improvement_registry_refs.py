from tools.validate_improvement_registry_refs import audit
import json


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def _candidate(cid="SI-0008", status="VERIFIED_CURRENT"):
    return {
        "candidate_id": cid,
        "title": "candidate",
        "candidate_type": "PROGRAM_OR_CODE",
        "status": status,
        "scope": "UNIVERSAL_IVDIVO",
        "source_provenance": [{"source_type": "GITHUB", "locator": "fixture"}],
        "owner_role": "test",
        "next_action": "next",
        "next_gate": "gate",
        "application_targets": ["x"],
        "verification_evidence": ["evidence"] if status == "VERIFIED_CURRENT" else [],
    }


def test_state_reference_must_resolve_exactly_once(tmp_path):
    state = tmp_path / "state.json"
    registry = tmp_path / "registry.json"
    ext = tmp_path / "ext"
    _write(state, {"current_candidate": "SI-0008"})
    _write(registry, {"candidates": []})
    result = audit(state, registry, ext)
    assert result["status"] == "FAIL"
    assert {"candidate_id": "SI-0008", "error": "STATE_REFERENCE_NOT_REGISTERED"} in result["errors"]


def test_extension_record_satisfies_state_reference(tmp_path):
    state = tmp_path / "state.json"
    registry = tmp_path / "registry.json"
    ext = tmp_path / "ext"
    _write(state, {"registry_candidate_record": "SI-0008"})
    _write(registry, {"candidates": []})
    _write(ext / "SI-0008.json", _candidate())
    result = audit(state, registry, ext)
    assert result["status"] == "PASS"
    assert "SI-0008" in result["registered_candidate_ids"]


def test_verified_current_requires_verification_evidence(tmp_path):
    state = tmp_path / "state.json"
    registry = tmp_path / "registry.json"
    _write(state, {})
    broken = _candidate()
    broken["verification_evidence"] = []
    _write(registry, {"candidates": [broken]})
    result = audit(state, registry, None)
    assert result["status"] == "FAIL"
    assert any(e["candidate_id"] == "SI-0008" and "verification_evidence" in e["error"] for e in result["errors"])


def test_duplicate_id_across_base_and_extension_fails_closed(tmp_path):
    state = tmp_path / "state.json"
    registry = tmp_path / "registry.json"
    ext = tmp_path / "ext"
    _write(state, {"current_candidate": "SI-0008"})
    _write(registry, {"candidates": [_candidate()]})
    _write(ext / "SI-0008.json", _candidate())
    try:
        audit(state, registry, ext)
    except ValueError as exc:
        assert "duplicate candidate_id" in str(exc)
    else:
        raise AssertionError("duplicate candidate_id must fail closed")
