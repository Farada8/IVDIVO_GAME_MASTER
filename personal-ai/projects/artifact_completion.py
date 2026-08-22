from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Mapping

from core.artifact_placement import ArtifactPlacementReceipt, PLACEMENT_VERIFIED
from projects.manager import ProjectStateManager


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _interception_candidate(receipt_dict: Mapping[str, Any], captured_at: str) -> dict[str, Any]:
    """Build durable evidence that the gate blocked an attempted DONE transition.

    This is deliberately a candidate, not promotion proof. Runtime state alone
    cannot prove that a receipt came from real provider traffic rather than a
    fixture or replay. Provider-origin confirmation remains an external gate.
    """
    return {
        "schema": "ivdivo.artifact_placement.interception_candidate/1.0",
        "captured_at": captured_at,
        "attempted_transition": "DONE",
        "caught_before_done": True,
        "receipt_status": receipt_dict.get("status"),
        "failures": list(receipt_dict.get("failures") or []),
        "provider": receipt_dict.get("provider"),
        "artifact_id": receipt_dict.get("artifact_id"),
        "expected_parent": receipt_dict.get("expected_parent"),
        "actual_parent": receipt_dict.get("actual_parent"),
        "expected_resource_type": receipt_dict.get("expected_resource_type"),
        "observed_resource_type": receipt_dict.get("observed_resource_type"),
        "provider_confirmation_required": True,
        "promotion_proof": False,
        "promotion_review_state": "UNVERIFIED_PROVIDER_ORIGIN",
    }


def _persist_gate_result(
    manager: ProjectStateManager,
    project_id: str,
    task_id: str,
    *,
    status: str,
    block_reason: str | None,
    receipt_dict: dict[str, Any] | None,
    interception_event: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Persist task status and artifact-placement evidence in one atomic replace.

    A task must never be durably visible as DONE before its placement receipt is
    durably present. Interception evidence is part of the same atomic write so a
    later dialog can prove the guard blocked DONE without relying on chat memory.
    """
    paths = manager.paths(project_id)
    tasks = json.loads(paths.tasks_json.read_text(encoding="utf-8"))
    if not isinstance(tasks, list):
        raise RuntimeError("tasks.json must contain a list")

    task: dict[str, Any] | None = None
    for stored in tasks:
        if stored.get("id") == task_id:
            captured_at = _utc_now()
            stored["status"] = status
            stored["updated_at"] = captured_at
            stored["block_reason"] = block_reason
            stored["completion_gate"] = "ARTIFACT_PLACEMENT"
            if receipt_dict is None:
                stored.pop("artifact_placement_receipt", None)
            else:
                stored["artifact_placement_receipt"] = receipt_dict
            if interception_event is not None:
                history = stored.get("artifact_placement_interceptions")
                if history is None:
                    history = []
                    stored["artifact_placement_interceptions"] = history
                if not isinstance(history, list):
                    raise RuntimeError("artifact_placement_interceptions must contain a list")
                history.append(interception_event)
            task = stored
            break
    if task is None:
        raise KeyError(f"task not found: {task_id}")

    tmp = paths.tasks_json.with_suffix(paths.tasks_json.suffix + ".tmp")
    tmp.write_text(json.dumps(tasks, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(paths.tasks_json)
    return task


def complete_task_with_artifact_gate(
    manager: ProjectStateManager,
    project_id: str,
    task_id: str,
    receipt: ArtifactPlacementReceipt | Mapping[str, Any] | None,
) -> dict[str, Any]:
    if receipt is None:
        return _persist_gate_result(
            manager,
            project_id,
            task_id,
            status="BLOCKED",
            block_reason="artifact placement receipt required before DONE",
            receipt_dict=None,
        )

    normalized = receipt if isinstance(receipt, ArtifactPlacementReceipt) else ArtifactPlacementReceipt.from_mapping(receipt)
    receipt_dict = normalized.to_dict()

    if normalized.status != PLACEMENT_VERIFIED:
        captured_at = _utc_now()
        interception = _interception_candidate(receipt_dict, captured_at)
        return _persist_gate_result(
            manager,
            project_id,
            task_id,
            status="BLOCKED",
            block_reason="artifact placement gate failed: " + ", ".join(normalized.failures()),
            receipt_dict=receipt_dict,
            interception_event=interception,
        )

    return _persist_gate_result(
        manager,
        project_id,
        task_id,
        status="DONE",
        block_reason=None,
        receipt_dict=receipt_dict,
    )
