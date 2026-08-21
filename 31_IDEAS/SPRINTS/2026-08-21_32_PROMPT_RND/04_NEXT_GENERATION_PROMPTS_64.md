# 64 NEXT-GENERATION PROMPTS

**Derivation rule:** exactly two follow-ups per original P01–P32: one implementation-oriented prompt and one independent validation/adversarial prompt. They are a queue, not an instruction to execute all 64 blindly.

## N01 — Implement canonical boot manifest
Create one machine-readable IVDIVO boot manifest that points to current GitHub system state, Drive Prompt Authority Index, CURRENT_PROMPTS, CURRENT_WORKSTATE, prompt router and project-state locations. Mark every pointer AUTHORITY / MIRROR / COMPATIBILITY / HISTORY. Do not duplicate story canon.

## N02 — Validate boot manifest against fresh state
Cold-start from the proposed boot manifest only. Verify that it resolves current schema/version/Drive IDs, D09 Founder gate and D04 downstream state without relying on chat memory or historical compatibility text. Fail on any stale or ambiguous pointer.

## N03 — Implement portfolio PROJECT_STATES coverage
Create minimal routing-state files for the highest-priority projects that still lack durable machine-readable state. Each file must contain authority pointer, phase, completed frontier, open gates, blockers, next safe action, do-not-repeat list and provenance without copying canon.

## N04 — Validate project-state recovery coverage
Simulate a new model resuming each project using only aggregate state plus PROJECT_STATES. Measure whether it can identify exact current phase and next obligation without searching chat history. Flag every project that still requires manual reconstruction.

## N05 — Repair SI-0008 registry/state integrity
Reconcile CURRENT_IVDIVO_SELF_IMPROVEMENT_STATE with the central Improvement Registry. Register the transcript-recovery extension under the correct candidate ID with provenance, owner, application targets, verification evidence, next action and gate, or correct the state if an existing candidate supersedes it.

## N06 — Add registry-reference invariant test
Implement a machine test that scans current system/self-improvement state for SI candidate references and fails if a referenced candidate is absent, lacks mandatory lifecycle fields or claims VERIFIED_CURRENT without verification evidence.

## N07 — Classify prompt/router files by function
Create a routing inventory that assigns every current prompt/router file one role: AUTHORITY, GENERATED MIRROR, COMPATIBILITY MAP, DOMAIN OVERLAY or HISTORY. Identify duplicate startup/continuation instructions and select the smallest controlling source.

## N08 — Cold-read router sprawl validation
Give an independent reviewer only the routing inventory and current files. Ask it to choose the correct boot path for a book, commercial drama and audio project. Fail if different reasonable routes produce different authority/frontier outcomes.

## N09 — Add evidence-class field to gates
Extend major gate/result templates with evidence_class, evidence_source, verification_method and what_this_evidence_cannot_prove. Preserve existing gate semantics and reject generic PASS unsupported by the required evidence class.

## N10 — Adversarial evidence-collapse test
Construct negative fixtures where tests are presented as literary proof, AI review as Human Signal, dry run as live render, prediction as market behavior and transcript extraction as canon. Verify all are rejected or downgraded.

## N11 — Run first real large transcript ingestion
Use the verified transcript-recovery protocol on one real large pasted/exported prior AI conversation. Execute deterministic extraction, semantic reconciliation, persisted-claim verification, disposition, accepted writes and readback. Record unresolved items without inventing details.

## N12 — Independent transcript-recovery audit
Audit the completed real transcript ingestion for missed tail content, false saved/locked claims, duplicate candidate recovery, secret leakage, canon overreach and premature INGESTION_COMPLETE. Require evidence for every promoted item.

## N13 — Build cross-model benchmark fixture pack
Create a fixed set of story/system diagnostic fixtures with locked sources and hidden expected defect classes. Define same-source parity, independent reasoning and scoring by evidence quality rather than agreement.

## N14 — Validate multi-AI concurrency guards
Run two simulated agents on overlapping and non-overlapping tasks. Confirm independent branches can proceed while attempts to mutate the same frontier are blocked or serialized through explicit ownership/rebase.

## N15 — Implement causal Story Core assertions
Add a Story Core validation contract that encodes causal edges between WANT, WHY NOW, ACTION, OPPOSITION, WRONG STRATEGY, PRICE, MIDPOINT, CLIMAX CHOICE and RESOLUTION. Fail label-only or permutable cores.

## N16 — Blind-test Story Core causality
Generate several superficially complete Story Cores, including intentionally broken ones. Ask an independent reviewer to apply the causal assertions without seeing labels such as good/bad. Measure false PASS rate and refine the gate.

## N17 — Implement protagonist state-change ledger
Create a conditional ledger tracking protagonist action, tactic, world/partner response, changed constraint/value, price and next adaptation per major unit. Count restraint/refusal/cooperation only when they materially change state.

## N18 — Validate agency without aggression bias
Test the agency ledger on quiet, relational, investigative and action protagonists. Confirm it rewards consequential non-confrontational choices and rejects passive screen presence or loud but inconsequential behavior.

## N19 — Implement opposition adaptation ledger
Create the opponent-adaptation tool: protagonist move -> opponent observation/inference -> counter-move -> new constraint -> protagonist adaptation -> price. Support person, institution, environment and social-system opposition.

## N20 — Validate causal escalation across genres
Apply the opposition ledger to one mystery, one romance/melodrama, one youth story and one Smith/OES case architecture. Verify counters are causally responsive rather than scheduled escalation or arbitrary cruelty.

## N21 — Implement behavioral contradiction card
Create a character contradiction card mapping competing values/desires to trigger, available actions, chosen action, cost, lie/self-justification and later changed pattern. Keep rehearsal biography private by default.

## N22 — Validate contradictions in scene behavior
Sample major characters from current projects and check whether stated contradictions actually alter choices under pressure. Reject adjective-only contradictions and proposed exposition that does not change action.

## N23 — Implement Social Reality Pressure Card
Create a conditional sociology card covering money, work, housing, class/status, family obligations, bureaucracy, law, community norms and institutional incentives. Require only pressures capable of changing strategy, access, risk or relationship.

## N24 — Validate sociology without exposition
Apply the sociology card to scenes in commercial romance, Orbital Youth and Smith/OES. Confirm social systems create action/resistance rather than speeches, policy explanation or generic poverty/status decoration.

## N25 — Build ensemble Relationship Authority Graph
Implement a project-neutral relationship graph with edge fields for current trust, boundary, power, debt, knowledge asymmetry, vulnerability, rupture, repair, consent state and unresolved obligation. Support romance, family, friendship, professional and antagonistic edges.

## N26 — Validate consent/power across timeline variants
Stress-test the relationship graph on erased-memory/time-loop, boss/employee, rescuer/rescued, wealthy/powerful lead and professional-investigative scenarios. Verify privileged knowledge never becomes automatic current consent or emotional debt.

## N27 — Implement pair-state dialogue card
Before major dialogue rewrite, require pair objective, resistance, status asymmetry, withheld fact, tactic sequence, listening behavior, interruption pressure, subtext and final state delta. Integrate with P51/P52/P53 conditionally.

## N28 — Blind-test dialogue rewrite causality
Compare dialogue rewritten with and without the pair-state card using locked scene function. Evaluate whether the revised version changes action/status/relationship rather than only voice polish or cleverness.

## N29 — Add scene delete/swap tests to block audit
Extend architecture/block audit with scene deletion and adjacency swap tests. Require explicit broken dependency when a scene is essential; route passing swaps to causality, evidence order, escalation or relationship-state diagnosis.

## N30 — Validate modularity detection
Apply delete/swap tests to a known strong causal block and to an intentionally modular/filler block. Confirm the test does not penalize legitimate montage/parallel structure while catching reorderable pseudo-causality.

## N31 — Define universal evidence-ledger schema
Create a machine-readable mystery/evidence schema for fact, trace/source, lineage, access, reliability, surface meaning, true meaning, alternative model, corroboration, current-timeline availability, action and payoff. Keep project content external.

## N32 — Validate final-proof fairness
Run the evidence schema against at least two completed mystery structures. Confirm the final solution is supported by current-line accessible evidence and not by author-only knowledge, loop memory or retrospective reinterpretation without trace.

## N33 — Extend Waiting-Question Ledger with decay
Add question_age, last_meaningful_update, transformation_count, delay_source, escalation, stale_risk, payoff_type and retirement_reason. Define thresholds as diagnostics, not automatic rewrite rules.

## N34 — Validate suspense vs stale withholding
Apply the extended ledger to a serialized block containing evolving questions and to one with repetitive cliffhangers. Confirm it distinguishes legitimate delayed payoff from unchanged withholding and confusion.

## N35 — Implement world-reveal transaction audit
Create a conditional audit using ordinary objective -> system/world constraint -> consequence -> choice -> new evidence/relationship/status. Flag terminology/ontology that does not alter reader model or action.

## N36 — Validate world reveal in ordinary life
Apply the audit to orbital housing/transport/work, Old Earth Security jurisdiction and commercial-hospital settings. Confirm the world feels different through lived constraints rather than lore paragraphs.

## N37 — Create Youth Authenticity overlay
Build a conditional youth overlay covering friends, attraction, jealousy, embarrassment, family, school/work, money, housing, hobbies, sport, parties, status, boredom, exclusion, independence and bad decisions, plus setting-specific pressures.

## N38 — Validate orbital-youth specificity
Compare an Earth-school-in-space outline with a genuinely orbital youth outline using the overlay. Verify habitat economics, transport, maintenance, AI/synthetic/nonhuman context materially change adolescence and choices.

## N39 — Implement emotional-inflation detector
Create a romance/melodrama diagnostic for repeated suffering, rupture, rescue, jealousy or temperature-5 beats without new choice, price, information or relationship state. Respect Project Romance Weight and genre promise.

## N40 — Validate emotional range on commercial serials
Apply the detector to a block with ordinary warmth/micro-care and to one with constant crisis. Check whether retention improves through contrast rather than simply reducing intensity everywhere.

## N41 — Implement upstream prose-defect router
Create a prose diagnostic that routes choppiness/repetition/stock phrasing upward through scene function, paragraph topic chain, reader-state continuity and inner/outer tempo before sentence-level repair.

## N42 — Blind-test anti-generated-text repair
Compare targeted upstream repair with mechanical style smoothing on the same passage. Evaluate causality, voice, rhythm and reader comprehension; reject revisions that merely diversify sentence length.

## N43 — Add aftermath/irreversibility to final gate
Extend final story gate with explicit fields for irreversible consequence, ordinary-life aftershock, changed relationship/world state and proof the series hook begins only after current conflict closure.

## N44 — Validate endings against false continuation
Test the extended final gate on complete endings, cliffhanger-as-ending, exposition epilogues and franchise-teaser endings. Confirm incomplete main conflicts cannot pass.

## N45 — Create problem-targeted reference queue
From the strict lifecycle ledger, map unsynthesized/integrity-blocked sources only to live unresolved decisions they could change. Assign expected information value and stop rules; leave unrelated sources untouched.

## N46 — Validate reference stopping discipline
Run the queue on a real craft question and show when marginal sources stop changing the decision. Confirm the system moves to pilot/test rather than endless library processing.

## N47 — Implement multi-axis source-distance challenge
Create an originality check across plot order, scene-function sequence, character configuration, signature inventions, clue chain, setting mechanism and distinctive dialogue. Require transformation evidence, not paraphrase.

## N48 — Independent derivative-risk red team
Give an independent reviewer the candidate work and reference passports/mechanisms without the author's rationale. Ask for high-risk similarity clusters and whether the abstraction/combination is sufficiently transformed.

## N49 — Build Promise-to-Payoff map
Create a marketing/reader contract linking title, description, key art, opening minute/chapter, central fantasy/question, midpoint promise and finale payoff. Separate acquisition hypothesis from actual demand data.

## N50 — Validate packaging truthfulness
Compare package promises with completed manuscripts/audio scripts. Flag bait-and-switch, absent romance/mystery intensity, misleading protagonist framing and promises that the finale does not pay.

## N51 — Implement audio adaptation delta ledger
Create a ledger for every non-trivial locked-text-to-audio change: source text/function, proposed spoken change, reason, protected facts/clues/consent, downstream effects, approval status and rollback path.

## N52 — Validate audio adaptation against story lock
Audit a sample adapted scene and prove every change preserves clue order, character choice, relationship meaning and legal/current authority. Reject hearability changes that silently alter story.

## N53 — Create performance binding card
Map P51 voice fingerprint + scene objective/tactic/status/subtext to audition blocks and direction-change tests. Keep provider IDs separate from character canon and require pair/ensemble tests where story function needs them.

## N54 — Blind-validate voice casting
Run blind loudness-matched auditions with dry audio, role-specific hard fails, direction response, long-form fatigue and device translation. Confirm the selected voice performs the role across states, not just one attractive line.

## N55 — Standardize one-listen evidence test
Create a blind-listen questionnaire for source identity, evidence object, who knows what, causal order, clue meaning boundary and confidence. Define routing from failure to performance/edit/mix/source identity.

## N56 — Validate sound fixes before text rewrite
Apply the one-listen test to an evidence-heavy scene before and after non-text audio repairs. Only reopen protected text if comprehension still fails after performance/edit/mix options are exhausted.

## N57 — Package transcript recovery into next engine release
Reconcile registry/state, include verified transcript-recovery tool/schema/tests in the next full engine package, update machine execution pointer and run fresh-unzip full regression plus exact artifact checksum.

## N58 — Independent package promotion audit
Verify the new ZIP from fresh bytes: file presence, hashes, all regression tests, negative fixtures, state/schema compatibility and no stale pre-extension package claims. Promote only after readback evidence.

## N59 — Implement blocked-frontier parallel scheduler
Add scheduler states for ACTIVE_UNBLOCKED, FOUNDER_BLOCKED, EXTERNAL_BLOCKED, TOOL_BLOCKED and SAFE_PARALLEL. Allow only independent authorized tasks under WIP limits while preserving the blocked project's exact gate.

## N60 — Validate scheduler cannot bypass Founder gates
Simulate D09-like Founder lock, provider-cost and human-signal blocks. Confirm the scheduler advances only independent work and never marks the blocked project complete, locked or progressed.

## N61 — Cluster sprint findings into minimal roadmap
Deduplicate all P01–P31 findings into the smallest set of implementable initiatives. Rank by P0–P6 priority, recurrence, evidence, dependency, cost, reversibility and impact on stronger completed books/audio.

## N62 — Red-team roadmap against meta-work bloat
Independently challenge the roadmap for unnecessary new modules, duplicate schemas, tool-overfit and production starvation. Require every retained initiative to name a concrete production failure it prevents or a measurable gate it closes.

## N63 — Select next 8 prompts by value of information
From N01–N62, choose the eight prompts whose results can most change the next production decision. Prefer integrity and production blockers over speculative research. Explain what decision each prompt unlocks.

## N64 — Run next-generation stopping rule
Define when the 64-prompt queue should stop, defer or be pruned: real gate closed, no new evidence, duplicate mechanism, marginal information value low, pilot more informative, or production priority higher. Produce a bounded execution tranche rather than auto-running all 64.
