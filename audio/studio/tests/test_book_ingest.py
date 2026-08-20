import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
import book_ingest as bi


class BookIngestTests(unittest.TestCase):
    def test_chapter_detection_and_exact_units(self):
        text = (
            "Front note.\r\n\r\n"
            "CHAPTER ONE\r\n"
            "First paragraph.\r\nStill first paragraph.\r\n\r\n"
            "Second paragraph.\r\n\r\n"
            "CHAPTER TWO\r\n"
            "Third paragraph.\r\n"
        )
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "book.txt"
            p.write_bytes(text.encode("utf-8"))
            result = bi.ingest(p, "TEST_BOOK", "1.0")
            self.assertEqual(result["manifest"]["gate"], "PASS")
            self.assertEqual(result["manifest"]["normalization_changes"], ["LINE_ENDINGS_TO_LF"])
            self.assertEqual(result["chapters"]["chapters"][0]["title"], "FRONT_MATTER")
            titles = [c["title"] for c in result["chapters"]["chapters"]]
            self.assertIn("CHAPTER ONE", titles)
            self.assertIn("CHAPTER TWO", titles)
            normalized = result["normalized_text"]
            for unit in result["units"]["units"]:
                self.assertEqual(
                    normalized[unit["source_start"]:unit["source_end"]],
                    unit["exact_text"],
                )

    def test_no_chapters_becomes_book_body(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "book.md"
            p.write_text("A paragraph.\n\nAnother paragraph.\n", encoding="utf-8")
            result = bi.ingest(p, "TEST", "1")
            self.assertEqual(result["manifest"]["gate"], "PASS")
            self.assertEqual(result["chapters"]["chapters"][0]["title"], "BOOK_BODY")
            self.assertEqual(result["manifest"]["source_unit_count"], 2)

    def test_unsupported_format_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "book.pdf"
            p.write_bytes(b"not a real pdf")
            with self.assertRaises(ValueError):
                bi.ingest(p, "TEST", "1")

    def test_non_utf8_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "book.txt"
            p.write_bytes(b"\xff\xfe\x00\x01")
            with self.assertRaises(ValueError):
                bi.ingest(p, "TEST", "1")


if __name__ == "__main__":
    unittest.main()
