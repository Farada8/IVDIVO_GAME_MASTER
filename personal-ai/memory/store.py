from __future__ import annotations

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


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _decode_row(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    item["metadata"] = json.loads(item.pop("metadata_json"))
    return item


class MemoryStore:
    """Persistent, auditable local memory on the shared Personal AI SQLite database."""

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
