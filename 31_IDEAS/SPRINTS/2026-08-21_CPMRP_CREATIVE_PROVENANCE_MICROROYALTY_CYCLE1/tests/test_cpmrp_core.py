from cpmrp_core import *

def fixture():
    content = b"original world bible v1"
    asset_id = content_asset_id("demo", content, "v1")
    passport = AssetPassport(asset_id, "creator:A", RightsBasis.COPYRIGHT_ASSERTED, "p1")
    policy = RightsPolicy(asset_id, "p1", {
        Action.READ: PriceRule(Action.READ, PolicyState.FREE, 0),
        Action.INFERENCE_REFERENCE: PriceRule(Action.INFERENCE_REFERENCE, PolicyState.OFFER, 100_000),
        Action.TRAIN: PriceRule(Action.TRAIN, PolicyState.LICENSE_REQUIRED, 100_000),
    })
    return asset_id, passport, policy

def test_asset_id_deterministic():
    assert content_asset_id("demo", b"x", "v1") == content_asset_id("demo", b"x", "v1")

def test_read_is_free():
    aid, pp, pol = fixture()
    req = UsageRequest("u1","k1","payer",aid,Action.READ)
    d = evaluate_license(pp, pol, req)
    assert d.state == PolicyState.FREE and d.amount_micro_eur == 0 and not d.creates_debt

def test_reference_offer_is_ten_cents_but_not_debt_before_acceptance():
    aid, pp, pol = fixture()
    req = UsageRequest("u2","k2","payer",aid,Action.INFERENCE_REFERENCE)
    d = evaluate_license(pp, pol, req)
    assert d.amount_micro_eur == 100_000 and not d.creates_debt
    r = LicenseReceipt.build(req, pp, d, accepted=True)
    assert r.amount_micro_eur == 100_000

def test_unknown_fails_closed_without_debt():
    aid, pp, pol = fixture()
    req = UsageRequest("u3","k3","payer",aid,Action.ADAPT)
    d = evaluate_license(pp, pol, req)
    assert d.state == PolicyState.UNKNOWN and d.amount_micro_eur == 0 and not d.creates_debt

def test_public_domain_always_free():
    aid, _, pol = fixture()
    pp = AssetPassport(aid, "creator:A", RightsBasis.PUBLIC_DOMAIN, "p1")
    req = UsageRequest("u4","k4","payer",aid,Action.TRAIN)
    d = evaluate_license(pp, pol, req)
    assert d.state == PolicyState.FREE and d.amount_micro_eur == 0

def test_rejected_offer_has_zero_receipt_amount():
    aid, pp, pol = fixture()
    req = UsageRequest("u5","k5","payer",aid,Action.INFERENCE_REFERENCE)
    d = evaluate_license(pp, pol, req)
    r = LicenseReceipt.build(req, pp, d, accepted=False)
    assert r.amount_micro_eur == 0

def test_ledger_is_idempotent():
    aid, pp, pol = fixture()
    req = UsageRequest("u6","k6","payer",aid,Action.INFERENCE_REFERENCE)
    r = LicenseReceipt.build(req, pp, evaluate_license(pp, pol, req), accepted=True)
    ledger = RoyaltyLedger()
    a = ledger.append(r)
    b = ledger.append(r)
    assert a == b
    assert ledger.aggregate_due("creator:A") == 100_000

def test_ledger_chain_verifies():
    aid, pp, pol = fixture()
    ledger = RoyaltyLedger()
    for i in range(3):
        req = UsageRequest(f"u{i+10}",f"k{i+10}","payer",aid,Action.INFERENCE_REFERENCE)
        r = LicenseReceipt.build(req, pp, evaluate_license(pp, pol, req), accepted=True)
        ledger.append(r)
    assert ledger.verify_chain()
    assert ledger.aggregate_due("creator:A") == 300_000

def test_similarity_never_creates_debt_or_legal_finding():
    ev = SimilarityEvidence(True,1.0,1.0,1.0,True)
    out = provenance_signal(ev)
    assert out["candidate_provenance_signal"]
    assert out["creates_debt"] is False
    assert out["legal_infringement_finding"] is False

def test_bad_timestamp_suppresses_signal():
    ev = SimilarityEvidence(False,1.0,1.0,1.0,False)
    out = provenance_signal(ev)
    assert out["score"] < 0.55

if __name__ == '__main__':
    import sys
    tests = [obj for name, obj in sorted(globals().items()) if name.startswith('test_') and callable(obj)]
    failures = []
    for test in tests:
        try:
            test()
            print(f'PASS {test.__name__}')
        except Exception as exc:
            failures.append((test.__name__, exc))
            print(f'FAIL {test.__name__}: {exc}')
    print(f'{len(tests)-len(failures)}/{len(tests)} PASS')
    sys.exit(1 if failures else 0)
