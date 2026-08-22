import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import fidelity_checker as fc

TRUTH = ROOT / "01_SOURCE_TRUTH.json"
GOOD = ROOT / "fixtures" / "good.dclg.xml"
DRIFT = ROOT / "fixtures" / "semantic_drift.dclg.xml"


def test_good_fixture_preserves_logical_ampersand_and_source_truth():
    result = fc.check(TRUTH, GOOD)
    assert result["status"] == "PASS_FIDELITY"
    assert result["observed_text_blocks"][0] == "Peter Thomas & Christian Johnston"
    assert result["mismatches"] == []
    assert result["official_structural_validation_proven_by_this_checker"] is False


def test_schema_candidate_with_semantic_drift_is_detected():
    result = fc.check(TRUTH, DRIFT)
    assert result["status"] == "FAIL_FIDELITY"
    assert result["mismatches"] == [
        {
            "index": 0,
            "expected": "Peter Thomas & Christian Johnston",
            "observed": "Peter Thomas and Christian Johnston",
            "kind": "TEXT_MISMATCH",
        }
    ]


def test_checker_never_promotes_market_or_external_evidence():
    for path in (GOOD, DRIFT):
        result = fc.check(TRUTH, path)
        assert result["buyer_demand_proven"] is False
        assert result["wtp_proven"] is False
        assert result["transaction_proven"] is False
        assert result["profitability_proven"] is False
        assert result["external_action_authorized"] is False


def test_missing_source_truth_fails_closed(tmp_path):
    missing = tmp_path / "missing.json"
    result = fc.check(missing, GOOD)
    assert result["status"] == "HOLD_INPUT_UNRESOLVED"
    assert any(x.startswith("SOURCE_TRUTH_UNREADABLE") for x in result["problems"])


def test_empty_source_truth_fails_closed(tmp_path):
    p = tmp_path / "truth.json"
    p.write_text(json.dumps({"expected_text_blocks": []}), encoding="utf-8")
    result = fc.check(p, GOOD)
    assert result["status"] == "HOLD_INPUT_UNRESOLVED"
    assert "SOURCE_TRUTH_EXPECTED_TEXT_BLOCKS_MISSING" in result["problems"]


def test_wrong_doclang_namespace_fails_closed(tmp_path):
    p = tmp_path / "bad.dclg.xml"
    p.write_text("<doclang><text>Hello</text></doclang>", encoding="utf-8")
    result = fc.check(TRUTH, p)
    assert result["status"] == "HOLD_INPUT_UNRESOLVED"
    assert "DOCLANG_NAMESPACE_OR_ROOT_MISMATCH" in result["problems"]


def test_block_count_loss_is_detected(tmp_path):
    p = tmp_path / "loss.dclg.xml"
    p.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<doclang xmlns="https://www.doclang.ai/ns/v0">\n'
        '<head><default_resolution width="512" height="512"/></head>\n'
        '<text><location value="50"/><location value="80"/><location value="200"/><location value="120"/>'
        'Peter Thomas &amp; Christian Johnston</text><page_break/></doclang>',
        encoding="utf-8",
    )
    result = fc.check(TRUTH, p)
    assert result["status"] == "FAIL_FIDELITY"
    assert result["mismatches"][-1]["kind"] == "BLOCK_COUNT_MISMATCH"
    assert result["mismatches"][-1]["expected"] == "B"
    assert result["mismatches"][-1]["observed"] is None
