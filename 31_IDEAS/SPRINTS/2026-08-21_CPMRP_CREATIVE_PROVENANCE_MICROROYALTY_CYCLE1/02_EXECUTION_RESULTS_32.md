# CPMRP CYCLE 1 — EXECUTION RESULTS 01–32

Each prompt was executed in sequence against the current IVDIVO engineering baseline, current public standards research, and the explicit evidence ceiling. `KEEP/BUILD/REUSE` means engineering disposition, not legal validation.

## R01 — Define the CPMRP problem and non-goals
**Result:** KEEP. Core product is licensing/provenance infrastructure, not an 'idea tax'. Non-goals must be normative because otherwise the system invites abusive claims.

## R02 — Map idea vs expression vs rights-bearing asset
**Result:** KEEP. Only rights-bearing or contractually licensed objects may trigger a debt. IDEA/STYLE/TROPE default FREE/NO_DEBT unless a separate enforceable agreement exists.

## R03 — Build a rights-basis matrix
**Result:** KEEP. Every decision must carry rights_basis; UNKNOWN cannot be converted into money owed.

## R04 — Test EU TDM opt-out fit
**Result:** REUSE. TDM reservation is a strong interoperability path for mining/training, but it does not generalize to all inspiration/reference uses.

## R05 — Test C2PA training/mining assertions
**Result:** REUSE. Add C2PA adapter. 'constrained' points to CPMRP policy/offer; do not invent new C2PA semantics.

## R06 — Test TDMRep + ODRL fit
**Result:** REUSE. TDMRep already supports policy discovery and ODRL-based financial compensation duty; CPMRP should profile rather than replace it.

## R07 — Map EU AI Act/GPAI obligations
**Result:** KEEP BOUNDED. Protocol can expose rights reservations and audit receipts; legal compliance remains provider/counsel responsibility.

## R08 — Assess EU-level TDM registry direction
**Result:** KEEP. Work-based identifiers, fingerprinting and metadata are directly aligned; design registry adapter rather than central monopoly.

## R09 — Benchmark AI Provenance Protocol prior art
**Result:** REUSE CONCEPTS. APP is output provenance; CPMRP is rights/licence/royalty provenance. Interoperate via external_provenance_refs.

## R10 — Define Asset ID
**Result:** BUILD. asset_id = namespace + canonical content SHA-256 + version identity; never use semantic similarity as identity.

## R11 — Define version lineage
**Result:** BUILD. parent_asset_ids + relation type; hash identifies exact version; registry ID identifies conceptual work/version lineage.

## R12 — Design Rights Passport
**Result:** BUILD. claimant, asset hash, rights basis, territories, actions, price rule, policy URI, provenance refs, status, timestamps, evidence ceiling.

## R13 — Design policy semantics
**Result:** BUILD. FREE, OFFER, LICENSE_REQUIRED, NEGOTIATE, PROHIBITED, UNKNOWN. UNKNOWN is fail-closed for automation and creates no debt.

## R14 — Normalize usage intent
**Result:** BUILD. UsageIntent is mandatory input to licence evaluation; price is action-specific.

## R15 — Model €0.10 pricing
**Result:** BUILD. Use integer euro-micro units; €0.10 = 100000 µEUR. No binary floats in accounting.

## R16 — Avoid payment-fee collapse
**Result:** BUILD. Append usage events to internal ledger, aggregate by payee/payer/period, settle only after threshold or scheduled batch.

## R17 — Design licence receipt
**Result:** BUILD. Receipt must be immutable/hash-addressed and signed/attested by platform when cryptographic signing exists.

## R18 — Guarantee idempotency
**Result:** BUILD. usage_event_id + idempotency_key unique per payer/action/asset/request lineage; duplicate event returns same receipt.

## R19 — Design similarity evidence engine
**Result:** BUILD BOUNDED. Engine outputs evidence signals + confidence + source candidates; debt requires accepted licence/contract or independently valid legal basis.

## R20 — Design provenance graph
**Result:** BUILD. Directed graph with typed edges: exact_copy, derived_from, declared_reference, training_source, licensed_use, disputed_similarity.

## R21 — Defend against false positives
**Result:** BUILD. Require multi-feature evidence, rarity weighting, timestamp ordering and access evidence where available; generic trope/style matches are suppressed.

## R22 — Handle independent creation
**Result:** BUILD. Independent-creation evidence may rebut provenance inference; similarity never creates an irreversible debt automatically.

## R23 — Handle public domain and open licences
**Result:** BUILD. PUBLIC_DOMAIN => zero price/no restriction; OPEN_LICENSE obeys licence conditions; CPMRP cannot add restrictions inconsistent with upstream licence.

## R24 — Protect private prompts and source files
**Result:** BUILD. Hashes/proofs may be public; raw prompts, drafts and private source assets default private. Disclosure is opt-in or dispute-specific.

## R25 — Design dispute/appeal flow
**Result:** BUILD. DISPUTED state freezes unsettled contested amount, preserves evidence, supports counter-evidence and human/legal review; no automated final infringement judgment.

## R26 — Defend against claim spam/Sybil attacks
**Result:** BUILD. claimant reputation, evidence requirement, duplicate/earlier-source detection, rate limits, stake/review for escalated claims; ideas/styles rejected at intake.

## R27 — Design platform API
**Result:** BUILD. REST/JSON first; later DID/VC/signatures optional. API must support offline verification of hashes and policy versions.

## R28 — Design creator UX
**Result:** BUILD. One-screen defaults: upload/hash, choose rights basis, select uses, set price, publish. Advanced legal fields hidden behind profiles.

## R29 — Design AI-agent integration
**Result:** BUILD. Agent flow: DISCOVER -> RESOLVE_POLICY -> EVALUATE_INTENT -> ACCEPT/FALLBACK -> RECEIPT -> USE -> LEDGER. Fallback means choose another source, not silently ignore.

## R30 — Bridge to IVDIVO self-improvement
**Result:** REUSE. Follow engineering_autorun and learning_loop; CPMRP remains bounded R&D until real creator/platform/legal evidence exists.

## R31 — Define MVP
**Result:** KEEP. MVP = exact asset hash registry + rights passport + €0.10 licence offer + idempotent receipt + hash-chain royalty ledger + TDMRep/C2PA policy export + no similarity charging.

## R32 — Red-team and gate
**Result:** KEEP. GO for closed sandbox pilot after deterministic tests and policy export validation. NO-GO for public claims of enforceable universal royalties, automated infringement decisions, or real payouts without payment/KYC/tax/legal design.
