from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from core.artifact_placement import (
    NOT_PERSISTED,
    PERSISTED_BUT_MISPLACED,
    PLACEMENT_VERIFIED,
    ArtifactPlacementReceipt,
)
from core.artifact_placement_adapters import (
    PlacementIntent,
    receipt_from_drive_observation,
    receipt_from_github_observation,
)

CHAT_CONNECTOR = "CHAT_CONNECTOR"
LOCAL_RUNTIME = "LOCAL_RUNTIME"

REAL_PROVIDER_READBACK = "REAL_PROVIDER_READBACK"
TEST_FIXTURE = "TEST_FIXTURE"
REPLAY = "REPLAY"
UNKNOWN_ORIGIN = "UNKNOWN"

ELIGIBLE_FOR_INDEPENDENT_LIVE_REVIEW = "ELIGIBLE_FOR_INDEPENDENT_LIVE_REVIEW"
VERIFIED_PLACEMENT_OBSERVATION = "VERIFIED_PLACEMENT_OBSERVATION"
TEST_ONLY_NOT_LIVE_EVIDENCE = "TEST_ONLY_NOT_LIVE_EVIDENCE"
POST_CLAIM_INCIDENT_NOT_PROSPECTIVE = "POST_CLAIM_INCIDENT_NOT_PROSPECTIVE"
UNVERIFIED_ORIGIN = "UNVERIFIED_ORIGIN"

_ALLOWED_ORIGINS = {
    REAL_PROVIDER_READBACK,
    TEST_FIXTURE,
    REPLAY,
    UNKNOWN_ORIGIN,
}


@dataclass(frozen=True)
class ConnectorPlacementCapture:
    """Classify ChatGPT connector-surface placement evidence without self-certification.

    This object is not platform middleware. It records evidence obtained by the
    synchronous operational protocol around a connector write/readback. Every
    capture remains non-authoritative for promotion until separately reviewed.
    """

    receipt: ArtifactPlacementReceipt
    evidence_origin: str
    provider_readback_ref: str | None
    captured_before_completion_claim: bool
    completion_claim_emitted: bool
    captured_at: str
    execution_surface: str = CHAT_CONNECTOR

    def __post_init__(self) -> None:
        origin = self.evidence_origin.strip().upper()
        if origin not in _ALLOWED_ORIGINS:
            raise ValueError(f"unsupported evidence_origin: {self.evidence_origin}")
        object.__setattr__(self, "evidence_origin", origin)
        if self.execution_surface != CHAT_CONNECTOR:
            raise ValueError("ConnectorPlacementCapture execution_surface must be CHAT_CONNECTOR")
        if not self.captured_at.strip():
            raise ValueError("captured_at is required and must be supplied by the caller")
        if self.provider_readback_ref is not None:
            cleaned = self.provider_readback_ref.strip()
            object.__setattr__(self, "provider_readback_ref", cleaned or None)

    @property
    def review_status(self) -> str:
        if self.evidence_origin in {TEST_FIXTURE, REPLAY}:
            return TEST_ONLY_NOT_LIVE_EVIDENCE
        if self.evidence_origin != REAL_PROVIDER_READBACK or not self.provider_readback_ref:
            return UNVERIFIED_ORIGIN
        if self.receipt.status == PLACEMENT_VERIFIED:
            return VERIFIED_PLACEMENT_OBSERVATION
        if not self.captured_before_completion_claim or self.completion_claim_emitted:
            return POST_CLAIM_INCIDENT_NOT_PROSPECTIVE
        if self.receipt.status in {PERSISTED_BUT_MISPLACED, NOT_PERSISTED}:
            return ELIGIBLE_FOR_INDEPENDENT_LIVE_REVIEW
        return UNVERIFIED_ORIGIN

    @property
    def promotion_proof(self) -> bool:
        # Deliberately impossible at runtime. Independent authority review owns
        # any later promotion decision.
        return False

    @property
    def independent_review_required(self) -> bool:
        return True

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["receipt"] = self.receipt.to_dict()
        data["review_status"] = self.review_status
        data["promotion_proof"] = self.promotion_proof
        data["independent_review_required"] = self.independent_review_required
        return data


def capture_from_receipt(
    receipt: ArtifactPlacementReceipt | Mapping[str, Any],
    *,
    evidence_origin: str,
    provider_readback_ref: str | None,
    captured_before_completion_claim: bool,
    completion_claim_emitted: bool,
    captured_at: str,
) -> ConnectorPlacementCapture:
    normalized = (
        receipt
        if isinstance(receipt, ArtifactPlacementReceipt)
        else ArtifactPlacementReceipt.from_mapping(receipt)
    )
    return ConnectorPlacementCapture(
        receipt=normalized,
        evidence_origin=evidence_origin,
        provider_readback_ref=provider_readback_ref,
        captured_before_completion_claim=captured_before_completion_claim,
        completion_claim_emitted=completion_claim_emitted,
        captured_at=captured_at,
    )


def capture_from_drive_readback(
    *,
    intent: PlacementIntent,
    artifact_metadata: Mapping[str, Any],
    start_here_readback_ok: bool,
    start_here_mentions_artifact: bool,
    provider_readback_ref: str | None,
    captured_before_completion_claim: bool,
    completion_claim_emitted: bool,
    captured_at: str,
    evidence_origin: str = REAL_PROVIDER_READBACK,
    legacy_conflicts: Sequence[str] = (),
    cross_store_pointer_present: bool = False,
) -> ConnectorPlacementCapture:
    receipt = receipt_from_drive_observation(
        intent=intent,
        artifact_metadata=artifact_metadata,
        start_here_readback_ok=start_here_readback_ok,
        start_here_mentions_artifact=start_here_mentions_artifact,
        legacy_conflicts=legacy_conflicts,
        cross_store_pointer_present=cross_store_pointer_present,
    )
    return capture_from_receipt(
        receipt,
        evidence_origin=evidence_origin,
        provider_readback_ref=provider_readback_ref,
        captured_before_completion_claim=captured_before_completion_claim,
        completion_claim_emitted=completion_claim_emitted,
        captured_at=captured_at,
    )


def capture_from_github_readback(
    *,
    intent: PlacementIntent,
    repository_full_name: str,
    path: str,
    file_observed: bool,
    current_index_readback_ok: bool,
    current_index_mentions_artifact: bool,
    provider_readback_ref: str | None,
    captured_before_completion_claim: bool,
    completion_claim_emitted: bool,
    captured_at: str,
    evidence_origin: str = REAL_PROVIDER_READBACK,
    legacy_conflicts: Sequence[str] = (),
    cross_store_pointer_present: bool = False,
) -> ConnectorPlacementCapture:
    receipt = receipt_from_github_observation(
        intent=intent,
        repository_full_name=repository_full_name,
        path=path,
        file_observed=file_observed,
        current_index_readback_ok=current_index_readback_ok,
        current_index_mentions_artifact=current_index_mentions_artifact,
        legacy_conflicts=legacy_conflicts,
        cross_store_pointer_present=cross_store_pointer_present,
    )
    return capture_from_receipt(
        receipt,
        evidence_origin=evidence_origin,
        provider_readback_ref=provider_readback_ref,
        captured_before_completion_claim=captured_before_completion_claim,
        completion_claim_emitted=completion_claim_emitted,
        captured_at=captured_at,
    )
