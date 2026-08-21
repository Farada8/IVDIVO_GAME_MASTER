# IVDIVO NARRATIVE OS — SYNC POLICY

**Status:** CANONICAL OPERATING RULE  
**Version:** 1.1  
**Established:** 2026-08-16  
**Updated:** 2026-08-21

## SOURCE OF TRUTH

For Narrative OS production rules, the canonical machine-readable source is the GitHub repository:

`Farada8/IVDIVO_GAME_MASTER/IVDIVO_NARRATIVE_OS/`

Google Drive is the human-readable working mirror and may temporarily contain a newer Founder-approved frontier waiting to be reconciled.

Persisted Project/GitHub/Drive state outranks chat recollection.

## UPDATE ORDER

When the Founder changes a Narrative OS rule:

1. Apply the Founder’s newest instruction.
2. Run a targeted delta check for any concurrent/current change that touches the same rule.
3. Update the relevant GitHub canonical file/version.
4. Update `IVDIVO_NARRATIVE_OS/CHANGELOG.md` or the current versioned change record.
5. Synchronize the corresponding Google Drive document/pointer.
6. Verify that both surfaces describe the same active rule.
7. Update current-state/handoff pointers when the change alters future continuation behavior.

Do not claim synchronization until verification succeeds.

## DELTA SWEEP LAW

At the start of substantial system or project work, compare the current persisted frontier against **material deltas**, not the entire archive.

Relevant surfaces may include:
- newer Founder / Project-conversation instructions;
- recent relevant GitHub authority/changelog/status changes;
- Google Drive current authority, handoffs and recently changed system/project files;
- current multi-model feedback/prompt state;
- newly added File Library engine/reference sources when they can change the active decision;
- downstream production authority if the workflow has reached that layer.

Deep-retrieve only where the delta can materially affect the decision.

Newest timestamp is a clue, not authority.

## CONFLICT RULE

If GitHub and Drive diverge and there is no newer direct Founder instruction:

1. inspect explicit `CURRENT / CANON / WORKING / SUPERSEDED / REJECTED` status and authority hierarchy;
2. check version/hash/change history where available;
3. prefer the newest **explicitly approved compatible authority**, not simply the newest modification time;
4. treat a newer verified Drive frontier as `PENDING_RECONCILIATION` rather than silently discarding it because GitHub has not yet been synchronized;
5. if approval/status/branch is ambiguous, do not merge silently;
6. mark the mismatch and resolve through current Router/Reconciler before using the disputed rule.

A stale Drive mirror must not silently override GitHub canon. A newer Founder-approved Drive edit must not be discarded merely because GitHub has not yet been synchronized.

Concurrent writes must be re-read before retrying after a version/SHA conflict. Never overwrite a newer neighboring-chat change from a stale local copy.

## PORTABILITY / PROMOTION LAW

When a stronger mechanism is discovered in another project/dialog:
1. classify it `PROJECT_ONLY / GENRE_OVERLAY_CANDIDATE / UNIVERSAL_CANDIDATE / REFERENCE_ONLY`;
2. abstract away project-specific canon/content;
3. compare against current equal/better mechanisms;
4. evaluate regression risk;
5. promote only if it materially improves production decisions or QA;
6. version + mirror + verify the accepted promotion.

Do not create parallel competing routers when an existing current authority can absorb the improvement. If a duplicate is created during concurrent work, reconcile it immediately and mark one authoritative/superseded.

## VERSION LAW

Every material system change increments version or creates an explicitly versioned new standard and records:
- date;
- changed file;
- rule changed;
- reason;
- downstream effect;
- affected pointers/handoffs;
- superseded artifact where applicable.

Minor formatting changes do not require a semantic version increment.

## CONTINUATION STATE LAW

A material work block that changes future routing is incomplete until the new frontier is persisted and verified when write access exists.

Future sessions should be able to recover:
`CURRENT AUTHORITY -> CURRENT PHASE -> LAST COMPLETED ARTIFACT -> OPEN GATES -> NEXT UNBLOCKED OBLIGATION`
without asking the Founder to reconstruct the session.
