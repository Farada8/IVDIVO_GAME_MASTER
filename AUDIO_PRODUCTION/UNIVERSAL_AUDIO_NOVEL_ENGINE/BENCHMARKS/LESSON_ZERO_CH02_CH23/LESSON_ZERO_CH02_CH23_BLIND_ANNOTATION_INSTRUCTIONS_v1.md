# LESSON ZERO CH02–CH23 — Blind Speaker Annotation Instructions v1

Status: `GROUND_TRUTH_COLLECTION / ENGINE PREDICTIONS HIDDEN`

Annotate every row in the CSV/JSONL packet without consulting the speaker-attribution engine, GitHub candidate registry, or any engine prediction output.

For each row:
- `ground_truth_speaker`: canonical speaker/role name if ownership is unambiguous.
- `disposition`: normally `SCORABLE_MATCH`; otherwise use one allowed EXCLUDE reason from the freeze manifest.
- `notes`: short evidence only when ambiguity/exclusion needs explanation.

Do not delete rows. Do not add engine predictions. Do not change candidate IDs, quote text, or context.

The packet intentionally hides which rule selected each row and what speaker the engine predicts. After independent annotation is complete, the frozen runtime is scored against this answer key.
