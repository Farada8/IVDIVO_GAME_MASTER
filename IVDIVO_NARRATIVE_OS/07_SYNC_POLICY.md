# IVDIVO NARRATIVE OS — SYNC POLICY

**Status:** CANONICAL OPERATING RULE  
**Version:** 1.1  
**Established:** 2026-08-16  
**Updated:** 2026-08-21

## SOURCE OF TRUTH

For Narrative OS production rules, the canonical machine-readable source is the GitHub repository:

`Farada8/IVDIVO_GAME_MASTER/IVDIVO_NARRATIVE_OS/`

Google Drive is the human-readable working mirror.

A conversation is an execution surface, not a durable source of production truth. Material progress must be persisted into the appropriate project artifact/state record before it is treated as cross-dialog complete.

## UPDATE ORDER

When the Founder changes a Narrative OS rule:

1. Apply the Founder’s newest instruction.
2. Update the relevant GitHub canonical file/version.
3. Update `IVDIVO_NARRATIVE_OS/CHANGELOG.md`.
4. Synchronize the corresponding Google Drive document.
5. Read back and verify that both surfaces describe the same active rule.

## MATERIAL PROGRESS WRITE-BACK

When a work block materially advances a project without changing universal law:

1. save/version the accepted result artifact;
2. update the project current-state/frontier pointer;
3. update project changelog/decision record when the change is material;
4. mirror to Google Drive where that project workflow requires a Drive mirror;
5. read back the changed surfaces;
6. only then report the cross-dialog state as persisted.

Do not inflate universal canon files with volatile local progress. Universal reusable rules belong in Narrative OS; changing project progress belongs in project state/frontier artifacts.

## CONFLICT RULE

If GitHub and Drive diverge and there is no newer direct Founder instruction:

1. separate **authority/canon conflict** from **progress freshness conflict**;
2. for rules/canon, prefer the highest/newest explicitly approved canonical authority;
3. for current stage/frontier, prefer the newest compatible provenance-valid accepted artifact;
4. if approval/compatibility is ambiguous, do not merge silently;
5. mark the mismatch and resolve through A00/A19 before using the disputed field.

A stale Drive mirror must not silently override GitHub canon. A newer Founder-approved Drive edit must not be discarded merely because GitHub has not yet been synchronized.

An authoritative older document may remain valid for rules while one embedded progress pointer is stale; do not roll back accepted work because of that stale pointer.

## MULTI-AI SYNC LAW

Outputs produced by another AI/dialogue are not rejected merely because they were produced elsewhere, and are not accepted merely because they exist.

Before reuse/promotion verify:
- active project/book and branch/build;
- source/version/hash where applicable;
- authority compatibility;
- output schema/completeness;
- acceptance gates;
- provenance;
- invalidation state.

Valid accepted artifacts are reused. Candidate/unverified outputs are validated before promotion. Do not duplicate accepted work.

## VERSION LAW

Every material system change increments version and records:
- date;
- changed file;
- rule changed;
- reason;
- downstream effect.

Minor formatting changes do not require a semantic version increment.
