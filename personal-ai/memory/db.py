from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id),
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class SQLiteStore:
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
            conn.executescript(SCHEMA)
            # Compatibility preflight for the PL-02 baseline schema.  The
            # hardened MemoryStore creates indexes on these columns, so legacy
            # databases must receive the additive columns before that schema
            # is executed.  No content rows are rewritten here.
            exists = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='memory_records'"
            ).fetchone()
            if exists:
                columns = {
                    row[1]
                    for row in conn.execute("PRAGMA table_info(memory_records)").fetchall()
                }
                additions = {
                    "project_id": "TEXT",
                    "source_id": "TEXT",
                    "confidence": "REAL",
                    "content_hash": "TEXT",
                    "version": "INTEGER NOT NULL DEFAULT 1",
                }
                for name, sql_type in additions.items():
                    if name not in columns:
                        conn.execute(
                            f"ALTER TABLE memory_records ADD COLUMN {name} {sql_type}"
                        )

    def ensure_demo(self, created_at: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO projects(id,name,status,created_at) VALUES(?,?,?,?)",
                ("demo-project", "PL-00 Demo Project", "READY", created_at),
            )
            conn.execute(
                "INSERT OR IGNORE INTO tasks(id,project_id,title,status,created_at) VALUES(?,?,?,?,?)",
                ("demo-task", "demo-project", "Verify persisted bootstrap", "READY", created_at),
            )

    def demo_snapshot(self) -> dict[str, Any]:
        with self.connect() as conn:
            project = conn.execute(
                "SELECT id,name,status,created_at FROM projects WHERE id=?", ("demo-project",)
            ).fetchone()
            task = conn.execute(
                "SELECT id,project_id,title,status,created_at FROM tasks WHERE id=?", ("demo-task",)
            ).fetchone()
            counts = {
                "projects": conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0],
                "tasks": conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
            }
        if project is None or task is None:
            raise RuntimeError("bootstrap persistence readback failed")
        return {"project": dict(project), "task": dict(task), "counts": counts}
