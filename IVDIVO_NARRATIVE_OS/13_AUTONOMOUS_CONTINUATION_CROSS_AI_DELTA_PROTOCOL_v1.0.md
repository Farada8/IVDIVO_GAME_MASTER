# IVDIVO — AUTONOMOUS CONTINUATION / CROSS-AI DELTA PROTOCOL v1.0

**Status:** CANONICAL OPERATING ADDENDUM  
**Established:** 2026-08-21  
**Scope:** all IVDIVO book, story, dorama, audio, production, research and multi-model workrooms

## 0. FOUNDER INTENT

The Founder must not have to type `и / дальше / продолжай` after every completed micro-step.

Those words remain valid shorthand, but they are **not a prerequisite** for continuation.

On every substantive project turn, when the active project and authority can be resolved from persisted sources, the studio must restore state and continue from the verified frontier automatically.

The assistant cannot initiate a new chat turn by itself. Within an active user turn, however, it must not stop merely because one small dependent subtask finished if further required work is already unblocked.

## 1. PRIMARY STATE MACHINE

`RESTORE -> DELTA SWEEP -> RECONCILE -> EXECUTE -> QA -> PERSIST -> VERIFY -> ADVANCE -> HANDOFF OR REAL BLOCKER`

### RESTORE
Resolve:
- ACTIVE PROJECT / BOOK / LINE;
- CURRENT AUTHORITY;
- CURRENT PHASE;
- LAST COMPLETED ARTIFACT;
- OPEN GATES;
- CURRENT BLOCKER;
- HIGHEST UNBLOCKED NEXT OBLIGATION.

Do not infer authority from chat memory or newest timestamp alone.

### DELTA SWEEP
Before substantial continuation, check only the surfaces capable of materially changing the decision:
1. Founder newest direct instruction / Project context.
2. GitHub current authority, current status files and recent relevant commits.
3. Google Drive current authority/index, project folder, latest handoff and accepted external-feedback records.
4. Multi-Model Production Memory when the line uses GPT/Claude/Grok or specialist review.
5. File Library/reference books only when a reference mechanism can materially improve the current decision.

Do not run a library-wide sweep for trivial/local work. Route by decision risk.

### RECONCILE
For every apparent new item determine:
`CURRENT / CANON / WORKING / OPTION / UNKNOWN / REFERENCE ONLY / SUPERSEDED / REJECTED / SESSION-ONLY`.

Authority is determined by explicit status + hierarchy + content, not modification time alone.

If GitHub and Drive differ:
- Founder newest instruction wins;
- current explicitly approved canonical source wins;
- a newer verified Drive frontier waiting for sync must be reconciled, not discarded;
- ambiguity fails closed rather than silently selecting a branch.

## 2. AUTONOMOUS CONTINUATION LAW

Any substantive instruction inside an established active line invokes continuation behavior unless the Founder explicitly asks to switch projects, brainstorm from zero, compare old versions, or stop after a bounded task.

After fulfilling the explicit request:
1. identify any mandatory dependent stage unlocked by that result;
2. execute it in the same work block when tools/data/authority allow;
3. repeat until a real stop condition is reached.

Do not end with `следующим шагом я могу...` when the step is already executable and belongs to the same requested workflow.

### REAL STOP CONDITIONS
Stop only for:
- unresolved Founder decision that materially changes direction;
- FATAL defect;
- missing authority/continuity fact that cannot be safely inferred;
- required external/human/specialist evidence not yet available;
- required LIVE provider execution or physical-world action unavailable to current tools;
- safety/legal/rights constraint;
- explicit Founder request to stop or limit scope.

A completed micro-artifact is not a stop condition.

## 3. NO REDUNDANT REWORK LAW

Before creating an artifact, ask:
`DOES A CURRENT ACCEPTED ARTIFACT ALREADY SATISFY THIS STAGE?`

If yes:
- use it;
- verify only the relevant assumptions;
- advance to the next unmet gate.

Do not repeat audits, rewrite locked material, regenerate manifests, or rerun ideation merely because a new chat has started.

Reopen completed work only for:
- Founder instruction;
- new evidence-backed FATAL/MAJOR;
- repeated human/external comprehension failure;
- factual/continuity error;
- changed provider/technical contract that invalidates execution;
- explicit version migration requirement.

## 4. CROSS-AI ROLE ROUTING

External models do not vote on canon.

Default division where useful:
- **GPT:** primary integrator, production execution, drafting/editing, continuity reconciliation, persistence, final assembly.
- **Claude:** independent architecture/causality/character/romance/systems/domain Red Team.
- **Grok:** orthogonal adversarial pressure, cold-audience/retention/market/promo/visual challenge, alternative diagnosis, anti-generated-text attack.
- **Specialist/human:** narrow factual, legal, medical, technical, performance or target-audience validation where real expertise/listening is required.

Run independent first-pass review when independence improves audit quality. Do not contaminate every reviewer with the previous model's conclusion.

## 5. EXTERNAL FINDING INTEGRATION CONTRACT

Every external finding is decomposed into:
1. `DIAGNOSIS` — what allegedly fails and where;
2. `EVIDENCE` — text/audio/data/support;
3. `PROPOSED FIX` — optional and evaluated separately;
4. `SEVERITY` — FATAL / MAJOR / MEDIUM / POLISH;
5. `DECISION` — ACCEPT / ACCEPT WITH MODIFICATION / HOLD FOR TEST / REJECT;
6. `EARLIEST FAILING LAYER`;
7. `AFFECTED DOWNSTREAM MATERIAL`;
8. `REGRESSION REQUIRED`.

A correct diagnosis does not automatically make the reviewer's proposed rewrite correct.

Do not merge models by majority vote. Prefer causal evidence, character truth, continuity and demonstrated audience/production effect.

Accepted fixes are applied at the earliest responsible layer, then regression runs only on dependent downstream material.

## 6. PERSISTENCE / SHARED MEMORY LAW

No material production decision may remain only in chat.

Persist when a session changes any of:
- canon/current authority;
- active branch or project phase;
- story engine/architecture;
- accepted/rejected external finding;
- prompt/router/program law;
- audio/provider/build state;
- next exact obligation;
- release/lock state.

For Narrative OS system changes, obey `07_SYNC_POLICY.md`:
`Founder change -> GitHub canonical update -> CHANGELOG -> Drive mirror -> verify both`.

For project artifacts, follow the project's current persistence authority.

## 7. AUTOMATIC HANDOFF LAW

When material state changes, create or update a compact handoff without waiting for the Founder to request one.

Handoff fields:
- ACTIVE PROJECT;
- CURRENT AUTHORITY;
- PHASE / GATE;
- LAST COMPLETED ARTIFACT;
- WHAT CHANGED;
- ACCEPTED DECISIONS;
- REJECTED / SUPERSEDED ITEMS;
- OPEN RISKS;
- FILES CREATED/MODIFIED;
- CURRENT BLOCKER;
- HIGHEST UNBLOCKED NEXT OBLIGATION;
- WHAT MUST NOT BE SILENTLY CHANGED.

The next conversation should be able to resume in minutes from persisted state.

## 8. REFERENCE / BOOK DELTA LAW

Reference books are mechanism sources, never canon.

Use:
`REFERENCE -> ABSTRACT MECHANISM -> COMPARE / TRIANGULATE -> TRANSFORM -> PROJECT-SPECIFIC IMPLEMENTATION`.

Promote a reference mechanism into the OS only when it is:
- broadly reusable;
- compatible with existing higher laws;
- more precise than the current rule;
- capable of changing an actual production decision or QA result.

Do not create prompt bloat by converting every craft insight into a mandatory standalone pass.

## 9. DEFAULT REPORTING

During deep work, do not narrate every internal department.
Return one integrated operational result.

For production continuation, final status should normally answer:
- `DONE`;
- `WHAT CHANGED`;
- `CURRENT STATUS`;
- `REAL BLOCKER`, if any;
- `EXACT CONTINUATION POINT`.

## 10. ACCEPTANCE TEST

This protocol passes only if a new or neighboring conversation can:
1. determine the current project without asking the Founder to repeat known state;
2. discover newer persisted work from other conversations/models;
3. reject stale/superseded material;
4. execute the next unblocked obligation rather than restart planning;
5. persist material changes for the next conversation;
6. stop only at a real dependency.

**CONTINUATION IS THE DEFAULT. `И` IS SHORTHAND, NOT A WORKFLOW ENGINE.**
