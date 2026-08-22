from __future__ import annotations

from typing import Any, Mapping

from core.artifact_placement import ArtifactPlacementReceipt, PLACEMENT_VERIFIED
from projects.manager import ProjectStateManager


def complete_task_with_artifact_gate(
    manager: ProjectStateManager,
    project_id: str,
    task_id: str,
    receipt: ArtifactPlacementReceipt | Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Complete an artifact-producing task only after placement/discoverability proof.

    This is the required completion path for tasks whose result lives in Drive,
    GitHub, or another external persistence surface. It deliberately does not
    change legacy ProjectStateManager.complete_task semantics; callers opt into
    the stronger gate when an external artifact is part of the definition of done.
    """
    if receipt is None:
        return manager._set_task_status(
            project_id,
            task_id,
            "BLOCKED",
            "artifact placement receipt required before DONE",
        )

    normalized = (
        receipt
        if isinstance(receipt, ArtifactPlacementReceipt)
        else ArtifactPlacementReceipt.from_mapping(receipt)
    )
    receipt_dict = normalized.to_dict()

    if normalized.status != PLACEMENT_VERIFIED:
        task = manager._set_task_status(
            project_id,
            task_id,
            "BLOCKED",
            "artifact placement gate failed: " + ", ".join(normalized.failures()),
        )
    else:
        task = manager._set_task_status(project_id, task_id, "DONE")

    # Persist the receipt on the task so readback can prove why DONE/BLOCKED was emitted.
    paths = manager.paths(project_id)
    tasks = __import__("json").loads(paths.tasks_json.read_text(encoding="utf-8"))
    for stored in tasks:
        if stored.get("id") == task_id:
            stored["artifact_placement_receipt"] = receipt_dict
            stored["completion_gate"] = "ARTIFACT_PLACEMENT"
            task = stored
            break
    tmp = paths.tasks_json.with_suffix(paths.tasks_json.suffix + ".tmp")
    tmp.write_text(__import__("json").dumps(tasks, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(paths.tasks_json)
    return task
