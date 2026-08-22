from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingestion import (
    MAX_FILE_BYTES,
    FileIngestionError,
    FileIngestionService,
    IngestionIntegrityError,
    UnsupportedFileTypeError,
)
from memory.store import MemoryStore
from projects.manager import ProjectStateManager


class FileIngestionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        self.inputs = Path(self.tmp.name) / "inputs"
        self.inputs.mkdir()
        self.projects = ProjectStateManager(self.home)
        self.projects.create_project("alpha", "Alpha")
        self.projects.create_project("beta", "Beta")
        self.service = FileIngestionService(self.home)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_bytes(self, name: str, value: bytes) -> Path:
        path = self.inputs / name
        path.write_bytes(value)
        return path

    def test_markdown_ingest_hashes_represents_persists_and_links_memory(self) -> None:
        raw = b"# Title\r\n\r\nBody text.\r\n"
        path = self.write_bytes("reference.md", raw)
        result = self.service.ingest("alpha", path)

        expected_raw_hash = hashlib.sha256(raw).hexdigest()
        expected_representation = "# Title\n\nBody text."
        expected_rep_hash = hashlib.sha256(expected_representation.encode("utf-8")).hexdigest()
        self.assertFalse(result["deduplicated"])
        self.assertEqual(result["raw_sha256"], expected_raw_hash)
        self.assertEqual(result["representation_sha256"], expected_rep_hash)
        self.assertEqual(result["representation_kind"], "normalized_utf8_markdown")

        object_path = self.home / result["object_path"]
        manifest_path = self.home / result["manifest_path"]
        self.assertEqual(object_path.read_bytes(), raw)
        self.assertEqual(hashlib.sha256(object_path.read_bytes()).hexdigest(), expected_raw_hash)
        persisted_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(persisted_manifest["document_memory_id"], result["document_memory_id"])

        memory = MemoryStore(self.home / "runtime" / "state.db")
        document = memory.get(result["document_memory_id"])
        source = memory.get(result["source_memory_id"])
        self.assertEqual(document["kind"], "DOCUMENT")
        self.assertEqual(document["content"], expected_representation)
        self.assertEqual(document["source_id"], source["id"])
        self.assertEqual(source["kind"], "SOURCE")
        self.assertEqual(document["metadata"]["raw_sha256"], expected_raw_hash)
        trace = memory.trace_source(document["id"])
        self.assertEqual([item["id"] for item in trace["chain"]], [document["id"], source["id"]])

    def test_same_project_same_content_same_handler_is_deduplicated(self) -> None:
        raw = b"same source\n"
        first_path = self.write_bytes("first.md", raw)
        second_path = self.write_bytes("renamed.md", raw)
        first = self.service.ingest("alpha", first_path)
        second = self.service.ingest("alpha", second_path)

        self.assertFalse(first["deduplicated"])
        self.assertTrue(second["deduplicated"])
        self.assertEqual(first["document_memory_id"], second["document_memory_id"])
        self.assertEqual(first["source_memory_id"], second["source_memory_id"])
        self.assertEqual(first["manifest_path"], second["manifest_path"])
        self.assertEqual(second["source_name"], "first.md")
        self.assertEqual(second["duplicate_input_name"], "renamed.md")

        memory = MemoryStore(self.home / "runtime" / "state.db")
        self.assertEqual(len(memory.versions(first["document_memory_id"])), 1)
        self.assertEqual(len(memory.versions(first["source_memory_id"])), 1)

    def test_cross_project_provenance_is_separate_but_raw_object_is_shared(self) -> None:
        path = self.write_bytes("shared.txt", b"identical bytes")
        alpha = self.service.ingest("alpha", path)
        beta = self.service.ingest("beta", path)

        self.assertEqual(alpha["raw_sha256"], beta["raw_sha256"])
        self.assertEqual(alpha["object_path"], beta["object_path"])
        self.assertNotEqual(alpha["source_memory_id"], beta["source_memory_id"])
        self.assertNotEqual(alpha["document_memory_id"], beta["document_memory_id"])
        self.assertNotEqual(alpha["manifest_path"], beta["manifest_path"])

    def test_same_bytes_different_handlers_share_raw_object_but_not_document(self) -> None:
        raw = b"plain content"
        txt = self.service.ingest("alpha", self.write_bytes("same.txt", raw))
        md = self.service.ingest("alpha", self.write_bytes("same.md", raw))
        self.assertEqual(txt["raw_sha256"], md["raw_sha256"])
        self.assertEqual(txt["object_path"], md["object_path"])
        self.assertNotEqual(txt["ingestion_fingerprint"], md["ingestion_fingerprint"])
        self.assertNotEqual(txt["document_memory_id"], md["document_memory_id"])

    def test_json_is_parsed_and_canonically_represented(self) -> None:
        path = self.write_bytes("data.json", b'{"z":2,"a":1}')
        result = self.service.ingest("alpha", path)
        document = MemoryStore(self.home / "runtime" / "state.db").get(
            result["document_memory_id"]
        )
        self.assertEqual(result["representation_kind"], "canonical_json")
        self.assertEqual(document["metadata"]["json_root_type"], "dict")
        self.assertEqual(json.loads(document["content"]), {"a": 1, "z": 2})
        self.assertLess(document["content"].index('"a"'), document["content"].index('"z"'))

    def test_csv_is_validated_and_records_shape_metadata(self) -> None:
        path = self.write_bytes("table.csv", b"name,value\na,1\nb,2\n")
        result = self.service.ingest("alpha", path)
        document = MemoryStore(self.home / "runtime" / "state.db").get(
            result["document_memory_id"]
        )
        self.assertEqual(document["metadata"]["row_count"], 3)
        self.assertEqual(document["metadata"]["max_columns"], 2)
        self.assertEqual(result["representation_kind"], "normalized_utf8_csv")

    def test_invalid_and_unsupported_inputs_fail_closed(self) -> None:
        cases = [
            ("bad.bin", b"abc", UnsupportedFileTypeError),
            ("bad.txt", b"\xff\xfe", FileIngestionError),
            ("empty.md", b"", FileIngestionError),
            ("bad.json", b"{broken", FileIngestionError),
        ]
        for name, raw, error in cases:
            with self.subTest(name=name):
                path = self.write_bytes(name, raw)
                with self.assertRaises(error):
                    self.service.ingest("alpha", path)

    def test_oversized_input_fails_before_persistence(self) -> None:
        path = self.inputs / "large.txt"
        with path.open("wb") as handle:
            handle.truncate(MAX_FILE_BYTES + 1)
        with self.assertRaisesRegex(FileIngestionError, "exceeds"):
            self.service.ingest("alpha", path)

    @unittest.skipIf(os.name == "nt", "symlink behavior requires POSIX CI semantics")
    def test_symlink_input_is_rejected(self) -> None:
        target = self.write_bytes("target.md", b"target")
        link = self.inputs / "link.md"
        link.symlink_to(target)
        with self.assertRaisesRegex(FileIngestionError, "symlink"):
            self.service.ingest("alpha", link)

    def test_tampered_raw_object_blocks_duplicate_acceptance(self) -> None:
        path = self.write_bytes("tamper.md", b"trusted bytes")
        first = self.service.ingest("alpha", path)
        (self.home / first["object_path"]).write_bytes(b"tampered")
        with self.assertRaisesRegex(IngestionIntegrityError, "checksum mismatch"):
            self.service.ingest("alpha", path)

    def test_tampered_manifest_blocks_duplicate_acceptance(self) -> None:
        path = self.write_bytes("manifest.md", b"trusted manifest")
        first = self.service.ingest("alpha", path)
        manifest_path = self.home / first["manifest_path"]
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["document_memory_id"] = "tampered-id"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(IngestionIntegrityError, "manifest conflicts"):
            self.service.ingest("alpha", path)

    def test_cli_ingest_file_roundtrip(self) -> None:
        path = self.write_bytes("cli.txt", b"CLI fixture\n")
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT)
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "run.py"),
                "--home",
                str(self.home),
                "ingest",
                "file",
                "alpha",
                str(path),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertFalse(result["deduplicated"])
        self.assertTrue((self.home / result["manifest_path"]).is_file())
        self.assertEqual(
            MemoryStore(self.home / "runtime" / "state.db").get(result["document_memory_id"])["kind"],
            "DOCUMENT",
        )


if __name__ == "__main__":
    unittest.main()
