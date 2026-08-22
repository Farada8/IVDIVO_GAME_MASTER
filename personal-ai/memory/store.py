from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MEMORY_TABLES = ("documents", "facts", "decisions", "sources", "outputs", "events")
REQUIRED_TABLES = ("projects", "tasks") + MEMORY_TABLES

_RECORD_SCHEMA = """
    id TEXT NOT NULL,
    version INTEGER NOT NULL,
    project_id TEXT,
    timestamp TEXT NOT NULL,
    source TEXT NOT NULL,
    source_id TEXT,
    confidence REAL,
    status TEXT NOT NULL,
    content TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
    invalidated_at TEXT,
    invalidation_reason TEXT,
    PRIMARY KEY (id, version)
"""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _validate_confidence(value: float | None) -> float | None:
    if value is None:
        return None
    value = float(value)
    if value < 0.0 or value > 1.0:
        raise ValueError("confidence must be between 0 and 1")
    return value


class LocalMemory:
    """Versioned, source-traceable SQLite memory.

    PL-00/PL-01 remain authoritative for operational project/task state. PL-02
    shares the same SQLite file and adds durable knowledge tables without
    silently replacing those earlier semantics.
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize(self) -> None:
        with self.connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, name TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id), title TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL)"
            )
            for table in MEMORY_TABLES:
                conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({_RECORD_SCHEMA})")
                conn.execute(
                    f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table}_current_id ON {table}(id) WHERE is_current = 1"
                )
                conn.execute(
                    f"CREATE INDEX IF NOT EXISTS idx_{table}_project_current ON {table}(project_id, is_current)"
                )

    @staticmethod
    def _table(entity: str) -> str:
        entity = entity.strip().lower()
        if entity not in MEMORY_TABLES:
            raise ValueError(
                f"unsupported memory entity: {entity}; choose from {', '.join(MEMORY_TABLES)}"
            )
        return entity

    @staticmethod
    def _row(row: sqlite3.Row | None, entity: str) -> dict[str, Any] | None:
        if row is None:
            return None
        out = dict(row)
        out["entity"] = entity
        out["is_current"] = bool(out["is_current"])
        return out

    def store(
        self,
        entity: str,
        record_id: str,
        content: str,
        *,
        project_id: str | None = None,
        source: str = "user",
        source_id: str | None = None,
        confidence: float | None = None,
        status: str = "ACTIVE",
    ) -> dict[str, Any]:
        table = self._table(entity)
        record_id = record_id.strip()
        content = content.strip()
        source = source.strip()
        status = status.strip().upper()
        if not record_id:
            raise ValueError("record_id cannot be empty")
        if not content:
            raise ValueError("content cannot be empty")
        if not source:
            raise ValueError("source cannot be empty")
        if not status:
            raise ValueError("status cannot be empty")
        confidence = _validate_confidence(confidence)
        now = _utc_now()
        with self.connect() as conn:
            exists = conn.execute(
                f"SELECT 1 FROM {table} WHERE id=? LIMIT 1", (record_id,)
            ).fetchone()
            if exists:
                raise ValueError(f"record already exists; use update: {table}/{record_id}")
            conn.execute(
                f"""INSERT INTO {table}
                (id,version,project_id,timestamp,source,source_id,confidence,status,content,content_hash,is_current,invalidated_at,invalidation_reason)
                VALUES(?,?,?,?,?,?,?,?,?,?,1,NULL,NULL)""",
                (
                    record_id,
                    1,
                    project_id,
                    now,
                    source,
                    source_id,
                    confidence,
                    status,
                    content,
                    _content_hash(content),
                ),
            )
        return self.get(table, record_id)

    def get(self, entity: str, record_id: str, version: int | None = None) -> dict[str, Any]:
        table = self._table(entity)
        with self.connect() as conn:
            if version is None:
                row = conn.execute(
                    f"SELECT * FROM {table} WHERE id=? AND is_current=1", (record_id,)
                ).fetchone()
            else:
                row = conn.execute(
                    f"SELECT * FROM {table} WHERE id=? AND version=?",
                    (record_id, int(version)),
                ).fetchone()
        result = self._row(row, table)
        if result is None:
            raise KeyError(f"record not found: {table}/{record_id}")
        return result

    def get_versions(self, entity: str, record_id: str) -> list[dict[str, Any]]:
        table = self._table(entity)
        with self.connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM {table} WHERE id=? ORDER BY version ASC", (record_id,)
            ).fetchall()
        results: list[dict[str, Any]] = []
        for row in rows:
            item = self._row(row, table)
            if item is not None:
                results.append(item)
        return results

    def update(
        self,
        entity: str,
        record_id: str,
        *,
        content: str | None = None,
        project_id: str | None = None,
        source: str | None = None,
        source_id: str | None = None,
        confidence: float | None = None,
        status: str | None = None,
    ) -> dict[str, Any]:
        table = self._table(entity)
        current = self.get(table, record_id)
        next_content = current["content"] if content is None else content.strip()
        if not next_content:
            raise ValueError("content cannot be empty")
        next_source = current["source"] if source is None else source.strip()
        if not next_source:
            raise ValueError("source cannot be empty")
        next_status = current["status"] if status is None else status.strip().upper()
        if not next_status:
            raise ValueError("status cannot be empty")
        next_confidence = (
            current["confidence"] if confidence is None else _validate_confidence(confidence)
        )
        next_project = current["project_id"] if project_id is None else project_id
        next_source_id = current["source_id"] if source_id is None else source_id
        next_version = int(current["version"]) + 1
        now = _utc_now()
        with self.connect() as conn:
            conn.execute(
                f"UPDATE {table} SET is_current=0 WHERE id=? AND is_current=1", (record_id,)
            )
            conn.execute(
                f"""INSERT INTO {table}
                (id,version,project_id,timestamp,source,source_id,confidence,status,content,content_hash,is_current,invalidated_at,invalidation_reason)
                VALUES(?,?,?,?,?,?,?,?,?,?,1,NULL,NULL)""",
                (
                    record_id,
                    next_version,
                    next_project,
                    now,
                    next_source,
                    next_source_id,
                    next_confidence,
                    next_status,
                    next_content,
                    _content_hash(next_content),
                ),
            )
        return self.get(table, record_id)

    def invalidate(
        self, entity: str, record_id: str, *, reason: str = "invalidated"
    ) -> dict[str, Any]:
        table = self._table(entity)
        current = self.get(table, record_id)
        if current["status"] == "INVALIDATED":
            return current
        reason = reason.strip() or "invalidated"
        next_version = int(current["version"]) + 1
        now = _utc_now()
        with self.connect() as conn:
            conn.execute(
                f"UPDATE {table} SET is_current=0 WHERE id=? AND is_current=1", (record_id,)
            )
            conn.execute(
                f"""INSERT INTO {table}
                (id,version,project_id,timestamp,source,source_id,confidence,status,content,content_hash,is_current,invalidated_at,invalidation_reason)
                VALUES(?,?,?,?,?,?,?,?,?,?,1,?,?)""",
                (
                    record_id,
                    next_version,
                    current["project_id"],
                    now,
                    current["source"],
                    current["source_id"],
                    current["confidence"],
                    "INVALIDATED",
                    current["content"],
                    current["content_hash"],
                    now,
                    reason,
                ),
            )
        return self.get(table, record_id)

    def search(
        self,
        query: str,
        *,
        entity: str | None = None,
        project_id: str | None = None,
        include_invalid: bool = False,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        query = query.strip().lower()
        if not query:
            raise ValueError("search query cannot be empty")
        if limit < 1 or limit > 500:
            raise ValueError("limit must be between 1 and 500")
        tables = (self._table(entity),) if entity else MEMORY_TABLES
        results: list[dict[str, Any]] = []
        needle = f"%{query}%"
        with self.connect() as conn:
            for table in tables:
                clauses = [
                    "is_current=1",
                    "(lower(id) LIKE ? OR lower(content) LIKE ? OR lower(source) LIKE ? OR lower(status) LIKE ?)",
                ]
                params: list[Any] = [needle, needle, needle, needle]
                if not include_invalid:
                    clauses.append("status != 'INVALIDATED'")
                if project_id is not None:
                    clauses.append("project_id = ?")
                    params.append(project_id)
                rows = conn.execute(
                    f"SELECT * FROM {table} WHERE {' AND '.join(clauses)} ORDER BY timestamp DESC LIMIT ?",
                    (*params, limit),
                ).fetchall()
                for row in rows:
                    item = self._row(row, table)
                    if item is not None:
                        results.append(item)
        results.sort(key=lambda r: r["timestamp"], reverse=True)
        return results[:limit]

    def trace_source(
        self, entity: str, record_id: str, *, max_depth: int = 20
    ) -> dict[str, Any]:
        if max_depth < 1 or max_depth > 100:
            raise ValueError("max_depth must be between 1 and 100")
        current = self.get(entity, record_id)
        chain = [current]
        seen = {(current["entity"], current["id"])}
        source_id = current.get("source_id")
        while source_id and len(chain) < max_depth:
            key = ("sources", source_id)
            if key in seen:
                return {"chain": chain, "cycle_detected": True, "truncated": False}
            try:
                parent = self.get("sources", source_id)
            except KeyError:
                return {
                    "chain": chain,
                    "cycle_detected": False,
                    "truncated": False,
                    "missing_source_id": source_id,
                }
            chain.append(parent)
            seen.add(key)
            source_id = parent.get("source_id")
        return {
            "chain": chain,
            "cycle_detected": False,
            "truncated": bool(source_id),
        }
