# CPMRP v0.1 — ARCHITECTURE, CONTRACTS, PROOFS & PROTOCOLS

## 1. Product boundary

### What CPMRP can do
- register a concrete creative asset/version fingerprint;
- store a claimant assertion and evidence references;
- publish machine-readable permission/licence rules;
- expose an opt-out/licence-discovery adapter for TDM;
- offer a €0.10 or other micro-licence for specific actions;
- let an AI agent/platform accept the offer before use;
- create an immutable licence receipt;
- append an idempotent royalty event to an auditable ledger;
- batch settlement obligations;
- record source/provenance graph edges;
- surface similarity evidence for review.

### What CPMRP must never infer automatically
- ownership of an abstract idea/style/trope;
- legal infringement from semantic similarity;
- debt from an unaccepted voluntary offer;
- validity of a claimant's copyright merely because they registered first;
- enforceability outside the declared rights/jurisdiction basis.

## 2. Core engine

`INGEST -> HASH -> PASSPORT -> RIGHTS_BASIS -> POLICY_COMPILE -> PUBLISH -> DISCOVER -> USAGE_INTENT -> LICENSE_RESOLVE -> ACCEPT/FALLBACK -> RECEIPT -> LEDGER -> AGGREGATE -> SETTLE -> PROVENANCE_GRAPH -> AUDIT`

Similarity is a side-channel:
`CANDIDATE_DISCOVERY -> EVIDENCE_BUNDLE -> HUMAN/LEGAL REVIEW`
and never a direct `-> DEBT` edge.

## 3. Engineering modules

1. **AssetIdentityEngine** — canonical hash, namespace, version ID.
2. **VersionLineageEngine** — parent/child and derivative relations.
3. **RightsPassportRegistry** — claimant assertion + evidence refs + status.
4. **RightsBasisClassifier** — copyright/contract/TDM/open/public-domain/tip/unknown.
5. **PolicyCompiler** — internal policy -> ODRL/TDMRep/C2PA-compatible representations.
6. **UsageIntentNormalizer** — maps platform action to protocol taxonomy.
7. **LicenseResolver** — returns FREE/OFFER/LICENSE_REQUIRED/NEGOTIATE/PROHIBITED/UNKNOWN.
8. **MicroPriceEngine** — integer µEUR accounting; never floats.
9. **ConsentAndReceiptEngine** — explicit acceptance and immutable receipt binding.
10. **IdempotencyGuard** — retries cannot double-charge.
11. **RoyaltyLedger** — append-only hash-chain usage accounting.
12. **SettlementAggregator** — payer/payee/period batching and payout threshold.
13. **ProvenanceGraphEngine** — typed lineage/reference edges.
14. **SimilarityEvidenceEngine** — candidate discovery only; no legal finding/debt.
15. **DisputeHoldEngine** — freezes contested unsettled amounts and preserves evidence.
16. **ClaimIntegrityEngine** — reject idea/style/trope claims; detect duplicates/earlier sources.
17. **PrivacyBoundaryEngine** — public proof hashes, private raw prompts/drafts by default.
18. **InteropPublisher** — TDMRep/C2PA/ODRL/HTTP/API publication adapters.
19. **AuditProofPackager** — evidence bundle for receipts, policies, hashes and lineage.
20. **IVDIVOSelfImprovementBridge** — bounded test -> evidence -> regression -> promotion review; no automatic SI promotion.

## 4. Normative contracts

### C-01 ASSET_IDENTITY
An `asset_id` MUST bind an exact content digest and version identity. Similarity fingerprints MUST NOT substitute for exact asset identity.

### C-02 RIGHTS_BASIS_REQUIRED
Every active monetizable policy MUST declare `rights_basis`. `UNKNOWN` MUST NOT create an automatic debt.

### C-03 IDEA_STYLE_TROPE_NO_DEBT
Abstract idea, style, genre, trope, common motif, method or unparticularized concept MUST NOT become a CPMRP payable asset solely through registration.

### C-04 ACTION_SPECIFIC_POLICY
A price/permission MUST bind a normalized usage action. "Use" without action semantics is insufficient for automatic charging.

### C-05 ACCEPTANCE_BEFORE_VOLUNTARY_DEBT
An `OFFER` MUST create zero debt until accepted. A platform MAY pre-authorize a standing licence contract, but the contract reference must be receipt-bound.

### C-06 INTEGER_ACCOUNTING
All monetary values MUST use integer minor/micro units. No binary floating-point values are allowed in ledger state.

### C-07 IDEMPOTENT_USAGE
`usage_event_id` and payer-scoped idempotency key MUST prevent duplicate charges under retries/replay.

### C-08 POLICY_VERSION_BINDING
Every receipt MUST bind the exact policy version that was resolved at the decision point.

### C-09 PROVENANCE_NOT_INFRINGEMENT
Similarity/provenance scores MUST expose `legal_infringement_finding=false` unless an external authorized legal adjudication object is explicitly attached.

### C-10 DISPUTE_FAIL_CLOSED
Contested unpaid amounts MUST be held, not silently paid or deleted, until a permitted resolution route completes.

### C-11 UPSTREAM_LICENSE_SUPREMACY
CPMRP MUST NOT impose restrictions inconsistent with public-domain status or an upstream open licence.

### C-12 PRIVACY_MINIMIZATION
Raw prompts/drafts/source assets MUST default private. Public registry proof may use hashes/commitments and disclosed metadata.

### C-13 EXTERNAL_STANDARD_PROFILE
CPMRP SHOULD profile/reuse TDMRep, ODRL and C2PA semantics rather than fork equivalent meanings.

### C-14 EVIDENCE_CEILING
Every machine state MUST declare what has and has not been proven.

### C-15 NO_AUTOMATIC_SI_PROMOTION
R&D output MUST NOT update IVDIVO CURRENT self-improvement authority without the existing promotion lifecycle.

### C-16 SETTLEMENT_SEPARATION
A valid micro-royalty ledger event is not itself a payment. Settlement/KYC/tax/payment proofs are separate evidence classes.

## 5. Proof obligations

**P-01 ExactHashDeterminism** — same bytes/namespace/version -> same asset ID.  
**P-02 FreeRead** — FREE action -> zero amount.  
**P-03 TenCentOffer** — INFERENCE_REFERENCE example -> 100000 µEUR.  
**P-04 OfferNoDebtBeforeAcceptance** — offer decision itself -> creates_debt=false.  
**P-05 UnknownNoDebt** — missing rule -> UNKNOWN/zero/fail-closed.  
**P-06 PublicDomainNoCharge** — public-domain basis overrides paid training rule.  
**P-07 RejectedOfferZeroReceipt** — declined licence -> zero receipt amount.  
**P-08 IdempotentLedger** — replay same usage event -> one ledger event.  
**P-09 HashChainIntegrity** — ledger chain verifies.  
**P-10 SimilarityNoDebt** — even maximal similarity signal -> creates_debt=false and no legal finding.

Cycle 1 deterministic local proof result: **10/10 PASS**.

## 6. Protocol objects

### AssetPassport
Minimum:
- `asset_id`
- `claimant_id`
- `rights_basis`
- `policy_version`
- `status`
- `evidence_refs[]`
- `parent_asset_ids[]`

### RightsPolicy
- `asset_id`
- `policy_version`
- rules keyed by normalized Action:
  - state
  - integer `amount_micro_eur`
  - optional constraints
  - territory/jurisdiction profile
  - policy URI

### UsageRequest
- `usage_event_id`
- `idempotency_key`
- `payer_id`
- `asset_id`
- `action`

### LicenseReceipt
- receipt digest/ID
- usage event
- payer/payee
- asset/action
- amount
- exact policy version
- accepted flag
- optional signature/attestation reference

### LedgerEntry
- monotonic sequence
- usage event
- receipt
- payer/payee
- amount
- previous entry hash
- entry hash

## 7. €0.10 flow

Example:
1. creator registers asset;
2. creator policy: `INFERENCE_REFERENCE = OFFER €0.10`;
3. AI agent discovers policy;
4. agent either accepts, uses a free alternative, or asks for negotiation;
5. accepted licence creates receipt for `100000 µEUR`;
6. ledger appends once even if the request retries;
7. settlement engine aggregates many events;
8. payout occurs under separate payment/KYC/tax rules.

This makes ten cents an **accounting unit**, not necessarily a ten-cent card transaction.

## 8. TDM / AI training flow

For web-hosted assets:
- publish TDM reservation by an appropriate machine-readable mechanism;
- expose policy URI;
- policy may describe how authorisation can be obtained;
- map protocol action `TRAIN/TDM` to the relevant TDM policy profile;
- for compatible media, optionally publish C2PA training-mining assertion as `constrained` with policy reference/context;
- save a resolution receipt before ingestion where platform contract requires it.

CPMRP does not claim that every jurisdiction gives identical effect to these signals.

## 9. Similarity / reference flow

The SimilarityEvidenceEngine can evaluate:
- exact/near-exact fingerprint;
- rare terminology;
- structural combinations;
- declared/access evidence;
- timestamp ordering;
- public-domain/common-trope controls.

Output:
- candidate score;
- explainable feature vector;
- candidate source IDs;
- `creates_debt=false`;
- `legal_infringement_finding=false`.

Only a separately valid licence/contract/legal process may convert a usage event into a payable obligation.

## 10. Anti-abuse protocol

Reject or hold:
- "I own dragons" / "I own first-person narration" / style-only claims;
- later registrations that attempt to overwrite earlier provenance;
- duplicate registration without lineage declaration;
- public-domain capture;
- unverified mass claims with no evidence refs;
- similarity alerts based only on generic tropes;
- fabricated access evidence;
- self-dealing loops intended to manufacture royalty volume.

## 11. Self-improvement bridge

CPMRP uses the existing IVDIVO laws:
`OBSERVE -> EARLIEST_FAILURE -> CHEAPEST_DISCRIMINATING_TEST -> MINIMAL_PATCH -> INDEPENDENT_EVIDENCE -> REGRESSION/ROLLBACK -> WRITE_THROUGH`

Candidate improvements from this cycle:
- rights-basis gating;
- similarity-no-debt invariant;
- policy-version receipts;
- accounting/payment separation;
- upstream-licence supremacy;
- machine-readable opt-out/licence adapters.

None are promoted to global SI authority by this sprint.

## 12. Pilot gates

### GO — closed sandbox
- all deterministic tests green;
- schema validation;
- ODRL/TDMRep export fixture validated;
- C2PA mapping reviewed;
- no real-money movement;
- clearly synthetic demo assets;
- no claim of universal legal enforceability.

### NO-GO — public enforcement
Until external proof exists:
- no universal "you owe €0.10" claim;
- no automatic infringement judgment;
- no payout network;
- no public dispute adjudication;
- no legal-advice positioning;
- no creator ownership verification claim.

## 13. Practical conclusion

The technically viable product is not "copyright on every idea". It is a **rights-policy and provenance transaction layer** that makes legitimate licensing cheaper than ignoring provenance. The first credible wedge is machine-readable licensing for concrete assets, especially AI/TDM workflows, with ten-cent micro-royalties accumulated in a ledger and settled in batches.
