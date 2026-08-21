# IVDIVO AUDIO NOVEL ENGINE — WAVE4 RED TEAM HARDENING + 88-TEST FINAL READBACK v1

**Date:** 2026-08-21  
**Status:** MACHINE CI GREEN / RED-TEAM SAFETY PATCHES PASS / LIVE EVIDENCE STILL HOLD

## 1. Why this addendum exists

The earlier CI readback recorded 86/86 PASS after repairing a pre-existing NumPy CI dependency defect. A subsequent internal Red Team found two material safety gaps in the controlled paid-provider wrapper. Those gaps were fixed and the full Audio Studio suite was rerun against GitHub's PR merge checkout.

This file supersedes only the machine-test count/status portion of `06_CI_AND_REBASE_READBACK_v1.md`; its freshness, authority and empirical-evidence boundaries remain valid.

## 2. Red-Team defect A — live dispatch gates were optional

Previous candidate behavior allowed a *new* `live=True` paid dispatch when neither:
- an exact identity manifest+fixture; nor
- an authenticated capability snapshot
had been supplied.

That contradicted the intended pre-spend identity/capability law.

### Repair

`audio/studio/controlled_provider_dispatch.py` now enforces for every **new** paid dispatch:
- identity fixture = PASS;
- authenticated capability snapshot = PASS;
- otherwise `NO_DISPATCH_LIVE_GATES` with provider call count zero.

An already-accepted request hash remains reusable without a new provider call; reusing persisted accepted evidence does not require re-paying or pretending to re-preflight a historical provider request.

## 3. Red-Team defect B — provider acceptance was too close to production acceptance

The provider adapter may persist paid provider evidence in MP3/PCM/other response formats. The strict canonical ingest module accepts only provable 48 kHz PCM WAV or explicitly-described PCM16 container wrapping and refuses guessing/silent transcoding.

Therefore:

`PROVIDER REQUEST ACCEPTED != PRODUCTION TAKE ACCEPTED != VOICE/PERFORMANCE LOCK`

### Repair

After provider evidence is persisted:
- the spend/provenance ledger may mark the paid request `ACCEPTED` so restart cannot pay twice;
- a separate `production_asset_gate` is evaluated;
- only strictly provable canonical 48 kHz WAV passes directly;
- raw PCM without explicit channel/sample metadata stays HOLD;
- MP3/unsupported provider audio remains durable provider evidence but returns `HOLD_EXPLICIT_UPSTREAM_CONVERSION_REQUIRED` before take/timeline use;
- `take_lock` remains `false`.

This separates economic/provenance truth from production/artistic truth.

## 4. Code/test commits

Controlled-dispatch hardening commit:
`f5fcfeada9906d6e58bfcee9f8bfee30e083d8d2`

Test hardening commit:
`621d376e58438defb87acea16544e6447c62f16d`

New regression cases include:
- new live dispatch requires identity + authenticated capability;
- accepted request hash still reuses without provider resend;
- connectivity uncertainty after POST quarantines to AMBIGUOUS;
- 4xx rejection becomes REJECTED, not ambiguous;
- provider acceptance is not a take lock;
- MP3 provider evidence is preserved but held before canonical production ingest.

## 5. Final GitHub Actions readback

Workflow: `Audio Studio Runtime Tests`

Run ID: `32509155735`  
Job ID: `96855988586`

Observed result:
- dependency install: PASS;
- dedicated Audio Novel runtime tests: **4/4 PASS**;
- full `audio/studio/tests/test_*.py` discovery: **88/88 PASS**;
- workflow/job conclusion: **SUCCESS**.

GitHub log ended with:
`Ran 88 tests ... OK`.

No test was disabled, skipped, weakened or converted to expected failure for this green result.

## 6. What 88/88 now proves at machine-contract level

Among the passing behaviors:
- malformed/unsupported or non-48k ingest fails closed;
- room dropout routes to room/ambience before music/mix;
- locked story is never auto-rewritten by audio repair routing;
- dry dispatch is default;
- identity drift blocks;
- **new live dispatch without identity+authenticated capability blocks before provider call**;
- accepted hashes are not resent after restart;
- post-POST connectivity uncertainty becomes AMBIGUOUS;
- provider rejection and ambiguity remain distinct;
- **provider acceptance does not become take lock**;
- **MP3 provider evidence cannot silently enter canonical timeline/take lineage**;
- capability drift forbids auto-substitution;
- freeze/resume preserves zero resent requests;
- human/fatigue evidence is required for performance lock;
- ambiguous provider attempts require reconciliation;
- stereo-collapse QC and timeline unresolved-anchor fail-closed behavior remain green.

## 7. What 88/88 does NOT prove

It does not prove:
- authenticated ElevenLabs/account inventory;
- real provider dispatch from this Wave4 work block;
- real Narrator/Ethan/Aoife candidates;
- `Ифа` / `Контакт` pronunciation quality;
- real Lesson Zero canary WAV/alignment/timeline;
- human naturalness/comprehension/fatigue/chemistry;
- actual spend/cost per accepted minute;
- portability under a third live project;
- v1.0 Production Ready.

## 8. Current Red-Team severity after patch

FATAL: **0 found in bounded Wave4 integration.**

MAJOR resolved in this pass:
- optional live identity/capability gates;
- provider-accepted vs production-take acceptance conflation.

MAJOR still open as empirical gates, not code assertions:
- authenticated inventory/casting/pronunciation;
- real Lesson Zero three-request canary;
- durable live WAV+alignment;
- human performance/comprehension;
- measured economics.

One integration item remains intentionally conservative:
`provider_reconciliation.py` can classify an ambiguous request from externally supplied provider lookup evidence, but provider-side lookup availability is not invented. Unsupported/unavailable lookup remains HOLD rather than blind retry.

## 9. Current next action

Internal:
`CURRENT-MAIN DELTA CHECK -> PR #94 DIFF RED TEAM -> CLOSE/SUPERSEDE PR #82 -> READY-FOR-REVIEW DECISION IF FATAL=0/MAJOR=0`.

External:
`AUTHENTICATED INVENTORY -> NARRATOR/ETHAN/AOIFE -> ИФА/КОНТАКТ -> PAIR/MULTI-STATE -> EXACT 3 LIVE REQUESTS -> DURABLE WAV+ALIGNMENT`.

**Machine contracts are green. Empirical product truth is still open.**
