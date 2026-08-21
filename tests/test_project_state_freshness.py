from tools.ivdivo_project_state_freshness import audit as freshness_audit
from tools.validate_authority_version_chain import audit as chain_audit


def manifest():
    return {
        "project_id": "D06",
        "sources": [
            {"source_key":"historical","locator":"drive:old","revision":"r1","authority_rank":1,"disposition":"SUPERSEDED","supersedes":[]},
            {"source_key":"current","locator":"drive:current","revision":"r2","authority_rank":2,"disposition":"CURRENT","supersedes":["historical"]},
        ],
    }


def live_same():
    return {
        "sources": [
            {"source_key":"historical","locator":"drive:old","revision":"r1","authority_rank":1,"disposition":"SUPERSEDED"},
            {"source_key":"current","locator":"drive:current","revision":"r2","authority_rank":2,"disposition":"CURRENT"},
        ]
    }


def test_unchanged_snapshot_is_fresh():
    result = freshness_audit(manifest(), live_same())
    assert result["status"] == "PASS_FRESH"
    assert result["canon_changed"] is False


def test_revision_change_requires_rebase_not_canon_mutation():
    live = live_same()
    live["sources"][1]["revision"] = "r3"
    result = freshness_audit(manifest(), live)
    assert result["status"] == "STALE_REBASE_REQUIRED"
    assert result["semantic_reread_required"] is True
    assert result["canon_changed"] is False
    assert any(x["reason"] == "REVISION_CHANGED" for x in result["stale"])


def test_new_current_authority_requires_rebase():
    live = live_same()
    live["sources"][1]["disposition"] = "SUPERSEDED"
    live["sources"].append({"source_key":"new","locator":"drive:new","revision":"r4","authority_rank":3,"disposition":"CURRENT"})
    result = freshness_audit(manifest(), live)
    assert result["status"] == "STALE_REBASE_REQUIRED"
    assert any(x["reason"] == "CURRENT_AUTHORITY_CHANGED" for x in result["stale"])


def test_missing_observation_requires_review_not_fake_freshness():
    live = live_same()
    live["sources"] = [live["sources"][1]]
    result = freshness_audit(manifest(), live)
    assert result["status"] == "REVIEW_REQUIRED"


def test_valid_authority_chain_passes():
    assert chain_audit(manifest())["status"] == "PASS"


def test_two_current_sources_fail():
    bad = manifest()
    bad["sources"][0]["disposition"] = "CURRENT"
    result = chain_audit(bad)
    assert result["status"] == "FAIL"
    assert any(x.startswith("CURRENT_COUNT") for x in result["errors"])


def test_supersession_cycle_fails():
    bad = manifest()
    bad["sources"][0]["supersedes"] = ["current"]
    result = chain_audit(bad)
    assert result["status"] == "FAIL"
    assert any(x.startswith("SUPERSESSION_CYCLE") for x in result["errors"])


def test_current_must_be_highest_rank():
    bad = manifest()
    bad["sources"][0]["authority_rank"] = 3
    result = chain_audit(bad)
    assert "CURRENT_NOT_HIGHEST_RANK" in result["errors"]
