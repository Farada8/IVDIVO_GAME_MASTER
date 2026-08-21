# AUDIO NOVEL ENGINE — WAVE11 PROVIDER EVIDENCE INTAKE 32→64

**Date:** 2026-08-21  
**Status:** WORKING / ENGINEERING DELTA IMPLEMENTED / CI + DRIVE + MERGE PENDING / AUTH_PROVIDER EXTERNAL EVIDENCE NOT YET OBSERVED IN PERSISTED STATE

## Purpose
Close the operational gap between the already-merged read-only `ElevenLabs Provider Snapshot Evidence` workflow and the already-merged Wave10 provider→cast modules. This is **not** a second Audio Engine, provider adapter, human-review system, or recovery runtime.

## Unique bounded delta
1. `audio/studio/runtime/provider_evidence_intake.py` — consumes a secret-free AUTH_PROVIDER artifact, revalidates class-specific trust, binds exact GitHub workflow run/attempt/source, cross-checks the separately stored snapshot, compiles normalized inventory, and optionally performs repeatability comparison.
2. `audio/studio/runtime/provider_execution_state.py` — fail-closed next-state resolver that can route only as far as real audition preparation; it cannot authorize human lock, spend, or paid dispatch.
3. `.github/workflows/elevenlabs-provider-evidence-intake.yml` — read-only `workflow_run` consumer for successful upstream provider-snapshot runs; downloads the exact triggering artifact and publishes only validated secret-free intake output.
4. Regression/security tests for receipt lineage, stale evidence, cross-account drift, secret-bearing keys, exact-run artifact binding, read-only permissions, trusted checkout, and no provider secret/synthesis in the intake workflow.

## Reused current authority
- ProviderSnapshot contract + authenticated read-only acquirer.
- durable `AUTH_PROVIDER` receipt and external-evidence trust adapters.
- Wave10 snapshot diff / inventory compiler / cast readiness.
- existing production-control spend/idempotency/dispatch gates.
- existing human-review/performance evidence and release gates.
- existing Self-Improvement durable/concurrency/earliest-cause laws.

## Parallel-development disposition
Fresh main `61c1540e91fb7b849dc0e775d001893e2cc6fda0` includes NMM Cycle5 external-evidence orchestration. Its prompt-frontier classifier is useful evidence for dependency-aware HOLD/READY routing, but it is project-specific. No NMM character IDs, candidate criteria, human tasks, story facts, or asset identities are transferred. The universal Wave11 delta is exact cross-run artifact intake and canonical provider evidence state transition.

## Evidence ceiling
At package creation: no persisted real provider/account read is visible in current shared project state; current connector cannot directly enumerate `workflow_dispatch` runs. Therefore the external state is **NO_PERSISTED_AUTH_PROVIDER_EVIDENCE_VISIBLE / REAL RUN STATUS NOT DIRECTLY ENUMERABLE HERE**, not a fabricated claim that no run exists. Paid synthesis=0; human listening=0; voice locks=0; pronunciation locks=0; live Lesson Zero requests=0; measured economics=none; story mutations=0.

## Next real gate
Run the already-merged provider snapshot workflow from a trusted GitHub Actions runtime with `ELEVENLABS_API_KEY` configured only as a repository Actions secret. Wave11 intake should then automatically validate the resulting secret-free artifact and advance only to the strongest admissible provider/cast state.
