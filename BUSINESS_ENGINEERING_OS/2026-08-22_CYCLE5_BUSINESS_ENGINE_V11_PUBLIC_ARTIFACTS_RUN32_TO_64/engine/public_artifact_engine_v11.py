from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Iterable, Mapping, Optional, Sequence, Tuple
from collections import deque
import hashlib
import json

class BusinessArtifactError(RuntimeError):
    pass

class EvidencePlane(str, Enum):
    K = "K"
    S = "S"
    E = "E"

class ExperimentVerdict(str, Enum):
    KEEP = "KEEP"
    RESHAPE = "RESHAPE"
    KILL = "KILL"
    HOLD = "HOLD"
    PROTECT_NO_CHANGE = "PROTECT_NO_CHANGE"

class RequirementClass(str, Enum):
    MUST = "MUST"
    SHOULD = "SHOULD"
    INFO = "INFO"
    UNKNOWN = "UNKNOWN"

PROOF_ORDER = {"E0":0,"E1":1,"E2":2,"E2_PLUS":2.5,"E3":3,"E4":4,"E5":5,"E6":6,"E7":7}

@dataclass(frozen=True)
class SourceEvidence:
    source_id: str
    title: str
    source_url: str
    authority: str
    published_at: Optional[str]
    retrieved_at: str
    current: bool
    lineage_parent: Optional[str] = None
    evidence_plane: EvidencePlane = EvidencePlane.S

    def validate(self) -> None:
        if not all([self.source_id, self.title, self.source_url, self.authority, self.retrieved_at]):
            raise BusinessArtifactError("SOURCE_EVIDENCE_INCOMPLETE")
        if self.evidence_plane is EvidencePlane.E:
            raise BusinessArtifactError("PUBLIC_SOURCE_CANNOT_SELF_DECLARE_MARKET_EVIDENCE")

@dataclass(frozen=True)
class Requirement:
    requirement_id: str
    text: str
    klass: RequirementClass
    source_id: str
    verified: bool
    fatal_if_missing: bool = False

@dataclass(frozen=True)
class TenderSnapshot:
    tender_id: str
    source_id: str
    title: str
    contracting_authority: str
    deadline: Optional[str]
    clarification_deadline: Optional[str]
    estimated_value_eur: Optional[float]
    procedure: Optional[str]
    cpv: Tuple[str, ...]
    scope_summary: str
    status: str

@dataclass(frozen=True)
class LineageDecision:
    current_source_id: str
    superseded_source_ids: Tuple[str, ...]
    inherited_fields: Mapping[str, Any]
    rejected_inheritance: Mapping[str, str]


def resolve_signal_lineage(snapshots: Sequence[TenderSnapshot]) -> LineageDecision:
    if not snapshots:
        raise BusinessArtifactError("NO_SNAPSHOTS")
    current = [s for s in snapshots if s.status == "CURRENT"]
    if len(current) != 1:
        raise BusinessArtifactError("EXACTLY_ONE_CURRENT_REQUIRED")
    cur = current[0]
    older = [s for s in snapshots if s.source_id != cur.source_id]
    inherited: dict[str, Any] = {}
    rejected: dict[str, str] = {}
    for field_name in ("deadline", "clarification_deadline", "estimated_value_eur", "procedure"):
        cur_value = getattr(cur, field_name)
        old_values = {getattr(x, field_name) for x in older}
        if cur_value is None and any(v is not None for v in old_values):
            rejected[field_name] = "OLD_VALUE_NOT_PROMOTED_TO_CURRENT"
        elif cur_value is not None:
            inherited[field_name] = cur_value
    return LineageDecision(cur.source_id, tuple(sorted(x.source_id for x in older)), inherited, rejected)

@dataclass(frozen=True)
class PublicArtifact:
    artifact_id: str
    opportunity_id: str
    artifact_type: str
    source_ids: Tuple[str, ...]
    requirements: Tuple[Requirement, ...]
    explicit_unknowns: Tuple[str, ...]
    hard_exclusions: Tuple[str, ...]
    buyer_role_public: Optional[str]
    budget_owner_public: Optional[str]
    proof_level: str = "E2_PLUS"
    professional_boundary: Optional[str] = None

    def validate(self) -> None:
        if not self.artifact_id or not self.opportunity_id or not self.artifact_type:
            raise BusinessArtifactError("ARTIFACT_IDENTITY_REQUIRED")
        if not self.source_ids:
            raise BusinessArtifactError("ARTIFACT_SOURCE_REQUIRED")
        if PROOF_ORDER[self.proof_level] > PROOF_ORDER["E2_PLUS"]:
            raise BusinessArtifactError("PUBLIC_ARTIFACT_PROOF_CEILING_EXCEEDED")
        if any(r.fatal_if_missing and not r.verified for r in self.requirements):
            raise BusinessArtifactError("FATAL_REQUIREMENT_UNVERIFIED")

    def digest(self) -> str:
        payload = asdict(self)
        payload["requirements"] = [{**asdict(r), "klass": r.klass.value} for r in self.requirements]
        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
        return hashlib.sha256(raw).hexdigest()

@dataclass(frozen=True)
class ArtifactExperiment:
    experiment_id: str
    artifact_id: str
    decision_before: str
    decision_after: str
    baseline_minutes: Optional[float]
    engine_minutes: Optional[float]
    baseline_errors: Optional[int]
    engine_errors: Optional[int]
    unique_information_added: bool
    external_buyer_event: bool = False
    external_payment_event: bool = False

@dataclass(frozen=True)
class ExperimentAssessment:
    verdict: ExperimentVerdict
    decision_changed: bool
    time_saved_minutes: Optional[float]
    errors_reduced: Optional[int]
    reason: str


def assess_experiment(exp: ArtifactExperiment) -> ExperimentAssessment:
    decision_changed = exp.decision_before != exp.decision_after
    time_saved = None
    if exp.baseline_minutes is not None and exp.engine_minutes is not None:
        time_saved = exp.baseline_minutes - exp.engine_minutes
    errors_reduced = None
    if exp.baseline_errors is not None and exp.engine_errors is not None:
        errors_reduced = exp.baseline_errors - exp.engine_errors
    if exp.external_payment_event:
        return ExperimentAssessment(ExperimentVerdict.KEEP, decision_changed, time_saved, errors_reduced, "REAL_PAYMENT_EVENT")
    if exp.external_buyer_event:
        return ExperimentAssessment(ExperimentVerdict.KEEP, decision_changed, time_saved, errors_reduced, "REAL_BUYER_EVENT")
    if decision_changed or exp.unique_information_added:
        return ExperimentAssessment(ExperimentVerdict.KEEP, decision_changed, time_saved, errors_reduced, "DECISION_OR_INFORMATION_GAIN")
    if exp.baseline_minutes is None or exp.engine_minutes is None:
        return ExperimentAssessment(ExperimentVerdict.HOLD, decision_changed, None, errors_reduced, "MEASUREMENT_NOT_RUN")
    return ExperimentAssessment(ExperimentVerdict.RESHAPE, decision_changed, time_saved, errors_reduced, "NO_DECISION_DELTA")


def public_proof_level(*, real_buyer_event: bool = False, real_payment_event: bool = False) -> str:
    if real_payment_event:
        return "E4"
    if real_buyer_event:
        return "E3"
    return "E2_PLUS"


def monetary_economics(*, actual_revenue_eur: Optional[float], actual_direct_cost_eur: Optional[float], measured_delivery_minutes: Optional[float]) -> Optional[dict[str, float]]:
    if actual_revenue_eur is None or actual_direct_cost_eur is None or measured_delivery_minutes is None:
        return None
    return {"actual_revenue_eur": actual_revenue_eur, "actual_direct_cost_eur": actual_direct_cost_eur, "measured_delivery_minutes": measured_delivery_minutes, "actual_contribution_eur": actual_revenue_eur - actual_direct_cost_eur}


def buyer_role_gate(role: Optional[str], source_public: bool) -> dict[str, Optional[str]]:
    if role is None:
        return {"role": None, "grade": "UNKNOWN"}
    return {"role": role, "grade": "PUBLIC_ROLE" if source_public else "UNVERIFIED"}


def payment_proof_gate(event: Mapping[str, Any]) -> str:
    allowed = {"PAID_INVOICE", "DEPOSIT_RECEIVED", "PURCHASE_ORDER", "SIGNED_PAID_PILOT"}
    event_type = event.get("event_type")
    evidence_ref = event.get("evidence_ref")
    if event_type in allowed and evidence_ref:
        return "E4"
    return "NOT_E4"

@dataclass(frozen=True)
class ArtifactDependency:
    source: str
    target: str
    semantic: bool = True


def build_artifact_dependency_graph(edges: Iterable[ArtifactDependency]) -> dict[str, tuple[str, ...]]:
    graph: dict[str, set[str]] = {}
    for e in edges:
        if not e.source or not e.target:
            raise BusinessArtifactError("DEPENDENCY_ENDPOINT_REQUIRED")
        if not e.semantic:
            continue
        graph.setdefault(e.source, set()).add(e.target)
    return {k: tuple(sorted(v)) for k, v in graph.items()}


def artifact_selective_invalidation(graph: Mapping[str, Sequence[str]], changed: Iterable[str], locked: Iterable[str] = ()) -> dict[str, tuple[str, ...]]:
    dirty = set(changed)
    locks = set(locked)
    blocked: set[str] = set()
    q = deque(changed)
    while q:
        node = q.popleft()
        for nxt in graph.get(node, ()):
            if nxt in locks:
                blocked.add(nxt)
                continue
            if nxt not in dirty:
                dirty.add(nxt)
                q.append(nxt)
    return {"dirty": tuple(sorted(dirty)), "blocked_locked": tuple(sorted(blocked))}

@dataclass(frozen=True)
class DecisionLedgerEntry:
    event_id: str
    opportunity_id: str
    evidence_ref: str
    decision_before: str
    decision_after: str
    rationale: str

    @property
    def changed(self) -> bool:
        return self.decision_before != self.decision_after


def decision_value(entry: DecisionLedgerEntry) -> str:
    return "DECISION_CHANGED" if entry.changed else "NO_DECISION_DELTA"


def artifact_stop_gate(history: Sequence[ExperimentAssessment], max_no_delta: int = 2) -> str:
    if not history:
        return "RUN_FIRST_ARTIFACT"
    recent = history[-max_no_delta:]
    if len(recent) == max_no_delta and all((not x.decision_changed and x.verdict in {ExperimentVerdict.RESHAPE, ExperimentVerdict.HOLD}) for x in recent):
        return "STOP_OR_CHANGE_HYPOTHESIS"
    return "CONTINUE_BOUNDED"

@dataclass(frozen=True)
class PortfolioCandidate:
    opportunity_id: str
    hypothesis_family: str
    ready: bool
    independent_information: bool
    priority_rank: int


def information_gain_portfolio(candidates: Sequence[PortfolioCandidate], primary_limit: int = 1, pilot_limit: int = 2) -> dict[str, tuple[str, ...]]:
    ready = sorted((c for c in candidates if c.ready), key=lambda c: (c.priority_rank, c.opportunity_id))
    primary: list[PortfolioCandidate] = ready[:primary_limit]
    used = {c.hypothesis_family for c in primary}
    pilots: list[PortfolioCandidate] = []
    for c in ready[primary_limit:]:
        if len(pilots) >= pilot_limit:
            break
        if not c.independent_information or c.hypothesis_family in used:
            continue
        pilots.append(c)
        used.add(c.hypothesis_family)
    selected = {c.opportunity_id for c in primary + pilots}
    held = [c.opportunity_id for c in ready if c.opportunity_id not in selected]
    return {"primary": tuple(c.opportunity_id for c in primary), "pilots": tuple(c.opportunity_id for c in pilots), "held": tuple(held)}

@dataclass(frozen=True)
class SelfImprovementObservation:
    observation_id: str
    problem_family: str
    evidence_refs: Tuple[str, ...]
    repeated_count: int
    regression_pass: bool
    readback_pass: bool
    decision_delta: bool


def self_improvement_disposition(obs: SelfImprovementObservation) -> str:
    if obs.repeated_count < 2:
        return "OBSERVE_MORE"
    if not obs.regression_pass or not obs.readback_pass:
        return "HOLD_EVIDENCE_INCOMPLETE"
    if not obs.decision_delta:
        return "PROTECT_NO_CHANGE"
    return "READY_FOR_BOUNDED_CANDIDATE_REVIEW"


def mechanism_prune(*, duplicate: bool, used_in_real_decision: bool, false_positive_rate: Optional[float]) -> str:
    if duplicate:
        return "MERGE"
    if false_positive_rate is not None and false_positive_rate > 0.25:
        return "NARROW"
    if not used_in_real_decision:
        return "HOLD_TELEMETRY"
    return "KEEP"


def build_artifact_manifest(artifacts: Sequence[PublicArtifact]) -> dict[str, Any]:
    ids = [a.artifact_id for a in artifacts]
    if len(ids) != len(set(ids)):
        raise BusinessArtifactError("DUPLICATE_ARTIFACT_ID")
    return {"artifact_count": len(artifacts), "artifacts": [{"artifact_id": a.artifact_id, "opportunity_id": a.opportunity_id, "sha256": a.digest()} for a in artifacts]}
