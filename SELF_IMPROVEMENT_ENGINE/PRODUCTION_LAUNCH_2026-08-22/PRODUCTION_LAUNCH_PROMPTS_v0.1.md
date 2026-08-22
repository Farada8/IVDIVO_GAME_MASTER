# Production Launch Prompts v0.1

## Shared execution header

Apply this header to every run card.

You are executing a production engineering card, not writing a concept essay. Produce the smallest useful implementation that can be persisted and tested.

Required output for every card:
- concrete files/code/state changes;
- inputs and outputs;
- executable command when applicable;
- tests/fixtures;
- actual acceptance result;
- blocker state if execution is impossible;
- readback/persistence evidence;
- next admissible action.

Never mark `DONE_VERIFIED` merely because a design, prompt or code snippet exists. If runnable implementation or required verification is missing, use `DESIGN_ONLY` or `BLOCKED`.

---

## PL-00 — MASTER PRODUCTION BOOTSTRAP

Act as lead software engineer and production architect. Create a minimal actually executable Personal AI Production System for one user on an ordinary laptop.

Primary domains:
1. BUSINESS
2. BOOKS
3. PROJECTS
4. RESEARCH
5. PERSONAL KNOWLEDGE
6. AI AUTOMATION

Technology baseline:
- Python 3.12+
- SQLite
- Git
- YAML/JSON
- local filesystem
- provider abstraction for GPT/Claude APIs
- later local-model integration through Ollama-compatible interface
- GitHub/Google Drive synchronization only when authorized and available

Create at minimum:

```text
personal-ai/
├── README.md
├── requirements.txt
├── .env.example
├── config/
├── core/
├── memory/
├── projects/
├── agents/
├── workflows/
├── business/
├── books/
├── research/
├── tests/
├── benchmarks/
├── logs/
└── run.py
```

`python run.py` must perform a real persisted action. Minimum smoke: initialize DB, create a demo project/task, persist state, read it back, write a log, run a test. Do not claim completion if the run path is unverified.

---

## PL-01 — PROJECT STATE SYSTEM

Create a real Project State Manager. Every project must own:

```text
project.yaml
state.json
tasks.json
decisions.md
artifacts/
references/
logs/
```

Implement:
- create_project()
- load_project()
- update_state()
- add_task()
- complete_task()
- block_task()
- record_decision()
- get_next_task()

Statuses: NEW, READY, RUNNING, BLOCKED, DONE, FAILED, ARCHIVED.

CLI minimum:

```bash
python run.py project create demo
python run.py project status demo
python run.py project next demo
```

Add unit tests and persisted readback.

---

## PL-02 — LOCAL MEMORY

Create local long-term memory using SQLite.

Minimum tables:
- projects
- tasks
- documents
- facts
- decisions
- sources
- outputs
- events

Each record requires ID, project_id where applicable, timestamp, source, confidence/status where applicable, content/text and content hash.

Required operations:
- STORE
- SEARCH
- UPDATE
- INVALIDATE
- TRACE_SOURCE

New claims must not silently overwrite old ones. Preserve version/history semantics. Add a CLI search path and tests.

---

## PL-03 — SOURCE / EVIDENCE LAYER

Create provenance-aware claim handling. Distinguish:
- FACT
- SOURCE_CLAIM
- USER_DECISION
- AI_INFERENCE
- HYPOTHESIS
- TEST_RESULT

A claim record must include claim text/type, source IDs, confidence, verified state and traceable provenance.

Implement `trace_claim(claim_id)` returning claim <- source <- document <- project where available.

Add a negative test proving an unverified AI inference cannot be emitted/stored as `VERIFIED_FACT` without an explicit verification event.

---

## PL-04 — AI PROVIDER ABSTRACTION

Create a provider-neutral AI interface:

```text
AIProvider
├── OpenAIProvider
├── AnthropicProvider
└── OllamaProvider
```

Business logic must not hard-code a model/provider.

Required methods:
- generate()
- analyze()
- classify()
- extract()

Configuration must support provider/model/temperature/max_tokens or equivalent supported fields without embedding API secrets.

Add a MockProvider so all core tests can run with zero paid API calls.

---

## PL-05 — AGENT EXECUTOR

Create a bounded practical agent executor.

Agent definition includes:
- ROLE
- GOAL
- INPUT
- TOOLS
- MEMORY
- MAX_STEPS
- OUTPUT_SCHEMA

Execution loop:
LOAD TASK -> LOAD CONTEXT -> PROPOSE ACTION -> CALL TOOL -> OBSERVE -> UPDATE STATE -> STOP.

Mandatory controls:
- max_steps
- timeout
- error handling
- action log
- no infinite recursion/loop
- allowlisted tools

Create one demo agent and an integration test that proves bounded completion and state persistence.

---

## PL-06 — BUSINESS CORE

Create Business Operations Module with minimum entities:
- Lead
- Customer
- Job
- Quote
- Invoice
- Supplier
- Expense
- Payment
- FollowUp

First workflow:
CLIENT REQUEST -> JOB DESCRIPTION -> COST ESTIMATE -> LABOUR -> MATERIAL -> MARGIN -> QUOTE -> SAVE.

Inputs include job type, area/quantity, materials where known, hours, labour rate and margin.

Outputs: structured quote JSON plus readable quote Markdown/text. Never invent missing prices; surface UNKNOWN/TBD instead.

---

## PL-07 — BUSINESS RESEARCH

Create a provenance-first research workflow for business decisions.

Input fields:
- research question
- geography
- industry
- as-of date

Outputs:
- sources.json
- claims.json
- comparison.csv or equivalent structured table
- conclusions.md
- open_questions.md

Every conclusion must trace to sources or calculations. Distinguish OBSERVED, CALCULATED, INFERRED, UNKNOWN. Track freshness/as-of date. Do not convert absence of evidence into zero/false.

---

## PL-08 — BOOK PRODUCTION CORE

Create Book Production Module with project structure:

```text
book/
├── book.yaml
├── canon.md
├── characters.json
├── locations.json
├── timeline.json
├── plot.json
├── chapters/
├── drafts/
├── critique/
├── continuity/
└── final/
```

State route:
IDEA -> CANON -> STORY_BIBLE -> OUTLINE -> CHAPTER_PLAN -> DRAFT -> CRITIQUE -> REWRITE -> CONTINUITY -> FINAL.

Each stage changes persisted state. FINAL must be fail-closed if continuity gate is not passed.

---

## PL-09 — CONTINUITY CHECKER

Create automatic book continuity checking for:
- names
- ages
- appearance
- relationships
- dates/time
- locations
- props/items
- event order
- character knowledge
- already-completed events

Issue schema:

```json
{
  "severity": "MAJOR",
  "chapter": 12,
  "issue": "...",
  "evidence_a": "...",
  "evidence_b": "...",
  "suggested_fix": "..."
}
```

Severity: FATAL, MAJOR, MINOR, STYLE.

Create fixtures with known contradictions and verify expected detection.

---

## PL-10 — MULTI-MODEL REVIEW

Create an independent review workflow:
Writer -> Critic A / Critic B / Critic C independently -> Aggregator -> Decision.

A critic may not see another critic's answer before completing its own evaluation.

Persist independent reviews separately. Minimum dimensions:
- correctness
- completeness
- consistency
- usefulness
- risk

Add a fixture proving critic isolation before aggregation.

---

## PL-11 — TEST / BENCHMARK ENGINE

Create a benchmark runner for business, books, memory and agents.

Every evaluated change records:
- BASELINE
- CANDIDATE
- DELTA
- PASS/FAIL

Acceptance law:
`tests == PASS AND critical_regressions == 0`.

Add deterministic fixtures and machine-readable result output. Do not infer subjective quality from test count alone.

---

## PL-12 — CHANGE CONTROL

Create Change Proposal System:
PROBLEM -> PROPOSE PATCH -> TEST PATCH -> BENCHMARK -> REVIEW -> ACCEPT/REJECT.

Every change stores:
- change_id
- reason
- files_changed
- expected_benefit
- test_results
- benchmark_delta
- decision

Provide rollback semantics. The AI must not silently mutate production code and declare success without passing this lifecycle.

---

## PL-13 — FILE INGESTION

Create ingest support for TXT, MD, PDF, DOCX, CSV and JSON where libraries/runtime permit.

For each file persist:
- metadata
- source
- SHA-256
- text/structured representation
- chunks where useful

Repeated ingestion of the same content hash must not create an uncontrolled duplicate. Add deduplication tests.

---

## PL-14 — PERSONAL KNOWLEDGE SEARCH

Create:

```bash
python run.py ask "what have we already done about ..."
```

The command should search relevant projects, documents, decisions and latest states, then return traceable sources. It must keep hypotheses/inferences separate from confirmed decisions/facts.

Add a fixture where both verified and unverified records exist and prove the answer labels them correctly.

---

## PL-15 — DAILY CONTROL PANEL

Create:

```bash
python run.py today
```

Output only real stored state:
- ACTIVE PROJECTS
- BLOCKED
- NEXT TASKS
- OVERDUE where dates exist
- RECENT OUTPUTS
- FAILED RUNS

No generic AI productivity advice. Add deterministic test data and expected output assertions.

---

## PL-16 — BACKUP AND RECOVERY

Create backup/restore for database, project states, configuration, prompts and important outputs. Exclude disposable caches.

Commands:

```bash
python run.py backup
python run.py restore <backup>
```

Before restore verify checksums and structure. Add a round-trip fixture proving restored state matches source state.

---

## PL-17 — SECURITY

Perform minimum production security hardening:
- secrets only from environment/secret store;
- `.env` ignored by Git;
- secrets redacted from logs/errors;
- filesystem/tool allowlists;
- destructive operations separately authorized;
- path traversal defense;
- safe handling of untrusted document text/instructions.

Create negative security tests for secret leakage, traversal and destructive-tool denial.

---

## PL-18 — COST CONTROL

Create AI cost/usage tracking per API call:
- provider
- model
- input tokens
- output tokens
- estimated/known cost where pricing is configured
- project
- task
- timestamp

Commands:

```bash
python run.py costs today
python run.py costs month
python run.py costs project <ID>
```

Add configurable budget limits and a fixture proving an over-budget call is blocked or escalated according to policy.

---

## PL-19 — LOCAL / CLOUD ROUTER

Create a task router that can send low-risk/simple tasks to a local model and complex/critical reasoning/verification to stronger cloud providers according to explicit policy.

Example categories: classification/extraction/simple summarization versus important reasoning/final verification.

Persist every routing decision and reason. Add policy tests. Do not claim cost savings until measured from real or fixture usage data.

---

## PL-20 — PRODUCTION GATE

Audit the assembled system and create `PRODUCTION_READINESS.md` from real tests/readbacks.

Check at minimum:
- clean install/bootstrap path
- DB initialization
- project creation/state
- memory
- AI mock
- bounded agent execution
- business workflow
- book workflow
- benchmark/tests
- backup/restore
- logs
- secret protection

Do not use `production-ready`, `complete` or `finished` if FATAL/MAJOR issues remain. Record exact blockers and next gate.

---

## PL-21 — FIRST REAL BUSINESS RUN

After PL-20 admits the pilot, run one real bounded business workflow:
lead -> job -> estimate -> quote -> follow-up task -> project state -> archived output.

Record:
- automatic steps
- human-required steps
- errors
- AI usage/cost
- execution time if measurable
- what should be automated/fixed next

Do not fabricate customer acceptance, payment or market response.

---

## PL-22 — FIRST REAL BOOK RUN

Take one existing book project. Do not rewrite the whole book.

Import/reconcile canon, characters, existing chapters, timeline and current status.

Run:
INGEST -> STRUCTURE -> CONTINUITY CHECK -> ISSUE REPORT.

Output only a concrete issue/fix list plus machine state. This becomes the first real benchmark for the Book Module.

---

## PL-23 — FAILURE ANALYSIS

Analyze failures from real pilot execution, not imagined feature wishes.

For each failure:
FAILURE -> ROOT CAUSE -> FREQUENCY/RECURRENCE -> DAMAGE -> FIX -> TEST.

Rank P0/P1/P2/P3 and address P0/P1 first. Preserve UNKNOWN when frequency/damage is not yet measured.

---

## PL-24 — V0.1 RELEASE

Only if critical gates pass, prepare release v0.1.

Required artifacts:
- CHANGELOG.md
- KNOWN_ISSUES.md
- INSTALL.md
- ARCHITECTURE.md
- TEST_REPORT.md
- pinned/locked dependency versions where practical
- Git tag/release marker

Freeze the v0.1 benchmark before starting v0.2. If critical gates fail, do not tag a verified release; persist a candidate/blocker state instead.

---

## Canonical execution order

Wave 1: PL-00 -> PL-01 -> PL-02 -> PL-04 -> PL-05 -> PL-11, reconciling already-proven artifacts rather than duplicating them.

Wave 2: PL-06 -> PL-07 -> PL-08 -> PL-09 -> PL-13 -> PL-14, subject to dependencies in the queue JSON.

Wave 3: PL-03 -> PL-10 -> PL-12 -> PL-16 -> PL-17 -> PL-18.

Wave 4: PL-15 -> PL-19 -> PL-20.

Wave 5: PL-21 -> PL-22 -> PL-23 -> PL-24.

The exact next card is determined by persisted dependency state, not by ritual sequencing. Current frontier at pack creation: `PL-00`.