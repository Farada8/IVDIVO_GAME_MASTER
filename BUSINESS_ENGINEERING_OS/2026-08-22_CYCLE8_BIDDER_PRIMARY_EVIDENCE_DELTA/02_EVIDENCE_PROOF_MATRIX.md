# CYCLE8 BIDDER PRIMARY EVIDENCE DELTA — PROOF MATRIX

| Evidence family | What it proves | What it does NOT prove | Current disposition |
|---|---|---|---|
| CORE official-interface screenshot | legal-name binding, company number 796820, company type, screen-displayed `Normal` | fresh certified CRO extract; present-time status unless screen capture freshness is independently proven | `PARTIAL_COMPANY_AUTHORITY` |
| CORE screen showing B1 registered 2026-05-22 | screen is not older than the displayed registered event | exact capture date; current status on 2026-08-22 | `FRESHNESS_LOWER_BOUND_ONLY` |
| Revenue Request for Payment dated 2026-08-05 | official tax correspondence existed on that date | Tax Clearance Certificate; current debt after later payments/filings | `HISTORICAL_TAX_CORRESPONDENCE` |
| ROS Online Statement timestamped 2026-08-07 20:19 | PAYE-EMP registration/account evidence and historical account state at that timestamp | present tax clearance or present balance | `TAX_REGISTRATION_PARTIAL` |
| May 2026 EWI invoice family | seller-issued commercial record for EWI/acrylic-render scope | payment, client acceptance, independent completion reference | `SELF_ISSUED_DELIVERY_RECORD` |
| June 2026 EWI invoice family | seller-issued EWI installation/detailing record | payment, client acceptance, tender threshold compliance | `SELF_ISSUED_DELIVERY_RECORD` |
| July 2026 EWI invoice family | seller-issued EWI work across multiple sites | payment, client acceptance, tender threshold compliance | `SELF_ISSUED_DELIVERY_RECORD` |
| May invoice duplicate variants | same invoice family exists in multiple stored versions | two independent jobs; resolved authoritative work-period metadata | `VERSION_CONFLICT_ONE_FAMILY` |
| Search for receipt/remittance | no matching independent payment artifact recovered in bounded Library search | proof that no payment ever occurred | `PAYMENT_EVIDENCE_NOT_FOUND_NOT_NONEXISTENCE` |
| Insurance bounded search | no actual company insurance policy/certificate recovered | proof company has no insurance | `INSURANCE_EVIDENCE_NOT_FOUND_NOT_NONEXISTENCE` |

## Evidence-owner routing
### Company identity / CRO
Owner evidence still needed: current official/certified CRO extract or equivalent authoritative current record if the target requires it.

### Tax
Owner evidence still needed: current Tax Clearance Certificate / TCAN or other target-authorized tax-clearance evidence. A historical ROS balance is never treated as a current clearance decision.

### Construction delivery
Current evidence is stronger than public marketing: dated seller-issued commercial records carry concrete EWI work scopes. But capability remains `PARTIAL` until the target requirements are known and, where required, completion/reference/certification evidence is supplied.

### Insurance / H&S / capacity
Remain `UNKNOWN/HOLD` until primary evidence is recovered.

### Bidder designation
Remains absent. The existence of Synthesis-Ivdivo evidence does not designate the company as bidder for `8872468`.

## Privacy rule
Public GitHub derivatives must not contain private client contact data, private tax identifiers, bank-account details or exact residential work addresses copied from raw evidence. Raw sources remain private and should be joined through provenance pointers/hashes rather than republished.
