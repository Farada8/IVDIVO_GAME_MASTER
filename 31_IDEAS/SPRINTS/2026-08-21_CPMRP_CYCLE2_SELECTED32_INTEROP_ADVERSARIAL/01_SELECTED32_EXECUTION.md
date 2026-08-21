# CPMRP CYCLE 2 — SELECTED32 EXECUTION RESULTS

**Execution set:** N05–N12, N17, N21, N29–N44, N49–N52, N61–N62.  
**Proof:** GitHub Actions `CPMRP Cycle2 Tests` run `32531823818` — Cycle1 10/10 PASS + Cycle2 32/32 PASS. `Self-Improvement Integrity` run `32531823816` — SUCCESS.

## N05 — ODRL profile for CPMRP actions
**Result:** REUSE/PROFILE. TDM-specific machine policy remains TDMRep's ODRL profile. CPMRP does not redefine `tdm:mine`, `obtainConsent`, or `compensate`. CPMRP-specific amount metadata is a separate sidecar linked by `policy_uid`.

## N06 — TDMRep exporter
**Result:** BUILT. `export_tdmrep()` emits `tdm_reservation=0` for FREE and `tdm_reservation=1` + `tdm_policy` for reserved cases. Paid offer fixture carries `obtainConsent` + `compensate`. Profile validator added.

## N07 — C2PA training-mining adapter
**Result:** BUILT. Mapping covers `c2pa.data_mining`, `c2pa.ai_inference`, `c2pa.ai_training`, `c2pa.ai_generative_training`; values map to allowed/notAllowed/constrained.

## N08 — Conflict/fail-closed semantics
**Result:** BUILT PARTIAL. Unresolved C2PA `constrained` returns `DENY_UNRESOLVED_CONSTRAINT`; unknown assertion returns HOLD. Full robots/site-terms precedence remains external legal/policy work, not silently encoded.

## N09 — EU registry technical direction
**Result:** INCORPORATED. Asset Passport v0.2 and future federation plan preserve work ID, exact fingerprint/hash, metadata and jurisdiction/territory fields. No assumption that CPMRP replaces a future EU registry.

## N10 — Registry federation adapter
**Result:** ARCHITECTURE DEFINED, implementation deferred. External registry refs are treated as evidence/provenance links; CPMRP remains complementary.

## N11 — Provenance interoperability benchmark
**Result:** BOUNDED. C2PA reused for content assertions; TDMRep/ODRL reused for TDM policy. Generic provenance remains typed external refs. No new global provenance vocabulary created.

## N12 — Interoperability matrix
**Result:** EXTRACTED. Normative reuse: TDMRep/ODRL/C2PA. CPMRP extension: asset/version identity, licence receipt, micro-royalty ledger, dispute/claim integrity. Deliberate non-overlap: legal adjudication and copyright ownership verification.

## N17 — Asset Passport v0.2
**Result:** BUILT. Adds jurisdiction, territories, upstream licence, evidence ceiling and mandatory `ownership_verified=false` in this evidence class.

## N21 — Extended UsageIntent
**Result:** BUILT. Operations now normalize retrieval indexing, RAG context, AI inference, AI/generative training and human editorial reference into bounded core actions. Unknown intent returns HOLD.

## N29 — Receipt signer interface
**Result:** BUILT BOUNDED. Supports unsigned-development commitment or external signer callback. `production_signature_proven=false` remains explicit.

## N30 — Offline verification + correction semantics
**Result:** BUILT. Receipt IDs verify offline from canonical payload. Corrections append a new `cpmrp.receipt-correction/0.2` object and preserve original history.

## N31 — Existing durable write contract reuse
**Result:** BUILT. `build_durable_registry_ledger_plan()` generates reversible GitHub registry + Drive ledger actions using the existing IVDIVO durable transaction vocabulary.

## N32 — Failure/recovery states
**Result:** PROVEN IN FIXTURES. NOT_STARTED -> EXECUTE_MISSING_SAFE_ACTIONS; STARTED_UNKNOWN reversible -> VERIFY_STORE_BEFORE_RETRY; CONFIRMED without readback -> VERIFY_READBACK; both confirmed/readback -> TRANSACTION_COMPLETE.

## N33 — SimilarityEvidence V2
**Result:** BUILT. Exact, near-duplicate, rare lexical, structural, access, timestamp and common-trope channels are explicit.

## N34 — Common-trope negative controls
**Result:** PROVEN. High common-trope ratio suppresses candidate provenance signals rather than manufacturing ownership/debt.

## N35 — Independent creation packet
**Result:** BUILT. Carries timestamp/process refs, `legal_conclusion=null`, `debt_effect=NONE_AUTOMATIC`.

## N36 — Threshold calibration law
**Result:** BUILT. Every similarity result explicitly reports `threshold_is_legal_test=false`, `legal_infringement_finding=false`, `creates_debt=false`.

## N37 — Provenance cycle detection
**Result:** BUILT/PROVEN. A->B->C->A is rejected as `PROVENANCE_CYCLE`.

## N38 — Multi-source royalty shares
**Result:** BUILT BOUNDED. Edges carry basis-point shares and graph can calculate incoming share total. Contract composition and over-100% allocation gate remains next-cycle work.

## N39 — Edge receipts
**Result:** BUILT. `declared_reference` and `licensed_use` generate distinct hash-addressed edge receipts; mere reference still creates no debt.

## N40 — Unavailable source handling
**Result:** BUILT. Source availability may become false while content hash + last-seen reference remain preserved as evidence.

## N41 — ClaimIntegrity
**Result:** BUILT. IDEA/STYLE/TROPE/GENRE/COMMON_MOTIF monetization claims are rejected; public-domain capture rejected; duplicate and earlier-source cases HOLD.

## N42 — Reputation metadata
**Result:** BUILT. Evidence-quality score can summarize history but explicitly returns `ownership_proof=false` and `automatic_priority=false`.

## N43 — Sybil controls
**Result:** BUILT. Mass/high-low-evidence claim patterns trigger `RATE_LIMIT_AND_REVIEW`; normal bounded intake remains allowed.

## N44 — Abuse appeal
**Result:** BUILT. Appeals are hash-addressed, counter-evidence deduplicated and always `HUMAN_REVIEW_REQUIRED`; no automatic override.

## N49 — REST/API semantics
**Result:** CORE SEMANTIC FUNCTION BUILT. `can_use()` is now the minimal API contract. Network/OpenAPI transport is deferred; semantic output is deterministic.

## N50 — MCP/agent semantics
**Result:** BUILT. `can_use(asset, operation)` produces ALLOW / OFFER_LICENSE / DENY / HOLD / HOLD_UNKNOWN_USAGE_INTENT without generating debt.

## N51 — Free alternative fallback
**Result:** BUILT/PROVEN. Resolver skips unresolved paid offer and selects a source whose policy permits the requested action FREE.

## N52 — Latency observability
**Result:** BUILT BOUNDED. Local `can_use` loop records average milliseconds and an engineering-only 10 ms target; it does not claim production/platform latency.

## N61 — Full deterministic integration
**Result:** PROVEN. Offer accepted -> receipt verifies offline -> ledger hash chain verifies -> €0.10 = 100000 µEUR -> aggregate due 100000 µEUR -> no legal finding.

## N62 — Red Team
**Result:** PROVEN AGAINST CURRENT FIXTURES. Blocks idea capture, public-domain capture, similarity-debt escalation, unresolved C2PA constraint, provenance cycles and unknown usage intent.

# Cycle2 synthesis

The protocol has crossed from architecture into a **bounded interoperable transaction prototype**. The strongest practical architecture is now:

`EXACT ASSET ID -> RIGHTS PASSPORT -> STANDARD POLICY SIGNALS -> AGENT RESOLUTION -> EXPLICIT ACCEPTANCE -> RECEIPT -> IDEMPOTENT LEDGER -> DURABLE READBACK -> PROVENANCE / DISPUTE EVIDENCE`

The major remaining blockers are no longer basic software architecture. They are:
1. real external standard conformance validation beyond hand-built fixtures;
2. federated registry semantics and conflict precedence;
3. formal policy composition for co-rightsholders and royalty splits;
4. production signatures / identities;
5. privacy/GDPR/KYC/tax/payment settlement;
6. legal review of jurisdiction-specific enforceability;
7. creator/platform human testing and economics.

No result in this cycle converts those missing evidence classes into claims.
