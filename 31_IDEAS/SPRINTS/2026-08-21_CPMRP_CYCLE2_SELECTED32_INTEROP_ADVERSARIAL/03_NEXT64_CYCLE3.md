# CPMRP CYCLE 3 — NEXT64 EVIDENCE PROMPTS

Derived only after Cycle2 32/32 deterministic proof. These prompts are designed, not claimed executed.

## Conformance / standards
N65 Validate Cycle2 TDMRep JSON-LD against an independent JSON-LD/ODRL processing path and report every profile mismatch.
N66 Build canonical TDMRep examples for FREE, consent-only, consent+compensation and reserved-with-no-offer cases and compare to W3C examples.
N67 Test PDF, HTML and HTTP-header publication representations for the same CPMRP TDM policy and prove semantic equivalence.
N68 Build a C2PA training-mining fixture using current CDDL field names and validate through an independent C2PA toolchain or parser.
N69 Test all four C2PA predefined AI/TDM use cases across allowed/notAllowed/constrained and unknown/missing entry behavior.
N70 Create a round-trip mapper from CPMRP policy -> C2PA/TDMRep -> normalized CPMRP intent and measure information loss explicitly.
N71 Define a formal `external_signal_conflict` object for contradictory TDMRep/C2PA/site-contract signals without deciding legal precedence.
N72 Build a standards-version registry so every emitted assertion/policy records which spec/profile version generated it.

## EU/federated registry
N73 Extract technical identifier/fingerprinting/metadata recommendations from the 2026 EU TDM registry study into a machine comparison table.
N74 Define `ExternalRegistryReference` schema with registry namespace, work ID, fingerprint type, status, timestamp and evidence URL.
N75 Build federation resolver fixtures where exact hash, sector identifier and EU-registry-style record all point to one work version.
N76 Test registry disagreement: same fingerprint, different claimant; return conflict HOLD with no automatic payment.
N77 Test version disagreement: conceptual work ID same, content hash different; preserve version lineage instead of overwriting.
N78 Design cache/freshness semantics for external registry lookups so stale opt-out data cannot silently become current authority.
N79 Define revocation/update handling for an external opt-out registry while preserving previous policy evidence.
N80 Red-team registry namespace squatting and forged external registry references.

## Co-rightsholders / policy composition
N81 Design RightsParty schema for authors, publishers, agents and other claimants without assuming legal priority.
N82 Build co-rightsholder percentage composition with exact 10000-bp conservation gate.
N83 Reject over-allocation above 10000 bp and unresolved under-allocation where automatic settlement is requested.
N84 Model one party FREE and another LICENSE_REQUIRED for the same right/action; route to conflict rather than choosing one silently.
N85 Model territory-specific rightsholders and select policy only for a declared target territory.
N86 Propagate upstream open-licence obligations through derived Asset Passports.
N87 Model public-domain source plus new protectable contribution without charging for the public-domain component.
N88 Build policy supersession chain and prove old receipts remain bound to old policy versions.

## Identity / signing / trust
N89 Define claimant identity assurance levels from anonymous assertion through verified organization without equating identity with rights ownership.
N90 Add signing-key metadata, rotation and revocation schema for receipt attestations.
N91 Implement a real asymmetric signing fixture using a test key and verify signatures offline; mark it cryptographic fixture, not production trust.
N92 Test signature replay across different receipt payloads and prove failure.
N93 Bind signer identity, policy version and receipt hash into an attestation envelope.
N94 Design multi-signature approval for co-rightsholder policies.
N95 Threat-model compromised claimant key and define emergency policy freeze/revocation behavior.
N96 Define trust-store update semantics without centralizing legal ownership judgment.

## Privacy / GDPR / unpublished works
N97 Create data-flow inventory for claimant identity, prompts, drafts, hashes, usage events, payer identity and disputes.
N98 Define minimum public fields for private/unpublished Asset Passports using commitments rather than raw work content.
N99 Test whether deterministic content hashes leak existence of known private files via dictionary matching and design mitigations.
N100 Design salted/private commitment mode and explain interoperability tradeoffs against public exact hashes.
N101 Define retention classes for usage receipts, dispute evidence and raw source material; require legal review before production values.
N102 Build selective-disclosure evidence packet exposing only the facts required for a licence/dispute decision.
N103 Threat-model personal data embedded inside creative works and registry metadata.
N104 Add explicit deletion-request versus immutable-ledger conflict handling without pretending to resolve GDPR law automatically.

## Settlement / finance sandbox
N105 Design creator statement schema separating gross royalty, fees, holds, corrections, taxes and paid amount.
N106 Implement monthly aggregation fixture over 100000 synthetic €0.10 events and verify exact integer totals.
N107 Model payout threshold behavior without losing sub-threshold accrued balances.
N108 Model payer fee as separate line item and prove it never mutates creator gross royalty history.
N109 Add refund/reversal ledger entries that net balances without deleting original receipts.
N110 Design dispute escrow state machine for accrued-but-unpaid amounts.
N111 Compare candidate payment rails at a requirements level: batch support, minimum payout, KYC, fee model, reconciliation APIs; do not choose by marketing claims.
N112 Build payment dispatch boundary interface that cannot execute unless a separate explicit irreversible-action gate is present.

## Security / abuse / provenance
N113 Generate 10,000 synthetic low-evidence Sybil claims and measure ClaimIntegrity/rate-limit behavior deterministically.
N114 Test hash-collision assumptions by attempting malformed/algorithm-substitution IDs; require algorithm identifier and exact digest length.
N115 Add maximum-depth/size limits to provenance graph traversal to prevent denial-of-service.
N116 Detect circular economic benefit across different identities even when the provenance graph itself is acyclic.
N117 Add duplicate receipt/edge/claim canonicalization to prevent volume inflation.
N118 Red-team timestamp evidence: future timestamps, unverifiable references, contradictory clocks and later-source laundering.
N119 Build public-domain corpus controls and prove no monetization policy can override the upstream PUBLIC_DOMAIN state.
N120 Build open-licence corpus controls for attribution/share-alike style conditions without interpreting unmodeled licence clauses as FREE.

## Agent/API/product proof
N121 Write OpenAPI 0.1 for register asset, resolve policy, can_use, accept licence, verify receipt, submit dispute and get statement.
N122 Build an MCP-style tool contract for `resolve_rights` and test deterministic outputs against the Python semantic core.
N123 Add policy-resolution trace explaining which exact signal/passport/rule produced ALLOW/OFFER/DENY/HOLD.
N124 Create agent budget rule: accept micro-licences only below explicit per-use and daily caps; otherwise fallback/HOLD.
N125 Test 1,000-candidate fallback selection for deterministic preference ordering and bounded latency.
N126 Build a synthetic RAG pipeline that resolves rights before adding documents to an index/context and records receipts only when required.
N127 Build a synthetic model-training ingestion manifest that excludes notAllowed/unresolved assets and records policy versions for included ones.
N128 Define Cycle3 promotion gate: which engineering claims may become stable, which require human/legal/payment evidence, and whether CPMRP should remain an IVDIVO module or move to a standalone repository.
