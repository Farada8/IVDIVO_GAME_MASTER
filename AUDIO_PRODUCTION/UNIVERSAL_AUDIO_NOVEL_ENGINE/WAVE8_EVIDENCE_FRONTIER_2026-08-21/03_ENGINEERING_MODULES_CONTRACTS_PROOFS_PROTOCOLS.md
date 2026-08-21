# WAVE8 — ENGINEERING MODULES, CONTRACTS, PROOFS & PROTOCOLS

## 1. Provider Snapshot Protocol

**Input authority:** existing credential-safe `audio/studio/provider_preflight.py` report.  
**Output:** `ivdivo.audio.provider_snapshot/1.0`.

Pipeline:
`AUTHENTICATED READ-ONLY PREFLIGHT -> SECRET FIREWALL -> STABLE CAPABILITY IDENTITY -> VOLATILE SESSION METADATA -> HASHES -> REQUIRED CAPABILITY GATE`

Laws:
- API key/token is runtime-only and never serialized.
- safe metadata such as `secret_env_present: true/false` may persist; credential-bearing fields may not.
- `TARGETED` means only explicitly queried models/voices were verified.
- `TARGETED` can gate those exact IDs but cannot claim a complete account inventory.
- stable identity drift => HOLD; volatile request/timestamp changes do not by themselves invalidate selected capability identity.
- no automatic model/voice substitution.

Proof obligations:
- secret-field negative fixture;
- stable hash deterministic under same stable data;
- volatile-only delta leaves stable hash unchanged;
- selected voice disappearance produces HOLD;
- targeted scope has `account_inventory_complete=false`.

## 2. Human Review Evidence Protocol

Pipeline:
`REAL AUDIO/SOURCE HASH -> HUMAN REVIEW -> TYPED EVENT -> EVENT HASH -> APPEND-ONLY HASH-CHAIN LEDGER -> EVIDENCE-FAMILY COVERAGE -> HUMAN LOCK ELIGIBILITY`

Evidence families:
- PRONUNCIATION
- MULTI_STATE
- PAIR
- FATIGUE
- BLIND_LISTEN
- TECHNICAL_QC

Laws:
- reviewer event must identify reviewer type/reference, source/audio hashes and review time;
- machine cannot impersonate human evidence;
- historical review events are never rewritten;
- exact duplicate event may be reused, not duplicated;
- hard fail dominates eligibility;
- a PASS and FAIL in a mandatory family create HOLD until reconciled by authorized review policy;
- machine terminal result is at most `ELIGIBLE_FOR_HUMAN_LOCK_DECISION`;
- `voice_lock=false`, `machine_may_auto_lock=false` always.

Proof obligations:
- tampering breaks event/ledger verification;
- missing required family holds;
- pair-required path holds without PAIR;
- complete coverage never auto-locks.

## 3. Live Provider Evidence Escrow Protocol

Pipeline:
`LOCKED SOURCE -> REQUEST HASH -> AUTH CAPABILITY SNAPSHOT -> CONTROLLED DISPATCH -> PROVIDER STATE -> SPEND LEDGER -> RAW AUDIO/ALIGNMENT HASHES + DURABLE REFS -> LINEAGE HASH -> EXACT-N ESCROW -> RECOVERY PLAN`

Laws:
- `PROVIDER ACCEPTED != PRODUCTION TAKE ACCEPTED != PERFORMANCE/VOICE LOCK`;
- ACCEPTED lineage requires provider request ID and durable audio evidence;
- alignment may remain absent/held, but an asserted alignment hash requires a durable alignment reference;
- AMBIGUOUS cannot assert accepted audio/alignment;
- duplicate request hashes are forbidden inside an exact canary escrow;
- missing expected lineage, duplicate block, unknown fourth lineage, source drift, request drift or ambiguous/nonaccepted lineage => escrow HOLD;
- `auto_retry_allowed=false`;
- recovery reads durable refs and returns missing artifacts; `auto_replay_provider=false`.

For Lesson Zero the project overlay may declare exactly `RB001/RB002/RB003`; the universal module itself contains no Lesson Zero IDs.

Proof obligations:
- exact three synthetic lineages pass structural escrow;
- fourth lineage fails;
- duplicate request fails;
- ambiguous response fails;
- source/request drift fails;
- recovery with missing refs routes recovery and never dispatch.

## 4. Typed Proof Manifest Protocol

Purpose: prevent claim laundering.

Evidence classes:
- SOURCE_AUTHORITY
- CODE_TEST
- GITHUB_CI
- AUTH_PROVIDER
- LIVE_AUDIO
- HUMAN_REVIEW
- MEASURED_ECONOMICS
- CROSS_PROJECT_REAL

Examples:
- CODE_READY requires CODE_TEST.
- CI_GREEN requires GITHUB_CI.
- HUMAN_QUALITY_PASS requires HUMAN_REVIEW; CI is insufficient.
- LIVE_AUDIO_ACCEPTED_AS_PROVIDER_EVIDENCE requires AUTH_PROVIDER + LIVE_AUDIO.
- V1_RELEASE_EVIDENCE_COMPLETE requires source + CI + provider + live audio + human + measured economics + cross-project real evidence.

The compiler may return `PROVEN` only when the exact required evidence classes are verified. It does not decide artistic release.

## 5. Self-Improvement Interface

Wave8 is currently an **engineering extension candidate**, not a new universal authority ID.

Observed recurring failure class:
`EVIDENCE EXISTS IN MULTIPLE STORES/LAYERS -> SEMANTIC STRENGTH IS UNCLEAR -> DOWNSTREAM STATE RISKS OVERCLAIM OR IRREVERSIBLE ACTION`.

Candidate mechanism family:
`TYPED EVIDENCE FRONTIER PROVENANCE BRIDGE`

Components:
- provider snapshot;
- human review provenance ledger;
- live evidence escrow;
- typed proof manifest.

Promotion evidence required before universal Self-Improvement authority:
1. integrated CI/regression PASS;
2. at least one real authenticated provider snapshot;
3. one real paid/live lineage recovered after restart without duplicate spend;
4. real human-review ledger used to support an actual lock decision;
5. second materially different audio project proves no project leakage;
6. Red Team finds no path from weaker evidence class to stronger claim;
7. Founder/domain review authorizes promotion.

Until then status must remain `PILOT_CODE / HOLD_REAL_EVIDENCE` or equivalent.

## 6. Rollback

All Wave8 additions are side-effect-free evidence/validation modules. Rollback removes the four new runtime modules/contracts/tests. Existing provider preflight, controlled dispatch, Studio Evidence, session checkpoint, post-render hardening and project authorities remain unchanged.
