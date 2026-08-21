from tools.validate_project_state_coverage import audit


def test_pass_with_explicit_blocked_recovery():
    data = {
        "required_project_ids": ["D01", "D06"],
        "coverage": [{"project_id": "D06", "state_path": "PROJECT_STATES/D06.json", "recovery": "PASS"}],
        "blocked_recovery": [{"project_id": "D01", "status": "BLOCKED_RECOVERY", "reason": "exact authority not yet reconciled"}],
        "portfolio_resumability_claim": "PASS_WITH_BLOCKED_RECOVERY",
    }
    result = audit(data)
    assert result["status"] == "PASS"
    assert result["blocked_project_ids"] == ["D01"]


def test_missing_required_project_fails():
    data = {
        "required_project_ids": ["D01", "D06"],
        "coverage": [{"project_id": "D06", "state_path": "PROJECT_STATES/D06.json", "recovery": "PASS"}],
        "blocked_recovery": [],
        "portfolio_resumability_claim": "PASS_FULL",
    }
    result = audit(data)
    assert result["status"] == "FAIL"
    assert any(e.get("error") == "UNROUTED_PROJECT" and e.get("project_id") == "D01" for e in result["errors"])


def test_false_full_claim_fails_when_blocked_exists():
    data = {
        "required_project_ids": ["D01"],
        "coverage": [],
        "blocked_recovery": [{"project_id": "D01", "status": "BLOCKED_RECOVERY", "reason": "needs exact authority"}],
        "portfolio_resumability_claim": "PASS_FULL",
    }
    result = audit(data)
    assert result["status"] == "FAIL"
    assert any(e.get("error") == "RESUMABILITY_CLAIM_MISMATCH" for e in result["errors"])


def test_project_cannot_be_both_routed_and_blocked():
    data = {
        "required_project_ids": ["D06"],
        "coverage": [{"project_id": "D06", "state_path": "PROJECT_STATES/D06.json", "recovery": "PASS"}],
        "blocked_recovery": [{"project_id": "D06", "status": "BLOCKED_RECOVERY", "reason": "contradiction"}],
        "portfolio_resumability_claim": "PASS_WITH_BLOCKED_RECOVERY",
    }
    result = audit(data)
    assert result["status"] == "FAIL"
    assert any(e.get("error") == "PROJECT_BOTH_ROUTED_AND_BLOCKED" for e in result["errors"])
