import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

import agent_commerce_readiness as scanner
import run_blind_test


def load_inputs():
    return json.loads((ROOT / "02_FIXTURE_INPUTS.json").read_text(encoding="utf-8"))["fixtures"]


def test_exactly_ten_blind_fixtures():
    assert len(load_inputs()) == 10


def test_fixture_ids_have_no_merchant_names_in_scanner_input():
    raw = (ROOT / "02_FIXTURE_INPUTS.json").read_text(encoding="utf-8").lower()
    patterns = [
        r"\betsy\b",
        r"\btarget\b",
        r"\bsephora\b",
        r"\bnordstrom\b",
        r"\blowe(?:'s|s)?\b",
        r"\bbest buy\b",
        r"\bhome depot\b",
        r"\bwayfair\b",
        r"\bglossier\b",
        r"\blloyds online\b",
    ]
    for pattern in patterns:
        assert re.search(pattern, raw) is None


def test_public_ucp_profile_is_positive_not_full_conformance_claim():
    result = scanner.scan_fixture(load_inputs()[0])
    assert result.disposition == "PUBLIC_PROTOCOL_SURFACE_PRESENT_BACKEND_UNVERIFIED"
    assert "UCP_PROFILE_PUBLICLY_OBSERVED" in result.positive_signals
    assert any(
        f.dimension == "authorization_trust_controls" and f.classification == "NOT_OBSERVABLE_PUBLICLY"
        for f in result.findings
    )


def test_documented_discovery_never_auto_promotes_checkout():
    fixture = copy.deepcopy(load_inputs()[2])
    assert fixture["observations"]["official_agentic_discovery"] == "PRESENT"
    assert fixture["observations"]["protocol_checkout_surface"] == "VENDOR_SPECIFIC_UNKNOWN"
    result = scanner.scan_fixture(fixture)
    assert result.disposition == "DISCOVERY_READY_SIGNAL_CHECKOUT_UNVERIFIED"
    assert result.proof_promotion is False


def test_verified_absence_is_actionable_but_nonfinding_is_not():
    fixture = copy.deepcopy(load_inputs()[2])
    fixture["observations"]["ucp_public_profile"] = "ABSENT_VERIFIED"
    result = scanner.scan_fixture(fixture)
    assert result.disposition == "PROTOCOL_SPECIFIC_GAP_FOUND"
    assert any(f.classification == "ACTIONABLE_GAP" for f in result.findings)


def test_not_observable_fails_closed_without_actionable_gap():
    result = scanner.scan_fixture(load_inputs()[2])
    assert not any(f.classification == "ACTIONABLE_GAP" for f in result.findings)
    assert any(f.classification == "NOT_OBSERVABLE_PUBLICLY" for f in result.findings)


def test_generic_seo_flag_cannot_change_route():
    a = copy.deepcopy(load_inputs()[2])
    b = copy.deepcopy(a)
    a["generic_seo_signal"] = True
    b["generic_seo_signal"] = False
    ra = scanner.scan_fixture(a)
    rb = scanner.scan_fixture(b)
    assert ra.disposition == rb.disposition
    assert ra.positive_signals == rb.positive_signals
    assert [f.classification for f in ra.findings] == [f.classification for f in rb.findings]


def test_invalid_observation_state_is_rejected():
    fixture = copy.deepcopy(load_inputs()[0])
    fixture["observations"]["ucp_public_profile"] = "MAYBE"
    try:
        scanner.scan_fixture(fixture)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid state must fail closed")


def test_dimension_omission_is_rejected():
    fixture = copy.deepcopy(load_inputs()[0])
    del fixture["observations"]["payment_handler_boundary"]
    try:
        scanner.scan_fixture(fixture)
    except ValueError:
        pass
    else:
        raise AssertionError("missing dimension must fail closed")


def test_blind_result_counts_are_deterministic():
    result = run_blind_test.run()
    assert result["fixture_count"] == 10
    assert result["positive_signal_count"] == 36
    assert result["issue_counts"] == {
        "NOT_OBSERVABLE_PUBLICLY": 28,
        "VENDOR_SPECIFIC_UNKNOWN": 26,
    }
    assert result["public_only_actionable_gap_count"] == 0


def test_blind_dispositions_are_deterministic():
    result = run_blind_test.run()
    assert result["disposition_counts"] == {
        "DISCOVERY_AND_CHANNEL_SIGNAL_BACKEND_UNVERIFIED": 1,
        "DISCOVERY_READY_SIGNAL_CHECKOUT_UNVERIFIED": 8,
        "PUBLIC_PROTOCOL_SURFACE_PRESENT_BACKEND_UNVERIFIED": 1,
    }


def test_blind_test_has_no_generic_advice_and_no_proof_promotion():
    result = run_blind_test.run()
    assert result["generic_seo_advice_emitted"] is False
    assert result["proof_promotion"] is False
    assert result["external_action_authorized"] is False
    scanner.validate_no_generic_advice(result["results"])
