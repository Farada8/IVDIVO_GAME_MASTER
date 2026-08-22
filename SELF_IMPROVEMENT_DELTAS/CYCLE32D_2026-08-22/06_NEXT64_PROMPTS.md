# CYCLE32D — NEXT 64 PROMPTS

Status: DESIGNED / NOT AUTO-EXECUTED

## Runtime / persistence hardening
1. Implement a local validator for persistence transaction records.
2. Create fixtures for empty file, wrong file, wrong branch and partial write.
3. Add semantic-anchor verification fixture.
4. Add idempotent retry fixture after partial Drive/GitHub write.
5. Create cross-store parity record schema.
6. Create stale-pointer detection fixture.
7. Create destination mismatch fixture.
8. Create closure gate requiring readback evidence.

## Registry / concurrency
9. Inventory active branches that modify Improvement Registry.
10. Design branch-safe candidate-ID reservation without central rewrite.
11. Test duplicate candidate ID detection across two branch snapshots.
12. Create collision-resolution protocol preserving provenance.
13. Create temporary UUID/local-ID strategy for unmerged candidates.
14. Test merge of two independently-created candidate records.
15. Define canonical ID assignment point.
16. Red Team the reservation mechanism for race and stale-read failures.

## Decision-yield canary
17. Select one real book-production task for prospective canary.
18. Record baseline workflow decisions/rework before profile use.
19. Run authority/freshness vector before task execution.
20. Run capability-dedupe before any new tool/prompt creation.
21. Use VOI router to select one decisive test.
22. Measure whether selected test changed a decision.
23. Measure duplicate work avoided and rework introduced.
24. Compare profile vs baseline and HOLD/PROMOTE/ROLLBACK locally.

## WIP / anti-bloat
25. Inventory active meta-work across GitHub and Drive.
26. Classify each item ACTIVE/BACKLOG/HOLD/STALE/DUPLICATE.
27. Apply one-integration-plus-two-pilots WIP rule.
28. Identify prompt packs with duplicate capability fingerprints.
29. Merge or deprecate one duplicate prompt family.
30. Measure document count removed without capability loss.
31. Add production-return checkpoint to active meta-cycle.
32. Red Team for meta-work starving story/audio production.

## v3 candidate proof
33. Map each v3 mechanism to existing v2 capability or true gap.
34. Identify which v3 mechanisms already have real-project evidence.
35. Choose one v3 mechanism for real production pilot.
36. Define guardrails and rollback before pilot.
37. Run policy-resistance analysis on the mechanism.
38. Run double-loop trigger fixture.
39. Separate synthetic proof from production evidence.
40. Reassess v3 promotion status after evidence; default HOLD.

## Learning / evidence quality
41. Audit Improvement Registry candidates for unsupported evidence labels.
42. Audit Learning Ledger for activity records masquerading as learnings.
43. Add decision-changed field to new experiment records.
44. Add invalidation/expiry field for stale learnings.
45. Define evidence-source independence rule for multi-AI reviews.
46. Define negative-result retention rule.
47. Create promotion evidence checklist by evidence class.
48. Run self-application audit on the learning system.

## Cross-dialog recovery
49. Test a large pasted transcript through recovery protocol.
50. Verify every persisted-claim item against GitHub/Drive.
51. Classify unresolved chat-only claims without invention.
52. Test final-tail processing on a long transcript.
53. Measure duplicate recovered items removed by dedupe.
54. Verify no secret/API-key persistence.
55. Confirm continuation resumes from real frontier after recovery.
56. Write production evidence into Learning Ledger only after readback.

## Governance / next architecture
57. Create a single current Self-Improvement capability map.
58. Create deprecation map for superseded prompt/engine documents.
59. Define universal vs domain-local promotion criteria.
60. Define when a candidate should be deleted rather than held.
61. Create self-improvement SLOs without vanity composite score.
62. Define stop conditions for research/meta cycles.
63. Run independent Red Team of Cycle32D architecture.
64. After real canary, decide: keep v2 extension, revise, or rollback.
