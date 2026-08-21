# IVDIVO NARRATIVE OS — CROSS-DIALOG / MULTI-AI STATE OS

**Status:** CANONICAL OPERATING LAYER  
**Version:** 1.0  
**Established:** 2026-08-21  
**Scope:** cross-conversation continuation, state recovery, handoff between ChatGPT/Claude/Grok/Codex/other AI workers, and write-back after material progress.  
**Parent authorities:** `IVDIVO_WRITING_PRODUCTION_CANON.md`, `00_NARRATIVE_OS_CANON.md`, `01_NARRATIVE_OS_CONFIG.yaml`.

---

## 1. PURPOSE

IVDIVO production must not depend on one chat remembering another chat.

The durable production state lives in verified project artifacts. A conversation is an execution surface, not the source of truth.

Required operating cycle:

`RESTORE -> RESOLVE CURRENT STATE -> EXECUTE -> VALIDATE -> WRITE BACK -> VERIFY -> HANDOFF/CONTINUE`.

The Founder must not need to repeatedly reconstruct work that is already recoverable from connected project state.

---

## 2. CURRENT-STATE RESOLVER

Before substantial continuation work, A00 resolves:

- `ACTIVE_PROJECT_OR_BOOK`;
- `ACTIVE_BRANCH`;
- `CURRENT_AUTHORITY`;
- `SOURCE_FILE / VERSION / HASH` where protected source exists;
- `CURRENT_MODE`;
- `LAST_VERIFIED_ACCEPTED_FRONTIER`;
- `LAST_COMPLETED_STAGE_OR_ARTIFACT`;
- `NEXT_UNBLOCKED_OBLIGATION`;
- `OPEN_FATAL`;
- `OPEN_MAJOR`;
- `FOUNDER_DECISION_REQUIRED`;
- `LOCKED / FORBIDDEN CHANGES`;
- `EVIDENCE_PROVENANCE`.

Do not infer CURRENT STATE from filename age or one stale index line alone.

### Authority vs freshness

Two questions are separate:

1. **Which source defines the rule/canon?** Use authority hierarchy.
2. **Which verified artifact defines progress/current stage?** Use the newest compatible, provenance-valid state artifact.

A structurally authoritative document may contain an obsolete progress pointer. Preserve its laws while using newer verified progress evidence.

If sources genuinely conflict and cannot be reconciled, fail closed on the disputed field rather than silently choosing.

---

## 3. CONTINUATION COMMAND LAW

When Founder says `и / дальше / продолжай / делай / работай / RUN THE STUDIO / AUDIO CONTINUE`, or opens a new conversation whose requested project is recoverable:

1. restore project authority;
2. resolve current state;
3. identify the highest unblocked obligation;
4. execute actual work;
5. continue through dependent stages in the same work block while gates allow;
6. do not redo a PASS/LOCKED stage without new evidence;
7. do not switch project/book/branch silently;
8. write back material progress before treating it as cross-dialog complete.

Do not answer with generic advice when an executable next obligation is known.

---

## 4. WRITE-BACK LAW

A result produced only inside a chat is not durable project progress.

After any **material** advancement, persist the minimum sufficient state to the proper source of truth.

Material advancement includes:

- a Founder decision;
- a canon/authority rule change;
- a stage/gate becoming PASS, FAIL, LOCKED or SUPERSEDED;
- accepted architecture/manuscript patch;
- new validated program/prompt/protocol;
- completed production artifact;
- changed active branch/frontier;
- newly discovered FATAL/MAJOR blocker;
- resolved blocker;
- provider/asset/voice/build lock;
- external-human evidence that changes production status.

Write-back order:

`artifact/result -> project current-state pointer -> relevant CHANGELOG/DECISION record -> Drive mirror where required -> read-back verification`.

Do not rewrite large canon files merely to record a local stage update. Put volatile progress in project state/frontier artifacts and stable reusable laws in Narrative OS.

---

## 5. NO-DUPLICATE-WORK / HASH REUSE LAW

Existence of a file is not proof that it remains valid.

Reuse an artifact only when:

- its authority is still valid;
- declared upstream hashes/versions still match where hashing is used;
- no explicit invalidation rule applies;
- a newer accepted artifact has not superseded it.

If valid, reuse it. Do not recreate it because another AI or another dialogue did the work.

When an upstream change occurs, invalidate only true descendants. Preserve unrelated accepted siblings.

---

## 6. SELECTIVE REPAIR LAW

The preferred repair sequence for diagnosed post-draft defects is:

`ISSUE -> PATCH_QUEUE -> PATCH_CONTRACT -> TARGETED CANDIDATE REPAIR -> LOCAL PATCH QA -> COMMIT TARGET SCOPE -> INVALIDATE TRUE DESCENDANTS -> REGRESSION GATES`.

Do not default to whole-book regeneration.

A patch contract must freeze the relevant authority and unaffected siblings by version/hash where available. Stale patch contracts must abort. Failed/no-effect candidates must not replace accepted manuscript bytes.

This law adopts the proven clean-room recovery behavior as a **general repair mechanism**, not the recovery package itself as canon authority.

---

## 7. WORKING RECOVERY / PROMOTION BOUNDARY

`IVDIVO IDEA -> STORY RECOVERY v0.4` is a useful WORKING clean-room recovery package, not CURRENT authority merely because its automated suite passes.

Its reusable validated mechanisms may be adopted individually after review, including bounded patch queue/contract/QA/regression behavior.

Do not label the package `IMPLEMENTED`, `CALIBRATED`, `CURRENT AUTHORITY` or `RELEASE_READY_ENGINE` without its stated promotion evidence: real Founder input, real literary/review providers, end-to-end calibration, no unresolved FATAL/MAJOR, required real human evidence, and explicit promotion.

Current Story Engine v4.1 / Narrative OS remain the authority layers unless explicitly superseded.

---

## 8. REFERENCE INTELLIGENCE REUSE

Do not re-read the full reference library on every continuation.

First use the current Story Engine v4.1 abstraction stack:

`Library Audit -> Source Passports -> Mechanism Banks -> Semantic Dedupe -> Source Role Map -> Core Mechanisms -> Crosswalk -> Story Assembly`.

Run a fresh source pass only when the current problem requires evidence not already represented, when the mechanism extraction is insufficient, or when a newer source materially changes the decision.

Reference material remains `REFERENCE ONLY` unless separately promoted by Founder authority.

---

## 9. MULTI-AI HANDOFF CONTRACT

AI providers/models are workers, not authorities.

Before assigning work to another AI, create or supply a compact handoff packet containing:

- project/book ID;
- task ID;
- authority sources and versions/hashes;
- active branch/build;
- current stage/frontier;
- exact input artifact(s);
- immutable locks;
- allowed change scope;
- forbidden changes;
- relevant reference mechanisms;
- required output schema/file names;
- acceptance gates;
- evidence/provenance requirements;
- exact next consumer stage.

The receiving AI must not infer missing canon from general knowledge or its own earlier conversation.

### Ingesting another AI's result

External AI output enters as `CANDIDATE / UNVERIFIED` unless it is already an explicitly accepted project artifact.

Before promotion:

1. verify source/branch/version/hash scope;
2. validate schema/output completeness;
3. run canon/continuity checks;
4. run task-specific acceptance gates;
5. run independent review where independence materially matters;
6. record provenance;
7. only then promote and write back.

Do not treat same-provider self-review as independent human or independent-model evidence.

---

## 10. CAPABILITY ROUTING, NOT BRAND ROUTING

Choose an AI/tool by capability and current task, not by brand prestige.

Possible roles include:

- generation;
- structural architecture;
- code/automation;
- factual research;
- adversarial review;
- continuity comparison;
- audio/visual execution;
- schema validation.

Where independent review matters, prefer a distinct reviewer path and preserve provenance. Human Signal remains external-human evidence only.

Provider-specific APIs are adapters behind internal project contracts. Provider response shapes must be normalized before downstream consumers rely on them.

---

## 11. CROSS-DOMAIN HANDOFF

A locked/current story may hand off to specialized production adapters without reopening story development:

`STORY LOCK/CURRENT SOURCE -> AUDIO / VISUAL / TRANSLATION / MARKETING ADAPTER`.

Each adapter must restore its own current specialized authority and bind to the story source/version/hash.

Project-specific identities, voice IDs, clue chains, relationship timing, sound motifs, visual locks and obsolete branch facts never transfer to another project merely because the production mechanism is reusable.

---

## 12. MINIMUM PROJECT STATE RECORD

Every active production line should maintain an equivalent of:

```yaml
project_id: ...
active_book_or_line: ...
active_branch: ...
authority_refs: []
source:
  file: ...
  version: ...
  sha256: ...
mode: ...
last_verified_frontier: ...
last_completed_stage: ...
last_completed_artifact: ...
next_unblocked_obligation: ...
open_fatal: []
open_major: []
founder_decision_required: []
locked_invariants: []
invalidated_artifacts: []
external_dependencies: []
updated_at: ...
updated_by: ...
provenance: []
```

Names may differ by project, but these semantics must be recoverable.

---

## 13. DIALOG-END CHECKPOINT

Before a substantial work block is considered complete, record:

`DONE / ACCEPTED OR CANDIDATE / GATE STATUS / WHAT CHANGED / WHAT DID NOT CHANGE / CURRENT FRONTIER / EXACT NEXT UNBLOCKED OBLIGATION / BLOCKERS / SOURCE PROVENANCE`.

If persistence tools are unavailable, state that the result is not yet durable instead of claiming cross-dialog completion.

---

## 14. FAIL-CLOSED RULES

Never:

- reconstruct unavailable canon from memory;
- treat a stale stage pointer as current against newer verified artifacts;
- redo accepted work merely because it was produced by another AI/dialogue;
- promote a clean-room/recovery package solely from test count;
- overwrite a whole manuscript to fix a local defect by default;
- manufacture Human Signal;
- let an external AI silently change canon;
- claim write-back before read-back verification.

**FINAL LAW:** restore once, execute forward, validate, persist, and make the next conversation resume from evidence rather than repetition.
