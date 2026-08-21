# IVDIVO — INTERRUPTION LEARNING EVIDENCE CONTRACT v1.0

**Status:** ENGINEERING CANDIDATE / SI-0014  
**Date:** 2026-08-21

## Purpose
Turn future interruption/recovery incidents into measurable Self-Improvement evidence rather than anecdotes.

## Event fields
Each event records:
- event/project/work-unit IDs;
- recovery decision;
- whether interruption was real or synthetic;
- false-resume flag;
- false-stop flag;
- duplicate work avoided;
- writes reconciled;
- checkpoint byte/tool-call overhead;
- recovery tool-call overhead.

## Safety law
`false_resume > 0` forces `HOLD` for promotion review.

No real interruption evidence forces `HOLD`.

Fewer than three real recoveries or fewer than two independent projects remains `CONTINUE_PILOT`.

Only after minimum cross-project evidence, zero false resume and acceptable false-stop rate may the summarizer return `ELIGIBLE_FOR_PROMOTION_REVIEW`.

That result is advisory only. It does not mutate the Self-Improvement registry.

## Evidence classes
Synthetic fixtures = INTERNAL MACHINE EVIDENCE.
Real page/runtime/store/provider interruption with durable readback = PRODUCTION RECOVERY EVIDENCE.
Human/Founder approval, artistic quality and market evidence remain separate evidence classes.

## Proof obligations
Tests must prove:
- no-real-evidence HOLD;
- any false resume HOLD;
- insufficient cross-project evidence CONTINUE_PILOT;
- excessive false-stop rate NARROW;
- minimum clean cross-project evidence only becomes eligible for review, never auto-promoted.
