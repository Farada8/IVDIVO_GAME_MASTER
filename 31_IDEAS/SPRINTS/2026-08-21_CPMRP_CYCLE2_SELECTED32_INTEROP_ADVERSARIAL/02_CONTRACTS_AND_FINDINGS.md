# CPMRP CYCLE 2 — CONTRACTS, FINDINGS, PATH TO IMPROVEMENT

## New / strengthened engineering contracts

### C2-01 STANDARD_PROFILE_PURITY
Normative external profiles MUST remain profile-conformant. CPMRP-specific commercial metadata MUST be linked as an extension/sidecar rather than silently redefining TDMRep/ODRL/C2PA semantics.

### C2-02 CONSTRAINED_FAIL_CLOSED
C2PA `constrained` MUST be treated as denied/unresolved until the stated condition or linked policy is successfully resolved.

### C2-03 FEDERATION_NOT_REPLACEMENT
External registries and sector identifiers MUST be interoperable evidence sources. CPMRP MUST NOT claim to replace a future EU registry or established identifier system.

### C2-04 CLAIM_ASSERTION_NOT_OWNERSHIP_PROOF
A registered Asset Passport is a claimant assertion plus evidence bundle. Registration alone MUST NOT set `ownership_verified=true`.

### C2-05 JURISDICTION_EXPLICIT
Rights policies intended for automated decisions MUST carry jurisdiction/territory scope or fail to a bounded HOLD/manual route.

### C2-06 CORRECTION_APPEND_ONLY
Receipt correction/refund/reversal MUST append a superseding object. Original evidence MUST remain addressable.

### C2-07 EXTERNAL_SIGNER_EVIDENCE_BOUNDARY
A signer interface may prove that a signer returned a value; it MUST NOT claim production cryptographic trust without independent key/identity/verification evidence.

### C2-08 DURABLE_RUNTIME_REUSE
CPMRP cross-store write planning MUST use the existing IVDIVO durable transaction compatibility interface. No second transaction/recovery runtime is permitted without a demonstrated incompatibility.

### C2-09 REVERSIBLE_BEFORE_PAYMENT
Registry/ledger persistence may be reversible/readback-gated. Payment/irreversible effects are a separate dispatch class and are forbidden in the current prototype.

### C2-10 COMMONNESS_SUPPRESSION
Similarity evidence MUST include controls for common tropes/styles/generic structures; commonness can reduce provenance confidence and can never increase debt.

### C2-11 INDEPENDENT_CREATION_COUNTEREVIDENCE
The dispute model MUST permit timestamp/process evidence for independent creation. Such evidence does not itself produce a legal judgment.

### C2-12 PROVENANCE_GRAPH_ACYCLIC_FOR_SETTLEMENT
Royalty-bearing provenance edges MUST reject cycles and self-reference, preventing circular/self-dealing settlement loops.

### C2-13 REPUTATION_NOT_TITLE
Claimant reputation/history may inform evidence quality and abuse controls but MUST NOT prove title/ownership or automatically outrank counter-evidence.

### C2-14 HUMAN_APPEAL_REQUIRED
Automated abuse controls MUST offer a human-review appeal route and MUST NOT self-reverse disputed ownership/rights decisions without review evidence.

### C2-15 AGENT_UNKNOWN_MEANS_HOLD_OR_FALLBACK
An AI agent that cannot map usage intent or resolve conditions MUST HOLD or choose another permitted source; it MUST NOT silently reinterpret UNKNOWN as FREE.

### C2-16 TRANSACTION_BEFORE_SETTLEMENT
The production roadmap MUST prove rights resolution, receipts, ledger integrity and durable persistence before introducing settlement/payment dispatch.

## Findings

### F1 — The simplest usable interface survived the Red Team
The public UX can remain simple: `FREE / €0.10 / CUSTOM / NO`. The complexity belongs in policy compilation, receipts, provenance and settlement infrastructure.

### F2 — Existing standards cover the signalling layer better than a proprietary format would
TDMRep/ODRL already provide reservation, policy discovery, consent and compensation semantics for TDM; C2PA provides asset-attached AI/TDM use assertions. CPMRP's unique value is transaction identity, licence acceptance, receipt/ledger, provenance and settlement orchestration.

### F3 — €0.10 is technically viable as ledger accounting, not necessarily as payment rail granularity
The protocol can accumulate 100000 µEUR events without incurring a card transaction per use. Real payout economics remain unproven.

### F4 — Similarity is now correctly demoted from billing to evidence discovery
The code and tests make this explicit. This substantially reduces false-claim and independent-creation risk.

### F5 — Durable recovery is solved architecturally by reuse
Existing SI-0014 semantics already express stale authority, ambiguous reversible writes, required readback and transaction completion. CPMRP needs an adapter and real readbacks, not a new durability subsystem.

### F6 — Registry registration is not rights verification
A serious public product requires a separate claimant identity/title/evidence process, probably jurisdiction- and asset-type-specific.

### F7 — Standard conflict precedence remains intentionally unresolved
robots.txt, contractual site terms, TDMRep, C2PA, platform agreements and statutory rights cannot be placed into a universal legal precedence table by an engineering prototype. The software should expose the signals and route conflicts rather than invent law.

## Path to improvement

**Phase A — Conformance fixtures**
Validate generated TDMRep JSON-LD against independent parsers/examples; validate C2PA assertion structure against current tooling/spec fixtures; create round-trip tests.

**Phase B — Federation + composition**
Add external identifier/registry adapter, claimant conflict resolution, co-rightsholder policy composition, share-total gates and upstream licence propagation.

**Phase C — Security/privacy identity**
Threat model private manuscripts/prompts, selective disclosure, real signing/key rotation, GDPR retention/minimization and claimant identity verification options.

**Phase D — Settlement sandbox**
Model statements, fees, thresholds, escrow/reversals and payment-provider/KYC/tax boundaries without sending money.

**Phase E — Human evidence**
Creator usability, platform/API integration testing, lawyer review, false-positive adjudication study and willingness-to-pay/unit-economics tests.

**Promotion rule:** none of these phases is satisfied by additional prompt volume. Promotion requires independent evidence for the specific claim being promoted.
