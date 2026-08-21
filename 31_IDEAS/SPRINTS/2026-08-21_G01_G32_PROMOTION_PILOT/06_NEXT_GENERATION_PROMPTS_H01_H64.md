# H01–H64 — FOURTH-GENERATION PROMPTS

**Derivation rule:** exactly 64 follow-up prompts from G01–G32 results. This is a queue, not permission to auto-run all 64. Re-run freshness/priority routing before every bounded tranche.

## H01 — Add atomic register-candidate command to Self-Improvement utility
Implement a transactional command that ingests a candidate JSON file, validates lifecycle/schema, semantic-dedupes candidate_id, snapshots registry, writes atomically and supports rollback.

## H02 — Regression-test atomic registry mutation
Run positive, duplicate-ID, malformed-lifecycle, stale-base, rollback and interruption fixtures. Require byte-preserving rollback and no partial writes.

## H03 — Apply SI-0008 with atomic registry command
Register SI-0008 from exact verified transcript-recovery payload, run invariant and read back the exact candidate without altering unrelated records.

## H04 — Mirror repaired registry to Drive after GitHub readback
Update Drive mirror only after GitHub main contains SI-0008 and invariant passes; prove the mirror is not an independent fork.

## H05 — Add registry/state invariant to CI or release gate
Fail any system release where current state references a missing candidate or VERIFIED_CURRENT lacks required evidence.

## H06 — Test invariant against malformed VERIFIED_CURRENT candidates
Inject missing evidence/application targets, duplicate IDs, unknown states and missing next actions; require explicit failure classes.

## H07 — Audit current SI registry for dormant/stale candidates
Classify each candidate CURRENT/HOLD/SUPERSEDED/REJECTED/NEEDS_EVIDENCE without deleting history.

## H08 — Prune only proven obsolete routing references
Remove/mark only references contradicted by current authority; preserve historical provenance and run boot regression.

## H09 — Promote project-state coverage as portfolio gate
Require every active/locked project to have a durable state pointer or explicit BLOCKED_RECOVERY before portfolio resumability is claimed.

## H10 — Cold-start D03 from new project state only
Verify active audio production, v1.6 text lock and Human Audio Signal boundary without chat history.

## H11 — Cold-start D05 from new project state only
Verify exact story lock, publication hold and current audio branch without aggregate prose.

## H12 — Cold-start Book 1 from new project state only
Verify publisher/external-feedback stage and no-rewrite guard; fail unsupported rewrite proposals.

## H13 — Recover D06 exact authority
Find SHE STOLE MY NAME current authority/final gate/downstream state and persist only if exact evidence exists.

## H14 — Recover D07 exact authority
Repeat evidence-first recovery for THE PERFECT WIFE KNOWS; never infer next action from aggregate labels.

## H15 — Recover D08 exact authority
Repeat evidence-first recovery for SHE FIRED THE BILLIONAIRE with provenance and do-not-repeat rules.

## H16 — Re-run portfolio state coverage after D06–D08 recovery
Update coverage/cold-start matrix and retain only gaps that materially affect real continuation.

## H17 — Create project-state staleness detector
Compare project-state authority pointers with newer Drive/GitHub artifacts and flag potential stale frontiers without auto-promoting them.

## H18 — Validate state detector on superseded-master chains
Use BODYGUARD v1.0→v1.6 and another version chain to prove title/recency cannot silently select superseded authority.

## H19 — Promote Evidence-Aware Gate Contract into writing QA candidate branch
Add evidence_class/source/verification/cannot_prove fields backward-compatibly; engineering tests cannot become literary proof.

## H20 — Run full writing regression with evidence-aware gates
Run current writing/story tests plus collapse fixtures and verify existing PASS meanings do not silently change.

## H21 — Promote evidence contract into audio QA candidate branch
Add DRY_RUN/LIVE_PROVIDER/HUMAN_SIGNAL/PERSISTED_READBACK distinctions without changing protected story text.

## H22 — Run audio regression on ROOM917/D04/D03 fixtures
Verify real-master evidence, dry manifests, human-listen gates and story locks remain distinct.

## H23 — Promote evidence classes into strict reference lifecycle
Attach evidence_class and cannot_prove to integrity, full-read, synthesis, comparison and application artifacts.

## H24 — Re-audit PASS-140 research ledger for evidence consistency
Sample complete/blocked sources and ensure checksum/TOC/snippet never equals full read or external validation.

## H25 — Add evidence-class field to Learning Ledger observations
Separate internal measurement, model inference, human signal, provider result, market behavior and Founder decision.

## H26 — Test learning promotion cannot cross evidence firewall
Low-class evidence attempting a higher-class claim must HOLD/REJECT with explicit next evidence requirement.

## H27 — Create one unified evidence taxonomy reference
Deduplicate evidence labels into one small taxonomy with domain overlays while preserving critical distinctions.

## H28 — Red-team evidence taxonomy for over-complexity
Collapse categories where safe; reject taxonomy growth that prevents no demonstrated failure.

## H29 — Materialize real ROOM917 transcript bytes for recovery pilot
Export the exact File Library conversation artifact into a tool-readable controlled file with source identity/hash and secret policy.

## H30 — Run transcript-recovery CLI on real ROOM917 conversation
Execute deterministic extraction; output ledger, unresolved claims and tail coverage with no automatic canon promotion.

## H31 — Independent Red Team the real recovery ledger
Check missed tail, false saved/locked claims, duplicates, secrets, cross-project contamination and premature completion.

## H32 — Reconcile accepted transcript deltas against current main
Classify each recovered claim ACCEPT/HOLD/REJECT/SUPERSEDED and write only genuinely missing deltas.

## H33 — Feed accepted transcript learnings into Learning Ledger
Persist only reconciled mechanisms/observations with provenance and evidence class.

## H34 — Measure transcript recovery precision/recall
Hand-label a bounded real segment and measure missed/false claims before quality promotion.

## H35 — Package transcript recovery into next engine release candidate
Include tool/schema/tests, registry integration and real-pilot evidence; build a fresh ZIP/checksum without overwriting v11.2 until promotion.

## H36 — Fresh-unzip audit transcript-recovery release candidate
Run full regression, negatives and one real transcript smoke from fresh bytes; promote only if package/state/registry agree.

## H37 — Connect a second external model backend for benchmark
Use an authorized Claude/Grok/other backend or imported independent output with locked source hashes; never simulate another provider persona.

## H38 — Run two-model same-source benchmark
Score independent evidence localization, defect class and false positives rather than agreement.

## H39 — Add third backend only if it changes the decision
Measure marginal information value; stop if a third model merely duplicates evidence.

## H40 — Create benchmark disagreement reconciler
Classify disagreement as source ambiguity, reasoning difference, stale authority, evidence mismatch or genuine uncertainty; no majority-vote canon.

## H41 — Run real concurrent-agent stale-write test
Two authorized agents read one revision and mutate an overlapping frontier; verify one must rebase rather than overwrite.

## H42 — Run real concurrent independent-branch test
Two agents work dependency-independent artifacts and converge by readback/reconciliation; measure duplicate work/conflicts.

## H43 — Add ownership/lease metadata to long-running tasks
Record task owner, base revision, dependency key, update time and rebase policy for contention-prone writes.

## H44 — Validate task leases cannot bypass Founder gates
Founder-blocked project stays blocked while independent safe R&D may proceed.

## H45 — Integrate Story Core validator into Story Gate candidate path
Run causal assertions before prose/architecture approval but label them machine evidence, not literary proof.

## H46 — Regression-test Story Core validator on current strong projects
Apply to D04, D09 and a non-romance IVDIVO architecture; record format-induced false failures before promotion.

## H47 — Create 20 adversarial Story Core fixtures
Include hidden passivity, delayed WHY NOW, false price, cosmetic midpoint, ally-solved climax, active non-aggressive hero and nonstandard structures.

## H48 — Measure Story Core validator precision
Calculate false PASS/false FAIL by defect class; adjust only rules supported by observed errors.

## H49 — Obtain independent blind Story Core review
Give fixtures without expected labels to an independent backend/human and capture evidence before machine verdict reveal.

## H50 — Calibrate Story Core thresholds against blind review
Separate deterministic causality failures from taste/genre disagreement.

## H51 — Pilot Opposition Adaptation Ledger on one open architecture
Use D10 or another open text project: hero move → opponent inference → counter → new constraint → adaptation → price. Do not reopen locked D04/D09.

## H52 — Red-team Opposition Ledger for scheduled-escalation bias
Ensure it does not force every beat into explicit villain reaction or misread environment/institutional pressure.

## H53 — Pilot Relationship Authority Graph on a complex relationship system
Track trust/boundary/power/debt/knowledge/consent without turning privileged knowledge into emotional debt.

## H54 — Blind-check Relationship Graph against scene behavior
Sample scenes and reject graph fields that do not predict/reflect real character choices.

## H55 — Pilot Pair-State Dialogue Card on locked-function scene copy
Create a non-authority candidate rewrite using objective/resistance/status/withheld fact/tactics/listening/subtext/state delta.

## H56 — Independent dialogue causality comparison
Judge whether candidate changes action/status/relationship rather than merely clever phrasing; preserve original if gain is not material.

## H57 — Pilot Scene Delete/Swap Audit on strong and weak blocks
Test one causal block and one intentionally modular/filler block without penalizing legitimate montage/parallel structure.

## H58 — Calibrate Delete/Swap Audit from pilot errors
Refine only if reorderability is confused with causality; keep it diagnostic, not automatic rewrite law.

## H59 — Pilot Universal Evidence Ledger on D04 final proof
Map every Moss proof item to source/access/reliability/current-line availability/alternative model/payoff and compare with existing Gate 3.

## H60 — Pilot Universal Evidence Ledger on a second mystery
Use a structurally different completed mystery to test portability and detect D04 overfitting.

## H61 — Build minimum promotion bundle for validated mechanisms
Require spec + executable test + regression + application target + rollback + evidence class. Exclude ideas lacking the bundle.

## H62 — Run anti-bloat Red Team on promotion bundle
Ask which proposed modules belong inside existing routers/gates instead of becoming new authorities; each retained module must prevent a demonstrated failure.

## H63 — Select next 8 tasks by production impact and information value
After fresh-main rebase, prefer integrity/evidence/real-pilot gates over additional schemas or prompt generation.

## H64 — Apply fourth-generation stopping/pruning rule
Stop/defer when gate closed, evidence unavailable, mechanism duplicates current authority, information value is low, real pilot is superior, or meta-work threatens actual book/audio production.
