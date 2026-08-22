# SELF-IMPROVEMENT DISCOVERY — BUSINESS LIBRARY / CONCURRENCY SALVAGE

No new CURRENT Self-Improvement ID is allocated here. Self-Improvement v2 remains CURRENT; v3/global promotion is forbidden without independent proof/regression.

## Candidate 1 — NAMESPACE_COLLISION_GATE
Observed defect: independent Cycle4 work reused the same numeric B/C ranges for different semantics.
Root cause: numeric availability was treated as semantic identity.
Repair: namespace + semantic-owner reservation and fail-closed collision HOLD; no auto-rename.
Test: B81/Public vs B81/Shillelagh must HOLD; same-owner BPUB reuse may pass.
Status: ENGINEERING CANARY ONLY.

## Candidate 2 — CONCURRENT_AUTHORITY_RESTORE
Observed defects: library authority advanced 69→71→78; PR #173 changed from active hardening branch to superseded while an older plan still expected a merge; during this salvage run main advanced again from Cycle4 into merged Cycle5.
Root cause: substantial writes were planned against a snapshot without a mandatory freshness gate.
Repair: compare expected/observed main SHA, relevant PR heads, library count and Drive current pointer before material writes/closure.
Status: ENGINEERING CANARY ONLY.

## Candidate 3 — LIBRARY_DELTA_AFTER_CYCLE_GATE
Observed defect: source uploads can land during a long cycle and make earlier counts stale.
Repair: closure requires prior/current counts plus a complete enumeration of new physical IDs; duplicate source weight is handled separately.
Status: ENGINEERING CANARY ONLY.

## Candidate 4 — DATASET_NEQ_ENGINE
Observed risk: repeated 32/64 opportunity packs can be mistaken for new engines because they are large/persisted.
Repair: persistence/size cannot create core authority; a unique reusable runtime contract, dedupe and review are required.
Status: ENGINEERING CANARY ONLY.

## Candidate 5 — SOURCE_WEIGHT_NORMALIZATION
Observed defect: a new physical copy of The Mom Test is exact-byte duplicate of an already-accounted source.
Repair: exact-byte duplicates contribute zero incremental evidence weight; work/edition identity stays explicit when unresolved.
Status: LIBRARY CANDIDATE.

## Candidate 6 — ROOT_WORKLOAD_DEDUPLICATION
Observed defect: 64 public opportunity labels contain repeated buyer jobs under different sector/regulatory language.
Repair: dedupe by recurring buyer workload + decision artifact while preserving domain rule/source lineage.
Status: DISCOVERY ONLY; merged Cycle5 artifact architecture now gives a natural downstream test surface.

## Promotion gates
For candidates 1–4:
1. deterministic regression PASS;
2. at least two independent live Business OS cycles where the guard correctly blocks or permits work;
3. false-positive analysis;
4. GitHub + Drive persistence/readback;
5. independent Red Team;
6. Founder/authority review.

For root-workload dedupe additionally require evidence that the ontology changes a real artifact/test decision without erasing domain-specific requirements.

## Improvement objective
Measure improvement as less wrong activity, not more modules:
`stale/duplicate idea paths avoided + WIP controlled + uncertainty made explicit + decision artifact quality improved`.
