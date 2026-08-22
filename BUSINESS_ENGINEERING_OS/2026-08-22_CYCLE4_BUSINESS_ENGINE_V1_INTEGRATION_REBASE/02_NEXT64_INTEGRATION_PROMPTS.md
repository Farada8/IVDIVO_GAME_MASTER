# BUSINESS ENGINE v1 — NEXT 64 INTEGRATION RUN CARDS

Status: DESIGNED / 0 EXECUTED. These are derived from the residual integration bottleneck after deduping the merged Cycle5 banks. Execute the smallest dependency-ready, highest-information subset rather than all 64 ritualistically.

## A — Dependency graph / selective invalidation
1. Define field-level nodes for Signal, Opportunity, Experiment, Offer, Contract, Payment, Delivery, Economics, Finance and Scale artifacts.
2. Define typed business edges with explicit invalidation semantics; reject semantic-free links.
3. Build a 32-opportunity dependency graph from current merged Cycle4 objects.
4. Mutate one tender deadline and prove only dependent opportunity/experiment/offer artifacts become dirty.
5. Mutate one buyer-role assumption and prove unrelated verticals remain valid.
6. Mutate one regulation/source effective date and prove downstream compliance artifacts recheck while creative/public-art artifacts stay valid.
7. Add conditional invalidation: evidence changes may require validator/recheck without automatic regeneration.
8. Measure repair-scope reduction versus whole-portfolio recomputation and record decision/evidence value.

## B — Founder locks / authority / concurrency
9. Define lock types: FOUNDER_LOCKED, CONTRACT_LOCKED, PAYMENT_OBSERVED, EXTERNAL_FACT_LOCKED, EVIDENCE_APPEND_ONLY.
10. Implement lock-conflict ChangeRequest object with reason, requested mutation and downstream impact.
11. Test new research contradicting a Founder-approved offer: evidence may append; offer semantics remain blocked pending Founder decision.
12. Test price hypothesis update against observed paid price: observed external payment outranks model hypothesis.
13. Test contract-scope change after signed/accepted external artifact: automatic mutation must fail closed.
14. Implement compare-and-swap freshness token for material Business Engine writes.
15. Replay the observed same-path writer collision as a deterministic concurrency fixture.
16. Build branch-selection protocol that chooses fresh-main semantic merge over force overwrite.

## C — Production contract / delivery / economics
17. Define BusinessArtifact schemas for Experiment, Offer, Contract, DeliveryRecord and EconomicsObservation.
18. Compile one current PRIMARY from Signal→Opportunity→Experiment with no lifecycle holes.
19. Compile one manual sample deliverable into DeliveryRecord with actual analyst minutes.
20. Add rework/error minutes to delivery economics instead of reporting only nominal production time.
21. Define contribution, cash timing and throughput metrics from observed events only.
22. Add delivery acceptance criteria and explicit client-dependency fields without simulating acceptance.
23. Build regression where missing payment cannot create revenue and missing delivery cannot create margin.
24. Implement local regeneration of one offer/deliverable when upstream evidence changes, preserving unaffected artifacts.

## D — Capital / finance / acquisition integration
25. Model customer deposit, PO, retainer, commission, supplier terms, invoice finance, loan, grant and investor as distinct capital events.
26. Require real external artifact before customer/supplier funding transitions from hypothesis to observed.
27. Build reimbursement-grant cash-gap fixture and prevent classification as zero cash.
28. Build invoice-finance readiness fixture that requires an eligible receivable, not merely E4 payment history.
29. Build loan-readiness schema that separates lender product availability from borrower approval.
30. Build acquisition deal dependency graph: target evidence→LOI→DD→financing→close→operations; keep all deal values null until deal-specific evidence.
31. Test acquisition downside-first invalidation when one material cash-flow assumption changes.
32. Compare CREATE/BROKER/ACQUIRE only on fields supported by equivalent proof levels; no cross-plane ranking.

## E — Domain profile integration
33. Bind current public-art OpportunityObjects to PUBLIC_ART profile and identify profile-only vetoes.
34. Bind current creative grants/residencies to CREATIVE_OPPORTUNITY profile and prove project budget is not artist income.
35. Bind current hospitality/digitalisation objects to HOSPITALITY profile and separate capex, service fee and public-support assumptions.
36. Bind construction/tender objects to CONSTRUCTION profile and enforce admin-support vs professional sign-off boundary.
37. Bind regulatory/compliance objects to REGULATORY_SHOCK profile and preserve legal/specialist handoff.
38. Bind zero-capital candidates to ZERO_CAPITAL profile and verify customer-funded route precedes founder cash.
39. Bind acquisition candidates to ACQUISITION profile only if a real operating-business target exists; otherwise HOLD.
40. Run cross-domain contamination Red Team: no art eligibility rule may block construction; no compliance rule may fabricate creative eligibility.

## F — Evidence transitions / future external proof
41. Define immutable BuyerInteractionEvidence schema for future E3 events; current execution remains blocked by NO_OUTREACH.
42. Define immutable PaymentProof schema for E4: amount, artifact, payer, date, scope, verification state.
43. Define ExternalDecline/NoResponse evidence taxonomy without treating silence as product failure by itself.
44. Define objection evidence that links to exact opportunity/offer version.
45. Pre-register E3 promotion criteria for PRIMARY without sending outreach.
46. Pre-register E4 paid-pilot gate and stop conditions without requesting payment now.
47. Define evidence revocation: fraudulent/misclassified external event can demote proof state with lineage.
48. Build model/public-source adversarial suite proving they can never populate BuyerInteractionEvidence or PaymentProof.

## G — Self-improvement / calibration
49. Add DecisionDeltaTelemetry: changed decision, false positive avoided, duplicate avoided, repair scope, protected lock, human escalation.
50. Run 32 current opportunities through dependency-aware vs whole-portfolio recomputation and compare unnecessary work.
51. Run false-invalidation corpus where graph is too broad; narrow edges only when evidence supports it.
52. Run missed-invalidation corpus where graph is too narrow; patch earliest causal edge and regression-test.
53. Build predictor calibration linking current E1/E2 hypotheses to future E3/E4 outcomes when they eventually exist.
54. Demote heuristics that repeatedly fail to predict external outcomes; do not change proof ladder.
55. Require three repeated same-mechanism defects before proposing universal Self-Improvement promotion unless severity is FATAL.
56. Prune modules that do not change decisions, catch defects, reduce work or protect authority.

## H — persistence / release / next frontier
57. Add CI for the integration runtime on fresh main and current-head PR paths.
58. Run cold-package replay with no external PYTHONPATH and capture file count, SHA and exact test count.
59. Create GitHub+Drive CrossStoreIdentity record for master, RUN32, NEXT64, runtime and test evidence.
60. Persist the Book Engine v0.7 dependency passport beside the current 78-file business-library manifest.
61. Read back every Drive integration artifact and compare nonempty content/hash/size markers.
62. Reread fresh main and semantically dedupe any new parallel Business Engine work before merge.
63. Close Cycle4 integration only if latest-head CI, Drive readback, dependency identity and authority freshness all PASS.
64. Derive the next backlog from the first observed bottleneck among selective invalidation accuracy, manual-delivery economics, external E3/E4 proof, financing readiness or acquisition evidence — not from prompt count.
