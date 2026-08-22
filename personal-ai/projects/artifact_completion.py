from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Mapping

from core.artifact_placement import ArtifactPlacementReceipt, PLACEMENT_VERIFIED
from projects.manager import ProjectStateManager


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _persist_gate_result(
    manager: ProjectStateManager,
    project_id: str,
    task_id: str,
    *,
    status: str,
    block_reason: str | None,
    receipt_dict: dict[str, Any] | None,
) -> dict[str, Any]:
    """Persist task status and artifact-placement evidence in one atomic replace.

    A task must never be durably visible as DONE before its placement receipt is
    durably present. The previous two-write sequence could leave DONE without a
    receipt if the process stopped between writes.
    """
    paths = manager.paths(project_id)
    tasks = json.loads(paths.tasks_json.read_text(encoding="utf-8"))
    if not isinstance(tasks, list):
        raise RuntimeError("tasks.json must contain a list")

    task: dict[str, Any] | None = None
    for stored in tasks:
        if stored.get("id") == task_id:
            stored["status"] = status
            stored["updated_at"] = _utc_now()
            stored["block_reason"] = block_reason
            stored["completion_gate"] = "ARTIFACT_PLACEMENT"
            if receipt_dict is None:
                stored.pop("artifact_placement_receipt", None)
            else:
                stored["artifact_placement_receipt"] = receipt_dict
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
        return _persist_gate_result(
            manager,
            project_id,
            task_id,
            status="BLOCKED",
            block_reason="artifact placement gate failed: " + ", ".join(normalized.failures()),
            receipt_dict=receipt_dict,
        )

    return _persist_gate_result(
        manager,
        project_id,
        task_id,
        status="DONE",
        block_reason=None,
        receipt_dict=receipt_dict,
    )
