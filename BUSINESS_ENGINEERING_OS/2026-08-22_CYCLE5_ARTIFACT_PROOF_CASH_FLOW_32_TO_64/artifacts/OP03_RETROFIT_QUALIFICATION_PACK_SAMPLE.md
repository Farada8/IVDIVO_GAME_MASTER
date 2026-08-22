# OP03 SAMPLE — RETROFIT LEAD QUALIFICATION / GRANT-READINESS PACK

**Evidence class:** PUBLIC RULE ARTIFACT / E2+ ceiling  
**Rules checked:** SEAI current public pages on windows/doors, heat pumps and business energy audits.  
**Purpose:** convert public grant rules into a structured lead packet. Not BER, technical, legal or grant-approval advice.

## A. Minimum lead intake
1. Applicant/entity type.
2. Property type and MPRN where applicable.
3. Build/occupation year.
4. Intended measure: windows/doors / heat pump / other.
5. Existing BER and Advisory Report available? HLI known?
6. Attic/wall insulation status.
7. Registered contractor selected?
8. Quote obtained?
9. Grant offer applied for/received?
10. Have works or ordering already begun?
11. Self-managed grant route or One Stop Shop?
12. Post-works BER plan.

## B. Windows/doors routing
Current SEAI public rules include: qualifying house built/occupied before 2011; high-performing replacement windows at U-value 1.4 W/m²K or lower; post-works BER; HLI 2.3 W/K·m² or lower **or** attic/walls rated Good/Very Good; registered contractor; grant offer before works for standard application path.

**Machine statuses:** `READY_TO_APPLY`, `NEEDS_BER_OR_INSULATION_CHECK`, `HOLD_ALREADY_STARTED`, `INELIGIBLE_BUILD_YEAR`, `RULE_REVALIDATION_REQUIRED`.

## C. Heat-pump routing
Current SEAI public rules include: property built/occupied before 2021; registered contractor; grant approval before works; technical assessment required for many pre-2007 homes unless valid BER/HLI demonstrates readiness; HLI threshold 2.3 W/(K.m²) is material to readiness. Current bundle can reach €12,500 depending on dwelling/system and conditions; the amount is not customer income and never exceeds eligible cost of works.

## D. Three synthetic lead fixtures

| Lead | Facts | Output |
|---|---|---|
| L1 | Semi-detached, 2005, windows, attic/walls Good, quote from registered contractor, no works begun | `READY_TO_APPLY`, subject to current SEAI checks and grant offer before works |
| L2 | Detached, 2015, windows replacement | `INELIGIBLE_BUILD_YEAR` for current individual windows/doors rule; verify if another route applies |
| L3 | 2003 home, heat pump, HLI 2.8, no technical assessment | `NEEDS_TECHNICAL_ASSESSMENT / FABRIC_READINESS`, not installation-ready |

## E. Business energy-audit adjacent route
For qualifying SMEs, SEAI currently offers a €2,000 energy-audit voucher subject to conditions including Republic of Ireland registration, tax compliance, non-obligated status and at least €10,000 annual site energy spend excluding transport. This is a separate business route, not a domestic lead rule.

## Canonical sources
- https://www.seai.ie/grants/home-energy-grants/individual-grants/windows-and-doors
- https://www.seai.ie/grants/home-energy-grants/individual-grants/heat-pump-systems
- https://www.seai.ie/grants/business-grants/energy-audits

## Artifact-test verdict
`RULE_TRACEABILITY_PASS / SYNTHETIC_ROUTING_PASS / REAL_CONTRACTOR_WORKLOAD_AND_WTP_HOLD / E2+ ONLY`
