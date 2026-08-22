from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from memory.db import SQLiteStore

MEMORY_SCHEMA = """
CREATE TABLE IF NOT EXISTS memory_records (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    content TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('ACTIVE','INVALID')),
    source TEXT,
    metadata_json TEXT NOT NULL,
    invalid_reason TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS memory_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id TEXT NOT NULL REFERENCES memory_records(id),
    action TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    detail_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_memory_records_status ON memory_records(status);
CREATE INDEX IF NOT EXISTS idx_memory_records_kind ON memory_records(kind);
CREATE INDEX IF NOT EXISTS idx_memory_events_memory_id ON memory_events(memory_id, event_id);
"""

VERSIONED_MEMORY_TABLES = ("documents", "facts", "decisions", "sources", "outputs", "events")
REQUIRED_PL02_TABLES = ("projects", "tasks") + VERSIONED_MEMORY_TABLES

_VERSIONED_RECORD_SCHEMA = """
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


def _decode_row(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    item["metadata"] = json.loads(item.pop("metadata_json"))
    return item


def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _validate_confidence(value: float | None) -> float | None:
    if value is None:
        return None
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError("confidence must be between 0 and 1")
    return value


class MemoryStore:
    """Compatibility PL-02 store preserved for the existing CLI and callers.

    This API remains operational after the stricter versioned PL-02 corrective.
    New provenance-sensitive code should use VersionedMemory below.
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.base = SQLiteStore(self.db_path)
        self.base.initialize()
        with self.base.connect() as conn:
            conn.executescript(MEMORY_SCHEMA)

    def _event(self, conn: sqlite3.Connection, memory_id: str, action: str, detail: dict[str, Any]) -> None:
        conn.execute(
            "INSERT INTO memory_events(memory_id,action,timestamp,detail_json) VALUES(?,?,?,?)",
            (memory_id, action, _utc_now(), json.dumps(detail, sort_keys=True)),
        )

    def store(
        self,
        content: str,
        *,
        kind: str = "NOTE",
        source: str | None = None,
        metadata: dict[str, Any] | None = None,
        record_id: str | None = None,
    ) -> dict[str, Any]:
        content = content.strip()
        kind = kind.strip().upper()
        if not content:
            raise ValueError("memory content cannot be empty")
        if not kind:
            raise ValueError("memory kind cannot be empty")
        record_id = record_id or f"mem-{uuid.uuid4().hex}"
        now = _utc_now()
        metadata = metadata or {}
        with self.base.connect() as conn:
            conn.execute(
                "INSERT INTO memory_records(id,kind,content,status,source,metadata_json,invalid_reason,created_at,updated_at) "
                "VALUES(?,?,?,?,?,?,?,?,?)",
                (record_id, kind, content, "ACTIVE", source, json.dumps(metadata, sort_keys=True), None, now, now),
            )
            self._event(conn, record_id, "STORE", {"kind": kind, "source": source})
        return self.get(record_id)

    def get(self, record_id: str) -> dict[str, Any]:
        with self.base.connect() as conn:
            row = conn.execute("SELECT * FROM memory_records WHERE id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(f"memory record not found: {record_id}")
        return _decode_row(row)

    def search(
        self,
        query: str,
        *,
        kind: str | None = None,
        include_invalid: bool = False,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        query = query.strip()
        if limit < 1 or limit > 500:
            raise ValueError("limit must be between 1 and 500")
        clauses = ["(content LIKE ? OR source LIKE ? OR metadata_json LIKE ?)"]
        pattern = f"%{query}%"
        params: list[Any] = [pattern, pattern, pattern]
        if not include_invalid:
            clauses.append("status='ACTIVE'")
        if kind:
            clauses.append("kind=?")
            params.append(kind.strip().upper())
        params.append(limit)
        sql = "SELECT * FROM memory_records WHERE " + " AND ".join(clauses) + " ORDER BY updated_at DESC LIMIT ?"
        with self.base.connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [_decode_row(row) for row in rows]

    def update(
        self,
        record_id: str,
        *,
        content: str | None = None,
        source: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        current = self.get(record_id)
        if current["status"] != "ACTIVE":
            raise RuntimeError("invalidated memory cannot be updated")
        new_content = current["content"] if content is None else content.strip()
        if not new_content:
            raise ValueError("memory content cannot be empty")
        new_source = current["source"] if source is None else source
        new_metadata = current["metadata"] if metadata is None else metadata
        now = _utc_now()
        with self.base.connect() as conn:
            conn.execute(
                "UPDATE memory_records SET content=?,source=?,metadata_json=?,updated_at=? WHERE id=?",
                (new_content, new_source, json.dumps(new_metadata, sort_keys=True), now, record_id),
            )
            self._event(
                conn,
                record_id,
                "UPDATE",
                {
                    "content_changed": new_content != current["content"],
                    "source_changed": new_source != current["source"],
                    "metadata_changed": new_metadata != current["metadata"],
                },
            )
        return self.get(record_id)

    def invalidate(self, record_id: str, reason: str) -> dict[str, Any]:
        reason = reason.strip()
        if not reason:
            raise ValueError("invalidation reason cannot be empty")
        current = self.get(record_id)
        if current["status"] == "INVALID":
            return current
        now = _utc_now()
        with self.base.connect() as conn:
            conn.execute(
                "UPDATE memory_records SET status='INVALID',invalid_reason=?,updated_at=? WHERE id=?",
                (reason, now, record_id),
            )
            self._event(conn, record_id, "INVALIDATE", {"reason": reason})
        return self.get(record_id)

    def trace(self, record_id: str) -> list[dict[str, Any]]:
        self.get(record_id)
        with self.base.connect() as conn:
            rows = conn.execute(
                "SELECT event_id,memory_id,action,timestamp,detail_json FROM memory_events WHERE memory_id=? ORDER BY event_id",
                (record_id,),
            ).fetchall()
        events: list[dict[str, Any]] = []
        for row in rows:
            event = dict(row)
            event["detail"] = json.loads(event.pop("detail_json"))
            events.append(event)
        return events


class VersionedMemory:
    """Strict PL-02 long-term memory with immutable versions and provenance.

    The original PL-02 prompt requires physical documents/facts/decisions/sources/
    outputs/events tables plus content hashes and version/history semantics. This
    class satisfies that contract while MemoryStore remains a compatibility API.
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.base = SQLiteStore(self.db_path)
        self.base.initialize()
        self.initialize()

    def initialize(self) -> None:
        with self.base.connect() as conn:
            for table in VERSIONED_MEMORY_TABLES:
                conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({_VERSIONED_RECORD_SCHEMA})")
                conn.execute(
                    f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table}_current_id ON {table}(id) WHERE is_current=1"
                )
                conn.execute(
                    f"CREATE INDEX IF NOT EXISTS idx_{table}_project_current ON {table}(project_id,is_current)"
                )

    @staticmethod
    def _table(entity: str) -> str:
        table = entity.strip().lower()
        if table not in VERSIONED_MEMORY_TABLES:
            raise ValueError(
                f"unsupported versioned memory entity: {table}; choose from {', '.join(VERSIONED_MEMORY_TABLES)}"
            )
        return table

    @staticmethod
    def _row(row: sqlite3.Row | None, entity: str) -> dict[str, Any] | None:
        if row is None:
            return None
        item = dict(row)
        item["entity"] = entity
        item["is_current"] = bool(item["is_current"])
        return item

    def get(self, entity: str, record_id: str, version: int | None = None) -> dict[str, Any]:
        table = self._table(entity)
        with self.base.connect() as conn:
            if version is None:
                row = conn.execute(
                    f"SELECT * FROM {table} WHERE id=? AND is_current=1", (record_id,)
                ).fetchone()
            else:
                row = conn.execute(
                    f"SELECT * FROM {table} WHERE id=? AND version=?", (record_id, int(version))
                ).fetchone()
        result = self._row(row, table)
        if result is None:
            raise KeyError(f"versioned memory record not found: {table}/{record_id}")
        return result

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
        confidence = _validate_confidence(confidence)
        now = _utc_now()
        with self.base.connect() as conn:
            if conn.execute(f"SELECT 1 FROM {table} WHERE id=? LIMIT 1", (record_id,)).fetchone():
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
        if current["status"] == "INVALIDATED":
            raise RuntimeError("invalidated versioned memory cannot be updated")
        next_content = current["content"] if content is None else content.strip()
        next_source = current["source"] if source is None else source.strip()
        next_status = current["status"] if status is None else status.strip().upper()
        if not next_content or not next_source or not next_status:
            raise ValueError("content/source/status cannot be empty")
        next_confidence = current["confidence"] if confidence is None else _validate_confidence(confidence)
        next_project = current["project_id"] if project_id is None else project_id
        next_source_id = current["source_id"] if source_id is None else source_id
        next_version = int(current["version"]) + 1
        now = _utc_now()
        with self.base.connect() as conn:
            conn.execute(f"UPDATE {table} SET is_current=0 WHERE id=? AND is_current=1", (record_id,))
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

    def invalidate(self, entity: str, record_id: str, *, reason: str = "invalidated") -> dict[str, Any]:
        table = self._table(entity)
        current = self.get(table, record_id)
        if current["status"] == "INVALIDATED":
            return current
        reason = reason.strip() or "invalidated"
        now = _utc_now()
        next_version = int(current["version"]) + 1
        with self.base.connect() as conn:
            conn.execute(f"UPDATE {table} SET is_current=0 WHERE id=? AND is_current=1", (record_id,))
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

    def versions(self, entity: str, record_id: str) -> list[dict[str, Any]]:
        table = self._table(entity)
        with self.base.connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM {table} WHERE id=? ORDER BY version ASC", (record_id,)
            ).fetchall()
        return [self._row(row, table) for row in rows if row is not None]

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
        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")
        tables = (self._table(entity),) if entity else VERSIONED_MEMORY_TABLES
        needle = f"%{query}%"
        results: list[dict[str, Any]] = []
        with self.base.connect() as conn:
            for table in tables:
                clauses = [
                    "is_current=1",
                    "(lower(id) LIKE ? OR lower(content) LIKE ? OR lower(source) LIKE ? OR lower(status) LIKE ?)",
                ]
                params: list[Any] = [needle, needle, needle, needle]
                if not include_invalid:
                    clauses.append("status != 'INVALIDATED'")
                if project_id is not None:
                    clauses.append("project_id=?")
                    params.append(project_id)
                rows = conn.execute(
                    f"SELECT * FROM {table} WHERE {' AND '.join(clauses)} ORDER BY timestamp DESC LIMIT ?",
                    (*params, limit),
                ).fetchall()
                for row in rows:
                    item = self._row(row, table)
                    if item is not None:
                        results.append(item)
        results.sort(key=lambda item: item["timestamp"], reverse=True)
        return results[:limit]

    def trace_source(self, entity: str, record_id: str, *, max_depth: int = 20) -> dict[str, Any]:
        if not 1 <= max_depth <= 100:
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
        return {"chain": chain, "cycle_detected": False, "truncated": bool(source_id)}
