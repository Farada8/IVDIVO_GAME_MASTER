from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from memory.db import SQLiteStore

TYPED_KIND_TO_TABLE = {
    "DOCUMENT": "documents",
    "FACT": "facts",
    "DECISION": "decisions",
    "SOURCE": "sources",
    "OUTPUT": "outputs",
    "EVENT": "events",
}
REQUIRED_TABLES = ("projects", "tasks", *TYPED_KIND_TO_TABLE.values())

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
    updated_at TEXT NOT NULL,
    project_id TEXT,
    source_id TEXT,
    confidence REAL,
    content_hash TEXT,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS memory_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id TEXT NOT NULL REFERENCES memory_records(id),
    action TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    detail_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS memory_versions (
    memory_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    kind TEXT NOT NULL,
    content TEXT NOT NULL,
    status TEXT NOT NULL,
    source TEXT,
    metadata_json TEXT NOT NULL,
    invalid_reason TEXT,
    timestamp TEXT NOT NULL,
    project_id TEXT,
    source_id TEXT,
    confidence REAL,
    content_hash TEXT NOT NULL,
    action TEXT NOT NULL,
    PRIMARY KEY(memory_id, version)
);
CREATE INDEX IF NOT EXISTS idx_memory_records_status ON memory_records(status);
CREATE INDEX IF NOT EXISTS idx_memory_records_kind ON memory_records(kind);
CREATE INDEX IF NOT EXISTS idx_memory_records_project ON memory_records(project_id);
CREATE INDEX IF NOT EXISTS idx_memory_events_memory_id ON memory_events(memory_id, event_id);
CREATE INDEX IF NOT EXISTS idx_memory_versions_memory_id ON memory_versions(memory_id, version);
"""

TYPED_RECORD_SCHEMA = """
    id TEXT NOT NULL,
    version INTEGER NOT NULL,
    project_id TEXT,
    timestamp TEXT NOT NULL,
    source TEXT,
    source_id TEXT,
    confidence REAL,
    status TEXT NOT NULL,
    content TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    is_current INTEGER NOT NULL CHECK(is_current IN (0,1)),
    invalidated_at TEXT,
    invalidation_reason TEXT,
    PRIMARY KEY(id, version)
"""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _confidence(value: float | None) -> float | None:
    if value is None:
        return None
    value = float(value)
    if not 0 <= value <= 1:
        raise ValueError("confidence must be between 0 and 1")
    return value


def _decode_row(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    item["metadata"] = json.loads(item.pop("metadata_json"))
    return item


class MemoryStore:
    """Persistent local memory with audit events, immutable versions and source provenance."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.base = SQLiteStore(self.db_path)
        self.base.initialize()
        with self.base.connect() as conn:
            conn.executescript(MEMORY_SCHEMA)
            for table in TYPED_KIND_TO_TABLE.values():
                conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({TYPED_RECORD_SCHEMA})")
                conn.execute(
                    f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table}_current ON {table}(id) WHERE is_current=1"
                )
            self._migrate_legacy(conn)

    def _migrate_legacy(self, conn: sqlite3.Connection) -> None:
        columns = {r[1] for r in conn.execute("PRAGMA table_info(memory_records)").fetchall()}
        additions = {
            "project_id": "TEXT",
            "source_id": "TEXT",
            "confidence": "REAL",
            "content_hash": "TEXT",
            "version": "INTEGER NOT NULL DEFAULT 1",
        }
        for name, sql_type in additions.items():
            if name not in columns:
                conn.execute(f"ALTER TABLE memory_records ADD COLUMN {name} {sql_type}")
        rows = conn.execute("SELECT * FROM memory_records").fetchall()
        for row in rows:
            item = dict(row)
            metadata = json.loads(item.get("metadata_json") or "{}")
            content_hash = item.get("content_hash") or _hash(item["content"])
            project_id = item.get("project_id") or (
                metadata.get("project") if isinstance(metadata.get("project"), str) else None
            )
            confidence = item.get("confidence")
            raw_conf = metadata.get("confidence")
            if confidence is None and isinstance(raw_conf, (int, float)) and 0 <= raw_conf <= 1:
                confidence = float(raw_conf)
            version = int(item.get("version") or 1)
            conn.execute(
                "UPDATE memory_records SET content_hash=?,project_id=?,confidence=?,version=? WHERE id=?",
                (content_hash, project_id, confidence, version, item["id"]),
            )
            exists = conn.execute(
                "SELECT 1 FROM memory_versions WHERE memory_id=? AND version=?",
                (item["id"], version),
            ).fetchone()
            if not exists:
                conn.execute(
                    """INSERT INTO memory_versions(memory_id,version,kind,content,status,source,metadata_json,invalid_reason,timestamp,project_id,source_id,confidence,content_hash,action)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        item["id"],
                        version,
                        item["kind"],
                        item["content"],
                        item["status"],
                        item["source"],
                        item["metadata_json"],
                        item["invalid_reason"],
                        item["updated_at"],
                        project_id,
                        item.get("source_id"),
                        confidence,
                        content_hash,
                        "LEGACY_SNAPSHOT",
                    ),
                )
            self._ensure_typed_snapshot(
                conn,
                {
                    **item,
                    "content_hash": content_hash,
                    "project_id": project_id,
                    "confidence": confidence,
                    "version": version,
                },
            )

    def _event(
        self, conn: sqlite3.Connection, memory_id: str, action: str, detail: dict[str, Any]
    ) -> None:
        conn.execute(
            "INSERT INTO memory_events(memory_id,action,timestamp,detail_json) VALUES(?,?,?,?)",
            (memory_id, action, _utc_now(), json.dumps(detail, sort_keys=True)),
        )

    def _ensure_typed_snapshot(
        self, conn: sqlite3.Connection, record: dict[str, Any]
    ) -> None:
        table = TYPED_KIND_TO_TABLE.get(str(record["kind"]).upper())
        if not table:
            return
        exists = conn.execute(
            f"SELECT 1 FROM {table} WHERE id=? AND version=?",
            (record["id"], int(record["version"])),
        ).fetchone()
        if exists:
            return
        conn.execute(
            f"UPDATE {table} SET is_current=0 WHERE id=? AND is_current=1", (record["id"],)
        )
        invalid = record["status"] == "INVALID"
        conn.execute(
            f"""INSERT INTO {table}(id,version,project_id,timestamp,source,source_id,confidence,status,content,content_hash,is_current,invalidated_at,invalidation_reason)
            VALUES(?,?,?,?,?,?,?,?,?,?,1,?,?)""",
            (
                record["id"],
                int(record["version"]),
                record.get("project_id"),
                record.get("updated_at") or _utc_now(),
                record.get("source"),
                record.get("source_id"),
                record.get("confidence"),
                record["status"],
                record["content"],
                record["content_hash"],
                record.get("updated_at") if invalid else None,
                record.get("invalid_reason") if invalid else None,
            ),
        )

    def _version_snapshot(
        self, conn: sqlite3.Connection, record: dict[str, Any], action: str
    ) -> None:
        conn.execute(
            """INSERT INTO memory_versions(memory_id,version,kind,content,status,source,metadata_json,invalid_reason,timestamp,project_id,source_id,confidence,content_hash,action)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                record["id"],
                int(record["version"]),
                record["kind"],
                record["content"],
                record["status"],
                record.get("source"),
                json.dumps(record.get("metadata", {}), sort_keys=True),
                record.get("invalid_reason"),
                record.get("updated_at") or _utc_now(),
                record.get("project_id"),
                record.get("source_id"),
                record.get("confidence"),
                record["content_hash"],
                action,
            ),
        )
        self._ensure_typed_snapshot(conn, record)

    def store(
        self,
        content: str,
        *,
        kind: str = "NOTE",
        source: str | None = None,
        metadata: dict[str, Any] | None = None,
        record_id: str | None = None,
        project_id: str | None = None,
        source_id: str | None = None,
        confidence: float | None = None,
    ) -> dict[str, Any]:
        content = content.strip()
        kind = kind.strip().upper()
        if not content:
            raise ValueError("memory content cannot be empty")
        if not kind:
            raise ValueError("memory kind cannot be empty")
        confidence = _confidence(confidence)
        record_id = record_id or f"mem-{uuid.uuid4().hex}"
        now = _utc_now()
        metadata = metadata or {}
        content_hash = _hash(content)
        with self.base.connect() as conn:
            conn.execute(
                """INSERT INTO memory_records(id,kind,content,status,source,metadata_json,invalid_reason,created_at,updated_at,project_id,source_id,confidence,content_hash,version)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
                (
                    record_id,
                    kind,
                    content,
                    "ACTIVE",
                    source,
                    json.dumps(metadata, sort_keys=True),
                    None,
                    now,
                    now,
                    project_id,
                    source_id,
                    confidence,
                    content_hash,
                ),
            )
            record = {
                "id": record_id,
                "version": 1,
                "kind": kind,
                "content": content,
                "status": "ACTIVE",
                "source": source,
                "metadata": metadata,
                "invalid_reason": None,
                "updated_at": now,
                "project_id": project_id,
                "source_id": source_id,
                "confidence": confidence,
                "content_hash": content_hash,
            }
            self._version_snapshot(conn, record, "STORE")
            self._event(
                conn,
                record_id,
                "STORE",
                {"kind": kind, "source": source, "content_hash": content_hash},
            )
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
        project_id: str | None = None,
        include_invalid: bool = False,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        query = query.strip()
        if not query:
            raise ValueError("search query cannot be empty")
        if limit < 1 or limit > 500:
            raise ValueError("limit must be between 1 and 500")
        clauses = ["(content LIKE ? OR source LIKE ? OR metadata_json LIKE ? OR id LIKE ?)"]
        pattern = f"%{query}%"
        params: list[Any] = [pattern, pattern, pattern, pattern]
        if not include_invalid:
            clauses.append("status='ACTIVE'")
        if kind:
            clauses.append("kind=?")
            params.append(kind.strip().upper())
        if project_id:
            clauses.append("project_id=?")
            params.append(project_id)
        params.append(limit)
        sql = (
            "SELECT * FROM memory_records WHERE "
            + " AND ".join(clauses)
            + " ORDER BY updated_at DESC LIMIT ?"
        )
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
        project_id: str | None = None,
        source_id: str | None = None,
        confidence: float | None = None,
    ) -> dict[str, Any]:
        current = self.get(record_id)
        if current["status"] != "ACTIVE":
            raise RuntimeError("invalidated memory cannot be updated")
        new_content = current["content"] if content is None else content.strip()
        if not new_content:
            raise ValueError("memory content cannot be empty")
        new_source = current["source"] if source is None else source
        new_metadata = current["metadata"] if metadata is None else metadata
        new_project = current.get("project_id") if project_id is None else project_id
        new_source_id = current.get("source_id") if source_id is None else source_id
        new_confidence = (
            current.get("confidence") if confidence is None else _confidence(confidence)
        )
        version = int(current.get("version") or 1) + 1
        now = _utc_now()
        content_hash = _hash(new_content)
        with self.base.connect() as conn:
            conn.execute(
                """UPDATE memory_records SET content=?,source=?,metadata_json=?,updated_at=?,project_id=?,source_id=?,confidence=?,content_hash=?,version=? WHERE id=?""",
                (
                    new_content,
                    new_source,
                    json.dumps(new_metadata, sort_keys=True),
                    now,
                    new_project,
                    new_source_id,
                    new_confidence,
                    content_hash,
                    version,
                    record_id,
                ),
            )
            record = {
                "id": record_id,
                "version": version,
                "kind": current["kind"],
                "content": new_content,
                "status": "ACTIVE",
                "source": new_source,
                "metadata": new_metadata,
                "invalid_reason": None,
                "updated_at": now,
                "project_id": new_project,
                "source_id": new_source_id,
                "confidence": new_confidence,
                "content_hash": content_hash,
            }
            self._version_snapshot(conn, record, "UPDATE")
            self._event(
                conn,
                record_id,
                "UPDATE",
                {
                    "version": version,
                    "content_hash": content_hash,
                    "previous_content_hash": current.get("content_hash"),
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
        version = int(current.get("version") or 1) + 1
        now = _utc_now()
        with self.base.connect() as conn:
            conn.execute(
                "UPDATE memory_records SET status='INVALID',invalid_reason=?,updated_at=?,version=? WHERE id=?",
                (reason, now, version, record_id),
            )
            record = {
                "id": record_id,
                "version": version,
                "kind": current["kind"],
                "content": current["content"],
                "status": "INVALID",
                "source": current["source"],
                "metadata": current["metadata"],
                "invalid_reason": reason,
                "updated_at": now,
                "project_id": current.get("project_id"),
                "source_id": current.get("source_id"),
                "confidence": current.get("confidence"),
                "content_hash": current.get("content_hash") or _hash(current["content"]),
            }
            self._version_snapshot(conn, record, "INVALIDATE")
            self._event(
                conn, record_id, "INVALIDATE", {"reason": reason, "version": version}
            )
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

    def versions(self, record_id: str) -> list[dict[str, Any]]:
        self.get(record_id)
        with self.base.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM memory_versions WHERE memory_id=? ORDER BY version",
                (record_id,),
            ).fetchall()
        result: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["metadata"] = json.loads(item.pop("metadata_json"))
            result.append(item)
        return result

    def trace_source(self, record_id: str, *, max_depth: int = 20) -> dict[str, Any]:
        if max_depth < 1 or max_depth > 100:
            raise ValueError("max_depth must be between 1 and 100")
        current = self.get(record_id)
        chain = [current]
        seen = {record_id}
        source_id = current.get("source_id")
        while source_id and len(chain) < max_depth:
            if source_id in seen:
                return {"chain": chain, "cycle_detected": True, "truncated": False}
            try:
                parent = self.get(source_id)
            except KeyError:
                return {
                    "chain": chain,
                    "cycle_detected": False,
                    "truncated": False,
                    "missing_source_id": source_id,
                }
            chain.append(parent)
            seen.add(source_id)
            source_id = parent.get("source_id")
        return {
            "chain": chain,
            "cycle_detected": False,
            "truncated": bool(source_id),
        }
