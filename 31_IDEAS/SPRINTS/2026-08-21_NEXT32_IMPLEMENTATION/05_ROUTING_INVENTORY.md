# CURRENT ROUTING INVENTORY — CANDIDATE N07/N08

## Controlling GitHub entrypoints
- `CURRENT_IVDIVO_SYSTEM_STATE.json` — ROUTING AUTHORITY / aggregate resume pointer.
- `CURRENT_IVDIVO_WRITING_PRODUCTION_AUTHORITY.md` — DOMAIN AUTHORITY for writing/story production.
- `IVDIVO_NARRATIVE_OS/13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md` — AUTHORITY for persisted-state continuation and concurrent rebase.
- `CURRENT_IVDIVO_SELF_IMPROVEMENT_AUTHORITY.md` — DOMAIN AUTHORITY for improvement lifecycle.
- `CURRENT_IVDIVO_SELF_IMPROVEMENT_STATE.json` — CURRENT MACHINE/ROUTING STATE, not story canon.
- `IVDIVO_NARRATIVE_OS/15_REFERENCE_MECHANISM_UPGRADE_PACK_v1.0.md` — DOMAIN OVERLAY / reference mechanism router.
- `CURRENT_IVDIVO_AUDIO_PRODUCTION_AUTHORITY.md` — DOMAIN AUTHORITY when active stage is audio.
- `PROJECT_STATES/...` — PROJECT ROUTING STATE subordinate to project canon/source-of-truth.

## Drive entrypoints
- `00_CURRENT_PROMPT_AUTHORITY_INDEX v1.1` — DRIVE ENTRYPOINT MIRROR.
- `CURRENT_PROMPTS_v2.2` — CURRENT PROMPT MIRROR.
- `CURRENT_WORKSTATE_v2.2` — CURRENT WORKSTATE MIRROR.
- `00A_READ_ME_FIRST_MANDATORY_STUDIO_ROUTER_v5.3` — DRIVE ROUTER.
- `03_PROMPT_ROUTER_P01_P53_MASTER_COMMANDS_v5.3` — DOMAIN/GENRE PROMPT OVERLAY.
- `00 IVDIVO — START HERE — Cross-Conversation Router v1.2` — DRIVE ENTRYPOINT.
- `00_START_HERE — MULTI-MODEL PRODUCTION MEMORY PROTOCOL v1.1` — MULTI-MODEL ENTRYPOINT.
- `SUPPLEMENTAL — CURRENT_PROMPTS_AND_SYSTEM_STATE_v1.3` — COMPATIBILITY MAP / HISTORY, never primary.

## Smallest cold-start path
`Founder instruction -> CURRENT_IVDIVO_SYSTEM_STATE -> active project state -> current domain authority -> Drive Prompt Authority Index only if prompt/program routing is needed -> task-specific overlay -> execute -> verify -> persist`.

## Cold-read validation N08
Three simulated task classes were routed without chat memory:
1. BOOK/WRITING: system state -> writing authority -> project state/Book status -> current phase. PASS.
2. COMMERCIAL DRAMA: system state -> project state -> Drive prompt authority/router only for generation/QA overlay. PASS.
3. AUDIO: system state -> project execution state -> audio production authority; writing authority remains source-text guard. PASS.

### Failure conditions
- starting from the supplemental compatibility map as primary;
- treating Drive mirror as higher than locked project source-of-truth;
- using prompt router to infer project phase;
- treating aggregate text-complete labels as exact project-state facts;
- entering audio through generic writing prompts after a current project audio state exists.

**N07 verdict:** PASS candidate inventory.
**N08 verdict:** INTERNAL COLD-READ PASS on current persisted pointers; human/independent-model parity still remains a separate evidence class.