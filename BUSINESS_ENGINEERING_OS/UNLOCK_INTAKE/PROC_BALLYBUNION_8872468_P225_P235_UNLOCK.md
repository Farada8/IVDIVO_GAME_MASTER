# PROC-BALLYBUNION-8872468 — P225 / P235 UNLOCK INTAKE

**Date:** 2026-08-22  
**Status:** `AWAITING_AUTHORIZED_INPUT`  
**Authority effect:** none until the specified input is actually supplied and read back.  
**Current roots:**
- `ROOT_A = TARGET_PACK_NOT_ACQUIRED`
- `ROOT_B = NO_EXPLICIT_BIDDER_DESIGNATION_AND_COMPLETE_PACKET`

This intake exists to remove ambiguity at the current causal gate. It does **not** authorize tender submission, outreach, payment, contract acceptance, legal determination, or proof promotion.

## Route A — unlock P225: current official tender pack

### Supply one of these
1. Authenticated eTenders export for resource `8872468`; or
2. User-provided official export/ZIP containing the current tender documents; or
3. All current official attachment files plus an authoritative attachment inventory/revision/addendum listing proving what the current pack is.

### Do not supply
- passwords;
- cookies/session values;
- tokens/API keys;
- copied credentials in metadata or filenames.

### What the engine will do automatically
`OFFICIAL_EXPORT -> SANITIZE_METADATA -> ACQUISITION_RECEIPT -> HASH/SIZE/TYPE/SOURCE/TIME -> CANONICAL_MANIFEST -> INVENTORY_COMPLETENESS_GATE -> REVISION/ADDENDUM_GRAPH -> TENDER_REQUIREMENT_REGISTRY`

Important law:
`OBSERVED_FILES != AUTHORITATIVELY_COMPLETE_PACK`.
A folder or ZIP with plausible filenames is not declared complete unless authoritative completeness evidence exists.

## Route B — unlock P235: actual case-specific bidder designation

Company identity already present in bounded evidence:
- legal entity: `SYNTHESIS-IVDIVO LIMITED`;
- registration number evidence: `796820`.

That identity is **not** bidder designation.

### Required explicit declaration from an authorized actor
Use this only if it is actually intended:

> I designate SYNTHESIS-IVDIVO LIMITED (registration number 796820) as the entity to be evaluated internally as a potential bidder for eTenders resource 8872468. Scope: internal eligibility/capability and BID/HOLD/NO-BID evaluation only. This declaration does not authorize tender submission, outreach, payment, contract acceptance, or legal commitment. Effective timestamp: [date/time]. Authorized actor: [name/role].

Until such a real declaration exists:
`BIDDER_DESIGNATION = MISSING`.

### Bidder evidence is separate from designation
After target requirements are known, the engine may request only evidence actually required by the pack, such as:
- current CRO/company record;
- Tax Clearance;
- insurance and required limits/expiry;
- financial capacity/turnover if required;
- H&S / PSCS / PSDP / certifications if required;
- named personnel and availability if required;
- project references within the required lookback/scope/value dimensions;
- current workload/geography/delivery capacity.

Existing partial evidence must be reused; do not re-search it blindly.

## What happens after one root moves
Progress on either root is valid but downstream requirement join remains blocked until both sides are sufficiently authoritative.

## What happens after both roots are sufficiently closed
`TARGET MANIFEST + BIDDER MANIFEST -> FREEZE -> ATOMIC REQUIREMENT JOIN -> MET / UNKNOWN / CURABLE / NONCURABLE / N/A -> FATAL/CURABLE/UNKNOWN SET -> BOUNDED BID/HOLD/NO-BID CANDIDATE -> INDEPENDENT PA4`

No scalar magic readiness score is authoritative.

## Proof boundary
Current proof remains:
- public/derived ceiling: `E2+`;
- procurement artifact maturity: `PA3`;
- `PA4=false`;
- `PA5=false`;
- `E3=false`;
- `E4=false`.

## Stop rule
If neither Route A nor Route B receives new admissible evidence:
`PROTECT_NO_CHANGE`.
Do not exhaust numeric prompts merely to create activity.
