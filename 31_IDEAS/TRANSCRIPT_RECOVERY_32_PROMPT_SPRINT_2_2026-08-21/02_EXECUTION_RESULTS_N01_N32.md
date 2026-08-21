# IVDIVO — SPRINT 2 — SEQUENTIAL EXECUTION RESULTS N01–N32

**Status:** 32/32 executed sequentially after freshness/rebase.  
**Truth boundary:** design/audit results are not live provider, Human Signal or market evidence. Candidate branches remain candidates until gates pass.

## N01 — Reconciled Recovery State v2 Rebase
**Result:** `EXTEND_EXISTING_CANDIDATE`  
PR #67 already defines Reconciled Recovery State v2 and a completion gate. Do not create a second state model. Extend it through evidence adapters, adversarial fixtures and the first real-corpus pilot.

## N02 — Authority Taxonomy Hardening
**Result:** `ACCEPT`  
Use `FOUNDER_DIRECT / LOCKED_PROJECT_CANON / CURRENT_PROJECT_AUTHORITY / CURRENT_DOMAIN_AUTHORITY / CURRENT_STATE_POINTER / WORKING_CANDIDATE / EXTERNAL_FINDING / ASSISTANT_OR_MODEL_CLAIM / REFERENCE_ONLY`. A lower class cannot silently promote itself.

## N03 — Verification State Machine
**Result:** `ACCEPT`  
`UNCHECKED -> VERIFIED | MISSING | SUPERSEDED | CONFLICT | UNRECOVERABLE | NOT_APPLICABLE`. VERIFIED/SUPERSEDED must carry evidence_ref when asserting persisted identity/currentness.

## N04 — Multi-Project Partitioning
**Result:** `ACCEPT`  
Partition by project_key + branch/line + artifact identity. Ambiguous material enters `UNKNOWN_PROJECT` quarantine. Universalization is a separate mechanism-extraction decision.

## N05 — Conflict Graph + Resolution
**Result:** `ACCEPT`  
Edges: `CONTRADICTS / SUPERSEDES / DUPLICATES / DEPENDS_ON`. Resolve by authority first, then compatible chronology/currentness; irreducible same-authority creative conflict returns to Founder.

## N06 — Unknown Contract
**Result:** `ACCEPT`  
Types: `MISSING_EXACT_DETAIL / UNAVAILABLE_STORE / INCOMPLETE_TRANSCRIPT / UNRESOLVED_CHRONOLOGY / UNRESOLVED_PROJECT_IDENTITY / EVIDENCE_NOT_RECEIVED / TOOL_UNAVAILABLE`. Material unknown blocks completion; nonmaterial unknown remains recorded.

## N07 — INGESTION_COMPLETE Contract
**Result:** `ALREADY_IMPLEMENTED_AND_GREEN_CANDIDATE`  
PR #67 already requires processed tail, material dispositions, terminal verification tasks, no material unknown/conflict, fresh frontier, write readback and secret firewall. Exact-source unit smoke there is 11/11 PASS; PR67 remains candidate pending wider integration/real-corpus evidence.

## N08 — v1→v2 Migration Contract
**Result:** `ACCEPT`  
Ledger v1 stays immutable extraction evidence. v2 references its source SHA/ref and stores semantic dispositions separately; migration never rewrites v1 findings to make them look authoritative.

## N09 — Claim→Evidence Registry
**Result:** `ACCEPT`  
Evidence families fixed: persistence claim→store readback; Founder lock→direct decision; machine PASS→exact runtime evidence; provider render→real job/output; human→actual response tied to stimulus; market→actual platform metric provenance; CURRENT→pointer+supersession proof.

## N10 — Founder Lock Evidence
**Result:** `ACCEPT`  
`READY_FOR_LOCK` and `RECOMMENDED_LOCK` are not approval. Lock requires a direct Founder decision trace or already-persisted Founder-lock evidence valid under the project authority hierarchy. Models cannot infer it.

## N11 — Automated Test PASS Evidence
**Result:** `ACCEPT`  
Minimum: exact source/version/hash, exact test identity, invocation/equivalent, material environment/fixture identity, exit status, pass/fail counts and log/evidence ref. Prose “tests passed” is insufficient.

## N12 — Provider Execution Evidence
**Result:** `ACCEPT`  
Real provider evidence requires provider/job/request identity plus returned asset/output metadata and persisted output pointer where relevant. A compiled request or dry manifest proves compilation only.

## N13 — Human Evidence Protocol
**Result:** `ACCEPT`  
Human evidence requires actual participant response tied to exact stimulus/build, method/date and blinded status/questions where material. AI review is not Human Signal.

## N14 — Market Evidence Protocol
**Result:** `ACCEPT`  
Market evidence requires actual platform/experiment source, period/cohort/denominator, metric definition and observed value. Forecast/model estimate remains hypothesis.

## N15 — Persistence Verification Adapter
**Result:** `ACCEPT`  
Adapter contract: `store + locator + expected identity/version/hash + read action + currentness rule + result + evidence_ref + checked_at + superseded_by`. Adapters read evidence; they do not decide canon.

## N16 — Supersession/Currentness Verifier
**Result:** `ACCEPT`  
Existence ≠ CURRENT. Currentness may be proven by controlling pointer/authority, explicit supersession chain, compatible newer project-specific gate, branch state and version/hash. Timestamp alone does not win.

## N17 — Nested Role-Marker Parser Red Team
**Result:** `PARTIALLY_IMPLEMENTED_CANDIDATE`  
Parser-hardening branch protects fenced code, blockquotes and indented role markers. Plain embedded role-like prose remains inherently ambiguous; structured export should be preferred when available.

## N18 — Markdown/Code/JSON False-Role Fixtures
**Result:** `PARTIALLY_IMPLEMENTED_CANDIDATE`  
Existing hardening tests cover fence/indent/blockquote cases. JSON/YAML/string-escaped cases should join the next adversarial/fuzz wave before any promotion.

## N19 — RU/UA Role + Directive Coverage
**Result:** `IMPLEMENTED_CANDIDATE`  
Hardening branch adds Russian/Ukrainian role aliases and directive/work-claim vocabulary. Keyword detection remains extraction only and carries no authority.

## N20 — Malformed/Partial Transcript Behavior
**Result:** `ACCEPT`  
Malformed/partial input downgrades completeness/role certainty, preserves unknown spans, never invents missing tail, and blocks completion when omitted material can alter authority/frontier.

## N21 — Fake Artifact Reference Fixtures
**Result:** `ACCEPT`  
References inside code/quotes may remain `UNVERIFIED` verification tasks. A safe false-positive lookup is preferable to losing a real referenced artifact, but no extracted reference self-verifies.

## N22 — Large-Corpus Checkpoint/Resume
**Result:** `ACCEPT`  
Checkpoint identity: source SHA + chunk ID/range + overlap hash + findings hash + tail flag. Source-hash change invalidates silent resume; only compatible checkpoints can be reused.

## N23 — Interrupted Recovery Resume
**Result:** `ACCEPT`  
Resume validates source SHA, prior checkpoint lineage, overlap and prior write/readback journal; incomplete last chunk is reprocessed and findings semantically deduped before new writes.

## N24 — Property/Fuzz Invariant Suite
**Result:** `ACCEPT`  
Invariants: transcript never self-promotes; assistant/model claims remain unverified until independent proof; secrets never persist; unprocessed tail/material unknown/conflict/readback failure prohibit completion; auto-continue cannot bypass Founder/human/provider gates.

## N25 — Recovery Write Transaction
**Result:** `ACCEPT`  
Write record: recovery_id, target, precondition revision/SHA, previous pointer, content fingerprint, intended mutation, result ref, readback, rollback/repair status. No material write is complete before readback.

## N26 — Idempotent Chat-Only Persistence
**Result:** `ACCEPT`  
Idempotency key: source SHA + project key + artifact class + normalized content hash + recovery lineage. Existing same key→NO_OP/DUPLICATE; changed authority→reconcile rather than duplicate.

## N27 — GitHub Stale-Write/Rebase
**Result:** `VERIFIED_BEHAVIOR`  
Stale SHA has already occurred during real parallel IVDIVO work. Rule: abort stale write, fetch fresh, semantic rebase; if independent use branch+PR. Force overwrite prohibited by default.

## N28 — Google Drive Revision Control
**Result:** `ACCEPT`  
For native Docs: fresh revision → writeControl where supported → mutation → content/revision readback. Conflict triggers re-read/reconcile; no blind repeated append.

## N29 — Partial-Write Repair
**Result:** `ACCEPT`  
Use `PARTIAL_WRITE_REPAIR_REQUIRED`; journal successful/failed targets; never global-rollback newer sibling work. Repair failed/touched surfaces against fresh state, then read back all accepted writes.

## N30 — Two-Chat Concurrency Simulation
**Result:** `ACCEPT_AS_TEST_DESIGN`  
Test independent-path and same-path races, stale preconditions, duplicate desired content and conflicting content. PASS = no lost update, no force overwrite, deterministic rebase/decision gate.

## N31 — Atomic/Sharded Improvement Registry
**Result:** `EXTEND_CURRENT_REGISTRY_FAMILY`  
Main already has base registry + `REGISTRY_EXTENSIONS` + family pointer and unique-ID law. Adopt shard+index as concurrent transaction model; monolithic base becomes compatibility/compacted read model rather than sole write surface.

## N32 — Registry Compaction Builder
**Result:** `ACCEPT`  
Compactor must read base+extensions, validate schema+unique IDs, stable-sort, emit pretty canonical JSON plus manifest of input SHAs/count/output SHA, compare/readback before pointer switch, and retain previous snapshot for rollback.

## Count

32/32 prompts dispositioned. Strongest result: semantic reconciliation/evidence/persistence is now more important than further parser expansion. The first real large pasted corpus is the next decisive evidence gate.
