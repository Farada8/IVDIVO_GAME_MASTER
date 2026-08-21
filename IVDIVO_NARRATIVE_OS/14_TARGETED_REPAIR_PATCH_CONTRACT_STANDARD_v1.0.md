# IVDIVO NARRATIVE OS — TARGETED REPAIR / PATCH CONTRACT STANDARD

**Status:** CURRENT UNIVERSAL REPAIR STANDARD
**Version:** 1.0
**Date:** 2026-08-21

## PURPOSE

Promote the strongest reusable repair behavior proven in IDEA→STORY recovery work into a universal Narrative OS rule **without** promoting the recovery package itself to authority.

Primary law: **Detection is not repair. Repair is not permission to rewrite everything.**

## 1. ENTRY CONDITION

A patch cycle may start only from a recorded defect with:
- severity;
- evidence location;
- affected authority/artifact;
- diagnosis separated from proposed fix;
- scope estimate: `LOCAL / MULTI_SCENE / STRUCTURAL_GLOBAL`.

POLISH alone does not reopen a locked story.

## 2. ROUTE BY SCOPE

### LOCAL / MULTI_SCENE
May use bounded patching.

### STRUCTURAL_GLOBAL
Do **not** patch symptoms locally. Route to the earliest failed authority/gate, for example:
- Story Core;
- Character/Relationship Architecture;
- Mystery/Continuity ledger;
- Causal Chapter Map;
- Story Gate.

## 3. PATCH PIPELINE

`ISSUE -> PATCH_QUEUE -> PATCH_CONTRACT -> CANDIDATE BRANCH -> LOCAL QA -> SELECTIVE COMMIT -> INVALIDATION -> REGRESSION -> CLOSE/REOPEN`

### PATCH_QUEUE
Each item records:
- issue ID;
- severity;
- target scene/chapter/range;
- diagnosis;
- acceptance test;
- dependencies;
- prohibited collateral changes.

### PATCH_CONTRACT
Before generation/editing, freeze:
- current source authority/version;
- target artifact hash where available;
- sibling artifact hashes where relevant;
- patch-queue hash/version;
- exact allowed range;
- protected canon/text/clues/relationship states;
- required downstream gates.

If the source/queue changed after contract creation, abort stale patch.

### CANDIDATE FIRST
Never mutate accepted manuscript/source first.
Generate/edit candidate output separately.

### LOCAL QA
Candidate must prove:
- target defect is actually changed;
- no protected fact/text is broken;
- no no-effect patch;
- no new local FATAL/MAJOR;
- scope remained bounded.

Failed local QA leaves current accepted bytes/state untouched.

### SELECTIVE COMMIT
Commit only accepted targets. Never regenerate unaffected locked siblings merely for stylistic consistency.

## 4. DOWNSTREAM INVALIDATION

A successful patch must invalidate only evidence that depended on changed material.

Possible invalidations:
- P51 voice evidence;
- P52 emotional-range evidence;
- P53 relationship/consent evidence;
- dialogue/line pass;
- Reader Advocate;
- continuity/mystery state;
- Human Signal on changed unit;
- audio exact-text/hash/manifests if locked text changed;
- downstream episode/chapter gates if knowledge state changed.

Do not preserve a PASS whose evidence source changed.

## 5. REGRESSION

After selective commit, rerun:
1. the original defect acceptance test;
2. local FATAL/MAJOR scan;
3. affected aggregate gates;
4. recurrence check for the original defect;
5. check for renamed/new defects created by the patch;
6. continuity/knowledge-state propagation where causal facts changed.

## 6. FINITE CYCLES

Set a finite repair-cycle cap appropriate to the work unit. If repeated local repair fails, escalate scope rather than self-edit indefinitely.

Repeated inability to repair locally is evidence the diagnosis may be structural.

## 7. LOCK PROTECTION

For a locked project:
- FATAL/MAJOR evidence or Founder instruction is required to reopen story text;
- downstream audio/video/publishing problems should be repaired in their own adapter layer when possible;
- never rewrite locked prose merely to make one provider easier to use.

## 8. PROVENANCE

Reusable mechanism source: IVDIVO IDEA→STORY RECOVERY v0.4 working clean-room recovery package.

Promotion boundary:
- **PROMOTED:** bounded patch contract / candidate-first / local QA / selective commit / invalidation / regression / finite cycles.
- **NOT PROMOTED:** recovery package authority status, deterministic fixtures, historical source-equivalence claims, or any claim that recovery Reference Intelligence replaces Story Engine v4.1.

## 9. VERDICT STATES

- `PATCH_READY`
- `PATCH_STALE_ABORT`
- `PATCH_QA_FAIL`
- `PATCH_COMMITTED`
- `REGRESSION_FAIL`
- `ISSUE_CLOSED`
- `ESCALATE_STRUCTURAL`

A patch is not closed until regression passes.
