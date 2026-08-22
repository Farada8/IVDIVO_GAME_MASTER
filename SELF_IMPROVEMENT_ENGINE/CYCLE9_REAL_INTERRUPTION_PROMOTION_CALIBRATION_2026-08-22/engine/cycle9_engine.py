from __future__ import annotations
from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Optional, Sequence, Any
import hashlib, json

class GateError(RuntimeError):
    pass

class EvidenceClass(str, Enum):
    SOURCE_INSPECTED="SOURCE_INSPECTED"
    TEST_EXECUTED="TEST_EXECUTED"
    CONTROLLED_INTEGRATION="CONTROLLED_INTEGRATION"
    REAL_INTERRUPTION="REAL_INTERRUPTION"
    REAL_PROJECT_PILOT="REAL_PROJECT_PILOT"
    HUMAN_VALIDATED="HUMAN_VALIDATED"
    PROVIDER_LIVE="PROVIDER_LIVE"
    MARKET_OBSERVED="MARKET_OBSERVED"

class Disposition(str, Enum):
    PASS="PASS"
    HOLD="HOLD"
    REJECT="REJECT"
    KEEP="KEEP"
    NARROW="NARROW"
    MERGE="MERGE"
    ROLLBACK="ROLLBACK"
    SUPERSEDE="SUPERSEDE"

@dataclass(frozen=True)
class AuthoritySnapshot:
    main_sha: str
    engine: str
    engine_status: str
    registry_path: str
    ledger_path: str
    captured_at: str
    def validate(self):
        if len(self.main_sha) != 40:
            raise GateError("INVALID_MAIN_SHA")
        if self.engine_status != "VERIFIED_CURRENT":
            raise GateError("CURRENT_ENGINE_NOT_VERIFIED")

@dataclass(frozen=True)
class SourcePointer:
    source_id: str
    locator: str
    source_type: str
    authority_effect: str = "NONE"
    copyright_private: bool = False

@dataclass
class LibraryRegistry:
    pointers: dict[str, SourcePointer] = field(default_factory=dict)
    def add(self, p: SourcePointer):
        if p.source_id in self.pointers and self.pointers[p.source_id] != p:
            raise GateError("SOURCE_ID_COLLISION")
        self.pointers[p.source_id] = p
    def public_export(self) -> list[dict[str, Any]]:
        return [asdict(x) for x in sorted(self.pointers.values(), key=lambda z:z.source_id)]

@dataclass(frozen=True)
class CandidateState:
    candidate_id: str
    status: str
    scope: str
    next_gate: str

class CandidateFamily:
    def __init__(self, items: Sequence[CandidateState]):
        self.items = {x.candidate_id:x for x in items}
        if len(self.items) != len(items):
            raise GateError("DUPLICATE_CANDIDATE_ID")
    def require_unique_new_id(self, new_id:str):
        if new_id in self.items:
            raise GateError("CANDIDATE_ID_OCCUPIED")
        return True

@dataclass(frozen=True)
class InterruptionObservation:
    event_id: str
    real_interruption: bool
    projects_recovered: tuple[str, ...]
    project_slice_readback_complete: bool
    store_identity_verified: bool
    zero_false_resume_proven: bool
    duplicate_irreversible_side_effects: int = 0
    secret_leak: bool = False
    synthetic: bool = False

@dataclass(frozen=True)
class InterruptionQualification:
    event_id: str
    qualifies: bool
    reasons: tuple[str, ...]

def qualify_interruption(o: InterruptionObservation) -> InterruptionQualification:
    reasons=[]
    if not o.real_interruption or o.synthetic: reasons.append("NOT_GENUINE_INTERRUPTION")
    if not o.project_slice_readback_complete: reasons.append("PROJECT_SLICE_READBACK_INCOMPLETE")
    if not o.store_identity_verified: reasons.append("STORE_IDENTITY_UNVERIFIED")
    if not o.zero_false_resume_proven: reasons.append("ZERO_FALSE_RESUME_UNPROVEN")
    if o.duplicate_irreversible_side_effects: reasons.append("DUPLICATE_IRREVERSIBLE_SIDE_EFFECT")
    if o.secret_leak: reasons.append("SECRET_LEAK")
    return InterruptionQualification(o.event_id, not reasons, tuple(reasons))

@dataclass
class RecoveryEvidenceCounter:
    qualified_events: list[InterruptionObservation] = field(default_factory=list)
    def add(self, o: InterruptionObservation):
        q=qualify_interruption(o)
        if q.qualifies:
            self.qualified_events.append(o)
        return q
    def promotion_ready(self, min_events=3, min_projects=2) -> bool:
        projects={p for e in self.qualified_events for p in e.projects_recovered}
        return len(self.qualified_events) >= min_events and len(projects) >= min_projects

@dataclass(frozen=True)
class ProjectSlice:
    project_id: str
    embedded_frontier: str
    controlling_frontier: Optional[str]
    slice_kind: str = "CURRENT"
    explicit_approval_required: bool = False
    approval_event_present: bool = False

def project_slice_freshness(s: ProjectSlice) -> str:
    if s.slice_kind in {"HISTORICAL","SUPERSEDED","REFERENCE"}:
        return "EXEMPT_HISTORICAL_SLICE"
    if s.controlling_frontier is None:
        return "UNRESOLVED_POINTER"
    if s.embedded_frontier != s.controlling_frontier:
        return "STALE_CURRENT_SLICE"
    if s.explicit_approval_required and not s.approval_event_present:
        return "APPROVAL_EVENT_MISSING"
    return "CURRENT_MATCH"

@dataclass(frozen=True)
class EvidenceClaim:
    claim_type: str
    evidence: frozenset[EvidenceClass]

_REQUIRED = {
    "ENGINEERING_PASS": {EvidenceClass.TEST_EXECUTED},
    "REAL_INTERRUPTION_RECOVERY": {EvidenceClass.REAL_INTERRUPTION},
    "HUMAN_PREFERENCE": {EvidenceClass.HUMAN_VALIDATED},
    "LIVE_PROVIDER": {EvidenceClass.PROVIDER_LIVE},
    "MARKET_EFFECT": {EvidenceClass.MARKET_OBSERVED},
}

def evidence_gate(c: EvidenceClaim) -> tuple[bool, tuple[str,...]]:
    req=_REQUIRED.get(c.claim_type,set())
    missing=req-set(c.evidence)
    return (not missing, tuple(sorted(x.value for x in missing)))

@dataclass(frozen=True)
class MetricProposal:
    metric_id: str
    decision_id: Optional[str]
    uncertainty_reduced: Optional[str]
    collection_cost: float
    expected_information_gain: float

def metric_gate(m: MetricProposal) -> str:
    if not m.decision_id or not m.uncertainty_reduced:
        return "REJECT_METRIC_WITHOUT_DECISION_RELEVANCE"
    if m.expected_information_gain <= 0:
        return "REJECT_NO_INFORMATION_GAIN"
    return "MEASURE" if m.expected_information_gain >= m.collection_cost else "HOLD_LOW_VOI"

@dataclass(frozen=True)
class WorkItem:
    item_id: str
    active: bool
    primary: bool
    independent_pilot: bool = False

def wip_gate(items: Sequence[WorkItem], primary_limit=1, pilot_limit=2) -> str:
    prim=sum(1 for x in items if x.active and x.primary)
    pilots=sum(1 for x in items if x.active and x.independent_pilot)
    if prim > primary_limit or pilots > pilot_limit:
        return "WIP_EXCEEDED"
    return "WIP_OK"

@dataclass(frozen=True)
class CausalHypothesis:
    intervention: str
    intended_effect: str
    feedbacks: tuple[str,...]
    delays: tuple[str,...]
    guardrails: tuple[str,...]
    compensating_responses: tuple[str,...]

def causal_model_gate(h: CausalHypothesis) -> str:
    if not h.intervention or not h.intended_effect:
        return "INCOMPLETE_CAUSAL_MODEL"
    if not h.feedbacks or not h.guardrails:
        return "INCOMPLETE_CAUSAL_MODEL"
    return "CAUSAL_MODEL_READY"

@dataclass(frozen=True)
class ExperimentResult:
    experiment_id: str
    local_metric_improved: bool
    system_metric_improved: Optional[bool]
    guardrail_regression: bool
    repeated_local_failure: bool = False

def policy_resistance_gate(r: ExperimentResult) -> str:
    if r.guardrail_regression:
        return "ROLLBACK_GUARDRAIL_REGRESSION"
    if r.local_metric_improved and r.system_metric_improved is False:
        return "POLICY_RESISTANCE_DETECTED"
    if r.repeated_local_failure:
        return "DOUBLE_LOOP_REVIEW"
    return "KEEP_MONITORING"

@dataclass(frozen=True)
class DecisionDelta:
    before: str
    after: str
    independent_information_added: bool

def decision_delta_value(d: DecisionDelta) -> str:
    if d.before != d.after:
        return "DECISION_CHANGED"
    if d.independent_information_added:
        return "INFORMATION_GAIN_WITHOUT_DECISION_CHANGE"
    return "NO_DECISION_DELTA"

@dataclass(frozen=True)
class MechanismRecord:
    mechanism_id: str
    semantic_key: str
    uses: int
    false_positives: int
    decision_changes: int
    duplicates_existing: bool=False

def mechanism_disposition(m: MechanismRecord) -> Disposition:
    if m.duplicates_existing:
        return Disposition.MERGE
    if m.false_positives > max(1, m.uses//5):
        return Disposition.NARROW
    if m.uses == 0:
        return Disposition.HOLD
    if m.decision_changes == 0 and m.uses >= 3:
        return Disposition.HOLD
    return Disposition.KEEP

@dataclass(frozen=True)
class StoreAction:
    action_id: str
    store: str
    intended_hash: str
    observed_hash: Optional[str]
    state: str
    reversible: bool=True

def cross_store_closure(actions: Sequence[StoreAction]) -> str:
    for a in actions:
        if a.state == "STARTED_UNKNOWN" and not a.reversible:
            return "QUARANTINE_AMBIGUOUS_IRREVERSIBLE"
        if a.state == "CONFIRMED" and a.observed_hash != a.intended_hash:
            return "STOP_IDENTITY_MISMATCH"
        if a.state not in {"CONFIRMED","NOT_REQUIRED"}:
            return "INCOMPLETE_TRANSACTION"
    return "TRANSACTION_COMPLETE"

@dataclass(frozen=True)
class PromotionPacket:
    candidate_id: str
    status: str
    application_targets: tuple[str,...]
    verification_evidence: tuple[str,...]
    real_pilot_evidence: tuple[str,...]
    rollback_defined: bool
    universal_claim: bool=False

def promotion_gate(p: PromotionPacket) -> str:
    if p.status == "VERIFIED_CURRENT":
        if not p.application_targets or not p.verification_evidence:
            return "BLOCK_DIRECT_VERIFIED_CURRENT"
    if not p.rollback_defined:
        return "BLOCK_MISSING_ROLLBACK"
    if p.universal_claim and not p.real_pilot_evidence:
        return "BLOCK_UNIVERSAL_WITHOUT_REAL_PILOT"
    if not p.real_pilot_evidence:
        return "HOLD_REAL_PILOT_REQUIRED"
    return "PROMOTION_REVIEW_READY"

@dataclass(frozen=True)
class SelfReferenceMutation:
    changes_promotion_rule: bool
    self_exempts_from_rule: bool
    evidence_before_change: bool
    rollback_defined: bool

def self_reference_guard(m: SelfReferenceMutation) -> str:
    if m.self_exempts_from_rule:
        return "REJECT_SELF_EXEMPTION"
    if m.changes_promotion_rule and not m.evidence_before_change:
        return "HOLD_EVIDENCE_FIRST"
    if not m.rollback_defined:
        return "HOLD_ROLLBACK_REQUIRED"
    return "ALLOW_BOUNDED_PILOT"

@dataclass(frozen=True)
class RunResult:
    run_id: str
    title: str
    status: str
    finding: str
    evidence: tuple[str,...]=()
    next_action: str=""

class SequentialLedger:
    def __init__(self, run_ids: Sequence[str]):
        self.run_ids=list(run_ids); self.results=[]
    def append(self, result: RunResult):
        expected=self.run_ids[len(self.results)] if len(self.results)<len(self.run_ids) else None
        if result.run_id != expected:
            raise GateError(f"RUN_ORDER_VIOLATION:{expected}->{result.run_id}")
        self.results.append(result)
    @property
    def complete(self): return len(self.results)==len(self.run_ids)
    def digest(self):
        raw=json.dumps([asdict(x) for x in self.results],sort_keys=True,separators=(',',':')).encode()
        return hashlib.sha256(raw).hexdigest()
