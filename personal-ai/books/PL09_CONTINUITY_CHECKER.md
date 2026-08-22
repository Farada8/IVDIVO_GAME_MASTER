# PL-09 Continuity Checker

PL-09 is a deterministic contradiction detector over **structured continuity evidence**. It is not a free-text claim that the whole manuscript has been understood.

## Acceptance contract

Known fixtures must yield issues with:
- deterministic `issue_id`;
- severity: `FATAL`, `MAJOR`, `MINOR`, or `STYLE`;
- chapter, category, subject, rule id and suggested fix;
- exactly two evidence references in `evidence_pair`;
- human-readable `evidence_a` and `evidence_b` excerpts.

Blocking severities are `FATAL` and `MAJOR`.

## Supported deterministic rules

- stable observation conflicts: NAME, AGE, APPEARANCE, RELATIONSHIP, DATE_TIME, LOCATION, PROP;
- inverse event order (`A before B` and `B before A`);
- character knowledge before the earliest supplied reveal;
- repeated completion of a non-repeatable event.

Facts are only compared inside their declared scope. A location in scene A and a different location in scene B is not a contradiction by itself.

## Evidence boundary

Input extraction is a separate problem. PL-09 only evaluates the normalized facts supplied to it. Therefore:
- zero detected issues means `NO_BLOCKING_ISSUES_DETECTED`, not proof of perfect continuity;
- `automatic_pass_allowed` is always `false`;
- clean reports require manual/independent review before PL-08 continuity PASS is written;
- PL-09 never mutates the PL-08 gate automatically.

## Content binding

A report stores both:
- `book_content_sha256` from the hash-bound PL-08 reviewed content;
- `input_sha256` from the structured evidence payload.

The deterministic report id is derived from those hashes. If reviewed story/manuscript content changes, the report id/content hash changes and the old report cannot be mistaken for evidence about the new content version.

## Persistence

Each run writes:
- JSON report under `book/continuity/`;
- readable Markdown report under `book/continuity/`;
- PL-02 `OUTPUT` memory containing the report and metadata.

## CLI

```bash
python personal-ai/run.py --home /tmp/pai book check-continuity PROJECT continuity-input.json
python personal-ai/run.py --home /tmp/pai book check-continuity PROJECT continuity-input.json --enforce
```

`--enforce` returns exit code 2 when any `FATAL` or `MAJOR` issue exists.

The persisted acceptance fixture is `books/fixtures/pl09_known_contradictions.json`.
