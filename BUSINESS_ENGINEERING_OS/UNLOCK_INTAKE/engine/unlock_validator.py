from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any, Dict, Optional, Sequence


EXPECTED_RESOURCE_ID = "8872468"
EXPECTED_LEGAL_ENTITY = "SYNTHESIS-IVDIVO LIMITED"
EXPECTED_REGISTRATION_NUMBER = "796820"
INTERNAL_EVALUATION_SCOPE = "INTERNAL_ELIGIBILITY_CAPABILITY_AND_BID_HOLD_NO_BID_EVALUATION_ONLY"

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PACK_PATH = _REPO_ROOT / "BUSINESS_ENGINEERING_OS/2026-08-22_CYCLE10_P257_P264_PACK_INGEST_HARDENING/engine/authenticated_pack_ingest.py"
_BIDDER_PATH = _REPO_ROOT / "BUSINESS_ENGINEERING_OS/2026-08-22_CYCLE10_P265_P272_BIDDER_EVIDENCE_HARDENING/engine/bidder_evidence_hardening.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load canonical module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pack = _load(_PACK_PATH, "ivdivo_business_pack_ingest")
bidder = _load(_BIDDER_PATH, "ivdivo_business_bidder_evidence")


def validate_p225_input(
    *,
    receipt,
    files: Sequence[Any],
    metadata: Optional[Dict[str, Any]] = None,
    authoritative_expected_ids: Optional[Sequence[str]] = None,
    authoritative_completeness_evidence: bool = False,
) -> Dict[str, Any]:
    """Validate an actual candidate P225 input without mutating authority.

    Acquisition and completeness remain separate. A valid official export may be
    accepted for ingest while completeness is still unproven.
    """
    if not files:
        return {
            "status": "HOLD_P225_NO_FILES",
            "admissible_for_ingest": False,
            "root_authority_mutated": False,
        }

    try:
        ingested = pack.AuthenticatedPackIngestAdapter().ingest(
            expected_resource_id=EXPECTED_RESOURCE_ID,
            receipt=receipt,
            files=files,
            metadata=metadata or {},
        )
    except ValueError as exc:
        return {
            "status": "HOLD_P225_INVALID_INPUT",
            "reason": str(exc),
            "admissible_for_ingest": False,
            "root_authority_mutated": False,
        }

    observed_ids = [f.filename for f in files]
    inventory = pack.inventory_state(
        observed_ids,
        authoritative_expected_ids,
        authoritative_completeness_evidence,
    )

    if inventory["authoritatively_complete"]:
        status = "P225_INPUT_ADMISSIBLE_COMPLETE_BY_AUTHORITY_GATE"
    elif inventory["status"] == "INVENTORY_INCOMPLETE":
        status = "P225_INPUT_ADMISSIBLE_PARTIAL_INVENTORY"
    else:
        status = "P225_INPUT_ADMISSIBLE_COMPLETENESS_UNPROVEN"

    return {
        "status": status,
        "admissible_for_ingest": True,
        "resource_id": ingested["resource_id"],
        "manifest_hash": ingested["manifest_hash"],
        "file_count": len(ingested["files"]),
        "inventory": inventory,
        "root_authority_mutated": False,
        "next_authority_action": "PERSIST_SOURCE_AND_READBACK_BEFORE_ROOT_RECONCILIATION",
    }


def validate_p235_input(designation) -> Dict[str, Any]:
    """Validate a real case-specific bidder designation candidate.

    This is stricter than the generic BidderDesignationV2 primitive: it binds the
    exact target, legal entity and internal-only scope. It never converts a test
    fixture into bidder authority.
    """
    generic = bidder.designation_v2_state(designation)
    if not generic.get("explicit"):
        return {
            "status": generic["status"],
            "admissible_for_authority_review": False,
            "root_authority_mutated": False,
        }

    if designation.resource_id != EXPECTED_RESOURCE_ID:
        return {
            "status": "HOLD_P235_RESOURCE_MISMATCH",
            "admissible_for_authority_review": False,
            "root_authority_mutated": False,
        }
    if designation.legal_entity != EXPECTED_LEGAL_ENTITY:
        return {
            "status": "HOLD_P235_LEGAL_ENTITY_MISMATCH",
            "admissible_for_authority_review": False,
            "root_authority_mutated": False,
        }
    if designation.scope != INTERNAL_EVALUATION_SCOPE:
        return {
            "status": "HOLD_P235_SCOPE_NOT_INTERNAL_ONLY",
            "admissible_for_authority_review": False,
            "root_authority_mutated": False,
        }

    return {
        "status": "P235_INPUT_ADMISSIBLE_FOR_AUTHORITY_REVIEW",
        "admissible_for_authority_review": True,
        "resource_id": designation.resource_id,
        "legal_entity": designation.legal_entity,
        "authorized_designator": designation.authorized_designator,
        "designated_at": designation.designated_at,
        "scope": designation.scope,
        "root_authority_mutated": False,
        "next_authority_action": "PERSIST_DECLARATION_AND_READBACK_BEFORE_ROOT_RECONCILIATION",
    }


def unlock_readiness(*, p225_result: Optional[Dict[str, Any]] = None, p235_result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    p225_ready = bool(p225_result and p225_result.get("admissible_for_ingest"))
    p235_ready = bool(p235_result and p235_result.get("admissible_for_authority_review"))
    return {
        "target_case": f"PROC-BALLYBUNION-{EXPECTED_RESOURCE_ID}",
        "p225_candidate_ready": p225_ready,
        "p235_candidate_ready": p235_ready,
        "both_candidate_inputs_ready": p225_ready and p235_ready,
        "authority_mutation": False,
        "proof_promotion": False,
        "external_action_authorized": False,
        "rule": "VALIDATED_INPUT_NEQ_AUTHORITY_UNTIL_PERSISTENCE_READBACK_AND_CORE_RECONCILIATION",
    }
