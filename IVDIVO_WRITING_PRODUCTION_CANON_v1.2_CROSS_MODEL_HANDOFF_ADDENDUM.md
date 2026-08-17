# IVDIVO — WRITING & STORY PRODUCTION CANON v1.2 — CROSS-MODEL HANDOFF ADDENDUM

**Status:** CANON ADDENDUM  
**Effective:** 2026-08-17  
**Authority:** Founder newest direct instruction  
**Relation:** Extends `IVDIVO_WRITING_PRODUCTION_CANON.md` v1.0 and `IVDIVO_WRITING_PRODUCTION_CANON_v1.1_STUDIO_V5_ADDENDUM.md`. Where this addendum conflicts with older routing/storage practice, this addendum controls.

## 1. PURPOSE

IVDIVO production may involve GPT, Claude, Grok and other external review passes. Chat-session memory is not a reliable production store. Future-critical state must be persisted in Drive/GitHub when the connected tools allow it.

## 2. CROSS-MODEL HANDOFF GATE

After any substantive production/review session:

1. Claude analysis/critique is stored under `00F_CROSS_MODEL_HANDOFF/CLAUDE_FEEDBACK`.
2. Grok analysis/critique is stored under `00F_CROSS_MODEL_HANDOFF/GROK_FEEDBACK`.
3. GPT experimental rewrites / patch candidates / non-authority drafts are stored under `00F_CROSS_MODEL_HANDOFF/GPT_DRAFTS` unless promoted into the project production authority.
4. Changes to active project, production stage, canon pointer, open defect or next action update `CURRENT_WORKSTATE`.
5. Changes to governing prompts or production process update `CURRENT_PROMPTS` and the Studio Router/Master when system-level.
6. `06_PROJECTS_CROSS_MODEL_INDEX` stores pointers to production authority, not duplicate canonical masters.
7. On startup, a model must read CURRENT_PROMPTS + CURRENT_WORKSTATE + active project authority + new source-specific feedback before asking Founder to repeat recoverable context.
8. Missing feedback/project/prompt/canon details must be marked UNKNOWN. Never invent data to make the registry look complete.
9. If write access is unavailable, the assistant must state that the handoff was not persisted and must not claim a save.

## 3. ONE AUTHORITY, MANY POINTERS

Cross-model handoff is operational memory, not story authority.

Authority remains:
1. Founder newest direct instruction;
2. approved/locked project canon and production authority;
3. current IVDIVO production canon / governing Studio Router;
4. specialized modules;
5. working drafts / external feedback / reference mechanisms.

Do not copy a locked recording master/manuscript into handoff folders merely for convenience. Store a pointer/index entry instead. This prevents parallel pseudo-canons.

## 4. EXTERNAL FEEDBACK LAW

External model feedback is never silently canonized.

Each feedback artifact should identify:
- source model;
- date;
- project and material reviewed;
- FATAL / MAJOR / MEDIUM / POLISH findings where applicable;
- proposed repair;
- Founder/integrator disposition: ACCEPTED / PARTIAL / REJECTED / UNRESOLVED.

Original feedback remains available after integration so later models can distinguish source criticism from accepted canon.

## 5. PROJECT REGISTRY LAW

The cross-model registry may contain VERIFIED projects and UNKNOWN slots.
Do not infer a missing sixth project merely because a previous note says “six projects.” Count completeness is lower priority than authority accuracy.

LESSON ZERO remains governed by its own Book One status and must not be reassigned into another roster merely to fill an index slot.

## 6. CURRENT ROUTER

The governing Drive router includes this requirement under **CROSS-MODEL HANDOFF GATE — MANDATORY**. Current Drive router at the time of this addendum: `00A_READ_ME_FIRST_MANDATORY_STUDIO_ROUTER_v5.2`.

## 7. FINAL RULE

**Do not let production truth exist only in a disappearing chat.**
Persist the minimum sufficient state to let the next qualified model restore the work without guessing, while preserving one clear canon authority.
