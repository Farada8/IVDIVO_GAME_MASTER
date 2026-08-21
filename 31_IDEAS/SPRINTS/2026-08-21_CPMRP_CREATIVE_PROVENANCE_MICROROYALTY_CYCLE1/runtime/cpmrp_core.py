from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Dict, List, Tuple
import json

MICRO_EUR_PER_EUR = 1_000_000

class RightsBasis(str, Enum):
    COPYRIGHT_ASSERTED = "COPYRIGHT_ASSERTED"
    CONTRACT_LICENSE = "CONTRACT_LICENSE"
    TDM_RESERVATION = "TDM_RESERVATION"
    OPEN_LICENSE = "OPEN_LICENSE"
    PUBLIC_DOMAIN = "PUBLIC_DOMAIN"
    VOLUNTARY_TIP = "VOLUNTARY_TIP"
    UNKNOWN = "UNKNOWN"

class PolicyState(str, Enum):
    FREE = "FREE"
    OFFER = "OFFER"
    LICENSE_REQUIRED = "LICENSE_REQUIRED"
    NEGOTIATE = "NEGOTIATE"
    PROHIBITED = "PROHIBITED"
    UNKNOWN = "UNKNOWN"

class Action(str, Enum):
    READ = "READ"
    INDEX = "INDEX"
    TDM = "TDM"
    TRAIN = "TRAIN"
    INFERENCE_REFERENCE = "INFERENCE_REFERENCE"
    REPRODUCE = "REPRODUCE"
    ADAPT = "ADAPT"
    DISTRIBUTE = "DISTRIBUTE"
    COMMERCIALIZE = "COMMERCIALIZE"

def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256_hex(data: bytes) -> str:
    return sha256(data).hexdigest()

def content_asset_id(namespace: str, content: bytes, version: str) -> str:
    digest = sha256_hex(content)
    return f"cpmrp:{namespace}:{version}:sha256:{digest}"

@dataclass(frozen=True)
class AssetPassport:
    asset_id: str
    claimant_id: str
    rights_basis: RightsBasis
    policy_version: str
    parent_asset_ids: Tuple[str, ...] = ()
    evidence_refs: Tuple[str, ...] = ()
    status: str = "ACTIVE"

@dataclass(frozen=True)
class PriceRule:
    action: Action
    state: PolicyState
    amount_micro_eur: int = 0

    def __post_init__(self):
        if self.amount_micro_eur < 0:
            raise ValueError("negative price not allowed")
        if self.state == PolicyState.FREE and self.amount_micro_eur != 0:
            raise ValueError("FREE must have zero price")

@dataclass
class RightsPolicy:
    asset_id: str
    policy_version: str
    rules: Dict[Action, PriceRule]

    def rule_for(self, action: Action) -> PriceRule:
        return self.rules.get(action, PriceRule(action, PolicyState.UNKNOWN, 0))

@dataclass(frozen=True)
class UsageRequest:
    usage_event_id: str
    idempotency_key: str
    payer_id: str
    asset_id: str
    action: Action

@dataclass(frozen=True)
class LicenseDecision:
    asset_id: str
    action: Action
    state: PolicyState
    amount_micro_eur: int
    creates_debt: bool
    reason: str
    policy_version: str

def evaluate_license(passport: AssetPassport, policy: RightsPolicy, req: UsageRequest) -> LicenseDecision:
    if req.asset_id != passport.asset_id or policy.asset_id != passport.asset_id:
        raise ValueError("asset mismatch")
    if passport.rights_basis == RightsBasis.PUBLIC_DOMAIN:
        return LicenseDecision(req.asset_id, req.action, PolicyState.FREE, 0, False,
                               "public domain", policy.policy_version)
    rule = policy.rule_for(req.action)
    if rule.state == PolicyState.UNKNOWN:
        return LicenseDecision(req.asset_id, req.action, PolicyState.UNKNOWN, 0, False,
                               "unknown policy: fail closed, no automatic debt", policy.policy_version)
    if rule.state == PolicyState.FREE:
        return LicenseDecision(req.asset_id, req.action, rule.state, 0, False,
                               "free permission", policy.policy_version)
    if rule.state == PolicyState.OFFER:
        return LicenseDecision(req.asset_id, req.action, rule.state, rule.amount_micro_eur, False,
                               "offer requires acceptance before debt", policy.policy_version)
    if rule.state == PolicyState.LICENSE_REQUIRED:
        return LicenseDecision(req.asset_id, req.action, rule.state, rule.amount_micro_eur, False,
                               "licence required; debt only after accepted licence/contract", policy.policy_version)
    return LicenseDecision(req.asset_id, req.action, rule.state, rule.amount_micro_eur, False,
                           "manual resolution required", policy.policy_version)

@dataclass(frozen=True)
class LicenseReceipt:
    receipt_id: str
    usage_event_id: str
    payer_id: str
    payee_id: str
    asset_id: str
    action: Action
    amount_micro_eur: int
    policy_version: str
    accepted: bool

    @staticmethod
    def build(req: UsageRequest, passport: AssetPassport, decision: LicenseDecision, accepted: bool) -> "LicenseReceipt":
        if not accepted:
            amount = 0
        elif decision.state not in (PolicyState.OFFER, PolicyState.LICENSE_REQUIRED):
            amount = 0
        else:
            amount = decision.amount_micro_eur
        payload = {
            "usage_event_id": req.usage_event_id,
            "payer_id": req.payer_id,
            "payee_id": passport.claimant_id,
            "asset_id": req.asset_id,
            "action": req.action.value,
            "amount_micro_eur": amount,
            "policy_version": decision.policy_version,
            "accepted": accepted,
        }
        rid = "cpmrp-receipt:" + sha256_hex(canonical_json(payload).encode("utf-8"))
        return LicenseReceipt(rid, req.usage_event_id, req.payer_id, passport.claimant_id,
                              req.asset_id, req.action, amount, decision.policy_version, accepted)

@dataclass(frozen=True)
class LedgerEntry:
    sequence: int
    usage_event_id: str
    receipt_id: str
    payer_id: str
    payee_id: str
    amount_micro_eur: int
    prev_hash: str
    entry_hash: str

class RoyaltyLedger:
    def __init__(self):
        self._entries: List[LedgerEntry] = []
        self._by_event: Dict[str, LedgerEntry] = {}

    def append(self, receipt: LicenseReceipt) -> LedgerEntry:
        if receipt.usage_event_id in self._by_event:
            return self._by_event[receipt.usage_event_id]
        prev = self._entries[-1].entry_hash if self._entries else "GENESIS"
        payload = {
            "sequence": len(self._entries) + 1,
            "usage_event_id": receipt.usage_event_id,
            "receipt_id": receipt.receipt_id,
            "payer_id": receipt.payer_id,
            "payee_id": receipt.payee_id,
            "amount_micro_eur": receipt.amount_micro_eur,
            "prev_hash": prev,
        }
        eh = sha256_hex(canonical_json(payload).encode("utf-8"))
        entry = LedgerEntry(entry_hash=eh, **payload)
        self._entries.append(entry)
        self._by_event[receipt.usage_event_id] = entry
        return entry

    def aggregate_due(self, payee_id: str) -> int:
        return sum(e.amount_micro_eur for e in self._entries if e.payee_id == payee_id)

    def verify_chain(self) -> bool:
        prev = "GENESIS"
        for i, e in enumerate(self._entries, start=1):
            payload = {
                "sequence": i,
                "usage_event_id": e.usage_event_id,
                "receipt_id": e.receipt_id,
                "payer_id": e.payer_id,
                "payee_id": e.payee_id,
                "amount_micro_eur": e.amount_micro_eur,
                "prev_hash": prev,
            }
            if e.sequence != i or e.prev_hash != prev:
                return False
            if e.entry_hash != sha256_hex(canonical_json(payload).encode("utf-8")):
                return False
            prev = e.entry_hash
        return True

@dataclass(frozen=True)
class SimilarityEvidence:
    exact_hash_match: bool = False
    rare_term_overlap: float = 0.0
    structural_overlap: float = 0.0
    access_evidence: float = 0.0
    timestamp_order_ok: bool = False

def provenance_signal(ev: SimilarityEvidence) -> Dict[str, object]:
    score = 0.0
    if ev.exact_hash_match:
        score += 0.7
    score += min(max(ev.rare_term_overlap, 0.0), 1.0) * 0.15
    score += min(max(ev.structural_overlap, 0.0), 1.0) * 0.10
    score += min(max(ev.access_evidence, 0.0), 1.0) * 0.05
    if not ev.timestamp_order_ok:
        score *= 0.25
    return {
        "score": round(min(score, 1.0), 6),
        "candidate_provenance_signal": score >= 0.55,
        "legal_infringement_finding": False,
        "creates_debt": False,
    }
