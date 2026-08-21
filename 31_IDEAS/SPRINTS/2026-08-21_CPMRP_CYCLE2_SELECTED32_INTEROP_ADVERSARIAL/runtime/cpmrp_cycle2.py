from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple
import json
import time

from cpmrp_core import (
    Action,
    AssetPassport,
    LicenseReceipt,
    PolicyState,
    RightsPolicy,
    UsageRequest,
    canonical_json,
    evaluate_license,
)
from tools.ivdivo_durable_transaction_interface import reconcile_si0014

CYCLE2_VERSION = "cpmrp.cycle2/0.2"
TDMREP_PROFILE = "http://www.w3.org/ns/tdmrep"
TDMREP_CONTEXT = [
    "http://www.w3.org/ns/odrl.jsonld",
    "http://www.w3.org/ns/tdmrep.jsonld",
]
C2PA_LABEL = "c2pa.training-mining"

EXTENDED_USAGE_MAP = {
    "READ": Action.READ,
    "INDEX": Action.INDEX,
    "RETRIEVAL_INDEX": Action.INDEX,
    "TDM": Action.TDM,
    "DATA_MINING": Action.TDM,
    "TRAIN": Action.TRAIN,
    "AI_TRAINING": Action.TRAIN,
    "AI_GENERATIVE_TRAINING": Action.TRAIN,
    "AI_INFERENCE": Action.INFERENCE_REFERENCE,
    "INFERENCE_REFERENCE": Action.INFERENCE_REFERENCE,
    "RAG_CONTEXT": Action.INFERENCE_REFERENCE,
    "HUMAN_EDITORIAL_REFERENCE": Action.READ,
    "REPRODUCE": Action.REPRODUCE,
    "ADAPT": Action.ADAPT,
    "DISTRIBUTE": Action.DISTRIBUTE,
    "COMMERCIALIZE": Action.COMMERCIALIZE,
}

C2PA_USE_MAP = {
    "DATA_MINING": "c2pa.data_mining",
    "AI_INFERENCE": "c2pa.ai_inference",
    "AI_TRAINING": "c2pa.ai_training",
    "AI_GENERATIVE_TRAINING": "c2pa.ai_generative_training",
}


def _digest(obj: Any) -> str:
    return sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def normalize_usage_intent(operation: str) -> Optional[Action]:
    if not isinstance(operation, str):
        return None
    return EXTENDED_USAGE_MAP.get(operation.strip().upper())


def export_tdmrep(
    *,
    asset_uri: str,
    policy_uri: str,
    assigner_uri: str,
    rule_state: PolicyState,
    amount_micro_eur: int = 0,
) -> Dict[str, Any]:
    """Export a profile-conformant TDMRep/ODRL policy plus a linked CPMRP sidecar.

    CPMRP-specific price metadata is intentionally NOT inserted into the normative
    TDMRep policy object. The sidecar is linked by policy_uid.
    """
    if amount_micro_eur < 0:
        raise ValueError("negative amount")
    if rule_state == PolicyState.FREE:
        return {
            "tdm_reservation": 0,
            "tdm_policy": None,
            "odrl_policy": None,
            "cpmrp_offer": None,
        }

    duties: List[Dict[str, Any]] = []
    if rule_state in {PolicyState.OFFER, PolicyState.LICENSE_REQUIRED, PolicyState.NEGOTIATE}:
        duties.append({"action": "obtainConsent"})
    if amount_micro_eur > 0 and rule_state in {PolicyState.OFFER, PolicyState.LICENSE_REQUIRED}:
        duties.append({"action": "compensate"})

    policy: Dict[str, Any] = {
        "@context": list(TDMREP_CONTEXT),
        "@type": "Offer",
        "profile": TDMREP_PROFILE,
        "uid": policy_uri,
        "assigner": assigner_uri,
        "permission": [{
            "target": asset_uri,
            "action": "tdm:mine",
            "duty": duties,
        }],
    }
    sidecar = {
        "schema": "cpmrp.offer-sidecar/0.2",
        "policy_uid": policy_uri,
        "asset_uri": asset_uri,
        "state": rule_state.value,
        "amount_micro_eur": amount_micro_eur,
        "currency": "EUR",
        "creates_debt": False,
        "acceptance_required": rule_state in {PolicyState.OFFER, PolicyState.LICENSE_REQUIRED},
    }
    if rule_state == PolicyState.PROHIBITED:
        # TDMRep reservation can express that rights are reserved, but the policy
        # must not fabricate a permission. Remove permission entirely.
        policy["permission"] = []
        sidecar["amount_micro_eur"] = 0
        sidecar["acceptance_required"] = False
    return {
        "tdm_reservation": 1,
        "tdm_policy": policy_uri,
        "odrl_policy": policy,
        "cpmrp_offer": sidecar,
    }


def validate_tdmrep_export(bundle: Dict[str, Any]) -> bool:
    reservation = bundle.get("tdm_reservation")
    if reservation not in {0, 1}:
        return False
    if reservation == 0:
        return bundle.get("tdm_policy") is None and bundle.get("odrl_policy") is None
    policy = bundle.get("odrl_policy")
    if not isinstance(policy, dict):
        return False
    return (
        policy.get("@context") == TDMREP_CONTEXT
        and policy.get("@type") == "Offer"
        and policy.get("profile") == TDMREP_PROFILE
        and isinstance(policy.get("uid"), str)
        and isinstance(policy.get("assigner"), str)
        and isinstance(policy.get("permission"), list)
    )


def c2pa_training_mining_assertion(
    use_states: Dict[str, PolicyState],
    *,
    policy_uri: Optional[str] = None,
) -> Dict[str, Any]:
    entries: Dict[str, Any] = {}
    for raw_use, state in sorted(use_states.items()):
        key = C2PA_USE_MAP.get(raw_use.upper())
        if key is None:
            continue
        if state == PolicyState.FREE:
            entries[key] = {"use": "allowed"}
        elif state == PolicyState.PROHIBITED:
            entries[key] = {"use": "notAllowed"}
        else:
            info = policy_uri or "Permission conditions must be resolved before use."
            entries[key] = {"use": "constrained", "constraint_info": info}
    return {"label": C2PA_LABEL, "entries": entries}


def c2pa_consumer_decision(assertion: Dict[str, Any], c2pa_use: str, *, constraint_resolved: bool = False) -> str:
    entry = assertion.get("entries", {}).get(c2pa_use)
    if not isinstance(entry, dict):
        return "HOLD_UNKNOWN"
    use = entry.get("use")
    if use == "allowed":
        return "ALLOW"
    if use == "notAllowed":
        return "DENY"
    if use == "constrained":
        return "ALLOW_CONDITIONALLY" if constraint_resolved else "DENY_UNRESOLVED_CONSTRAINT"
    return "HOLD_UNKNOWN"


def asset_passport_v02(passport: AssetPassport, *, jurisdiction: str, territories: Iterable[str], upstream_license: Optional[str] = None, evidence_ceiling: str = "CLAIMANT_ASSERTION_ONLY") -> Dict[str, Any]:
    territories = sorted(set(str(t) for t in territories if str(t).strip()))
    if not jurisdiction.strip() or not territories:
        raise ValueError("jurisdiction and at least one territory required")
    return {
        "schema": "cpmrp.asset-passport/0.2",
        "asset_id": passport.asset_id,
        "claimant_id": passport.claimant_id,
        "rights_basis": passport.rights_basis.value,
        "policy_version": passport.policy_version,
        "status": passport.status,
        "parent_asset_ids": list(passport.parent_asset_ids),
        "evidence_refs": list(passport.evidence_refs),
        "jurisdiction": jurisdiction,
        "territories": territories,
        "upstream_license": upstream_license,
        "evidence_ceiling": evidence_ceiling,
        "ownership_verified": False,
    }


def receipt_attestation(receipt: LicenseReceipt, signer: Optional[Callable[[bytes], str]] = None) -> Dict[str, Any]:
    payload = asdict(receipt)
    payload["action"] = receipt.action.value
    commitment = _digest(payload)
    if signer is None:
        return {
            "mode": "UNSIGNED_DEVELOPMENT",
            "payload_sha256": commitment,
            "signature": None,
            "production_signature_proven": False,
        }
    signature = signer(canonical_json(payload).encode("utf-8"))
    if not isinstance(signature, str) or not signature:
        raise ValueError("signer returned invalid signature")
    return {
        "mode": "EXTERNAL_SIGNER",
        "payload_sha256": commitment,
        "signature": signature,
        "production_signature_proven": False,
    }


def verify_receipt_offline(receipt: LicenseReceipt) -> bool:
    payload = {
        "usage_event_id": receipt.usage_event_id,
        "payer_id": receipt.payer_id,
        "payee_id": receipt.payee_id,
        "asset_id": receipt.asset_id,
        "action": receipt.action.value,
        "amount_micro_eur": receipt.amount_micro_eur,
        "policy_version": receipt.policy_version,
        "accepted": receipt.accepted,
    }
    expected = "cpmrp-receipt:" + sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    return receipt.receipt_id == expected


def receipt_correction(original: LicenseReceipt, *, reason: str, corrected_amount_micro_eur: int) -> Dict[str, Any]:
    if corrected_amount_micro_eur < 0:
        raise ValueError("negative corrected amount")
    if not reason.strip():
        raise ValueError("reason required")
    body = {
        "schema": "cpmrp.receipt-correction/0.2",
        "supersedes_receipt_id": original.receipt_id,
        "reason": reason,
        "corrected_amount_micro_eur": corrected_amount_micro_eur,
        "history_deleted": False,
    }
    body["correction_id"] = "cpmrp-correction:" + _digest(body)
    return body


def build_durable_registry_ledger_plan(
    *,
    transaction_id: str,
    project_id: str,
    repo_main_sha: str,
    state_revision: str,
    registry_artifact_id: str,
    ledger_artifact_id: str,
    registry_state: str = "NOT_STARTED",
    ledger_state: str = "NOT_STARTED",
    registry_readback: bool = False,
    ledger_readback: bool = False,
) -> Dict[str, Any]:
    return {
        "transaction_id": transaction_id,
        "project_id": project_id,
        "work_unit": "CPMRP_REGISTRY_LEDGER_WRITE",
        "authority_snapshot": {
            "repo_main_sha": repo_main_sha,
            "state_revision": state_revision,
        },
        "actions": [
            {
                "action_id": "CPMRP_REGISTRY_WRITE",
                "artifact_id": registry_artifact_id,
                "store": "GITHUB",
                "operation": "WRITE_REGISTRY_STATE",
                "effect_class": "REVERSIBLE_WRITE",
                "side_effect_state": registry_state,
                "readback_verified": registry_readback,
                "intended_identity": {"artifact_id": registry_artifact_id},
                "observed_identity": {"artifact_id": registry_artifact_id} if registry_state in {"CONFIRMED", "RECONCILED"} else {},
            },
            {
                "action_id": "CPMRP_LEDGER_WRITE",
                "artifact_id": ledger_artifact_id,
                "store": "DRIVE",
                "operation": "WRITE_LEDGER_STATE",
                "effect_class": "REVERSIBLE_WRITE",
                "side_effect_state": ledger_state,
                "readback_verified": ledger_readback,
                "intended_identity": {"artifact_id": ledger_artifact_id},
                "observed_identity": {"artifact_id": ledger_artifact_id} if ledger_state in {"CONFIRMED", "RECONCILED"} else {},
            },
        ],
        "evidence_boundary": [
            "NO_PAYMENT_DISPATCH",
            "REVERSIBLE_WRITES_ONLY",
            "READBACK_REQUIRED",
            "NO_AUTOMATIC_SI_PROMOTION",
        ],
    }


def reconcile_cpmrp_durable_plan(plan: Dict[str, Any], *, current_repo_main_sha: str, current_state_revision: str) -> Dict[str, Any]:
    return reconcile_si0014(
        plan,
        current_repo_main_sha=current_repo_main_sha,
        current_state_revision=current_state_revision,
    )


@dataclass(frozen=True)
class SimilarityEvidenceV2:
    exact_hash: bool = False
    near_duplicate: float = 0.0
    rare_lexical: float = 0.0
    structural_combo: float = 0.0
    access_evidence: float = 0.0
    timestamp_order_ok: bool = False
    common_trope_ratio: float = 0.0


def similarity_signal_v2(e: SimilarityEvidenceV2) -> Dict[str, Any]:
    def clamp(x: float) -> float:
        return min(max(float(x), 0.0), 1.0)
    score = 0.75 if e.exact_hash else 0.0
    score += clamp(e.near_duplicate) * 0.30
    score += clamp(e.rare_lexical) * 0.20
    score += clamp(e.structural_combo) * 0.15
    score += clamp(e.access_evidence) * 0.10
    score -= clamp(e.common_trope_ratio) * 0.35
    if not e.timestamp_order_ok:
        score *= 0.25
    score = min(max(score, 0.0), 1.0)
    return {
        "score": round(score, 6),
        "candidate_provenance_signal": score >= 0.60,
        "legal_infringement_finding": False,
        "creates_debt": False,
        "threshold_is_legal_test": False,
    }


def independent_creation_packet(*, creator_id: str, artifact_hash: str, timestamp_refs: List[str], process_refs: List[str]) -> Dict[str, Any]:
    return {
        "schema": "cpmrp.independent-creation/0.2",
        "creator_id": creator_id,
        "artifact_hash": artifact_hash,
        "timestamp_refs": list(timestamp_refs),
        "process_refs": list(process_refs),
        "legal_conclusion": None,
        "debt_effect": "NONE_AUTOMATIC",
    }


class ProvenanceGraph:
    def __init__(self) -> None:
        self.edges: List[Tuple[str, str, str, int]] = []

    def _adj(self, extra: Optional[Tuple[str, str]] = None) -> Dict[str, List[str]]:
        out: Dict[str, List[str]] = {}
        for src, dst, _, _ in self.edges:
            out.setdefault(src, []).append(dst)
        if extra:
            out.setdefault(extra[0], []).append(extra[1])
        return out

    def _has_cycle(self, extra: Optional[Tuple[str, str]] = None) -> bool:
        adj = self._adj(extra)
        visiting, visited = set(), set()
        def dfs(node: str) -> bool:
            if node in visiting:
                return True
            if node in visited:
                return False
            visiting.add(node)
            for nxt in adj.get(node, []):
                if dfs(nxt):
                    return True
            visiting.remove(node)
            visited.add(node)
            return False
        return any(dfs(n) for n in list(adj))

    def add_edge(self, source: str, target: str, relation: str, royalty_share_bp: int = 0) -> Dict[str, Any]:
        if not source or not target or source == target:
            return {"decision": "REJECT", "reason": "INVALID_EDGE"}
        if royalty_share_bp < 0 or royalty_share_bp > 10000:
            return {"decision": "REJECT", "reason": "INVALID_SHARE"}
        if self._has_cycle((source, target)):
            return {"decision": "REJECT", "reason": "PROVENANCE_CYCLE"}
        self.edges.append((source, target, relation, royalty_share_bp))
        return {"decision": "ACCEPT", "edge_id": "cpmrp-edge:" + _digest([source, target, relation, royalty_share_bp])}

    def share_total_bp(self, target: str) -> int:
        return sum(bp for _, dst, _, bp in self.edges if dst == target)


def provenance_edge_receipt(source: str, target: str, relation: str, licensed: bool) -> Dict[str, Any]:
    body = {
        "source": source,
        "target": target,
        "relation": relation,
        "licensed": licensed,
        "creates_debt": False,
    }
    body["edge_receipt_id"] = "cpmrp-edge-receipt:" + _digest(body)
    return body


def unavailable_source_proof(asset_id: str, content_hash: str, last_seen_ref: str) -> Dict[str, Any]:
    return {
        "asset_id": asset_id,
        "content_hash": content_hash,
        "last_seen_ref": last_seen_ref,
        "source_available": False,
        "hash_evidence_preserved": True,
    }


def claim_integrity_decision(*, claim_class: str, evidence_refs: List[str], public_domain: bool = False, duplicate_of: Optional[str] = None, earlier_source_ref: Optional[str] = None) -> Dict[str, Any]:
    cls = claim_class.strip().upper()
    if cls in {"IDEA", "STYLE", "TROPE", "GENRE", "COMMON_MOTIF"}:
        return {"decision": "REJECT_MONETIZATION", "reason": "UNPARTICULARIZED_CONCEPT"}
    if public_domain:
        return {"decision": "REJECT_MONETIZATION", "reason": "PUBLIC_DOMAIN_CAPTURE"}
    if duplicate_of:
        return {"decision": "HOLD", "reason": "DUPLICATE_CLAIM", "duplicate_of": duplicate_of}
    if earlier_source_ref:
        return {"decision": "HOLD", "reason": "EARLIER_SOURCE_REVIEW", "earlier_source_ref": earlier_source_ref}
    if len(set(r for r in evidence_refs if r)) < 1:
        return {"decision": "HOLD", "reason": "INSUFFICIENT_EVIDENCE"}
    return {"decision": "ACCEPT_CLAIM_ASSERTION", "ownership_verified": False}


def claimant_reputation_metadata(*, successful_receipts: int, upheld_disputes: int, rejected_claims: int) -> Dict[str, Any]:
    successful_receipts = max(successful_receipts, 0)
    upheld_disputes = max(upheld_disputes, 0)
    rejected_claims = max(rejected_claims, 0)
    raw = successful_receipts + 2 * upheld_disputes - 3 * rejected_claims
    return {
        "evidence_quality_score": max(min(raw, 100), -100),
        "ownership_proof": False,
        "automatic_priority": False,
    }


def sybil_guard(*, claimant_id: str, claims_last_hour: int, low_evidence_ratio: float) -> Dict[str, Any]:
    ratio = min(max(low_evidence_ratio, 0.0), 1.0)
    if claims_last_hour > 100 or (claims_last_hour > 20 and ratio > 0.8):
        return {"decision": "RATE_LIMIT_AND_REVIEW", "claimant_id": claimant_id}
    return {"decision": "ALLOW_BOUNDED_INTAKE", "claimant_id": claimant_id}


def abuse_appeal(claim_id: str, reason: str, counter_evidence_refs: List[str]) -> Dict[str, Any]:
    if not claim_id or not reason.strip():
        raise ValueError("claim_id and reason required")
    body = {
        "claim_id": claim_id,
        "reason": reason,
        "counter_evidence_refs": sorted(set(counter_evidence_refs)),
        "status": "HUMAN_REVIEW_REQUIRED",
        "automatic_override": False,
    }
    body["appeal_id"] = "cpmrp-appeal:" + _digest(body)
    return body


def can_use(passport: AssetPassport, policy: RightsPolicy, *, payer_id: str, operation: str, usage_event_id: str = "preview", idempotency_key: str = "preview") -> Dict[str, Any]:
    action = normalize_usage_intent(operation)
    if action is None:
        return {"decision": "HOLD_UNKNOWN_USAGE_INTENT", "creates_debt": False}
    req = UsageRequest(usage_event_id, idempotency_key, payer_id, passport.asset_id, action)
    decision = evaluate_license(passport, policy, req)
    if decision.state == PolicyState.FREE:
        outcome = "ALLOW"
    elif decision.state in {PolicyState.OFFER, PolicyState.LICENSE_REQUIRED}:
        outcome = "OFFER_LICENSE"
    elif decision.state == PolicyState.PROHIBITED:
        outcome = "DENY"
    else:
        outcome = "HOLD"
    return {
        "decision": outcome,
        "policy_state": decision.state.value,
        "amount_micro_eur": decision.amount_micro_eur,
        "creates_debt": False,
        "action": action.value,
        "policy_version": decision.policy_version,
    }


def choose_fallback(candidates: List[Tuple[AssetPassport, RightsPolicy]], *, payer_id: str, operation: str) -> Dict[str, Any]:
    for passport, policy in candidates:
        decision = can_use(passport, policy, payer_id=payer_id, operation=operation)
        if decision["decision"] == "ALLOW":
            return {"decision": "SELECT_FREE_SOURCE", "asset_id": passport.asset_id}
    return {"decision": "NO_FREE_SOURCE", "asset_id": None}


def measure_can_use_latency(passport: AssetPassport, policy: RightsPolicy, operation: str, iterations: int = 100) -> Dict[str, Any]:
    start = time.perf_counter()
    for i in range(iterations):
        can_use(passport, policy, payer_id="bench", operation=operation, usage_event_id=f"bench-{i}", idempotency_key=f"bench-{i}")
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    return {
        "iterations": iterations,
        "elapsed_ms": elapsed_ms,
        "avg_ms": elapsed_ms / max(iterations, 1),
        "performance_target_ms": 10.0,
        "target_is_engineering_only": True,
    }


def full_integration_flow(passport: AssetPassport, policy: RightsPolicy, req: UsageRequest, *, accepted: bool) -> Dict[str, Any]:
    decision = evaluate_license(passport, policy, req)
    receipt = LicenseReceipt.build(req, passport, decision, accepted=accepted)
    from cpmrp_core import RoyaltyLedger
    ledger = RoyaltyLedger()
    entry = ledger.append(receipt)
    return {
        "decision": decision.state.value,
        "receipt_verified": verify_receipt_offline(receipt),
        "ledger_chain_verified": ledger.verify_chain(),
        "amount_micro_eur": entry.amount_micro_eur,
        "aggregate_due_micro_eur": ledger.aggregate_due(passport.claimant_id),
        "creates_legal_finding": False,
    }


def red_team_cycle2(*, passport: AssetPassport, policy: RightsPolicy) -> Dict[str, str]:
    results: Dict[str, str] = {}
    results["idea_capture"] = claim_integrity_decision(claim_class="IDEA", evidence_refs=["x"])["decision"]
    results["public_domain_capture"] = claim_integrity_decision(claim_class="TEXT_FRAGMENT", evidence_refs=["x"], public_domain=True)["decision"]
    results["similarity_debt"] = "BLOCKED" if similarity_signal_v2(SimilarityEvidenceV2(True, 1, 1, 1, 1, True, 0))["creates_debt"] is False else "FAILED"
    results["unresolved_c2pa_constraint"] = c2pa_consumer_decision(c2pa_training_mining_assertion({"AI_TRAINING": PolicyState.OFFER}, policy_uri="https://example.invalid/policy"), "c2pa.ai_training", constraint_resolved=False)
    graph = ProvenanceGraph()
    graph.add_edge("A", "B", "derived_from")
    graph.add_edge("B", "C", "derived_from")
    results["provenance_cycle"] = graph.add_edge("C", "A", "derived_from")["decision"]
    results["unknown_usage"] = can_use(passport, policy, payer_id="x", operation="MAGIC_UNDEFINED")["decision"]
    return results
