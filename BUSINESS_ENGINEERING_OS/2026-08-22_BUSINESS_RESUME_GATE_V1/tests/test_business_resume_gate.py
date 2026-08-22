import importlib.util
from pathlib import Path

MODULE = Path(__file__).parents[1] / "runtime" / "business_resume_gate.py"
spec = importlib.util.spec_from_file_location("business_resume_gate", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
BusinessResumeState = mod.BusinessResumeState
route_business_resume = mod.route_business_resume


def check(state, route, prompt=None):
    out = route_business_resume(state)
    assert out["route"] == route, out
    assert out["earliest_prompt"] == prompt, out
    assert out["external_action_authorized"] is False
    assert out["proof_promotion"] is False
    return out


def test_current_real_state_protects_no_change():
    out = check(BusinessResumeState(), "PROTECT_NO_CHANGE", None)
    assert "P225_OR_P235" in out["reason"]


def test_target_pack_event_resumes_processing_not_bidding():
    check(BusinessResumeState(target_pack_acquired=True), "RESUME_P226_P234", 226)


def test_bidder_designation_alone_routes_back_to_missing_target_pack():
    check(BusinessResumeState(actual_bidder_designation=True), "RESUME_P225", 225)


def test_target_registry_without_bidder_routes_p235():
    check(
        BusinessResumeState(target_pack_acquired=True, target_requirement_registry_ready=True),
        "RESUME_P235",
        235,
    )


def test_designated_bidder_without_packet_routes_p236():
    check(
        BusinessResumeState(
            target_pack_acquired=True,
            target_requirement_registry_ready=True,
            actual_bidder_designation=True,
        ),
        "RESUME_P236_P251",
        236,
    )


def test_authorities_without_both_frozen_manifests_hold():
    check(
        BusinessResumeState(
            target_pack_acquired=True,
            target_requirement_registry_ready=True,
            actual_bidder_designation=True,
            authoritative_bidder_packet_ready=True,
        ),
        "HOLD_FREEZE_BOTH_MANIFESTS",
        252,
    )


def test_both_frozen_manifests_resume_atomic_chain():
    check(
        BusinessResumeState(
            target_pack_acquired=True,
            target_requirement_registry_ready=True,
            actual_bidder_designation=True,
            authoritative_bidder_packet_ready=True,
            frozen_target_manifest=True,
            frozen_bidder_manifest=True,
        ),
        "RESUME_P252_P280",
        252,
    )


def test_decision_packet_without_reviewer_holds_p281():
    check(
        BusinessResumeState(
            target_pack_acquired=True,
            target_requirement_registry_ready=True,
            actual_bidder_designation=True,
            authoritative_bidder_packet_ready=True,
            frozen_target_manifest=True,
            frozen_bidder_manifest=True,
            bounded_decision_packet_ready=True,
        ),
        "HOLD_P281_P283_REVIEWER",
        281,
    )


def test_reviewer_ready_does_not_authorize_external_action():
    check(
        BusinessResumeState(
            target_pack_acquired=True,
            target_requirement_registry_ready=True,
            actual_bidder_designation=True,
            authoritative_bidder_packet_ready=True,
            frozen_target_manifest=True,
            frozen_bidder_manifest=True,
            bounded_decision_packet_ready=True,
            independent_reviewer_ready=True,
        ),
        "RESUME_P281_P283_THEN_HOLD_EXTERNAL",
        281,
    )


def test_explicit_external_authorization_routes_p284_without_claiming_action_authority():
    check(
        BusinessResumeState(
            target_pack_acquired=True,
            target_requirement_registry_ready=True,
            actual_bidder_designation=True,
            authoritative_bidder_packet_ready=True,
            frozen_target_manifest=True,
            frozen_bidder_manifest=True,
            bounded_decision_packet_ready=True,
            independent_reviewer_ready=True,
            external_interaction_authorized=True,
        ),
        "RESUME_P284_P287",
        284,
    )


def test_completed_real_use_derives_new_frontier_not_p288_replay():
    out = check(
        BusinessResumeState(
            target_pack_acquired=True,
            target_requirement_registry_ready=True,
            actual_bidder_designation=True,
            authoritative_bidder_packet_ready=True,
            frozen_target_manifest=True,
            frozen_bidder_manifest=True,
            bounded_decision_packet_ready=True,
            independent_reviewer_ready=True,
            external_interaction_authorized=True,
            real_decision_use_ready=True,
        ),
        "DERIVE_NEW_FRONTIER_AFTER_REAL_EVIDENCE",
        None,
    )
    assert "DO_NOT_REEXECUTE_P288" in out["reason"]


def test_impossible_registry_without_pack_fails_closed():
    check(BusinessResumeState(target_requirement_registry_ready=True), "HOLD_INCONSISTENT_STATE", None)


def test_impossible_bidder_packet_without_designation_fails_closed():
    check(BusinessResumeState(authoritative_bidder_packet_ready=True), "HOLD_INCONSISTENT_STATE", None)


def test_impossible_frozen_target_without_registry_fails_closed():
    check(
        BusinessResumeState(target_pack_acquired=True, frozen_target_manifest=True),
        "HOLD_INCONSISTENT_STATE",
        None,
    )


def test_impossible_decision_packet_without_manifests_fails_closed():
    check(BusinessResumeState(bounded_decision_packet_ready=True), "HOLD_INCONSISTENT_STATE", None)


def test_real_use_without_external_authorization_fails_closed():
    check(BusinessResumeState(real_decision_use_ready=True), "HOLD_INCONSISTENT_STATE", None)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"BUSINESS_RESUME_GATE_V1: {len(tests)}/{len(tests)} PASS")
