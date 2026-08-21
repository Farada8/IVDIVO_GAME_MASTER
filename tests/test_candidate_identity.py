import json
from pathlib import Path

from tools.ivdivo_candidate_identity import audit_repo, next_free_id


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def candidate(cid, title="candidate", mechanism="mechanism"):
    return {
        "candidate_id": cid,
        "title": title,
        "candidate_type": "TOOLING_OR_AUTOMATION",
        "status": "READY_FOR_PILOT",
        "scope": "UNIVERSAL_IVDIVO",
        "problem_or_opportunity": "problem",
        "proposed_mechanism": mechanism,
        "dedupe_relation": "EXTENSION",
    }


def make_repo(tmp_path: Path):
    base = tmp_path / "31_IDEAS" / "CURRENT_IMPROVEMENT_REGISTRY.json"
    ext = tmp_path / "31_IDEAS" / "REGISTRY_EXTENSIONS"
    pending = tmp_path / "31_IDEAS" / "PENDING"
    family = tmp_path / "31_IDEAS" / "CURRENT_IMPROVEMENT_REGISTRY_FAMILY.json"
    debt = tmp_path / "31_IDEAS" / "CANDIDATE_IDENTITY_MIGRATION_DEBT.json"
    write_json(base, {"candidates": [candidate("SI-0008", "recovery", "recover transcripts")]})
    write_json(family, {"known_extensions": []})
    write_json(debt, {"tracked_collisions": []})
    return base, ext, pending, family, debt


def test_different_mechanisms_same_id_fail(tmp_path):
    base, ext, pending, family, debt = make_repo(tmp_path)
    write_json(ext / "a.json", candidate("SI-0009", "recovery v2", "reconcile recovery"))
    write_json(pending / "b.json", candidate("SI-0009", "audio compiler", "repair audio"))
    result = audit_repo(tmp_path, base, [ext, pending], family, debt)
    assert result["status"] == "FAIL"
    assert result["collisions"][0]["classification"] == "ID_COLLISION_DIFFERENT_MECHANISM"


def test_exact_tracked_collision_becomes_debt_not_pass(tmp_path):
    base, ext, pending, family, debt = make_repo(tmp_path)
    write_json(ext / "a.json", candidate("SI-0010", "registry", "transaction"))
    write_json(pending / "b.json", candidate("SI-0010", "session", "checkpoint"))
    write_json(family, {"known_extensions": ["31_IDEAS/REGISTRY_EXTENSIONS/a.json"]})
    write_json(debt, {"tracked_collisions": [{
        "candidate_id": "SI-0010",
        "expected_source_paths": ["31_IDEAS/PENDING/b.json", "31_IDEAS/REGISTRY_EXTENSIONS/a.json"],
        "repair_locator": "PR108"
    }]})
    result = audit_repo(tmp_path, base, [ext, pending], family, debt)
    assert result["status"] == "PASS_WITH_TRACKED_DEBT"
    assert result["promotion_eligible"] is False
    assert result["tracked_collision_debt"][0]["candidate_id"] == "SI-0010"


def test_redirect_preserves_history_without_active_collision(tmp_path):
    base, ext, pending, family, debt = make_repo(tmp_path)
    write_json(ext / "SI-0015.json", candidate("SI-0015", "audio", "repair audio"))
    write_json(pending / "old.json", {
        "record_type": "CANDIDATE_ID_REDIRECT",
        "old_candidate_id": "SI-0009",
        "new_candidate_id": "SI-0015",
        "reason": "identity repair",
    })
    write_json(family, {"known_extensions": ["31_IDEAS/REGISTRY_EXTENSIONS/SI-0015.json"]})
    result = audit_repo(tmp_path, base, [ext, pending], family, debt)
    assert result["status"] == "PASS"
    assert any(r["new_candidate_id"] == "SI-0015" for r in result["redirects"])


def test_dangling_redirect_fails(tmp_path):
    base, ext, pending, family, debt = make_repo(tmp_path)
    write_json(pending / "old.json", {
        "record_type": "CANDIDATE_ID_REDIRECT",
        "old_candidate_id": "SI-0009",
        "new_candidate_id": "SI-0099",
        "reason": "bad target",
    })
    result = audit_repo(tmp_path, base, [ext, pending], family, debt)
    assert result["status"] == "FAIL"
    assert any(x.startswith("DANGLING_REDIRECT") for x in result["errors"])


def test_unindexed_extension_is_tracked_debt_not_clean_pass(tmp_path):
    base, ext, pending, family, debt = make_repo(tmp_path)
    write_json(ext / "SI-0015.json", candidate("SI-0015"))
    result = audit_repo(tmp_path, base, [ext, pending], family, debt)
    assert result["status"] == "PASS_WITH_TRACKED_DEBT"
    assert "31_IDEAS/REGISTRY_EXTENSIONS/SI-0015.json" in result["unindexed_extensions"]


def test_next_free_respects_reserved_ids():
    assert next_free_id({"SI-0001", "SI-0002"}, {"SI-0003"}) == "SI-0004"
