from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from memory.store import MemoryStore
from projects.manager import ProjectStateManager


class KnowledgeSearchError(ValueError):
    pass


_STOPWORDS = {
    "a", "an", "and", "about", "already", "did", "do", "done", "for", "have", "on", "the", "we", "what", "with",
    "и", "о", "об", "по", "про", "с", "для", "на", "мы", "что", "уже", "делали", "сделано",
}


def _terms(query: str) -> list[str]:
    raw = [token.casefold() for token in re.findall(r"\w+", query, flags=re.UNICODE)]
    terms = [token for token in raw if token not in _STOPWORDS and len(token) > 1]
    if not terms:
        terms = [token for token in raw if len(token) > 1]
    if not terms:
        raise KnowledgeSearchError("query must contain searchable text")
    return list(dict.fromkeys(terms))


def _matches(text: str, terms: list[str]) -> bool:
    haystack = text.casefold()
    return all(term in haystack for term in terms)


def _snippet(text: str, terms: list[str], width: int = 240) -> str:
    compact = " ".join(text.split())
    folded = compact.casefold()
    positions = [folded.find(term) for term in terms if folded.find(term) >= 0]
    if not positions:
        return compact[:width]
    center = min(positions)
    start = max(0, center - width // 3)
    end = min(len(compact), start + width)
    return compact[start:end]


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


class PersonalKnowledgeSearch:
    """PL-14 lexical retrieval with project isolation and evidence/source separation.

    This is intentionally not a semantic-search or truth-verification layer.
    """

    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")
        self.output_root = self.home / "runtime" / "knowledge_search"

    def ask(self, query: str, *, project_id: str | None = None, limit: int = 20) -> dict[str, Any]:
        query = query.strip()
        if not query:
            raise KnowledgeSearchError("query cannot be empty")
        if limit < 1 or limit > 200:
            raise KnowledgeSearchError("limit must be between 1 and 200")
        terms = _terms(query)

        project_ids = self._project_scope(project_id)
        results: list[dict[str, Any]] = []
        results.extend(self._project_file_results(project_ids, terms))
        results.extend(self._memory_results(terms, project_id=project_id))
        results = self._deduplicate(results)
        results.sort(key=lambda item: (item["project_id"] or "", item["source_type"], item["source_ref"]))
        results = results[:limit]

        status = "FOUND" if results else "UNKNOWN"
        counts = Counter(item["source_type"] for item in results)
        snapshot = [
            {
                "result_id": item["result_id"],
                "project_id": item.get("project_id"),
                "source_ref": item["source_ref"],
                "content_hash": item.get("content_hash"),
            }
            for item in results
        ]
        fingerprint_payload = json.dumps(
            {"query": query, "project_id": project_id, "snapshot": snapshot},
            sort_keys=True,
            ensure_ascii=False,
        )
        result_id = hashlib.sha256(fingerprint_payload.encode("utf-8")).hexdigest()

        response = {
            "schema": "ivdivo.personal_ai.knowledge_search/0.1",
            "result_id": result_id,
            "query": query,
            "query_terms": terms,
            "scope": {"mode": "PROJECT" if project_id else "GLOBAL", "project_id": project_id},
            "search_mode": "LEXICAL_ONLY",
            "status": status,
            "answer": (
                "Traceable stored matches found; inspect source-separated results. No evidence authority was upgraded."
                if results
                else "UNKNOWN: no matching active stored evidence/state was found."
            ),
            "result_count": len(results),
            "source_separation": dict(sorted(counts.items())),
            "results": results,
            "boundaries": [
                "retrieval != truth verification",
                "lexical search != semantic understanding",
                "invalidated memory is excluded",
                "project-scoped search excludes other projects",
                "verified claims remain distinct from VERIFIED_FACT records",
                "no-hit remains UNKNOWN",
                "search output is persisted outside searchable memory to prevent self-feedback",
            ],
        }
        scope_name = project_id or "_global"
        output_path = self.output_root / scope_name / f"{result_id}.json"
        _write_json(output_path, response)
        response["persisted_result"] = str(output_path.relative_to(self.home))
        return response

    def _project_scope(self, project_id: str | None) -> list[str]:
        if project_id is not None:
            return [self.projects.load_project(project_id)["project_id"]]
        if not self.projects.projects_root.exists():
            return []
        project_ids: list[str] = []
        for path in sorted(self.projects.projects_root.iterdir()):
            if not path.is_dir() or path.is_symlink():
                continue
            try:
                project_ids.append(self.projects.load_project(path.name)["project_id"])
            except (FileNotFoundError, RuntimeError, ValueError):
                continue
        return project_ids

    def _project_file_results(self, project_ids: list[str], terms: list[str]) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for project_id in project_ids:
            project = self.projects.load_project(project_id)
            paths = self.projects.paths(project_id)

            state_text = json.dumps(
                {"state": project["state"], "tasks": project["tasks"]},
                sort_keys=True,
                ensure_ascii=False,
            )
            if _matches(state_text, terms):
                results.append(
                    self._file_result(
                        project_id=project_id,
                        source_type="PROJECT_STATE",
                        authority="SYSTEM_STATE",
                        source_ref=str(paths.state_json.relative_to(self.home)),
                        text=state_text,
                        terms=terms,
                    )
                )

            decisions_text = paths.decisions_md.read_text(encoding="utf-8")
            if _matches(decisions_text, terms):
                results.append(
                    self._file_result(
                        project_id=project_id,
                        source_type="DECISION_FILE",
                        authority="USER_DECISION_RECORD",
                        source_ref=str(paths.decisions_md.relative_to(self.home)),
                        text=decisions_text,
                        terms=terms,
                    )
                )
        return results

    def _file_result(
        self,
        *,
        project_id: str,
        source_type: str,
        authority: str,
        source_ref: str,
        text: str,
        terms: list[str],
    ) -> dict[str, Any]:
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        result_id = hashlib.sha256(
            f"{project_id}\0{source_type}\0{source_ref}\0{content_hash}".encode("utf-8")
        ).hexdigest()
        return {
            "result_id": result_id,
            "project_id": project_id,
            "source_type": source_type,
            "authority": authority,
            "source_ref": source_ref,
            "content_hash": content_hash,
            "snippet": _snippet(text, terms),
            "provenance_chain": [source_ref, project_id],
        }

    def _memory_results(self, terms: list[str], *, project_id: str | None) -> list[dict[str, Any]]:
        candidates: dict[str, dict[str, Any]] = {}
        for term in terms:
            for record in self.memory.search(term, project_id=project_id, include_invalid=False, limit=500):
                candidates[record["id"]] = record

        results: list[dict[str, Any]] = []
        for record in candidates.values():
            searchable = json.dumps(
                {
                    "content": record.get("content", ""),
                    "source": record.get("source"),
                    "metadata": record.get("metadata") or {},
                },
                sort_keys=True,
                ensure_ascii=False,
            )
            if not _matches(searchable, terms):
                continue
            if project_id is not None and record.get("project_id") != project_id:
                continue
            authority = self._authority(record)
            chain_ids = [item.get("id") for item in self.memory.trace_source(record["id"])["chain"]]
            results.append(
                {
                    "result_id": record["id"],
                    "project_id": record.get("project_id"),
                    "source_type": self._source_type(record),
                    "authority": authority,
                    "source_ref": f"memory:{record['id']}",
                    "memory_id": record["id"],
                    "source_id": record.get("source_id"),
                    "source_label": record.get("source"),
                    "confidence": record.get("confidence"),
                    "content_hash": record.get("content_hash"),
                    "snippet": _snippet(record.get("content", ""), terms),
                    "provenance_chain": chain_ids,
                }
            )
        return results

    @staticmethod
    def _source_type(record: dict[str, Any]) -> str:
        kind = str(record.get("kind") or "MEMORY").upper()
        return {
            "DOCUMENT": "DOCUMENT",
            "SOURCE": "SOURCE",
            "DECISION": "DECISION_MEMORY",
            "CLAIM": "CLAIM",
            "FACT": "FACT",
            "OUTPUT": "OUTPUT",
            "EVENT": "EVENT",
        }.get(kind, "MEMORY")

    @staticmethod
    def _authority(record: dict[str, Any]) -> str:
        kind = str(record.get("kind") or "").upper()
        metadata = record.get("metadata") or {}
        if kind == "CLAIM":
            claim_type = str(metadata.get("claim_type") or "CLAIM").upper()
            state = str(metadata.get("verified_state") or "UNVERIFIED").upper()
            return f"{claim_type}_{state}"
        if (
            kind == "FACT"
            and metadata.get("record_role") == "VERIFIED_FACT"
            and metadata.get("verified_state") == "VERIFIED"
        ):
            return "VERIFIED_FACT"
        if kind == "DECISION":
            return "USER_DECISION_RECORD"
        if kind in {"DOCUMENT", "SOURCE"}:
            return "SOURCE_MATERIAL_NOT_TRUTH_VERIFIED"
        if kind == "TEST_RESULT":
            return "TEST_RESULT_RECORD"
        return "UNVERIFIED_STORED_RECORD"

    @staticmethod
    def _deduplicate(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[tuple[str, str]] = set()
        output: list[dict[str, Any]] = []
        for item in results:
            key = (item["source_type"], item["source_ref"])
            if key in seen:
                continue
            seen.add(key)
            output.append(item)
        return output
