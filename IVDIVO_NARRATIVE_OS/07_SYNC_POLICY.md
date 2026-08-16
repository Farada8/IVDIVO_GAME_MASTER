# IVDIVO NARRATIVE OS — SYNC POLICY

**Status:** CANONICAL OPERATING RULE  
**Version:** 1.0  
**Established:** 2026-08-16

## SOURCE OF TRUTH

For Narrative OS production rules, the canonical machine-readable source is the GitHub repository:

`Farada8/IVDIVO_GAME_MASTER/IVDIVO_NARRATIVE_OS/`

Google Drive is the human-readable working mirror.

## UPDATE ORDER

When the Founder changes a Narrative OS rule:

1. Apply the Founder’s newest instruction.
2. Update the relevant GitHub canonical file/version.
3. Update `IVDIVO_NARRATIVE_OS/CHANGELOG.md`.
4. Synchronize the corresponding Google Drive document.
5. Verify that both surfaces describe the same active rule.

## CONFLICT RULE

If GitHub and Drive diverge and there is no newer direct Founder instruction:

1. check timestamps/change history;
2. prefer the newest explicitly approved canonical version;
3. if approval status is ambiguous, do not merge silently;
4. mark the mismatch and resolve through A00/A19 before using the disputed rule.

A stale Drive mirror must not silently override GitHub canon. A newer Founder-approved Drive edit must not be discarded merely because GitHub has not yet been synchronized.

## VERSION LAW

Every material system change increments version and records:
- date;
- changed file;
- rule changed;
- reason;
- downstream effect.

Minor formatting changes do not require a semantic version increment.
