# WAVE8 — ENGINEERING CROSSWALKS, CONTRACTS AND SELF-IMPROVEMENT

## 1. ProviderSnapshotContract
Purpose: bridge authenticated provider reality into the already-existing fail-closed dispatch without storing secrets.

Required stable/semi-stable fields:
- `schema_version`, `provider`, `snapshot_id`, `captured_at`, `snapshot_hash`;
- secret-free account fingerprint / subscription-plan class;
- `models[model_id]` with supported request modes, alignment/output capabilities and status;
- `voices[voice_id]` with availability/status and provider-exposed metadata needed for filtering;
- capability version/source evidence;
- separate `volatile` object for quota/remaining credits/rate-limit/current service status.

Forbidden:
- API key, bearer token, cookies, raw auth headers.
- inferred voice/model entries not returned by authenticated evidence.

Rule: current dispatch remains authoritative for no-auto-swap. Missing bound voice/model => no dispatch.

## 2. HumanEvidenceLockContract
Generic reviewer roles only:
`HUMAN_LISTENER | HUMAN_ENGINEER | HUMAN_DIRECTOR`.

Every judgment binds:
- artifact SHA256;
- provider snapshot hash;
- voice/model IDs;
- exact text/context hash where pronunciation is evaluated;
- test type and randomized/blind pack ID when applicable;
- reviewer type;
- status `PASS | FAIL | HOLD`;
- reviewed_at;
- structured findings.

Lock law:
- machine evidence may prepare packs and flag defects;
- machine-only evidence cannot create pronunciation or voice PASS;
- any HOLD keeps lock HOLD;
- BODYGUARD/ROOM917 reviewer names, text, role IDs or voice IDs may not transfer.

## 3. LiveEscrowContract
One provider request lineage must persist:
`project_id -> block_id -> exact_text/request_hash -> identity fixture hash -> provider snapshot hash -> voice/model bindings -> spend-ledger PLAN/SENT/ACCEPTED|REJECTED|AMBIGUOUS -> provider_request_id -> response metadata hash -> charge evidence -> raw audio SHA/path -> alignment SHA/path -> canonical-ingest evidence -> human/take status`.

Recovery protocol:
1. read escrow without chat memory;
2. compare request hash + ledger state;
3. `ACCEPTED` => reuse, never resend;
4. `AMBIGUOUS` => reconcile provider history before retry;
5. provider bytes are provenance/spend evidence, not take lock;
6. downstream timeline/mix may consume only accepted canonical audio/alignment.

## 4. ArchitectureRefreezeProtocol
Current main: `58f434d7582a193ab3e120491159ccdec349717e`.
No new generic runtime module is admissible merely because an idea looks useful.

A runtime delta may open only from one of:
- reproducible failing CI/regression;
- authenticated provider capability failure not representable by current contracts;
- real audio/human failure with a missing contract;
- measured economics showing a deterministic control-plane defect;
- recovery drill failure;
- cross-project replication showing a universal boundary leak.

Otherwise improve through evidence, project adapters, tests, telemetry and operational manifests.

## 5. SelfImprovementEvidenceLoop
Use:
`AUTHORITY -> EVIDENCE CONTRACT -> TEST/EXPERIMENT -> PROVENANCE -> EARLIEST FAILURE LAYER -> MINIMAL PATCH -> REGRESSION -> METRICS -> CANDIDATE MECHANISM -> FOUNDER REVIEW`.

Earliest failure layer taxonomy:
`SOURCE / LOCALIZATION / TERMINOLOGY / VOICE DESIGN / PROVIDER / PERFORMANCE / EDIT / MIX / DEVICE / TEST DESIGN / MARKET`.

Rules:
- patch only the earliest failed layer and invalidated descendants;
- duplicate evidence family counts once;
- project story facts never become universal engine facts;
- two real independent projects can make a domain mechanism `ELIGIBLE_FOR_FOUNDER_REVIEW`, never automatic current authority;
- when HOLD, choose the highest-expected-information next experiment, not another broad architecture cycle.

## 6. Baseline-Before-Challenger Spend Protocol
Sequence:
1. authenticated snapshot;
2. cheapest viable baseline candidate per role;
3. pronunciation micro-test;
4. state responsiveness;
5. pair/fatigue;
6. only then challengers where expected information gain justifies spend.

Until authenticated pricing/quota exists, the numeric ceiling is deliberately `UNRESOLVED`; no invented euro/credit limit.
