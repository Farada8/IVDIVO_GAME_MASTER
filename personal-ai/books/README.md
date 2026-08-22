# PL-08 Book Production Core

Persisted book-production state machine for one existing Personal AI project.

## Required book structure

```text
book/
├── book.yaml
├── state.json
├── canon.md
├── characters.json
├── locations.json
├── timeline.json
├── plot.json
├── chapters/
├── drafts/
├── critique/
├── continuity/
└── final/
```

## State route

`IDEA -> CANON -> STORY_BIBLE -> OUTLINE -> CHAPTER_PLAN -> DRAFT -> CRITIQUE -> REWRITE -> CONTINUITY -> FINAL`

Transitions are strictly one step at a time. Stage skipping is rejected.

`CONTINUITY -> FINAL` is fail-closed: it is impossible unless the persisted continuity gate is `PASS`. A `FAIL` gate leaves the book at `CONTINUITY` and marks the parent project `BLOCKED`. A later explicit PASS may unblock it.

PL-08 does not claim to perform the continuity analysis itself. PL-09 owns automatic contradiction detection. PL-08 only provides the production structure, state route and enforcement gate.

## CLI

```bash
python personal-ai/run.py --home /tmp/pai project create demo
python personal-ai/run.py --home /tmp/pai book init demo --title "Demo Book"
python personal-ai/run.py --home /tmp/pai book status demo
python personal-ai/run.py --home /tmp/pai book advance demo
python personal-ai/run.py --home /tmp/pai book advance demo --to CANON
python personal-ai/run.py --home /tmp/pai book continuity demo --pass-gate --evidence "fixture continuity check passed"
```

The continuity command is admissible only while the book is in `CONTINUITY`.
