from cpmrp_core import *
from cpmrp_cycle2 import *


def fixture():
    aid = content_asset_id("cycle2", b"creative asset v2", "v2")
    pp = AssetPassport(aid, "creator:A", RightsBasis.COPYRIGHT_ASSERTED, "p2", evidence_refs=("e1", "e2"))
    pol = RightsPolicy(aid, "p2", {
        Action.READ: PriceRule(Action.READ, PolicyState.FREE, 0),
        Action.INDEX: PriceRule(Action.INDEX, PolicyState.FREE, 0),
        Action.TDM: PriceRule(Action.TDM, PolicyState.LICENSE_REQUIRED, 100_000),
        Action.TRAIN: PriceRule(Action.TRAIN, PolicyState.OFFER, 100_000),
        Action.INFERENCE_REFERENCE: PriceRule(Action.INFERENCE_REFERENCE, PolicyState.OFFER, 100_000),
        Action.REPRODUCE: PriceRule(Action.REPRODUCE, PolicyState.PROHIBITED, 0),
    })
    return aid, pp, pol


def test_tdmrep_free_has_no_policy():
    b = export_tdmrep(asset_uri="https://x/a", policy_uri="https://x/p", assigner_uri="https://x/r", rule_state=PolicyState.FREE)
    assert b["tdm_reservation"] == 0 and b["tdm_policy"] is None
    assert validate_tdmrep_export(b)


def test_tdmrep_paid_offer_is_reserved_and_profile_clean():
    b = export_tdmrep(asset_uri="https://x/a", policy_uri="https://x/p", assigner_uri="https://x/r", rule_state=PolicyState.OFFER, amount_micro_eur=100_000)
    assert b["tdm_reservation"] == 1
    assert b["odrl_policy"]["@context"] == TDMREP_CONTEXT
    duties = b["odrl_policy"]["permission"][0]["duty"]
    assert {d["action"] for d in duties} == {"obtainConsent", "compensate"}
    assert b["cpmrp_offer"]["amount_micro_eur"] == 100_000
    assert b["cpmrp_offer"]["creates_debt"] is False
    assert validate_tdmrep_export(b)


def test_tdmrep_prohibited_does_not_fabricate_permission():
    b = export_tdmrep(asset_uri="https://x/a", policy_uri="https://x/p", assigner_uri="https://x/r", rule_state=PolicyState.PROHIBITED)
    assert b["tdm_reservation"] == 1 and b["odrl_policy"]["permission"] == []


def test_c2pa_mapping():
    a = c2pa_training_mining_assertion({
        "DATA_MINING": PolicyState.FREE,
        "AI_INFERENCE": PolicyState.OFFER,
        "AI_TRAINING": PolicyState.PROHIBITED,
    }, policy_uri="https://x/p")
    assert a["label"] == "c2pa.training-mining"
    assert a["entries"]["c2pa.data_mining"]["use"] == "allowed"
    assert a["entries"]["c2pa.ai_inference"]["use"] == "constrained"
    assert a["entries"]["c2pa.ai_training"]["use"] == "notAllowed"


def test_c2pa_unresolved_constraint_fails_closed():
    a = c2pa_training_mining_assertion({"AI_TRAINING": PolicyState.OFFER}, policy_uri="https://x/p")
    assert c2pa_consumer_decision(a, "c2pa.ai_training", constraint_resolved=False) == "DENY_UNRESOLVED_CONSTRAINT"
    assert c2pa_consumer_decision(a, "c2pa.ai_training", constraint_resolved=True) == "ALLOW_CONDITIONALLY"


def test_asset_passport_v02_keeps_ownership_unverified():
    _, pp, _ = fixture()
    out = asset_passport_v02(pp, jurisdiction="IE/EU", territories=["IE", "EU"])
    assert out["schema"] == "cpmrp.asset-passport/0.2"
    assert out["ownership_verified"] is False
    assert out["territories"] == ["EU", "IE"]


def test_extended_usage_mapping():
    assert normalize_usage_intent("rag_context") == Action.INFERENCE_REFERENCE
    assert normalize_usage_intent("ai_generative_training") == Action.TRAIN
    assert normalize_usage_intent("unknown_magic") is None


def test_unsigned_attestation_is_not_production_signature():
    aid, pp, pol = fixture()
    req = UsageRequest("u-att","k-att","payer",aid,Action.INFERENCE_REFERENCE)
    r = LicenseReceipt.build(req, pp, evaluate_license(pp, pol, req), accepted=True)
    a = receipt_attestation(r)
    assert a["mode"] == "UNSIGNED_DEVELOPMENT"
    assert a["production_signature_proven"] is False


def test_external_signer_interface_is_bounded():
    aid, pp, pol = fixture()
    req = UsageRequest("u-sign","k-sign","payer",aid,Action.INFERENCE_REFERENCE)
    r = LicenseReceipt.build(req, pp, evaluate_license(pp, pol, req), accepted=True)
    a = receipt_attestation(r, signer=lambda payload: "demo:" + sha256(payload).hexdigest())
    assert a["mode"] == "EXTERNAL_SIGNER"
    assert a["signature"].startswith("demo:")
    assert a["production_signature_proven"] is False


def test_offline_receipt_verification_and_correction_append_only():
    aid, pp, pol = fixture()
    req = UsageRequest("u-v","k-v","payer",aid,Action.INFERENCE_REFERENCE)
    r = LicenseReceipt.build(req, pp, evaluate_license(pp, pol, req), accepted=True)
    assert verify_receipt_offline(r)
    c = receipt_correction(r, reason="refund/adjustment evidence", corrected_amount_micro_eur=0)
    assert c["supersedes_receipt_id"] == r.receipt_id and c["history_deleted"] is False


def test_durable_plan_safe_missing_actions():
    plan = build_durable_registry_ledger_plan(transaction_id="tx1", project_id="CPMRP", repo_main_sha="abc", state_revision="s1", registry_artifact_id="reg1", ledger_artifact_id="led1")
    out = reconcile_cpmrp_durable_plan(plan, current_repo_main_sha="abc", current_state_revision="s1")
    assert out["decision"] == "EXECUTE_MISSING_SAFE_ACTIONS"
    assert set(out["action_ids"]) == {"CPMRP_REGISTRY_WRITE", "CPMRP_LEDGER_WRITE"}


def test_durable_plan_ambiguous_reversible_requires_readback_before_retry():
    plan = build_durable_registry_ledger_plan(transaction_id="tx2", project_id="CPMRP", repo_main_sha="abc", state_revision="s1", registry_artifact_id="reg1", ledger_artifact_id="led1", registry_state="STARTED_UNKNOWN")
    out = reconcile_cpmrp_durable_plan(plan, current_repo_main_sha="abc", current_state_revision="s1")
    assert out["decision"] == "VERIFY_STORE_BEFORE_RETRY"


def test_durable_plan_confirmed_without_readback_holds():
    plan = build_durable_registry_ledger_plan(transaction_id="tx3", project_id="CPMRP", repo_main_sha="abc", state_revision="s1", registry_artifact_id="reg1", ledger_artifact_id="led1", registry_state="CONFIRMED", registry_readback=False)
    out = reconcile_cpmrp_durable_plan(plan, current_repo_main_sha="abc", current_state_revision="s1")
    assert out["decision"] == "VERIFY_READBACK"


def test_durable_plan_complete_after_both_readbacks():
    plan = build_durable_registry_ledger_plan(transaction_id="tx4", project_id="CPMRP", repo_main_sha="abc", state_revision="s1", registry_artifact_id="reg1", ledger_artifact_id="led1", registry_state="CONFIRMED", ledger_state="CONFIRMED", registry_readback=True, ledger_readback=True)
    out = reconcile_cpmrp_durable_plan(plan, current_repo_main_sha="abc", current_state_revision="s1")
    assert out["decision"] == "TRANSACTION_COMPLETE"


def test_similarity_exact_can_signal_but_never_debt_or_legal_finding():
    out = similarity_signal_v2(SimilarityEvidenceV2(True,1,1,1,1,True,0))
    assert out["candidate_provenance_signal"] is True
    assert out["creates_debt"] is False
    assert out["legal_infringement_finding"] is False
    assert out["threshold_is_legal_test"] is False


def test_common_trope_negative_control_suppresses_alert():
    out = similarity_signal_v2(SimilarityEvidenceV2(False,0.1,0.05,0.5,0,True,1.0))
    assert out["candidate_provenance_signal"] is False


def test_bad_timestamp_suppresses_similarity_v2():
    out = similarity_signal_v2(SimilarityEvidenceV2(False,1,1,1,1,False,0))
    assert out["score"] < 0.60


def test_independent_creation_packet_has_no_automatic_debt_effect():
    p = independent_creation_packet(creator_id="B", artifact_hash="h", timestamp_refs=["t1"], process_refs=["p1"])
    assert p["legal_conclusion"] is None and p["debt_effect"] == "NONE_AUTOMATIC"


def test_provenance_graph_rejects_cycles():
    g = ProvenanceGraph()
    assert g.add_edge("A","B","derived_from")["decision"] == "ACCEPT"
    assert g.add_edge("B","C","derived_from")["decision"] == "ACCEPT"
    assert g.add_edge("C","A","derived_from")["reason"] == "PROVENANCE_CYCLE"


def test_provenance_multi_source_shares():
    g = ProvenanceGraph()
    g.add_edge("S1","T","licensed_use",2500)
    g.add_edge("S2","T","declared_reference",1000)
    assert g.share_total_bp("T") == 3500


def test_provenance_edge_receipt_distinguishes_license():
    a = provenance_edge_receipt("S","T","declared_reference",False)
    b = provenance_edge_receipt("S","T","licensed_use",True)
    assert a["licensed"] is False and b["licensed"] is True and a["edge_receipt_id"] != b["edge_receipt_id"]


def test_unavailable_source_preserves_hash_evidence():
    p = unavailable_source_proof("a","hash","archive-ref")
    assert p["source_available"] is False and p["hash_evidence_preserved"] is True


def test_claim_integrity_rejects_idea_and_public_domain_capture():
    assert claim_integrity_decision(claim_class="IDEA", evidence_refs=["e"])["decision"] == "REJECT_MONETIZATION"
    assert claim_integrity_decision(claim_class="TEXT_FRAGMENT", evidence_refs=["e"], public_domain=True)["reason"] == "PUBLIC_DOMAIN_CAPTURE"


def test_claim_integrity_holds_duplicate_and_earlier_source():
    assert claim_integrity_decision(claim_class="IMAGE", evidence_refs=["e"], duplicate_of="old")["decision"] == "HOLD"
    assert claim_integrity_decision(claim_class="IMAGE", evidence_refs=["e"], earlier_source_ref="earlier")["reason"] == "EARLIER_SOURCE_REVIEW"


def test_reputation_is_not_ownership_proof():
    r = claimant_reputation_metadata(successful_receipts=100, upheld_disputes=5, rejected_claims=0)
    assert r["ownership_proof"] is False and r["automatic_priority"] is False


def test_sybil_guard_limits_mass_low_evidence_claims():
    assert sybil_guard(claimant_id="x", claims_last_hour=1000, low_evidence_ratio=0.99)["decision"] == "RATE_LIMIT_AND_REVIEW"
    assert sybil_guard(claimant_id="x", claims_last_hour=3, low_evidence_ratio=0.1)["decision"] == "ALLOW_BOUNDED_INTAKE"


def test_abuse_appeal_never_auto_overrides():
    a = abuse_appeal("c1","false positive",["z","a","z"])
    assert a["status"] == "HUMAN_REVIEW_REQUIRED" and a["automatic_override"] is False
    assert a["counter_evidence_refs"] == ["a","z"]


def test_can_use_free_offer_prohibited_unknown():
    aid, pp, pol = fixture()
    assert can_use(pp, pol, payer_id="p", operation="READ")["decision"] == "ALLOW"
    assert can_use(pp, pol, payer_id="p", operation="RAG_CONTEXT")["decision"] == "OFFER_LICENSE"
    assert can_use(pp, pol, payer_id="p", operation="REPRODUCE")["decision"] == "DENY"
    assert can_use(pp, pol, payer_id="p", operation="MAGIC")["decision"] == "HOLD_UNKNOWN_USAGE_INTENT"


def test_fallback_selects_free_source_not_unresolved_offer():
    aid, pp, pol = fixture()
    aid2 = content_asset_id("cycle2", b"free alt", "v1")
    pp2 = AssetPassport(aid2, "creator:B", RightsBasis.COPYRIGHT_ASSERTED, "p1")
    pol2 = RightsPolicy(aid2, "p1", {Action.INFERENCE_REFERENCE: PriceRule(Action.INFERENCE_REFERENCE, PolicyState.FREE, 0)})
    out = choose_fallback([(pp,pol),(pp2,pol2)], payer_id="p", operation="RAG_CONTEXT")
    assert out["decision"] == "SELECT_FREE_SOURCE" and out["asset_id"] == aid2


def test_latency_measurement_is_observability_not_claim_of_platform_performance():
    _, pp, pol = fixture()
    out = measure_can_use_latency(pp, pol, "READ", iterations=10)
    assert out["iterations"] == 10 and out["avg_ms"] >= 0 and out["target_is_engineering_only"] is True


def test_full_integration_register_to_ledger():
    aid, pp, pol = fixture()
    req = UsageRequest("u-full","k-full","payer",aid,Action.INFERENCE_REFERENCE)
    out = full_integration_flow(pp, pol, req, accepted=True)
    assert out["receipt_verified"] and out["ledger_chain_verified"]
    assert out["amount_micro_eur"] == 100_000 and out["aggregate_due_micro_eur"] == 100_000
    assert out["creates_legal_finding"] is False


def test_red_team_blocks_core_escalations():
    _, pp, pol = fixture()
    out = red_team_cycle2(passport=pp, policy=pol)
    assert out["idea_capture"] == "REJECT_MONETIZATION"
    assert out["public_domain_capture"] == "REJECT_MONETIZATION"
    assert out["similarity_debt"] == "BLOCKED"
    assert out["unresolved_c2pa_constraint"] == "DENY_UNRESOLVED_CONSTRAINT"
    assert out["provenance_cycle"] == "REJECT"
    assert out["unknown_usage"] == "HOLD_UNKNOWN_USAGE_INTENT"


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
            print(f'FAIL {test.__name__}: {type(exc).__name__}: {exc}')
    print(f'{len(tests)-len(failures)}/{len(tests)} PASS')
    sys.exit(1 if failures else 0)
