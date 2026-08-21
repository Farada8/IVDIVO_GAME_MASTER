# IVDIVO — TRANSCRIPT EXTRACTOR HARDENING v1.1 — RUNTIME VERIFICATION

**Date:** 2026-08-21  
**Status:** CANDIDATE HARDENING SMOKE GREEN — NOT YET CURRENT/PACKAGED  
**Branch:** `system/transcript-extractor-hardening-v1-1-20260821`  
**Parent CURRENT:** `tools/ivdivo_transcript_recovery.py` v1 first-pass extractor / 18B protocol

## Scope of candidate hardening

This branch does not change the fundamental v1 evidence boundary. The extractor still outputs `EXTRACTED_UNVERIFIED`, never decides canon, never verifies persistence by itself and never sets `INGESTION_COMPLETE`.

Hardening changes:
- speaker-role boundaries accept only 0–3 leading spaces, avoiding 4-space code-indented false turns;
- fenced code blocks (``` / ~~~) do not create speaker boundaries;
- Russian role aliases: `Пользователь / Ассистент / Основатель`;
- Ukrainian role aliases: `Користувач / Асистент / Засновник`;
- Ukrainian directive/work/authority/next-action/system-improvement keyword coverage;
- quoted/code artifact references remain UNVERIFIED and are never self-promoted;
- negative completed-work phrases may remain safe first-pass noise, but cannot self-verify or complete ingestion.

## Exact-source identity

`tools/ivdivo_transcript_recovery.py`
- GitHub branch blob SHA: `5263f6a8c58f206df512bb8bdbc5e745c5097d2d`;
- reconstructed local execution source Git-blob SHA: `5263f6a8c58f206df512bb8bdbc5e745c5097d2d`;
- identity: **MATCH**.

Baseline `tests/test_transcript_recovery.py`
- GitHub main blob SHA: `38b96dea71e75b503bb3b755e6cd4bf292b65dcc`;
- local test source Git-blob SHA: `38b96dea71e75b503bb3b755e6cd4bf292b65dcc`;
- identity: **MATCH**.

Candidate `tests/test_transcript_recovery_adversarial.py`
- GitHub branch blob SHA: `413ad9124f8dc428859454f2670686a61699d056`;
- local test source Git-blob SHA: `413ad9124f8dc428859454f2670686a61699d056`;
- identity: **MATCH**.

## Runtime result

Exact-source pytest run of baseline + adversarial suites:
- **13 passed**;
- **0 failed**;
- exit code **0**.

Covered candidate contracts:
1. original secret-redaction contract remains green;
2. original Founder-directive/work-claim extraction remains green;
3. saved/LOCK claims remain UNVERIFIED;
4. original source hash/tail behavior remains green;
5. system-improvement discovery remains DISCOVERY_ONLY;
6. `Assistant:` inside fenced code does not split outer turns;
7. 4-space-indented `Assistant:` does not create a false outer turn;
8. Ukrainian user role/directive is recognized;
9. Russian user/assistant aliases are recognized;
10. Ukrainian assistant work claim is extracted but remains UNVERIFIED;
11. blockquoted `> Assistant:` does not become an outer role boundary;
12. artifact-like references inside quoted code remain UNVERIFIED verification noise, never persistence proof;
13. negative completed-work phrasing may be extracted as safe noise but remains UNVERIFIED and cannot complete ingestion.

## Red-Team disposition of remaining noise

### Negative work-claim language
Example: `No files were created and nothing was saved.` currently matches the first-pass completed-work keyword detector.

Disposition: **MEDIUM / SAFE NOISE, DEFER TO SEMANTIC RECONCILIATION**. It cannot self-verify, cannot promote canon and cannot complete recovery. Adding a brittle deterministic negation grammar risks false negatives across languages. Reconciled Recovery State v2 may classify it `NOT_APPLICABLE` semantically.

### Artifact-like references inside code/quotes
Example: quoted `fake.json` remains an UNVERIFIED artifact reference and verification task.

Disposition: **MEDIUM / SAFE VERIFICATION NOISE, KEEP FOR RECALL**. Suppressing all code/quoted artifact references would lose legitimate filenames pasted as evidence. The correct boundary is to keep them UNVERIFIED and let semantic reconciliation/dedupe decide whether they matter.

## Remaining promotion gates

- broader malformed/transcript UI/huge-input fixtures;
- integration with Reconciled Recovery State v2 semantics;
- first real large pasted-corpus pilot;
- regression against existing engine package before next ZIP promotion.

Therefore this hardening branch remains a **candidate** and must not silently replace the verified current v1 extractor yet.
