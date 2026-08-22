# CURRENT TENDER PACK ACQUISITION STATE — 8872468

## Current official case
Resource: `8872468`.
Decision use: procurement qualification artifact / test fixture.

Externally observable current facts remain limited to notice/workspace-level data plus the official document route. The complete current document byte set, revision history, addenda and attachment inventory have not been recovered through the accessible indexed surface.

### Current acquisition result
`CURRENT_PACK_STATUS = BLOCKED_AUTHENTICATED_OR_NONINDEXED_DOCUMENT_SURFACE`

This is a first-class result, not a retrieval failure to be hidden.

## Historical same-buyer analog
Historical resource: `8176962`.
Classification: `HISTORICAL_ANALOG_ONLY`.

The historical document surface exposed six entries:
1. Billsoft document;
2. `St.Josephs-Etender.zip` / drawings-documents bundle;
3. tender structure XML;
4. ESPD request — national criteria;
5. extended ESPD request;
6. ESPD request PDF.

## Allowed use of the analog
The analog may define a retrieval checklist:
- seek the current tender ZIP/document bundle;
- seek pricing/Billsoft or equivalent pricing structure;
- seek tender-structure data;
- seek ESPD/exclusion/selection documentation;
- seek all current addenda and revision artifacts;
- hash recovered bytes and preserve source/revision provenance.

## Forbidden use
The historical tender must not be used to assert that the current tender has the same mandatory criteria, thresholds, insurance limits, turnover requirements, contract terms, bonds/retention, evaluation weights, references/experience tests, H&S/PSCS requirements, site constraints, or pricing mechanism.

Engineering invariant: `HISTORICAL_REQUIREMENT != CURRENT_REQUIREMENT`.

## Current next evidence action
Acquire the complete current official pack from the official eTenders document surface or another authoritative current source. Only then compile `OfficialPackInventory`, hash every current document/addendum/revision, and unlock tender-specific requirement extraction.
