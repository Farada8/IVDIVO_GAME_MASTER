# BUSINESS ENGINEERING OS — OPPORTUNITY ROOT REGISTRY — POST CX32

**Input provenance:** 32 public-regulatory objects + 32 Procurement/Capital LIVE32 objects.  
**Evidence ceiling:** public/source only. `willingness_to_pay=null`, `payment_evidence=0`, `profitability=null`.  
**Rule:** rows are recurring buyer workloads, not markets proven to exist at profitable scale.

| Root | Buyer workload | Canonical decision artifact | Fatal assumption | Cheapest public observable | Ceiling | WIP |
|---|---|---|---|---|---|---|
| R01 | Tender/procurement qualification + bid/no-bid | `TenderDecisionObject` | enough SMEs repeatedly face relevant tenders and lose time/fit decisions | public tender frequency + eligibility/evidence complexity + repeat-buyer/supplier patterns | S<=4/E<=2 | ACTIVE PRIMARY |
| R02 | Retrofit/energy-upgrade lead + grant qualification/orchestration | `RetrofitQualificationObject` | coordination/qualification pain is not already fully bundled by installers/SEAI workflow | public grant steps, installer offers, assessor/quote/document gaps | S<=4/E<=2 | ACTIVE PILOT |
| R03 | Building/EPBD/renovation/solar technical-readiness planning | `BuildingReadinessObject` | addressable workflow exists outside state/installer tools and can be standardized | public Irish implementation, assessor tools, solar/renovation workflow gaps | S<=4/E<=2 | RESERVE |
| R04 | AI governance/transparency/literacy/vendor evidence | `AIEvidenceRegister` | SMEs have fragmented cross-tool evidence rather than incumbent HR/LMS/platform coverage | public chatbot disclosure scan, policies, LMS/HR feature coverage, vendor docs | S<=4/E<=2 | RESERVE |
| R05 | Process-specific AI/workflow automation decision | `WorkflowAutomationDecisionObject` | a repeatable business process bottleneck can be diagnosed from evidence and mapped to measurable automation options | public workflow/job descriptions, tool coverage, before/after task model | K/S only/E<=2 | ACTIVE PILOT |
| R06 | CRA product-security lifecycle + incident reporting | `ProductSecurityEvidenceObject` | affected SMEs lack CRA-specific field/timing orchestration | official field/timing requirements vs public incident/SBOM tooling | S<=4/E<=2 | RESERVE |
| R07 | NIS2/entity cyber governance + vendor/controls evidence | `EntityCyberReadinessObject` | uncertainty still produces active readiness workload in Ireland | public tenders/jobs/guidance/control mappings | S<=4/E<=2 | RESERVE |
| R08 | Supplier/product compliance evidence for PPWR/DPP/EUDR/CBAM | `SupplierProductEvidenceBundle` + versioned rule objects | shared data normalization is valuable without becoming a full traceability platform | public schemas, supplier documents, SKU/product data gaps | S<=4/E<=2 | RESERVE |
| R09 | Repair/product-service data access | `RepairDataAccessObject` | a narrow product vertical has fragmented repair/data-access information that can be normalized | public repair pages, spare data, vendor API/access procedures | S<=4/E<=2 | RESERVE |
| R10 | Cloud/data portability + exit readiness | `CloudExitPassport` | switching/exit work recurs enough to support a repeatable productized service | public export/contract/portability differences across SME stacks | S<=4/E<=2 | HOLD_RECURRENCE |
| R11 | Accessibility regression/evidence | `AccessibilityRegressionPacket` | generic accessibility tools do not already satisfy the operational evidence job | scan public SME sites + compare checker outputs/evidence gaps | S<=4/E<=2 | RESERVE |
| R12 | Regulated third-party/vendor register maintenance | `ThirdPartyRegisterObject` | maintenance/data-quality burden remains material after implementation | public schemas, job roles, register-maintenance artifacts | S<=4/E<=2 | HOLD_MAINTENANCE |
| R13 | Employer/payroll/workforce compliance exceptions | `EmployerExceptionReconciliationObject` | enough exception classes remain outside payroll/HR automation | public help-centre topics, payroll integrations, guidance changes | S<=4/E<=2 | RESERVE |
| R14 | Digital grant/change qualification and implementation sequence | `DigitalChangeFundingObject` | provider/founder eligibility and programme rules allow a viable delivery route | public eligibility matrix + approved/eligible software/process rules | S<=4/E<=2 | RESERVE_ZERO_CASH |
| R15 | Infrastructure/project/supplier opportunity intelligence | `ProjectOpportunityDecisionObject` | heterogeneous sectors can share qualification mechanics without losing domain-specific evidence | recurring public procurement notices + supplier qualification fields | S<=4/E<=2 | HOLD_DOMAIN_SPLIT |
| R16 | Circular/refurbishment/unsold-inventory disposition | `DispositionEvidenceObject` | recurring compliance/economic workflow is externally addressable rather than incumbent/internal | public sustainability reports, repair/refurbishment programmes, disposition partners | S<=4/E<=2 | RESERVE |

## Shared primitives allowed
- `SourcePassport`
- `Buyer/EntityObject`
- `EligibilityRuleObject`
- `EvidenceRequirement`
- `Deadline/VersionObject`
- `UnknownField(null)`
- `FatalAssumption`
- `PublicObservable`
- `DecisionReceipt`
- `SupplierEvidence`
- `ProductData`
- `BuildingObject`
- `GrantRuleObject`

Sharing primitives does not merge legal regimes, buyer jobs or markets.

## Active WIP law
Current Business OS authority caps market WIP at 3. After CX32:
1. **R01 PRIMARY — TenderDecisionObject**
2. **R02 PILOT — RetrofitQualificationObject**
3. **R05 PILOT — WorkflowAutomationDecisionObject**

R04 is first reserve because the public-regulatory signal is strong, but opening it before a current WIP slot closes would violate the Reinertsen-derived WIP constraint and current authority.

## Kill law
A root is KILL/MUTATE when its public-artifact test cannot distinguish it from generic consulting, produces no repeatable input schema/decision artifact, or the decisive public observable shows incumbent/state/provider tooling already closes the job at negligible external coordination cost.
