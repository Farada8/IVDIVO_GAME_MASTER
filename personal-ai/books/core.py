from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from memory.store import MemoryStore
from projects.manager import ProjectStateManager

BOOK_STATES = {"DRAFT", "CONTINUITY_REVIEW", "READY_FOR_FINAL", "FINAL"}
GATE_STATES = {"NOT_RUN", "PASS", "FAIL"}
_SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_id(value: str, field: str) -> str:
    clean = value.strip()
    if not _SAFE_ID.fullmatch(clean):
        raise ValueError(f"{field} must be 1-128 safe characters: letters, digits, dot, underscore or dash")
    return clean


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


class BookProductionCore:
    """Persisted book state machine. PL-09 may later supply continuity results."""

    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")

    def _root(self, project_id: str, book_id: str) -> Path:
        project = self.projects.load_project(project_id)
        return Path(project["root"]) / "artifacts" / "books" / _safe_id(book_id, "book_id")

    def _state_path(self, project_id: str, book_id: str) -> Path:
        return self._root(project_id, book_id) / "state.json"

    def _load(self, project_id: str, book_id: str) -> dict[str, Any]:
        path = self._state_path(project_id, book_id)
        if not path.is_file():
            raise FileNotFoundError(f"book not found: {book_id}")
        state = json.loads(path.read_text(encoding="utf-8"))
        if state.get("state") not in BOOK_STATES:
            raise RuntimeError("book state file has invalid state")
        return state

    def _save(self, project_id: str, book_id: str, state: dict[str, Any]) -> dict[str, Any]:
        state["updated_at"] = _utc_now()
        state["version"] = int(state.get("version", 0)) + 1
        _write_json(self._state_path(project_id, book_id), state)
        return state

    def create_book(self, project_id: str, book_id: str, title: str) -> dict[str, Any]:
        book_id = _safe_id(book_id, "book_id")
        title = title.strip()
        if not title:
            raise ValueError("title cannot be empty")
        root = self._root(project_id, book_id)
        if root.exists():
            raise FileExistsError(f"book already exists: {book_id}")
        root.mkdir(parents=True)
        now = _utc_now()
        state = {
            "schema": "ivdivo.personal_ai.book_state/0.1",
            "project_id": project_id,
            "book_id": book_id,
            "title": title,
            "state": "DRAFT",
            "version": 1,
            "created_at": now,
            "updated_at": now,
            "manuscript": {
                "path": str(root / "manuscript.md"),
                "sha256": None,
                "updated_at": None,
            },
            "continuity_gate": {
                "status": "NOT_RUN",
                "manuscript_sha256": None,
                "source": None,
                "findings": [],
                "checked_at": None,
                "attempt": 0,
            },
            "final": {"path": None, "sha256": None, "output_memory_id": None, "finalized_at": None},
        }
        _write_json(root / "state.json", state)
        return state

    def status(self, project_id: str, book_id: str) -> dict[str, Any]:
        return self._load(project_id, book_id)

    def update_manuscript(self, project_id: str, book_id: str, text: str) -> dict[str, Any]:
        state = self._load(project_id, book_id)
        if state["state"] == "FINAL":
            raise RuntimeError("FINAL manuscript is immutable")
        if not text.strip():
            raise ValueError("manuscript cannot be empty")
        path = Path(state["manuscript"]["path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        digest = _sha256_text(text)
        state["manuscript"] = {"path": str(path), "sha256": digest, "updated_at": _utc_now()}
        # Any manuscript change invalidates a previous continuity result.
        state["continuity_gate"] = {
            "status": "NOT_RUN",
            "manuscript_sha256": None,
            "source": None,
            "findings": [],
            "checked_at": None,
            "attempt": int(state.get("continuity_gate", {}).get("attempt", 0)),
        }
        state["state"] = "DRAFT"
        return self._save(project_id, book_id, state)

    def submit_for_continuity(self, project_id: str, book_id: str) -> dict[str, Any]:
        state = self._load(project_id, book_id)
        if state["state"] == "FINAL":
            raise RuntimeError("FINAL book cannot re-enter continuity review")
        manuscript_path = Path(state["manuscript"]["path"])
        if not state["manuscript"]["sha256"] or not manuscript_path.is_file():
            raise RuntimeError("manuscript is required before continuity review")
        actual = _sha256_text(manuscript_path.read_text(encoding="utf-8"))
        if actual != state["manuscript"]["sha256"]:
            raise RuntimeError("manuscript hash mismatch; update manuscript through BookProductionCore")
        state["state"] = "CONTINUITY_REVIEW"
        state["continuity_gate"]["status"] = "NOT_RUN"
        state["continuity_gate"]["manuscript_sha256"] = actual
        return self._save(project_id, book_id, state)

    def record_continuity_result(
        self,
        project_id: str,
        book_id: str,
        *,
        passed: bool,
        source: str,
        findings: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        state = self._load(project_id, book_id)
        if state["state"] != "CONTINUITY_REVIEW":
            raise RuntimeError("continuity result can only be recorded in CONTINUITY_REVIEW")
        source = source.strip()
        if not source:
            raise ValueError("continuity source cannot be empty")
        findings = list(findings or [])
        if not passed and not findings:
            raise ValueError("failed continuity result requires at least one finding")
        if any(not isinstance(item, dict) for item in findings):
            raise ValueError("continuity findings must be JSON objects")
        manuscript_path = Path(state["manuscript"]["path"])
        actual = _sha256_text(manuscript_path.read_text(encoding="utf-8"))
        expected = state["manuscript"]["sha256"]
        if actual != expected:
            raise RuntimeError("manuscript changed during continuity review")
        attempt = int(state["continuity_gate"].get("attempt", 0)) + 1
        state["continuity_gate"] = {
            "status": "PASS" if passed else "FAIL",
            "manuscript_sha256": actual,
            "source": source,
            "findings": findings,
            "checked_at": _utc_now(),
            "attempt": attempt,
        }
        state["state"] = "READY_FOR_FINAL" if passed else "CONTINUITY_REVIEW"
        return self._save(project_id, book_id, state)

    def finalize(self, project_id: str, book_id: str) -> dict[str, Any]:
        state = self._load(project_id, book_id)
        if state["state"] != "READY_FOR_FINAL":
            raise RuntimeError("FINAL is blocked until continuity gate passes")
        gate = state["continuity_gate"]
        if gate.get("status") != "PASS":
            raise RuntimeError("FINAL is blocked until continuity gate passes")
        manuscript_path = Path(state["manuscript"]["path"])
        text = manuscript_path.read_text(encoding="utf-8")
        actual = _sha256_text(text)
        if actual != state["manuscript"]["sha256"] or actual != gate.get("manuscript_sha256"):
            raise RuntimeError("continuity PASS does not match current manuscript")

        final_path = self._root(project_id, book_id) / "final.md"
        shutil.copyfile(manuscript_path, final_path)
        memory = self.memory.store(
            text,
            kind="OUTPUT",
            source="PL-08 Book Production Core FINAL",
            project_id=project_id,
            metadata={
                "book_id": book_id,
                "title": state["title"],
                "state": "FINAL",
                "manuscript_sha256": actual,
                "continuity_source": gate["source"],
                "continuity_attempt": gate["attempt"],
                "final_path": str(final_path),
            },
        )
        state["state"] = "FINAL"
        state["final"] = {
            "path": str(final_path),
            "sha256": actual,
            "output_memory_id": memory["id"],
            "finalized_at": _utc_now(),
        }
        return self._save(project_id, book_id, state)
