from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Literal

Verdict = Literal[
    "NO_PROMOTION","NO_FINITE_STATE","EXACT","APPROXIMATE",
    "RESOURCE_ONLY","INCONCLUSIVE","HOLD","PASS","FAIL"
]

@dataclass(frozen=True)
class ContextContract:
    context_id: str
    kind: str
    description: str
    required_exact: bool = True
    tolerance: float = 0.0

@dataclass
class PromotionProblem:
    problem_id: str
    micro_states: list[Any]
    contexts: list[ContextContract]
    tolerance: float = 0.0
    admissibility: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class GateResult:
    gate: str
    passed: bool
    metric: float | None = None
    threshold: float | None = None
    reason: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)

@dataclass
class PromotionDecision:
    verdict: Verdict
    candidate_id: str | None
    gates: list[GateResult]
    semantic_state_count: int | None = None
    notes: list[str] = field(default_factory=list)
    def to_dict(self):
        return {"verdict":self.verdict,"candidate_id":self.candidate_id,
                "semantic_state_count":self.semantic_state_count,
                "gates":[asdict(g) for g in self.gates],"notes":list(self.notes)}

@dataclass
class EvidenceRecord:
    evidence_id: str
    claim_id: str
    evidence_class: str
    source_ref: str
    supports: bool
    payload: dict[str, Any]
    cannot_prove: list[str] = field(default_factory=list)

@dataclass
class ImprovementProposal:
    proposal_id: str
    parent_revision: str
    hypothesis: str
    mutation_scope: list[str]
    target_metrics: dict[str, float]
    forbidden_mutations: list[str]
    benchmark_ids: list[str]
    rollback_ref: str
    status: str = "PROPOSED"
    metadata: dict[str, Any] = field(default_factory=dict)
