from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
from typing import Any

from memory.store import MemoryStore
from projects.manager import ProjectStateManager

MAX_FILE_BYTES = 10 * 1024 * 1024
SUPPORTED_EXTENSIONS = {
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".json": "application/json",
    ".csv": "text/csv",
}


class FileIngestionError(ValueError):
    pass


class UnsupportedFileTypeError(FileIngestionError):
    pass


class IngestionIntegrityError(RuntimeError):
    pass


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IngestionIntegrityError(f"invalid ingestion manifest: {path}") from exc
    if not isinstance(value, dict):
        raise IngestionIntegrityError(f"ingestion manifest must be an object: {path}")
    return value


def _decode_utf8(raw: bytes, source_name: str) -> str:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise FileIngestionError(f"{source_name} is not valid UTF-8") from exc
    if "\x00" in text:
        raise FileIngestionError(f"{source_name} contains NUL bytes")
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        raise FileIngestionError(f"{source_name} has no representable text content")
    return text


def _represent(raw: bytes, extension: str, source_name: str) -> tuple[str, str, dict[str, Any]]:
    text = _decode_utf8(raw, source_name)
    if extension == ".json":
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            raise FileIngestionError(f"{source_name} contains invalid JSON") from exc
        representation = json.dumps(
            value,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        return representation, "canonical_json", {"json_root_type": type(value).__name__}

    if extension == ".csv":
        try:
            rows = list(csv.reader(io.StringIO(text), strict=True))
        except csv.Error as exc:
            raise FileIngestionError(f"{source_name} contains invalid CSV") from exc
        if not rows:
            raise FileIngestionError(f"{source_name} has no CSV rows")
        return text, "normalized_utf8_csv", {
            "row_count": len(rows),
            "max_columns": max((len(row) for row in rows), default=0),
        }

    if extension == ".md":
        return text, "normalized_utf8_markdown", {}
    return text, "normalized_utf8_text", {}


class FileIngestionService:
    """PL-13 bounded file ingestion with raw hashing, representation and deduplication."""

    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")
        self.ingestion_root = self.home / "runtime" / "ingestion"
        self.objects_root = self.ingestion_root / "objects"
        self.manifests_root = self.ingestion_root / "manifests"

    def ingest(self, project_id: str, input_path: Path | str) -> dict[str, Any]:
        project = self.projects.load_project(project_id)
        project_id = project["project_id"]
        source = Path(input_path).expanduser()

        if source.is_symlink():
            raise FileIngestionError("symlink inputs are rejected")
        if not source.exists():
            raise FileNotFoundError(f"input file not found: {source}")
        if not source.is_file():
            raise FileIngestionError("input path must be a regular file")

        extension = source.suffix.casefold()
        media_type = SUPPORTED_EXTENSIONS.get(extension)
        if media_type is None:
            supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
            raise UnsupportedFileTypeError(
                f"unsupported file type {extension or '<none>'}; supported: {supported}"
            )

        byte_size = source.stat().st_size
        if byte_size == 0:
            raise FileIngestionError("empty files are rejected")
        if byte_size > MAX_FILE_BYTES:
            raise FileIngestionError(
                f"file exceeds PL-13 limit of {MAX_FILE_BYTES} bytes"
            )

        raw = source.read_bytes()
        if len(raw) != byte_size:
            raise IngestionIntegrityError("file size changed during read")
        raw_sha256 = _sha256_bytes(raw)
        representation, representation_kind, representation_details = _represent(
            raw, extension, source.name
        )
        representation_sha256 = _sha256_text(representation)

        ingestion_fingerprint = hashlib.sha256(
            f"{raw_sha256}\0{extension}\0{representation_kind}".encode("utf-8")
        ).hexdigest()
        project_fingerprint = hashlib.sha256(
            f"{project_id}\0{ingestion_fingerprint}".encode("utf-8")
        ).hexdigest()
        source_memory_id = f"ing-src-{project_fingerprint[:32]}"
        document_memory_id = f"ing-doc-{project_fingerprint[:32]}"

        object_path = self.objects_root / raw_sha256[:2] / raw_sha256
        manifest_path = self.manifests_root / project_id / f"{ingestion_fingerprint}.json"

        existing = self._existing_document(document_memory_id)
        if existing is not None:
            source_record = self._verify_existing(
                existing,
                project_id=project_id,
                raw_sha256=raw_sha256,
                representation_sha256=representation_sha256,
                source_memory_id=source_memory_id,
                object_path=object_path,
            )
            if manifest_path.is_file():
                manifest = _read_json(manifest_path)
                self._verify_manifest(
                    manifest,
                    document=existing,
                    raw_sha256=raw_sha256,
                    representation_sha256=representation_sha256,
                    object_path=object_path,
                    manifest_path=manifest_path,
                )
            else:
                manifest = self._manifest_from_existing(
                    existing,
                    source_record,
                    media_type=media_type,
                    extension=extension,
                    object_path=object_path,
                    manifest_path=manifest_path,
                    representation_kind=representation_kind,
                    representation_details=representation_details,
                )
                _write_json(manifest_path, manifest)
            return {
                **manifest,
                "deduplicated": True,
                "duplicate_input_name": source.name,
                "duplicate_input_path": str(source.resolve()),
            }

        self._persist_object(object_path, raw, raw_sha256)
        source_record = self._ensure_source_record(
            source_memory_id,
            project_id=project_id,
            source=source,
            raw_sha256=raw_sha256,
            byte_size=byte_size,
            extension=extension,
            media_type=media_type,
            object_path=object_path,
            ingestion_fingerprint=ingestion_fingerprint,
        )

        document_record = self.memory.store(
            representation,
            kind="DOCUMENT",
            source="PL-13 File Ingestion",
            record_id=document_memory_id,
            project_id=project_id,
            source_id=source_record["id"],
            metadata={
                "schema": "ivdivo.personal_ai.ingested_document/0.1",
                "raw_sha256": raw_sha256,
                "representation_sha256": representation_sha256,
                "ingestion_fingerprint": ingestion_fingerprint,
                "representation_kind": representation_kind,
                "media_type": media_type,
                "extension": extension,
                "byte_size": byte_size,
                "object_path": str(object_path.relative_to(self.home)),
                **representation_details,
            },
        )

        manifest = {
            "schema": "ivdivo.personal_ai.file_ingestion_manifest/0.1",
            "project_id": project_id,
            "source_name": source.name,
            "source_path": str(source.resolve()),
            "extension": extension,
            "media_type": media_type,
            "byte_size": byte_size,
            "raw_sha256": raw_sha256,
            "representation_sha256": representation_sha256,
            "representation_kind": representation_kind,
            "representation_details": representation_details,
            "ingestion_fingerprint": ingestion_fingerprint,
            "object_path": str(object_path.relative_to(self.home)),
            "manifest_path": str(manifest_path.relative_to(self.home)),
            "source_memory_id": source_record["id"],
            "document_memory_id": document_record["id"],
            "ingested_at": document_record["updated_at"],
            "deduplicated": False,
        }
        _write_json(manifest_path, manifest)
        return manifest

    def _existing_document(self, document_memory_id: str) -> dict[str, Any] | None:
        try:
            return self.memory.get(document_memory_id)
        except KeyError:
            return None

    def _verify_existing(
        self,
        document: dict[str, Any],
        *,
        project_id: str,
        raw_sha256: str,
        representation_sha256: str,
        source_memory_id: str,
        object_path: Path,
    ) -> dict[str, Any]:
        metadata = document.get("metadata", {})
        expected = {
            "project_id": project_id,
            "raw_sha256": raw_sha256,
            "representation_sha256": representation_sha256,
            "source_id": source_memory_id,
        }
        actual = {
            "project_id": document.get("project_id"),
            "raw_sha256": metadata.get("raw_sha256"),
            "representation_sha256": metadata.get("representation_sha256"),
            "source_id": document.get("source_id"),
        }
        if document.get("status") != "ACTIVE" or actual != expected:
            raise IngestionIntegrityError("existing ingestion record conflicts with expected identity")
        source_record = self.memory.get(source_memory_id)
        source_metadata = source_record.get("metadata", {})
        if (
            source_record.get("status") != "ACTIVE"
            or source_record.get("project_id") != project_id
            or source_metadata.get("raw_sha256") != raw_sha256
        ):
            raise IngestionIntegrityError("existing source record conflicts with expected identity")
        self._verify_object(object_path, raw_sha256)
        return source_record

    def _verify_manifest(
        self,
        manifest: dict[str, Any],
        *,
        document: dict[str, Any],
        raw_sha256: str,
        representation_sha256: str,
        object_path: Path,
        manifest_path: Path,
    ) -> None:
        expected = {
            "project_id": document["project_id"],
            "raw_sha256": raw_sha256,
            "representation_sha256": representation_sha256,
            "source_memory_id": document["source_id"],
            "document_memory_id": document["id"],
            "object_path": str(object_path.relative_to(self.home)),
            "manifest_path": str(manifest_path.relative_to(self.home)),
        }
        actual = {key: manifest.get(key) for key in expected}
        if manifest.get("schema") != "ivdivo.personal_ai.file_ingestion_manifest/0.1" or actual != expected:
            raise IngestionIntegrityError("persisted ingestion manifest conflicts with memory/object identity")

    def _manifest_from_existing(
        self,
        document: dict[str, Any],
        source_record: dict[str, Any],
        *,
        media_type: str,
        extension: str,
        object_path: Path,
        manifest_path: Path,
        representation_kind: str,
        representation_details: dict[str, Any],
    ) -> dict[str, Any]:
        metadata = document["metadata"]
        source_metadata = source_record["metadata"]
        return {
            "schema": "ivdivo.personal_ai.file_ingestion_manifest/0.1",
            "project_id": document["project_id"],
            "source_name": source_metadata["source_name"],
            "source_path": source_metadata["source_path"],
            "extension": extension,
            "media_type": media_type,
            "byte_size": metadata["byte_size"],
            "raw_sha256": metadata["raw_sha256"],
            "representation_sha256": metadata["representation_sha256"],
            "representation_kind": representation_kind,
            "representation_details": representation_details,
            "ingestion_fingerprint": metadata["ingestion_fingerprint"],
            "object_path": str(object_path.relative_to(self.home)),
            "manifest_path": str(manifest_path.relative_to(self.home)),
            "source_memory_id": document["source_id"],
            "document_memory_id": document["id"],
            "ingested_at": document["updated_at"],
            "deduplicated": False,
        }

    def _persist_object(self, object_path: Path, raw: bytes, raw_sha256: str) -> None:
        object_path.parent.mkdir(parents=True, exist_ok=True)
        if object_path.exists():
            self._verify_object(object_path, raw_sha256)
            return
        tmp = object_path.with_suffix(".tmp")
        tmp.write_bytes(raw)
        if _sha256_bytes(tmp.read_bytes()) != raw_sha256:
            tmp.unlink(missing_ok=True)
            raise IngestionIntegrityError("raw object checksum failed before commit")
        tmp.replace(object_path)
        self._verify_object(object_path, raw_sha256)

    def _verify_object(self, object_path: Path, raw_sha256: str) -> None:
        if not object_path.is_file():
            raise IngestionIntegrityError("ingested raw object is missing")
        actual = _sha256_bytes(object_path.read_bytes())
        if actual != raw_sha256:
            raise IngestionIntegrityError("ingested raw object checksum mismatch")

    def _ensure_source_record(
        self,
        source_memory_id: str,
        *,
        project_id: str,
        source: Path,
        raw_sha256: str,
        byte_size: int,
        extension: str,
        media_type: str,
        object_path: Path,
        ingestion_fingerprint: str,
    ) -> dict[str, Any]:
        try:
            existing = self.memory.get(source_memory_id)
        except KeyError:
            existing = None
        if existing is not None:
            metadata = existing.get("metadata", {})
            if (
                existing.get("status") != "ACTIVE"
                or existing.get("project_id") != project_id
                or metadata.get("raw_sha256") != raw_sha256
            ):
                raise IngestionIntegrityError("existing source record conflicts with expected identity")
            return existing

        descriptor = {
            "source_name": source.name,
            "source_path": str(source.resolve()),
            "raw_sha256": raw_sha256,
            "byte_size": byte_size,
            "extension": extension,
            "media_type": media_type,
            "object_path": str(object_path.relative_to(self.home)),
            "ingestion_fingerprint": ingestion_fingerprint,
        }
        return self.memory.store(
            json.dumps(descriptor, sort_keys=True, ensure_ascii=False),
            kind="SOURCE",
            source="PL-13 File Ingestion",
            record_id=source_memory_id,
            project_id=project_id,
            metadata={
                "schema": "ivdivo.personal_ai.ingested_source/0.1",
                **descriptor,
            },
        )
