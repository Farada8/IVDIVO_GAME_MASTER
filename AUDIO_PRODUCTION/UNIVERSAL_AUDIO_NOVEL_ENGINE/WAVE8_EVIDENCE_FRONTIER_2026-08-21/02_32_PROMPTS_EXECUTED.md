# WAVE8 EVIDENCE FRONTIER — 32 PROMPTS EXECUTED SEQUENTIALLY

**Evidence law:** processing a prompt does not force PASS. External/live/human work remains HOLD when the required evidence is unavailable.

## A — Freshness, dedupe, evidence frontier

**01 — Fresh current-main readback.**  
PROMPT: identify exact current main and all audio merges after Wave7.  
RESULT: **PASS_READBACK**. Cycle started from main `b4c29e4a81fc368f440f39827df0adda46b4c897`; PR103 and later session/persistence work already present.

**02 — PR103 post-merge verification.**  
PROMPT: prove post-render hardening is current rather than candidate architecture.  
RESULT: **PASS_EVIDENCE**. PR103 merged; final recorded Audio Studio regression 158/158 and dedicated runtime 4/4.

**03 — Wave7 Drive readback.**  
PROMPT: recover prior 32/32 results and do not duplicate blocked tasks.  
RESULT: **PASS_READBACK**. Provider calls 0; human claims 0; true frontier authenticated provider/cast/human audio.

**04 — PMV177–208 reusable-mechanism crosswalk.**  
PROMPT: extract only provider/reviewer/evidence mechanisms, never BODYGUARD project facts.  
RESULT: **PASS_TRANSFER_MAP**. Reuse credential-safe preflight, review-to-lock firewall, baseline-first, bounded-slice and evidence-contract laws.

**05 — Provider preflight contract audit.**  
PROMPT: find what current `provider_preflight.py` proves and what it does not.  
RESULT: **PASS_FINDING**. It safely verifies requested models/voice IDs but lacks stable/volatile snapshot normalization and scope semantics.

**06 — Studio Evidence human-gate audit.**  
PROMPT: test whether boolean human evidence is enough for durable review provenance.  
RESULT: **PASS_FINDING**. No: append-only reviewer/audio/source provenance ledger was absent.

**07 — Session resilience vs live provider evidence audit.**  
PROMPT: determine whether checkpoint + dispatch already bind request/audio/alignment/spend into one restart lineage.  
RESULT: **PASS_FINDING**. They do not; exact live-evidence escrow is a genuine bounded gap.

**08 — Architecture re-freeze.**  
PROMPT: allow shared-runtime changes only for demonstrated gaps 05–07 plus proof-class safety.  
RESULT: **PASS_POLICY**. No second runtime or generic architecture expansion authorized.

## B — Provider evidence engineering

**09 — Credential-safe provider snapshot module.**  
PROMPT: compile existing preflight into deterministic reusable evidence without credentials.  
RESULT: **PASS_CODE**. Added `runtime/provider_snapshot.py`.

**10 — Stable vs volatile provider metadata.**  
PROMPT: separate model/voice identity capability from timestamp/request metadata.  
RESULT: **PASS_CODE**. Independent stable and volatile hashes implemented.

**11 — Inventory scope truthfulness.**  
PROMPT: prevent targeted voice verification from being called account-wide inventory.  
RESULT: **PASS_CODE**. Explicit `TARGETED / ACCOUNT_WIDE`; targeted sets `account_inventory_complete=false`.

**12 — Provider drift/no-auto-swap gate.**  
PROMPT: missing selected model/voice must HOLD, never silently substitute.  
RESULT: **PASS_CODE**. Required capability gate implemented; auto substitution false.

## C — Human evidence / review-to-lock engineering

**13 — Human review event contract.**  
PROMPT: bind reviewer, evidence family, source/audio hash, time, decision, scores and hard-fails.  
RESULT: **PASS_CODE**. Added `runtime/human_review_evidence.py`.

**14 — Append-only human review ledger.**  
PROMPT: make review evidence restart-auditable and tamper evident.  
RESULT: **PASS_CODE**. Hash-chain ledger + identical-event reuse implemented.

**15 — Review-to-lock firewall.**  
PROMPT: complete evidence may create eligibility but machine cannot lock voice/performance.  
RESULT: **PASS_CODE**. Terminal machine state is `ELIGIBLE_FOR_HUMAN_LOCK_DECISION`, never voice lock.

**16 — Evidence-family completeness.**  
PROMPT: require pronunciation/multi-state/fatigue/pair where configured; hard fails dominate.  
RESULT: **PASS_CODE**.

## D — Paid/live evidence lineage engineering

**17 — Live evidence lineage compiler.**  
PROMPT: bind request, source, capability snapshot, provider ID/state, audio/alignment hashes/refs and spend evidence.  
RESULT: **PASS_CODE**. Added `runtime/live_evidence_escrow.py`.

**18 — Exact-N live escrow.**  
PROMPT: missing, duplicate, unknown fourth, duplicate request hash, ambiguous response or source/request drift => HOLD.  
RESULT: **PASS_CODE**.

**19 — Provider acceptance separation.**  
PROMPT: accepted paid response must never become take/performance acceptance automatically.  
RESULT: **PASS_CODE**. Every lineage records `production_take_status=NOT_ACCEPTED`, `take_lock=false`.

**20 — Restart recovery without provider replay.**  
PROMPT: return checkpoint-compatible missing/durable artifact plan; never replay paid request.  
RESULT: **PASS_CODE**.

## E — Proofs and contracts

**21 — Typed proof manifest.**  
PROMPT: prevent code/CI evidence from laundering into provider/live/human/economics claims.  
RESULT: **PASS_CODE**. Added `runtime/evidence_proof.py`.

**22 — Provider snapshot JSON contract.**  
RESULT: **PASS_SCHEMA**.

**23 — Human review event JSON contract.**  
RESULT: **PASS_SCHEMA**.

**24 — Live evidence escrow + proof manifest JSON contracts.**  
RESULT: **PASS_SCHEMA**.

## F — Adversarial fixtures / external frontier

**25 — Provider snapshot adversarial tests.**  
PROMPT: secrets, targeted-vs-account scope, volatile drift, stable drift, missing voice, tamper, unauthenticated state.  
RESULT: **READY_FOR_CI**. Test suite added; repository CI is the evidence gate.

**26 — Human review adversarial tests.**  
PROMPT: event tamper, fake machine reviewer, ledger restart tamper, missing family, pair requirement, hard fail, no auto-lock.  
RESULT: **READY_FOR_CI**.

**27 — Live escrow adversarial tests.**  
PROMPT: unknown fourth lineage, duplicates, ambiguity, source/request drift, missing durable evidence and recovery without replay.  
RESULT: **READY_FOR_CI**.

**28 — Proof-class anti-laundering tests.**  
PROMPT: CI must not prove human quality; auth must not prove live audio; V1 requires cross-project evidence.  
RESULT: **READY_FOR_CI**.

**29 — Authenticated provider snapshot execution.**  
PROMPT: run real account snapshot without persisting key.  
RESULT: **BLOCKED_EXTERNAL / NO_FAKE_PASS**. No authenticated provider credential/account connector is available in this runtime.

**30 — Real cast + pronunciation/performance evidence.**  
PROMPT: shortlist real Narrator/Ethan/Aoife and collect human-heard pronunciation/multi-state/pair/fatigue events.  
RESULT: **DEPENDENCY_BLOCKED** by 29 and real audio/human review.

**31 — Exact three-request Lesson Zero live canary.**  
PROMPT: dispatch only after source/identity/snapshot/voice/pronunciation gates, then escrow exactly RB001/RB002/RB003.  
RESULT: **NO_GO_CORRECT**. Paid dispatch remains forbidden; zero provider calls claimed.

**32 — Integration + Self-Improvement + persistence closure.**  
PROMPT: full CI, Red Team, fresh-main rebase, PR, Drive mirror/readback, learning disposition and next 64 prompts.  
RESULT: **IN_PROGRESS** until CI/PR/Drive closure. No domain promotion is authorized by code-only evidence.

## Current aggregate before integration gate

- prompts processed: **32/32**
- new bounded runtime modules: **4**
- new machine contract schemas: **4**
- new test suites: **4**
- real provider calls: **0**
- human listening claims: **0**
- voice/pronunciation locks: **0**
- story mutations: **0**

The correct next step is repository CI + Red Team and persistence, not another architecture brainstorm.
