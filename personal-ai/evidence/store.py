from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Iterable

from memory.store import MemoryStore

CLAIM_TYPES = (
    "FACT",
    "SOURCE_CLAIM",
    "USER_DECISION",
    "AI_INFERENCE",
    "HYPOTHESIS",
    "TEST_RESULT",
)
VERIFICATION_STATES = ("UNVERIFIED", "VERIFIED", "REJECTED")


class EvidenceError(ValueError):
    pass


class VerificationRequiredError(RuntimeError):
    pass


def _clean_text(value: Any, field: str) -> str:
    text = str(value).strip() if value is not None else ""
    if not text:
        raise EvidenceError(f"{field} cannot be empty")
    return text


def _claim_type(value: str) -> str:
    normalized = _clean_text(value, "claim_type").upper()
    if normalized not in CLAIM_TYPES:
        raise EvidenceError(f"unsupported claim_type: {normalized}")
    return normalized


def _confidence(value: float | None) -> float | None:
    if value is None:
        return None
    parsed = float(value)
    if not 0 <= parsed <= 1:
        raise EvidenceError("confidence must be between 0 and 1")
    return parsed


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex}"


class EvidenceStore:
    """PL-03 provenance-aware claims backed by the PL-02 MemoryStore."""

    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")

    def create_document(
        self,
        project_id: str,
        text: str,
        *,
        source_label: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        project_id = _clean_text(project_id, "project_id")
        text = _clean_text(text, "document text")
        payload = dict(metadata or {})
        payload.update({"evidence_layer": "PL-03", "record_role": "DOCUMENT"})
        return self.memory.store(
            text,
            kind="DOCUMENT",
            source=source_label or "PL-03 document",
            metadata=payload,
            record_id=_new_id("doc"),
            project_id=project_id,
        )

    def create_source(
        self,
        project_id: str,
        document_id: str,
        text: str,
        *,
        source_label: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        project_id = _clean_text(project_id, "project_id")
        document = self.memory.get(_clean_text(document_id, "document_id"))
        if document["kind"] != "DOCUMENT":
            raise EvidenceError("source parent must be a DOCUMENT record")
        if document.get("project_id") != project_id:
            raise EvidenceError("source and document must belong to the same project")
        payload = dict(metadata or {})
        payload.update(
            {
                "evidence_layer": "PL-03",
                "record_role": "SOURCE",
                "document_id": document["id"],
            }
        )
        return self.memory.store(
            _clean_text(text, "source text"),
            kind="SOURCE",
            source=source_label or "PL-03 source",
            metadata=payload,
            record_id=_new_id("src"),
            project_id=project_id,
            source_id=document["id"],
        )

    def create_claim(
        self,
        project_id: str,
        text: str,
        claim_type: str,
        *,
        source_ids: Iterable[str] = (),
        confidence: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        project_id = _clean_text(project_id, "project_id")
        ctype = _claim_type(claim_type)
        confidence = _confidence(confidence)
        normalized_sources = self._validated_sources(project_id, source_ids)
        payload = dict(metadata or {})
        payload.update(
            {
                "evidence_layer": "PL-03",
                "record_role": "CLAIM",
                "claim_type": ctype,
                "source_ids": normalized_sources,
                "verified_state": "UNVERIFIED",
                "verification_event_id": None,
                "verified_by": None,
                "emitted_fact_id": None,
            }
        )
        return self.memory.store(
            _clean_text(text, "claim text"),
            kind="CLAIM",
            source="PL-03 Source Evidence Layer",
            metadata=payload,
            record_id=_new_id("claim"),
            project_id=project_id,
            source_id=normalized_sources[0] if normalized_sources else None,
            confidence=confidence,
        )

    def verify_claim(
        self,
        claim_id: str,
        *,
        verifier: str,
        evidence: str,
        verification_source_ids: Iterable[str] = (),
    ) -> dict[str, Any]:
        claim = self._claim(claim_id)
        if claim["metadata"].get("verified_state") == "REJECTED":
            raise EvidenceError("rejected claim cannot be verified without a new claim record")
        project_id = claim.get("project_id")
        verification_sources = self._validated_sources(project_id, verification_source_ids)
        event = self.memory.store(
            _clean_text(evidence, "verification evidence"),
            kind="EVENT",
            source="PL-03 explicit verification",
            metadata={
                "evidence_layer": "PL-03",
                "event_type": "CLAIM_VERIFICATION",
                "result": "VERIFIED",
                "claim_id": claim["id"],
                "verifier": _clean_text(verifier, "verifier"),
                "verification_source_ids": verification_sources,
            },
            record_id=_new_id("verify"),
            project_id=project_id,
            source_id=claim["id"],
        )
        metadata = dict(claim["metadata"])
        metadata.update(
            {
                "verified_state": "VERIFIED",
                "verification_event_id": event["id"],
                "verified_by": _clean_text(verifier, "verifier"),
                "verification_source_ids": verification_sources,
            }
        )
        updated = self.memory.update(claim["id"], metadata=metadata)
        return {"claim": updated, "verification_event": event}

    def reject_claim(self, claim_id: str, *, verifier: str, evidence: str) -> dict[str, Any]:
        claim = self._claim(claim_id)
        event = self.memory.store(
            _clean_text(evidence, "rejection evidence"),
            kind="EVENT",
            source="PL-03 explicit verification",
            metadata={
                "evidence_layer": "PL-03",
                "event_type": "CLAIM_VERIFICATION",
                "result": "REJECTED",
                "claim_id": claim["id"],
                "verifier": _clean_text(verifier, "verifier"),
            },
            record_id=_new_id("verify"),
            project_id=claim.get("project_id"),
            source_id=claim["id"],
        )
        metadata = dict(claim["metadata"])
        metadata.update(
            {
                "verified_state": "REJECTED",
                "verification_event_id": event["id"],
                "verified_by": _clean_text(verifier, "verifier"),
            }
        )
        return {"claim": self.memory.update(claim["id"], metadata=metadata), "verification_event": event}

    def emit_verified_fact(self, claim_id: str) -> dict[str, Any]:
        claim = self._claim(claim_id)
        metadata = claim["metadata"]
        if metadata.get("verified_state") != "VERIFIED":
            raise VerificationRequiredError(
                "claim cannot be emitted as VERIFIED_FACT without explicit verification"
            )
        event_id = metadata.get("verification_event_id")
        if not event_id:
            raise VerificationRequiredError("verified claim is missing verification_event_id")
        event = self.memory.get(event_id)
        if not self._valid_verification_event(event, claim["id"]):
            raise VerificationRequiredError("verification_event_id does not prove this claim")
        existing_id = metadata.get("emitted_fact_id")
        if existing_id:
            try:
                existing = self.memory.get(existing_id)
            except KeyError:
                existing = None
            if existing and existing["status"] == "ACTIVE":
                return existing
        fact = self.memory.store(
            claim["content"],
            kind="FACT",
            source="PL-03 verified fact emission",
            metadata={
                "evidence_layer": "PL-03",
                "record_role": "VERIFIED_FACT",
                "verified_state": "VERIFIED",
                "derived_from_claim_id": claim["id"],
                "original_claim_type": metadata.get("claim_type"),
                "verification_event_id": event_id,
                "source_ids": list(metadata.get("source_ids") or []),
            },
            record_id=_new_id("fact"),
            project_id=claim.get("project_id"),
            source_id=claim["id"],
            confidence=claim.get("confidence"),
        )
        claim_metadata = dict(metadata)
        claim_metadata["emitted_fact_id"] = fact["id"]
        self.memory.update(claim["id"], metadata=claim_metadata)
        return fact

    def trace_claim(self, claim_id: str) -> dict[str, Any]:
        claim = self._claim(claim_id)
        sources: list[dict[str, Any]] = []
        documents: list[dict[str, Any]] = []
        document_ids: set[str] = set()
        for source_id in claim["metadata"].get("source_ids") or []:
            source = self.memory.get(source_id)
            sources.append(source)
            document_id = source.get("source_id")
            if document_id and document_id not in document_ids:
                document = self.memory.get(document_id)
                if document["kind"] != "DOCUMENT":
                    raise EvidenceError(f"source {source_id} does not trace to a DOCUMENT")
                documents.append(document)
                document_ids.add(document_id)
        verification_event = None
        event_id = claim["metadata"].get("verification_event_id")
        if event_id:
            verification_event = self.memory.get(event_id)
        emitted_fact = None
        fact_id = claim["metadata"].get("emitted_fact_id")
        if fact_id:
            emitted_fact = self.memory.get(fact_id)
        return {
            "claim": claim,
            "sources": sources,
            "documents": documents,
            "project_id": claim.get("project_id"),
            "verification_event": verification_event,
            "emitted_fact": emitted_fact,
            "provenance_route": "claim <- source <- document <- project",
        }

    def _validated_sources(self, project_id: str | None, source_ids: Iterable[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for raw in source_ids:
            source_id = _clean_text(raw, "source_id")
            if source_id in seen:
                continue
            source = self.memory.get(source_id)
            if source["kind"] != "SOURCE":
                raise EvidenceError(f"claim source must be SOURCE record: {source_id}")
            if source.get("project_id") != project_id:
                raise EvidenceError("claim and source must belong to the same project")
            normalized.append(source_id)
            seen.add(source_id)
        return normalized

    def _claim(self, claim_id: str) -> dict[str, Any]:
        claim = self.memory.get(_clean_text(claim_id, "claim_id"))
        if claim["kind"] != "CLAIM" or claim["metadata"].get("record_role") != "CLAIM":
            raise EvidenceError("record is not a PL-03 claim")
        return claim

    @staticmethod
    def _valid_verification_event(event: dict[str, Any], claim_id: str) -> bool:
        metadata = event.get("metadata") or {}
        return (
            event.get("kind") == "EVENT"
            and event.get("source_id") == claim_id
            and metadata.get("event_type") == "CLAIM_VERIFICATION"
            and metadata.get("result") == "VERIFIED"
            and metadata.get("claim_id") == claim_id
        )
