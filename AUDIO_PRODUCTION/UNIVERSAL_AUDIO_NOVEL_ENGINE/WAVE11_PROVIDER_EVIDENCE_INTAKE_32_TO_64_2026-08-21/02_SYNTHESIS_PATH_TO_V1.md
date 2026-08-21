# WAVE11 — SYNTHESIS / PATH TO AUDIO STUDIO V1

## What changed
Wave10 made provider snapshots consumable by deterministic code. Wave11 makes the **durable GitHub Actions evidence event itself consumable** without manual copying or trust laundering.

The new boundary is:
`UPSTREAM WORKFLOW SUCCESS -> EXACT RUN ARTIFACT -> AUTH_PROVIDER REVALIDATION -> RUN/ATTEMPT/SOURCE BINDING -> SNAPSHOT FILE CROSS-CHECK -> INVENTORY -> OPTIONAL REPEATABILITY -> TYPED NEXT STATE`.

## Why this matters
Before Wave11, a real upstream provider artifact could exist while the downstream state still depended on a human/model manually finding and loading it. That creates four failure classes: wrong run, stale artifact, cross-account/cross-run contamination, and accidental escalation from metadata to artistic/spend authority. Wave11 closes those mechanics without adding another provider integration.

## Concrete defect found during implementation
An early version of the new execution-state resolver accepted caller booleans for human lock/pre-spend progression. That would have violated the existing external-evidence trust law. It was removed before integration. Final resolver stops at `AUDITION_REQUIRED`; human lock/spend remain receipt/authority-bound existing gates.

## Shortest path to V1 from here
1. Real AUTH_PROVIDER workflow event and Wave11 intake PASS.
2. Second read-only snapshot and same-account repeatability PASS.
3. Real current inventory -> provisional NARRATOR/ETHAN/AOIFE candidates.
4. Human-heard Ифа/Контакт + multi-state + pair + fatigue evidence.
5. Authorized locks + fresh capability revalidation + exact pre-spend GO.
6. Sequential RB001 -> sanity check -> RB002 -> RB003 with durable raw/spend lineage.
7. Real 36/36 alignment -> timeline -> protected-silence/acoustic/Foley mini-mix.
8. Same-source three-mode blind human benchmark.
9. Measured provider/manual economics.
10. Independent second-project live portability + recovery evidence.
11. Independent Red Team -> Founder V1 decision.

## Self-Improvement conclusion
The dominant bottleneck is now evidence acquisition and evidence handoff, not generic architecture. The useful improvement pattern is `external event -> durable evidence -> exact lineage validation -> typed state -> smallest next experiment`. Promotion claims must stay bounded by evidence class and project independence.
