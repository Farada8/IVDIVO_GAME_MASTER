from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from typing import Any, Dict, Iterable, List, Optional, Sequence
import json


CREDENTIAL_TOKENS = (
    "password", "passwd", "token", "cookie", "authorization",
    "session", "secret", "api_key", "apikey", "bearer",
)

ALLOWED_RELATIONS = {"SUPPLEMENTS", "REPLACES", "WITHDRAWS", "UNKNOWN_RELATION"}


@dataclass(frozen=True)
class FileRecord:
    filename: str
    sha256: str
    size: int
    media_type: str
    source_ref: str
    revision_id: Optional[str] = None


@dataclass(frozen=True)
class AcquisitionReceipt:
    resource_id: str
    channel: str
    acquired_at: str
    actor: str
    source_url: str
    evidence_class: str


@dataclass(frozen=True)
class SupersessionEdge:
    source_id: str
    target_id: str
    relation: str


@dataclass(frozen=True)
class AuthorityGapCertificateV2:
    resource_id: str
    missing_authority: tuple[str, ...]
    blocked_downstream: tuple[str, ...]
    cheapest_admissible_action: str
    evidence_grade_unchanged: bool = True


def _contains_credential_key(obj: Any) -> bool:
    if isinstance(obj, dict):
        for key, value in obj.items():
            lowered = str(key).lower()
            if any(token in lowered for token in CREDENTIAL_TOKENS):
                return True
            if _contains_credential_key(value):
                return True
    elif isinstance(obj, (list, tuple)):
        return any(_contains_credential_key(v) for v in obj)
    return False


def sanitize_ingest_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Reject credential-bearing metadata rather than attempting lossy redaction."""
    if _contains_credential_key(metadata):
        raise ValueError("credential-like metadata is forbidden in persisted pack artifacts")
    return dict(metadata)


def bind_receipt(receipt: AcquisitionReceipt, expected_resource_id: str) -> AcquisitionReceipt:
    if not expected_resource_id or receipt.resource_id != expected_resource_id:
        raise ValueError("acquisition receipt resource mismatch")
    required = (
        receipt.channel, receipt.acquired_at, receipt.actor,
        receipt.source_url, receipt.evidence_class,
    )
    if not all(required):
        raise ValueError("acquisition receipt is incomplete")
    return receipt


def canonical_manifest_payload(files: Sequence[FileRecord]) -> List[Dict[str, Any]]:
    rows = [asdict(f) for f in files]
    rows.sort(key=lambda r: (
        r["filename"], r["sha256"], r["size"], r["media_type"],
        r["source_ref"], r.get("revision_id") or "",
    ))
    return rows


def canonical_manifest_hash(files: Sequence[FileRecord]) -> str:
    payload = canonical_manifest_payload(files)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256(encoded).hexdigest()


def inventory_state(
    observed_ids: Iterable[str],
    authoritative_expected_ids: Optional[Iterable[str]] = None,
    authoritative_completeness_evidence: bool = False,
) -> Dict[str, Any]:
    observed = sorted(set(observed_ids))
    if authoritative_expected_ids is None:
        return {
            "status": "OBSERVED_ONLY_COMPLETENESS_UNPROVEN",
            "observed": observed,
            "missing": None,
            "authoritatively_complete": False,
        }

    expected = sorted(set(authoritative_expected_ids))
    missing = sorted(set(expected) - set(observed))
    unexpected = sorted(set(observed) - set(expected))
    if missing:
        return {
            "status": "INVENTORY_INCOMPLETE",
            "observed": observed,
            "expected": expected,
            "missing": missing,
            "unexpected": unexpected,
            "authoritatively_complete": False,
        }

    if not authoritative_completeness_evidence:
        return {
            "status": "EXPECTED_SET_OBSERVED_COMPLETENESS_AUTHORITY_UNPROVEN",
            "observed": observed,
            "expected": expected,
            "missing": [],
            "unexpected": unexpected,
            "authoritatively_complete": False,
        }

    return {
        "status": "AUTHORITATIVELY_COMPLETE",
        "observed": observed,
        "expected": expected,
        "missing": [],
        "unexpected": unexpected,
        "authoritatively_complete": True,
    }


def build_supersession_graph(edges: Sequence[SupersessionEdge]) -> Dict[str, Any]:
    normalized: List[Dict[str, str]] = []
    for edge in edges:
        if edge.source_id == edge.target_id:
            raise ValueError("self-supersession edge is invalid")
        if edge.relation not in ALLOWED_RELATIONS:
            raise ValueError("unsupported supersession relation")
        normalized.append(asdict(edge))
    normalized.sort(key=lambda e: (e["source_id"], e["target_id"], e["relation"]))
    return {"edges": normalized, "unknown_relation_count": sum(e["relation"] == "UNKNOWN_RELATION" for e in normalized)}


def target_requirements_only(
    target_requirements: Sequence[str],
    benchmark_requirements: Sequence[str],
    target_pack_complete: bool,
) -> Dict[str, Any]:
    """Benchmark material may exercise parsers but never fills current target rows."""
    return {
        "target_requirements": list(target_requirements),
        "benchmark_requirements_excluded": list(benchmark_requirements),
        "benchmark_rows_carried_over": 0,
        "target_pack_complete": bool(target_pack_complete),
    }


def compile_authority_gap_certificate_v2(
    resource_id: str,
    missing_authority: Sequence[str],
    blocked_downstream: Sequence[str],
    cheapest_admissible_action: str,
) -> AuthorityGapCertificateV2:
    if not resource_id:
        raise ValueError("resource_id is required")
    missing = tuple(x for x in missing_authority if x)
    blocked = tuple(x for x in blocked_downstream if x)
    if not missing:
        raise ValueError("gap certificate requires an actual missing-authority statement")
    if not cheapest_admissible_action:
        raise ValueError("next admissible action is required")
    return AuthorityGapCertificateV2(
        resource_id=resource_id,
        missing_authority=missing,
        blocked_downstream=blocked,
        cheapest_admissible_action=cheapest_admissible_action,
    )


class AuthenticatedPackIngestAdapter:
    """Credential-neutral boundary for already-exported official files/metadata."""

    def ingest(
        self,
        *,
        expected_resource_id: str,
        receipt: AcquisitionReceipt,
        files: Sequence[FileRecord],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        bound = bind_receipt(receipt, expected_resource_id)
        safe_metadata = sanitize_ingest_metadata(metadata or {})
        return {
            "resource_id": expected_resource_id,
            "receipt": asdict(bound),
            "manifest_hash": canonical_manifest_hash(files),
            "files": canonical_manifest_payload(files),
            "metadata": safe_metadata,
            "pack_completeness": "UNPROVEN_UNTIL_SEPARATE_AUTHORITY_GATE",
        }
