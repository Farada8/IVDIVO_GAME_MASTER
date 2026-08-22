# BOOK INTELLIGENCE v1.1 — EXACT REPOSITORY CI GATE

Purpose: trigger the Book Intelligence v1.1 pull-request workflow against the exact repository runtime and regression test files already present on main.

No production authority or mechanism is changed by this file.

Acceptance:
- `BOOK_INTELLIGENCE_ENGINE/tests/test_book_intelligence_v1_1.py` passes;
- `tools/ivdivo_book_intelligence.py` compiles;
- CI evidence is recorded separately from real-project validation.
