from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from memory.db import SQLiteStore


def bootstrap(home: Path) -> dict[str, Any]:
    home = Path(home)
    runtime_dir = home / "runtime"
    log_dir = home / "logs"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    created_at = datetime.now(timezone.utc).isoformat()
    store = SQLiteStore(runtime_dir / "state.db")
    store.initialize()
    store.ensure_demo(created_at)
    snapshot = store.demo_snapshot()

    result = {
        "action": "PL00_BOOTSTRAP",
        "persisted": True,
        "db_path": str(store.db_path),
        "project": snapshot["project"],
        "task": snapshot["task"],
        "counts": snapshot["counts"],
    }
    with (log_dir / "bootstrap.log").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(result, sort_keys=True) + "\n")
    return result
