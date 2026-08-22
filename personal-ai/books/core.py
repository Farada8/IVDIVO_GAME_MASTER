from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from projects.manager import ProjectStateManager

BOOK_STAGES = (
    "IDEA",
    "CANON",
    "STORY_BIBLE",
    "OUTLINE",
    "CHAPTER_PLAN",
    "DRAFT",
    "CRITIQUE",
    "REWRITE",
    "CONTINUITY",
    "FINAL",
)

_REQUIRED_FILES = (
    "book.yaml",
    "state.json",
    "canon.md",
    "characters.json",
    "locations.json",
    "timeline.json",
    "plot.json",
)

_REQUIRED_DIRS = (
    "chapters",
    "drafts",
    "critique",
    "continuity",
    "final",
)


class BookProductionError(RuntimeError):
    pass


class ContinuityGateError(BookProductionError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_title(value: str | None, project_id: str) -> str:
    title = (value or project_id).strip()
    if not title:
        raise ValueError("book title cannot be empty")
    if "\n" in title or "\r" in title:
        raise ValueError("book title must be a single line")
    return title


class BookProductionCore:
    """Persisted PL-08 book state machine with a fail-closed FINAL gate."""

    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)

    def _book_root(self, project_id: str) -> Path:
        project = self.projects.load_project(project_id)
        return Path(project["root"]) / "book"

    def initialize(self, project_id: str, title: str | None = None) -> dict[str, Any]:
        project = self.projects.load_project(project_id)
        root = Path(project["root"]) / "book"
        if root.exists():
            raise FileExistsError(f"book core already exists for project: {project_id}")

        root.mkdir(parents=True)
        now = _utc_now()
        display_title = _safe_title(title, project_id)

        (root / "book.yaml").write_text(
            "schema: ivdivo.personal_ai.book/0.1\n"
            f"project_id: {project_id}\n"
            f"title: {json.dumps(display_title)}\n"
            f"created_at: {now}\n",
            encoding="utf-8",
        )
        (root / "canon.md").write_text(f"# Canon — {display_title}\n\n", encoding="utf-8")
        _write_json(root / "characters.json", [])
        _write_json(root / "locations.json", [])
        _write_json(root / "timeline.json", [])
        _write_json(root / "plot.json", {})
        for dirname in _REQUIRED_DIRS:
            (root / dirname).mkdir()

        state = {
            "schema": "ivdivo.personal_ai.book_state/0.1",
            "project_id": project_id,
            "title": display_title,
            "stage": "IDEA",
            "created_at": now,
            "updated_at": now,
            "version": 1,
            "continuity_gate": {
                "status": "NOT_RUN",
                "evidence": None,
                "updated_at": None,
            },
            "history": [
                {
                    "from": None,
                    "to": "IDEA",
                    "at": now,
                    "reason": "BOOK_CORE_INITIALIZED",
                }
            ],
        }
        _write_json(root / "state.json", state)
        self.projects.update_state(
            project_id,
            "READY",
            domain="BOOK",
            book_stage="IDEA",
            continuity_gate_status="NOT_RUN",
        )
        return self.load(project_id)

    def load(self, project_id: str) -> dict[str, Any]:
        root = self._book_root(project_id)
        if not root.is_dir():
            raise FileNotFoundError(f"book core not found for project: {project_id}")

        missing_files = [name for name in _REQUIRED_FILES if not (root / name).is_file()]
        missing_dirs = [name for name in _REQUIRED_DIRS if not (root / name).is_dir()]
        if missing_files or missing_dirs:
            raise BookProductionError(
                f"book structure incomplete: files={missing_files}, dirs={missing_dirs}"
            )

        state = _read_json(root / "state.json")
        if state.get("stage") not in BOOK_STAGES:
            raise BookProductionError(f"invalid persisted book stage: {state.get('stage')}")
        gate = state.get("continuity_gate")
        if not isinstance(gate, dict) or gate.get("status") not in {"NOT_RUN", "PASS", "FAIL"}:
            raise BookProductionError("invalid persisted continuity gate")

        return {
            "project_id": project_id,
            "root": str(root),
            "state": state,
            "required_structure_present": True,
            "next_stage": self.next_stage(state["stage"]),
        }

    @staticmethod
    def next_stage(stage: str) -> str | None:
        if stage not in BOOK_STAGES:
            raise ValueError(f"invalid book stage: {stage}")
        index = BOOK_STAGES.index(stage)
        if index == len(BOOK_STAGES) - 1:
            return None
        return BOOK_STAGES[index + 1]

    def advance(self, project_id: str, to_stage: str | None = None) -> dict[str, Any]:
        loaded = self.load(project_id)
        root = Path(loaded["root"])
        state = loaded["state"]
        current = state["stage"]
        expected = self.next_stage(current)
        if expected is None:
            raise BookProductionError("book is already FINAL")

        target = (to_stage or expected).strip().upper()
        if target not in BOOK_STAGES:
            raise ValueError(f"invalid target stage: {target}")
        if target != expected:
            raise BookProductionError(
                f"stage skipping is forbidden: current={current}, expected={expected}, requested={target}"
            )
        if target == "FINAL" and state["continuity_gate"]["status"] != "PASS":
            raise ContinuityGateError(
                "FINAL is blocked until continuity_gate.status == PASS"
            )

        now = _utc_now()
        state["stage"] = target
        state["updated_at"] = now
        state["version"] = int(state.get("version", 0)) + 1
        state.setdefault("history", []).append(
            {
                "from": current,
                "to": target,
                "at": now,
                "reason": "STAGE_ADVANCE",
            }
        )
        _write_json(root / "state.json", state)

        project_status = "DONE" if target == "FINAL" else "RUNNING"
        self.projects.update_state(
            project_id,
            project_status,
            domain="BOOK",
            book_stage=target,
            continuity_gate_status=state["continuity_gate"]["status"],
        )
        return self.load(project_id)

    def set_continuity_gate(
        self,
        project_id: str,
        *,
        passed: bool,
        evidence: str,
    ) -> dict[str, Any]:
        loaded = self.load(project_id)
        root = Path(loaded["root"])
        state = loaded["state"]
        if state["stage"] != "CONTINUITY":
            raise ContinuityGateError(
                "continuity gate can only be recorded while stage == CONTINUITY"
            )
        clean_evidence = evidence.strip()
        if not clean_evidence:
            raise ValueError("continuity evidence cannot be empty")

        now = _utc_now()
        status = "PASS" if passed else "FAIL"
        state["continuity_gate"] = {
            "status": status,
            "evidence": clean_evidence,
            "updated_at": now,
        }
        state["updated_at"] = now
        state["version"] = int(state.get("version", 0)) + 1
        state.setdefault("history", []).append(
            {
                "from": "CONTINUITY",
                "to": "CONTINUITY",
                "at": now,
                "reason": f"CONTINUITY_GATE_{status}",
            }
        )
        _write_json(root / "state.json", state)

        self.projects.update_state(
            project_id,
            "RUNNING" if passed else "BLOCKED",
            domain="BOOK",
            book_stage="CONTINUITY",
            continuity_gate_status=status,
        )
        return self.load(project_id)
