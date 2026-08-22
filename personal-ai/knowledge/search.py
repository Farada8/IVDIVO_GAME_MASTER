from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from memory.store import MemoryStore
from projects.manager import ProjectStateManager

SEARCH_MODE = "LITERAL_CASE_INSENSITIVE_SUBSTRING"
MAX_MEMORY_SCAN = 500


class KnowledgeSearchError(ValueError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _clean_text(value: Any, field: str) -> str:
    text = str(value).strip() if value is not None else ""
    if not text:
        raise KnowledgeSearchError(f"{field} cannot be empty")
    return text


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _contains(text: str, query: str) -> bool:
    return query.casefold() in text.casefold()


def _snippet(text: str, query: str, limit: int = 600) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    lower = compact.casefold()
    needle = query.casefold()
    position = lower.find(needle)
    if position < 0:
        return compact[: limit - 1] + "…"
    radius = max(40, (limit - len(query)) // 2)
    start = max(0, position - radius)
    end = min(len(compact), position + len(query) + radius)
    value = compact[start:end]
    if start > 0:
        value = "…" + value
    if end < len(compact):
        value += "…"
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


class PersonalKnowledgeSearch:
    """PL-14 bounded project-local literal retrieval with explicit source separation."""

    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")

    def ask(self, project_id: str, query: str, *, limit: int = 50) -> dict[str, Any]:
        project_id = _clean_text(project_id, "project_id")
        query = _clean_text(query, "query")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 200:
            raise KnowledgeSearchError("limit must be an integer between 1 and 200")

        project = self.projects.load_project(project_id)
        paths = self.projects.paths(project_id)

        groups: dict[str, list[dict[str, Any]]] = {
            "project_state": [],
            "documents": [],
            "decisions": [],
            "memory": [],
        }

        self._search_project_state(project_id, project, query, groups["project_state"])
        self._search_decision_log(project_id, paths.decisions_md, query, groups["decisions"])
        self._search_memory(project_id, query, groups)

        remaining = limit
        limited: dict[str, list[dict[str, Any]]] = {}
        for name in ("project_state", "documents", "decisions", "memory"):
            selected = groups[name][:remaining]
            limited[name] = selected
            remaining -= len(selected)
            if remaining <= 0:
                for rest in ("project_state", "documents", "decisions", "memory"):
                    limited.setdefault(rest, [])
                break

        hit_count = sum(len(items) for items in limited.values())
        result: dict[str, Any] = {
            "schema": "ivdivo.personal_ai.knowledge_search/0.1",
            "search_id": f"ask-{uuid.uuid4().hex}",
            "project_id": project_id,
            "query": query,
            "search_mode": SEARCH_MODE,
            "semantic_search": False,
            "embeddings_used": False,
            "source_separation_enforced": True,
            "invalidated_memory_excluded": True,
            "cross_project_search": False,
            "status": "HIT" if hit_count else "NO_HIT",
            "answer_status": "EVIDENCE_FOUND" if hit_count else "UNKNOWN",
            "hit_count": hit_count,
            "groups": limited,
            "created_at": _utc_now(),
            "evidence_boundary": (
                "Retrieval is literal project-local evidence lookup, not truth verification or semantic understanding. "
                "NO_HIT remains UNKNOWN and is never converted into a fabricated answer."
            ),
        }
        artifact_path = (
            Path(project["root"])
            / "artifacts"
            / "knowledge-search"
            / f"{result['search_id']}.json"
        )
        result["artifact_path"] = str(artifact_path)
        _write_json(artifact_path, result)
        return result

    def _search_project_state(
        self,
        project_id: str,
        project: dict[str, Any],
        query: str,
        output: list[dict[str, Any]],
    ) -> None:
        state_text = _canonical_json(project["state"])
        if _contains(state_text, query):
            output.append(
                {
                    "source_group": "project_state",
                    "source_type": "PROJECT_STATE",
                    "project_id": project_id,
                    "record_id": "state.json",
                    "path": "state.json",
                    "status": "ACTIVE",
                    "snippet": _snippet(state_text, query),
                }
            )
        for task in project.get("tasks", []):
            task_text = _canonical_json(task)
            if _contains(task_text, query):
                output.append(
                    {
                        "source_group": "project_state",
                        "source_type": "PROJECT_TASK",
                        "project_id": project_id,
                        "record_id": str(task.get("id") or "unknown-task"),
                        "path": "tasks.json",
                        "status": str(task.get("status") or "UNKNOWN"),
                        "snippet": _snippet(task_text, query),
                    }
                )

    def _search_decision_log(
        self,
        project_id: str,
        path: Path,
        query: str,
        output: list[dict[str, Any]],
    ) -> None:
        text = path.read_text(encoding="utf-8")
        sections = text.split("\n## ")
        for index, section in enumerate(sections):
            if index == 0:
                continue
            normalized = "## " + section
            if not _contains(normalized, query):
                continue
            heading = section.splitlines()[0].strip() if section.splitlines() else "decision"
            output.append(
                {
                    "source_group": "decisions",
                    "source_type": "PROJECT_DECISION_LOG",
                    "project_id": project_id,
                    "record_id": f"decision-log-{index:04d}",
                    "path": "decisions.md",
                    "decision_timestamp": heading,
                    "status": "ACTIVE",
                    "snippet": _snippet(normalized, query),
                }
            )

    def _search_memory(
        self,
        project_id: str,
        query: str,
        groups: dict[str, list[dict[str, Any]]],
    ) -> None:
        records = self.memory.search(
            query,
            project_id=project_id,
            include_invalid=False,
            limit=MAX_MEMORY_SCAN,
        )
        for record in records:
            kind = str(record.get("kind") or "UNKNOWN").upper()
            metadata = record.get("metadata") or {}
            claim_type = str(metadata.get("claim_type") or "").upper()

            if kind in {"DOCUMENT", "SOURCE"}:
                group = "documents"
                source_type = "MEMORY_DOCUMENT" if kind == "DOCUMENT" else "MEMORY_SOURCE"
            elif kind == "DECISION" or (kind == "CLAIM" and claim_type == "USER_DECISION"):
                group = "decisions"
                source_type = "MEMORY_DECISION" if kind == "DECISION" else "USER_DECISION_CLAIM"
            else:
                group = "memory"
                source_type = "GENERIC_MEMORY"

            groups[group].append(
                {
                    "source_group": group,
                    "source_type": source_type,
                    "project_id": project_id,
                    "record_id": record["id"],
                    "kind": kind,
                    "status": record["status"],
                    "source": record.get("source"),
                    "source_id": record.get("source_id"),
                    "content_hash": record.get("content_hash"),
                    "confidence": record.get("confidence"),
                    "updated_at": record.get("updated_at"),
                    "snippet": _snippet(record["content"], query),
                    "metadata": metadata,
                }
            )
