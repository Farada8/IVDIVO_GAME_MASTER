from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def _safe(value: str, field: str) -> str:
    value = value.strip()
    if not _SAFE_ID.fullmatch(value):
        raise ValueError(f"{field} must be a safe identifier")
    return value


def _atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    _atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


class BusinessStore:
    """Small local persistence layer for business entities and project quote artifacts."""

    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.entities_root = self.home / "runtime" / "business" / "entities"

    def save_entity(self, entity_type: str, entity_id: str, value: dict[str, Any]) -> Path:
        entity_type = _safe(entity_type.lower(), "entity_type")
        entity_id = _safe(entity_id, "entity_id")
        path = self.entities_root / entity_type / f"{entity_id}.json"
        _atomic_json(path, value)
        return path

    def load_entity(self, entity_type: str, entity_id: str) -> dict[str, Any]:
        entity_type = _safe(entity_type.lower(), "entity_type")
        entity_id = _safe(entity_id, "entity_id")
        path = self.entities_root / entity_type / f"{entity_id}.json"
        if not path.is_file():
            raise FileNotFoundError(f"business entity not found: {entity_type}/{entity_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def save_quote_artifacts(
        self,
        project_root: Path,
        quote_id: str,
        document: dict[str, Any],
        markdown: str,
    ) -> tuple[Path, Path]:
        quote_id = _safe(quote_id, "quote_id")
        root = Path(project_root) / "artifacts" / "business" / "quotes"
        json_path = root / f"{quote_id}.json"
        md_path = root / f"{quote_id}.md"
        _atomic_json(json_path, document)
        _atomic_text(md_path, markdown)
        return json_path, md_path
