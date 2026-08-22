from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_STATUSES = {"NEW", "READY", "RUNNING", "BLOCKED", "DONE", "FAILED", "ARCHIVED"}
TASK_STATUSES = {"NEW", "READY", "RUNNING", "BLOCKED", "DONE", "FAILED", "ARCHIVED"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_project_id(value: str) -> str:
    value = value.strip()
    if not value or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", value):
        raise ValueError("project id must be 1-128 safe characters: letters, digits, dot, underscore or dash")
    return value


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


@dataclass(frozen=True)
class ProjectPaths:
    root: Path

    @property
    def project_yaml(self) -> Path:
        return self.root / "project.yaml"

    @property
    def state_json(self) -> Path:
        return self.root / "state.json"

    @property
    def tasks_json(self) -> Path:
        return self.root / "tasks.json"

    @property
    def decisions_md(self) -> Path:
        return self.root / "decisions.md"


class ProjectStateManager:
    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.projects_root = self.home / "projects"
        self.projects_root.mkdir(parents=True, exist_ok=True)

    def paths(self, project_id: str) -> ProjectPaths:
        project_id = _safe_project_id(project_id)
        return ProjectPaths(self.projects_root / project_id)

    def create_project(self, project_id: str, name: str | None = None) -> dict[str, Any]:
        project_id = _safe_project_id(project_id)
        paths = self.paths(project_id)
        if paths.root.exists():
            raise FileExistsError(f"project already exists: {project_id}")

        now = _utc_now()
        paths.root.mkdir(parents=True)
        for child in ("artifacts", "references", "logs"):
            (paths.root / child).mkdir()

        display_name = (name or project_id).strip() or project_id
        paths.project_yaml.write_text(
            "schema: ivdivo.personal_ai.project/0.1\n"
            f"id: {project_id}\n"
            f"name: {json.dumps(display_name)}\n"
            f"created_at: {now}\n",
            encoding="utf-8",
        )
        state = {
            "project_id": project_id,
            "status": "NEW",
            "created_at": now,
            "updated_at": now,
            "version": 1,
        }
        _write_json(paths.state_json, state)
        _write_json(paths.tasks_json, [])
        paths.decisions_md.write_text(f"# Decisions — {display_name}\n\n", encoding="utf-8")
        return self.load_project(project_id)

    def load_project(self, project_id: str) -> dict[str, Any]:
        paths = self.paths(project_id)
        if not paths.root.is_dir():
            raise FileNotFoundError(f"project not found: {project_id}")
        required = [paths.project_yaml, paths.state_json, paths.tasks_json, paths.decisions_md]
        missing = [str(p.name) for p in required if not p.exists()]
        if missing:
            raise RuntimeError(f"project structure incomplete: {missing}")
        return {
            "project_id": _safe_project_id(project_id),
            "root": str(paths.root),
            "state": _read_json(paths.state_json),
            "tasks": _read_json(paths.tasks_json),
            "required_structure_present": all(
                (paths.root / child).exists()
                for child in ("artifacts", "references", "logs")
            ),
        }

    def update_state(self, project_id: str, status: str, **fields: Any) -> dict[str, Any]:
        if status not in PROJECT_STATUSES:
            raise ValueError(f"invalid project status: {status}")
        paths = self.paths(project_id)
        state = _read_json(paths.state_json)
        state.update(fields)
        state["status"] = status
        state["updated_at"] = _utc_now()
        state["version"] = int(state.get("version", 0)) + 1
        _write_json(paths.state_json, state)
        return state

    def add_task(
        self,
        project_id: str,
        title: str,
        task_id: str | None = None,
        *,
        requires_artifact_placement_receipt: bool = False,
    ) -> dict[str, Any]:
        paths = self.paths(project_id)
        tasks = _read_json(paths.tasks_json)
        if not isinstance(tasks, list):
            raise RuntimeError("tasks.json must contain a list")
        task_id = task_id or f"task-{len(tasks) + 1:04d}"
        if any(t.get("id") == task_id for t in tasks):
            raise ValueError(f"duplicate task id: {task_id}")
        now = _utc_now()
        task = {
            "id": task_id,
            "title": title.strip(),
            "status": "READY",
            "created_at": now,
            "updated_at": now,
            "block_reason": None,
            "requires_artifact_placement_receipt": bool(requires_artifact_placement_receipt),
        }
        if not task["title"]:
            raise ValueError("task title cannot be empty")
        tasks.append(task)
        _write_json(paths.tasks_json, tasks)
        return task

    def _task_by_id(self, project_id: str, task_id: str) -> dict[str, Any]:
        tasks = self.load_project(project_id)["tasks"]
        for task in tasks:
            if task.get("id") == task_id:
                return task
        raise KeyError(f"task not found: {task_id}")

    def _set_task_status(self, project_id: str, task_id: str, status: str, block_reason: str | None = None) -> dict[str, Any]:
        if status not in TASK_STATUSES:
            raise ValueError(f"invalid task status: {status}")
        paths = self.paths(project_id)
        tasks = _read_json(paths.tasks_json)
        for task in tasks:
            if task.get("id") == task_id:
                task["status"] = status
                task["updated_at"] = _utc_now()
                task["block_reason"] = block_reason
                _write_json(paths.tasks_json, tasks)
                return task
        raise KeyError(f"task not found: {task_id}")

    def start_task(self, project_id: str, task_id: str) -> dict[str, Any]:
        return self._set_task_status(project_id, task_id, "RUNNING")

    def complete_task(self, project_id: str, task_id: str) -> dict[str, Any]:
        task = self._task_by_id(project_id, task_id)
        if bool(task.get("requires_artifact_placement_receipt", False)):
            raise RuntimeError(
                "artifact-producing task cannot use direct complete_task; "
                "route completion through complete_task_with_artifact_gate"
            )
        return self._set_task_status(project_id, task_id, "DONE")

    def fail_task(self, project_id: str, task_id: str, reason: str) -> dict[str, Any]:
        if not reason.strip():
            raise ValueError("failure reason cannot be empty")
        return self._set_task_status(project_id, task_id, "FAILED", reason.strip())

    def block_task(self, project_id: str, task_id: str, reason: str) -> dict[str, Any]:
        if not reason.strip():
            raise ValueError("block reason cannot be empty")
        return self._set_task_status(project_id, task_id, "BLOCKED", reason.strip())

    def record_decision(self, project_id: str, decision: str) -> str:
        if not decision.strip():
            raise ValueError("decision cannot be empty")
        paths = self.paths(project_id)
        timestamp = _utc_now()
        with paths.decisions_md.open("a", encoding="utf-8") as fh:
            fh.write(f"## {timestamp}\n\n{decision.strip()}\n\n")
        return timestamp

    def get_next_task(self, project_id: str) -> dict[str, Any] | None:
        tasks = self.load_project(project_id)["tasks"]
        for preferred in ("READY", "NEW"):
            for task in tasks:
                if task.get("status") == preferred:
                    return task
        return None
