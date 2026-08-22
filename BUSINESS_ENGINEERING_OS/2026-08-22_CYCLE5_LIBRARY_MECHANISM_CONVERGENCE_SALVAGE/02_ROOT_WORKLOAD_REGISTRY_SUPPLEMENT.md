# ROOT WORKLOAD REGISTRY SUPPLEMENT — CYCLE5 SALVAGE

This file preserves the unique semantic dedupe result from CX21–CX32. It does **not** replace merged Cycle5 public-artifact authority, PA0–PA5, or P33–P96.

Input provenance: 32 public-regulatory opportunity rows + 32 procurement/capital LIVE32 rows. Compression criterion: recurring buyer workload + decision artifact, not title/category similarity.

## 16 root workloads
R01 Tender/procurement qualification + bid/no-bid -> `TenderDecisionObject` — CURRENT PRIMARY.
R02 Retrofit/energy-upgrade grant qualification/route triage -> `RetrofitQualificationObject` — CURRENT PILOT, narrowed by Cycle5 substitute analysis.
R03 Building/EPBD/renovation/solar technical readiness -> `BuildingReadinessObject` — reserve; requires real property/site packet for deeper work.
R04 AI governance/transparency/literacy/vendor evidence -> `AIEvidenceRegister` — reserve.
R05 Process-specific workflow implementation/automation decision -> `WorkflowAutomationDecisionObject` — CURRENT PILOT, now explicitly post-Digital-for-Business residual job under Cycle5.
R06 CRA product-security lifecycle/incident evidence -> `ProductSecurityEvidenceObject`.
R07 NIS2/entity cyber governance/vendor controls -> `EntityCyberReadinessObject`.
R08 Supplier/product compliance evidence across PPWR/DPP/EUDR/CBAM -> shared Supplier/Product evidence primitives plus separate versioned rule objects.
R09 Repair/product-service data access -> `RepairDataAccessObject`.
R10 Cloud/data portability/exit readiness -> `CloudExitPassport`.
R11 Accessibility regression/evidence -> `AccessibilityRegressionPacket`.
R12 Regulated third-party/vendor register maintenance -> `ThirdPartyRegisterObject`.
R13 Employer/payroll/workforce compliance exceptions -> `EmployerExceptionReconciliationObject`.
R14 Digital grant/change qualification and implementation sequence -> `DigitalChangeFundingObject`.
R15 Infrastructure/project/supplier opportunity intelligence -> `ProjectOpportunityDecisionObject` with domain adapters.
R16 Circular/refurbishment/unsold-inventory disposition -> `DispositionEvidenceObject`.

## Shared primitives allowed
`SourcePassport`, `EntityObject`, `EligibilityRuleObject`, `EvidenceRequirement`, `Deadline/VersionObject`, `UnknownField(null)`, `FatalAssumption`, `PublicObservable`, `DecisionReceipt`, `SupplierEvidence`, `ProductData`, `BuildingObject`, `GrantRuleObject`.

Shared primitives do not merge legal regimes, buyer segments or markets.

## Current WIP crosswalk after merged Cycle5
- R01 = procurement PA3 / PASS_WITH_HOLD; now first Cycle6 causal block P33–P48.
- R02 = retrofit PA3 / NARROWED_PASS_WITH_HOLD; waits for real property packet.
- R05 = workflow implementation PA3 / NARROWED_PASS_WITH_HOLD; waits for real post-Digital-for-Business workflow/report.
Maximum WIP remains 3. R04 is reserve, not a fourth live lane.

## Generic consulting kill law
Generic “AI consulting”, “CISO-as-a-Service”, “digital transformation”, “tourism consulting”, or “implementation support” is not a root workload merely because it can be sold as a service. It must resolve to repeatable inputs, an evidence object, a decision output and a falsifiable observable, or mutate/kill.

## Evidence ceiling
This registry is ontology/deduplication evidence. It does not upgrade PA3 to PA4/PA5 or public E2+ to E3/E4.
