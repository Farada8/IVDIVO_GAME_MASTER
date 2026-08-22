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

## Project DONE scope

PL-08 preserves its registered behavior of setting the parent project status to `DONE` when the internal book-production state reaches `FINAL`. That status is explicitly scoped as:

- `completion_scope = INTERNAL_BOOK_PRODUCTION`
- `external_artifact_completion = NOT_ASSERTED`

Therefore:

`PROJECT_DONE != EXTERNAL_ARTIFACT_DONE`.

`FINAL` means the PL-08 internal state machine has completed after its continuity authorization. It does **not** mean a manuscript/export/package has been written to Google Drive, GitHub or another external provider; it does not mean canonical placement was verified; and it does not mean publishing/distribution occurred.

Any task that claims an external artifact must separately declare `requires_artifact_placement_receipt=true` and pass the Artifact Placement completion gate before that task may become `DONE`. Reaching PL-08 `FINAL` never completes or overrides such a task.

## Hash-bound continuity authorization

A PASS is not a timeless flag. When the gate is recorded, PL-08 computes a deterministic SHA-256 over the continuity-relevant book inputs:
- `canon.md`;
- `characters.json`, `locations.json`, `timeline.json`, `plot.json`;
- every file under `chapters/` and `drafts/`, ordered by relative path.

The digest is stored as `continuity_gate.content_sha256`. Immediately before `FINAL`, the digest is recomputed. If any reviewed story/manuscript input has changed, been added or removed, FINAL is rejected as a **stale continuity PASS**. The book remains at `CONTINUITY` and requires an explicit recheck; there is no silent state mutation or automatic re-approval.

`critique/`, `continuity/` and `final/` are intentionally excluded from the reviewed-content digest because they contain review/output artifacts rather than the story/manuscript inputs being authorized.

PL-08 does not claim to perform the continuity analysis itself. PL-09 owns automatic contradiction detection. PL-08 provides the production structure, state route, content-version binding and enforcement gate.

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
