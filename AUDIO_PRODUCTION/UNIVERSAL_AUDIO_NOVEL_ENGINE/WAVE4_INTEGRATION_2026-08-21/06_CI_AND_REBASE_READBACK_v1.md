# IVDIVO AUDIO NOVEL ENGINE — WAVE4 CI + REBASE READBACK v1

**Date:** 2026-08-21  
**Status:** CI GREEN / FRESH-MAIN SYNTHETIC MERGE TESTED / PR #94 DRAFT

## 1. Fresh-main replacement

Old PR #82 was based on a much earlier `main` frontier and became stale while sibling dialogs continued writing. A new branch was created from fresh `main`:

`audio-novel-engine/wave4-integration-rebased-2026-08-21`

Draft PR: **#94 — Audio Novel Engine Wave4: fresh-main production-control integration**.

Fresh reconciliation v2 explicitly inspected Audio Studio v3.3, PMV112, provider discovery and the commit labelled `Add current ElevenLabs adapter v2`. That commit was correctly classified as BODYGUARD-specific provider metadata, not a replacement for the universal `audio/studio/elevenlabs_adapter.py`.

After the first rebase, main continued advancing to PMV176 and other sibling work. Current policy remains stale-write safe: PR merge commits are tested against the current base; do not force-overwrite new main work.

## 2. First CI run — real failure found

GitHub Actions run: `32508643274`  
Job: `96854423036`

Result:
- dedicated Audio Novel runtime tests: **4/4 PASS**;
- full Audio Studio discovery: **FAIL** before completion because pre-existing `test_stereo_integrity_qc.py` imports NumPy but the workflow did not install NumPy;
- failure class: `CI_ENVIRONMENT_DEPENDENCY_MISSING`, not a Wave4 production-control assertion failure.

The log reached **85 tests**, with the only error:

`ModuleNotFoundError: No module named 'numpy'`

This exposed a real CI defect that predated the Wave4 code.

## 3. CI repair

The workflow trigger surface was already widened for integration coverage. It was then minimally repaired by adding:

`python -m pip install --disable-pip-version-check numpy`

No test was disabled, skipped, weakened or rewritten to obtain green status.

## 4. Second CI run — GREEN

GitHub Actions run: `32508759917`  
Job: `96854777391`

Result:
- dependency install: PASS;
- dedicated Audio Novel runtime tests: **4/4 PASS**;
- full `audio/studio/tests/test_*.py` discovery: **86/86 PASS**;
- workflow conclusion: **SUCCESS**.

The full suite includes the new Wave4 controls plus existing provider, alignment, stereo-integrity, timeline, ingest and runtime tests.

New Wave4 behaviors observed PASS in the real CI log include:
- 48 kHz ingest and malformed/unsupported audio fail-closed;
- locked story cannot be auto-rewritten by audio repair router;
- room dropout routes before music/mix;
- controlled dispatch defaults dry;
- identity drift blocks before dispatch;
- accepted request hash is not resent after restart;
- connectivity uncertainty after POST becomes AMBIGUOUS;
- missing capability/voice blocks;
- exact identity fixture drift fails;
- capability drift forbids substitution;
- freeze/resume produces zero resent requests;
- performance lock requires human/fatigue evidence;
- ambiguous attempt requires reconciliation;
- provider reconciliation rejects incomplete/invalid lookup evidence;
- stereo collapse detection still passes once NumPy is installed;
- timeline unresolved-anchor failures still fail closed.

## 5. PMV176 delta after CI

Current main subsequently promoted `P53_AUTO_CONTROL/32_CURRENT_RUNTIME_AUTHORITY_INDEX_v1_5_PMV176.md`.

Portable PMV176 findings are compatible with this integration:
- TTD remains a dry/candidate experiment, not universal authority;
- dependency invalidation/rollback exists in the BODYGUARD multilingual lab;
- external native/practitioner/provider/audio evidence remains real-gate material;
- optimize information gain rather than document count.

This does **not** prove a current universal persistent paid-request ledger, ambiguous-response quarantine, canonical 48 kHz ingest or universal controlled-dispatch wrapper already exists on main. Those Wave4 deltas remain bounded candidates.

## 6. Current verdict

`WAVE4_RUNTIME_INTEGRATION = CI_GREEN / REVIEW_PENDING`

`FULL_AUDIO_STUDIO_TESTS = 86/86 PASS`

`LIVE_PROVIDER = HOLD`

`VOICE_PRONUNCIATION_LOCK = HOLD`

`LESSON_ZERO_LIVE_CANARY = HOLD`

`HUMAN_PERFORMANCE = HOLD`

`ECONOMICS = HOLD`

`V1_PRODUCTION_READY = HOLD`

## 7. Exact next action

Internal:
1. independent diff/Red-Team review of PR #94;
2. verify no newer main module duplicates the six bounded production-control files;
3. if no FATAL/MAJOR conflict, mark PR ready for review/merge path;
4. never chase moving main by force-overwrite; rely on current-base merge/check evidence and reconcile real conflicts only.

External:
`AUTHENTICATED SECRET-FREE INVENTORY → NARRATOR/ETHAN/AOIFE → ИФА/КОНТАКТ → PAIR/MULTI-STATE → EXACT 3 REQUESTS → DURABLE WAV+ALIGNMENT`.

No live provider, human listening, cost or voice-lock evidence is claimed by this CI result.
