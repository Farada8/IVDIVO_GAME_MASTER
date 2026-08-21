from tools.ivdivo_evidence_class_gate import audit_packet


def ev(eid, cls, family="one", status="PASS"):
    return {
        "evidence_id": eid,
        "evidence_class": cls,
        "source_locator": f"fixture:{eid}",
        "source_family": family,
        "status": status,
    }


def claim(cid, classes, minimum=None):
    row = {
        "claim_id": cid,
        "claim_text": cid,
        "required_evidence_classes": classes,
    }
    if minimum:
        row["minimum_independent_source_families"] = minimum
    return row


def test_ai_review_cannot_impersonate_human_signal():
    result = audit_packet({
        "claims": [claim("human_clarity", ["HUMAN_SIGNAL"])],
        "evidence": [ev("ai1", "INTERNAL_AI_REVIEW")],
    })
    assert result["status"] == "FAIL"
    hit = result["claim_results"][0]["forbidden_impersonations_detected"]
    assert {"offered_class": "INTERNAL_AI_REVIEW", "required_class": "HUMAN_SIGNAL"} in hit


def test_machine_test_cannot_impersonate_provider():
    result = audit_packet({
        "claims": [claim("provider_bound", ["PROVIDER"])],
        "evidence": [ev("unit", "DETERMINISTIC_MACHINE")],
    })
    assert result["status"] == "FAIL"


def test_source_hash_cannot_impersonate_market_evidence():
    result = audit_packet({
        "claims": [claim("market_success", ["MARKET"])],
        "evidence": [ev("hash", "SOURCE_PROVENANCE")],
    })
    assert result["status"] == "FAIL"


def test_story_or_machine_gate_cannot_clear_specialist_release():
    result = audit_packet({
        "claims": [claim("specialist_release", ["SPECIALIST"])],
        "evidence": [ev("storygate", "DETERMINISTIC_MACHINE")],
    })
    assert result["status"] == "FAIL"
    assert "SPECIALIST" in result["claim_results"][0]["missing_classes"]


def test_same_root_reports_do_not_satisfy_two_family_requirement():
    result = audit_packet({
        "claims": [claim("replication", ["PRODUCTION_OBSERVATION"], {"PRODUCTION_OBSERVATION": 2})],
        "evidence": [
            ev("r1", "PRODUCTION_OBSERVATION", family="same-root"),
            ev("r2", "PRODUCTION_OBSERVATION", family="same-root"),
        ],
    })
    assert result["status"] == "FAIL"
    failure = result["claim_results"][0]["independence_failures"][0]
    assert failure["actual"] == 1


def test_two_independent_human_families_can_satisfy_explicit_requirement():
    result = audit_packet({
        "claims": [claim("listener_replication", ["HUMAN_SIGNAL"], {"HUMAN_SIGNAL": 2})],
        "evidence": [
            ev("h1", "HUMAN_SIGNAL", family="listener-A"),
            ev("h2", "HUMAN_SIGNAL", family="listener-B"),
        ],
    })
    assert result["status"] == "PASS"
    assert result["promotion_or_lock"] == "NOT_AUTHORIZED_BY_THIS_GATE"


def test_founder_authority_is_not_inferred_from_other_evidence():
    result = audit_packet({
        "claims": [claim("founder_lock", ["FOUNDER_AUTHORITY"])],
        "evidence": [
            ev("ai", "INTERNAL_AI_REVIEW"),
            ev("human", "HUMAN_SIGNAL"),
            ev("machine", "DETERMINISTIC_MACHINE"),
        ],
    })
    assert result["status"] == "FAIL"
