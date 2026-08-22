# BIDDER PRIMARY EVIDENCE DELTA — POST-MERGE CLOSURE

**Date:** 2026-08-22  
**Core PR:** #253  
**Core merge:** `071d4b37e8d2cef395f9e12bcfb919eefb1158cc`  
**Final reviewed head:** `28567d74e4ce17d0e533c72aadec92c15753f2c3`  
**Exact-head CI:** `32551065277` — SUCCESS  
**Review threads:** 0  
**Drive readback:** PASS 2/2.

## Merged evidence state
`PARTIAL_IDENTITY_PLUS_CORE_SCREEN_PLUS_TAX_ACCOUNT_EVIDENCE_PLUS_SELF_ISSUED_EWI_RECORDS`.

This is an additive supplier-side evidence upgrade only. It is not a bidder designation and not a verified SupplierCapabilityPacket.

## Admissible evidence delta
- official CORE-interface screenshot binds legal identity to registration number `796820` and shows status `Normal`, with capture timestamp unproven;
- Revenue/ROS evidence establishes tax registration/account evidence and historical account state at 2026-08-07 20:19 +01:00, not Tax Clearance;
- three seller-issued EWI invoice families across May/June/July 2026 contain concrete external-insulation/render scope;
- at least two counterparty groups and multiple sites are represented;
- May duplicate variants are one invoice family with unresolved period conflict;
- independent payment evidence was not recovered;
- actual insurance certificate was not recovered;
- independent client completion/reference evidence remains absent.

## Backlog effects
- P235 HOLD_NO_EXPLICIT_BIDDER_DESIGNATION;
- P237 PARTIAL_OFFICIAL_SCREEN_REG_NUMBER_CURRENT_CERTIFIED_EXTRACT_MISSING;
- P243 PARTIAL_TAX_REGISTRATION_AND_HISTORICAL_ACCOUNT_EVIDENCE_CLEARANCE_MISSING;
- P244 HOLD_NO_INSURANCE_CERTIFICATE;
- P248 PARTIAL_SELF_ISSUED_EWI_RECORDS_THIRD_PARTY_REFERENCE_UNPROVEN;
- P250–P255 BLOCKED_PRECONDITIONS.

## Proof boundary
E2+ public/derived ceiling; PA3 artifact plane; PA4/PA5/E3/E4 remain false. No target BID/HOLD/NO-BID, paid-revenue, procurement-eligibility, legal-clearance or profitability claim.

## Drive
Folder `1x_Y-X-Bqd-tbAV1Lkbs2sksXcZAi5-WZ`.
- dossier `1tzCl_iRPwtepuk_PaaYh4y2tCnxKifpluUwGjO_0Hmc` — readback PASS;
- machine/proofs `1AtcvNgOQF21z1e4w_0nLodfb2lMSYUh0qLcc6yeChCc` — readback PASS.

## Current causal frontier
`TARGET_PACK_NOT_ACQUIRED + BIDDER_DESIGNATION_MISSING` still block the atomic join.

Use this merged evidence to avoid duplicate searches. Acquire only decision-changing evidence next: authenticated current target pack, explicit bidder designation, and target-required missing bidder evidence.
