# ZERO CAPITAL EVIDENCE ENGINE v3.0

## Mission
Discover and rank time-bound mandatory-spend / compliance-data opportunities that can be investigated and prototyped with €0 new founder cash, while respecting NO_OUTREACH and refusing to fabricate market proof.

## Engineering modules
1. `M01 FreshAuthorityResolver` — Resolve GitHub main/Drive current state before each material write.
2. `M02 UserConstraintGuard` — Reject outreach, spend or other actions disabled by the current user directive.
3. `M03 OfficialSourceGate` — Require first-party EU/Irish authority for regulatory dates/scope claims.
4. `M04 DeadlineNormalizer` — Store effective/application/reporting dates separately and re-evaluate urgency.
5. `M05 AffectedActorResolver` — Map rule -> economic operator role -> sector -> size/jurisdiction qualifiers.
6. `M06 MandatoryActionExtractor` — Convert rules/guidance into concrete operational actions without legal conclusions.
7. `M07 PublicEvidenceGrader` — Grade official rule, implementation system, guidance, procurement/job/vendor evidence.
8. `M08 PublicEvidenceCeiling` — Hard-cap analysis-only proof at E2+.
9. `M09 ZeroCashDeliveryGate` — Require manual v0 with zero new founder cash.
10. `M10 LiabilityBoundaryClassifier` — Flag legal/certification/security/emissions/conformity claims for specialist handoff.
11. `M11 SubstitutePressureScanner` — Penalise free official tools, cheap templates and mature commodity services.
12. `M12 DataArtifactMapper` — Map each pain into named fields, owners, sources, evidence and handoff artefacts.
13. `M13 ComplianceDataGraph` — Canonical entity/product/obligation/field/evidence/source/change graph.
14. `M14 DPPReadinessAdapter` — DPP identifiers, data ownership, registry/API readiness and missing-data mapping.
15. `M15 EUDREvidenceAdapter` — Supplier/geolocation/evidence completeness and DDS handoff mapping.
16. `M16 CRAReportingAdapter` — 24h/72h/final-report workflow, RACI and evidence readiness.
17. `M17 PPWREvidenceAdapter` — Packaging/SKU/supplier evidence register and change backlog.
18. `M18 GreenTransitionChangeAdapter` — Claims, guarantee/durability information and product-page change inventory.
19. `M19 RepairInformationAdapter` — Repair-service/spares/information completeness mapping.
20. `M20 CBAMDataHandoffAdapter` — Supplier emissions/provenance data tracking with verifier handoff.
21. `M21 NIS2CyFunAdapter` — RMM/CyFun control-to-evidence mapping, with transposition-state gate.
22. `M22 CrossRegulationOverlapEngine` — Find reusable evidence and shared buyers without merging distinct legal tests.
23. `M23 OpportunityScorecard` — Deterministic heuristic routing score; never a proof grade.
24. `M24 KeepMutateKillGovernor` — KEEP/MUTATE/MERGE/KILL based on new evidence and constraints.
25. `M25 PersistenceTransactionAdapter` — GitHub feature branch + Drive mirror + readback; no stale overwrite.
26. `M26 SelfImprovementDeltaAdapter` — Observed defect -> minimal repair -> regression -> provenance -> rollback.

## Engineering contracts
- **C01 NO_OUTREACH** — No emails/calls/DMs/contact while user constraint is active.
- **C02 ZERO_NEW_CASH** — Founder new cash-out must remain €0 in research/manual-v0 stage.
- **C03 FRESH_AUTHORITY** — Material action requires fresh GitHub/Drive authority read.
- **C04 OFFICIAL_SOURCE** — Regulatory dates/scope require current first-party authority.
- **C05 DATE_SEMANTICS** — Entry-into-force, application, reporting and future full-application dates cannot be conflated.
- **C06 PUBLIC_PROOF_CEILING** — Analysis/public evidence cannot exceed E2+.
- **C07 NO_EVIDENCE_LAUNDERING** — Model score, sample artifact, persisted file or public source is not buyer/payment proof.
- **C08 LIABILITY_BOUNDARY** — No legal advice, certification, conformity, security assurance or emissions verification claims.
- **C09 SCOPE_UNKNOWN_FAIL_CLOSED** — Unknown jurisdiction/operator classification remains UNKNOWN and blocks definitive claims.
- **C10 MANUAL_V0** — Candidate must have a meaningful manual deliverable before software.
- **C11 BUYER_BEFORE_BUILD** — No SaaS/product build before real E3/E4 if outreach is later enabled.
- **C12 SUBSTITUTE_PENALTY** — Free/official commodity substitutes reduce score and can trigger KILL.
- **C13 DATA_ACCESS_FEASIBILITY** — Candidate must identify required data and whether a client could practically supply it.
- **C14 ARTIFACT_SPECIFICITY** — Every opportunity must compile to named inputs/outputs, not vague consulting.
- **C15 ECONOMICS_NULL_UNTIL_MEASURED** — Unmeasured time, price, conversion and margin remain null.
- **C16 FINANCE_AFTER_PROOF** — Debt/grants/investors may accelerate only after demand proof; never substitute for it.
- **C17 STALE_WRITER_CAS** — Concurrent stale writes cannot overwrite newer authority.
- **C18 READBACK_REQUIRED** — Persistence is incomplete until destination readback verifies content.
- **C19 NO_DUPLICATE_RUNTIME** — Reuse current Self-Improvement/persistence primitives; add only domain adapters.
- **C20 STOP_IF_NO_DECISION_DELTA** — Prompts/modules that do not change a decision, artifact or proof state are pruned.

## Proof ladder
- `E0` — hypothesis only.
- `E1` — current first-party authority signal exists.
- `E2` — observable implementation workload/pain from official systems, guidance, required data or credible public operational evidence.
- `E2+` — multiple independent public/official signals plus a reproducible manual artifact/fixture; **maximum allowed in NO_OUTREACH mode**.
- `E3` — explicit real buyer engagement/request. Not reachable in this cycle.
- `E4` — real payment/deposit/PO. Not reachable in this cycle.
- `E5` — repeat paid delivery.
- `E6` — measured retention/economics/bankability.
- `E7` — scaled repeatable system.

## Protocols
- `R-AUTH`: fresh repo/Drive -> resolve active authority -> classify stale/superseded -> only then act.
- `R-SHOCK`: official source -> exact date semantics -> affected actor -> mandatory action -> operational artefact.
- `R-ZERO`: artefact -> required inputs -> manual workflow -> zero-cash gate -> specialist boundaries.
- `R-SUBSTITUTE`: official/free tools -> vendor/commodity substitutes -> remaining messy-data pain -> score/kill.
- `R-OVERLAP`: buyer/product -> multiple obligations -> shared evidence primitives -> rule-specific adapters -> no false equivalence.
- `R-PROOF`: source refs -> fixture/readback -> E2/E2+ only; no E3/E4 promotion without external events.
- `R-KMK`: new evidence -> KEEP/MUTATE/MERGE/KILL -> update state -> retire superseded prompts.
- `R-PERSIST`: feature branch write -> Drive mirror -> readback -> compare freshness -> PR draft.
- `R-SI`: defect -> minimal delta -> regression -> provenance -> rollback -> promote only after evidence.

## State machine
`FRESH_AUTHORITY -> USER_CONSTRAINTS -> OFFICIAL_SIGNAL -> ACTOR/SCOPE -> MANDATORY_ACTION -> ARTIFACT -> ZERO_CASH -> SUBSTITUTE/LIABILITY -> PUBLIC_EVIDENCE -> E2/E2+ -> KEEP/MUTATE/KILL -> PERSIST`

External branch is intentionally absent while `NO_OUTREACH=true`.
