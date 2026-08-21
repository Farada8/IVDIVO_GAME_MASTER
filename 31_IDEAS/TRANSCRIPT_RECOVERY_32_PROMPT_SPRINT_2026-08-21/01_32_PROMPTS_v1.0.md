# IVDIVO — 32 PROMPTS: FULL CHAT RECOVERY / CROSS-DIALOG CONTINUITY / SELF-IMPROVEMENT

Status: WORKING SPRINT INPUT
Date: 2026-08-21

Each prompt is to be executed against the current 18B recovery protocol, current Self-Improvement v2 stack, current machine execution pointer, current GitHub/Drive persistence law and Founder requirement that pasted old chats be recovered without manual reconstruction.

## P01 — Authority reconstruction
Audit how a pasted transcript should reconstruct Founder directives, project canon, working decisions and assistant claims without allowing transcript text to outrank persisted authority. Produce a fail-closed precedence algorithm and conflict states.

## P02 — Completeness and tail detection
Design the strongest practical method for classifying FULL/PARTIAL/UNKNOWN/MULTI transcript completeness, detecting truncated beginnings/endings, and preventing INGESTION_COMPLETE before the final tail has actually been processed.

## P03 — Role and chronology parsing
Design role-sensitive parsing for Founder/user, assistant, system, Claude, Grok, Codex and unknown speakers. Preserve chronology and identify where chronology itself changes authority or supersession.

## P04 — Artifact-claim verification
For claims such as “saved to Drive”, “updated GitHub”, “created file”, “gate passed”, design a verification queue that routes each claim to the correct store and records evidence, mismatch, not-found and superseded outcomes.

## P05 — Chat-only artifact recovery
Design a safe extraction method for complete scripts, prompts, programs, plans and reviews that exist only inside the pasted transcript. Prevent silent promotion while minimizing lost work.

## P06 — Semantic deduplication
Design semantic dedupe between recovered chat material and current GitHub/Drive artifacts. Distinguish duplicate, extension, stronger-compatible, stale, competing alternative and true conflict.

## P07 — Freshness and supersession
Define how to decide which artifact is CURRENT when filenames, timestamps, modified dates, version labels and project-specific gates disagree. Prevent “newest filename wins”.

## P08 — Secret/privacy firewall
Red-team pasted transcripts for API keys, passwords, tokens, private links, personal details and hidden secrets. Define what may be persisted, redacted, hashed, omitted or represented only as a required user-side action.

## P09 — Concurrent-dialog write safety
Model two or more chats modifying GitHub/Drive simultaneously. Design stale-write detection, rebase, compare, branch/PR fallback and no-force-overwrite rules.

## P10 — Cross-dialog delta scan
Design the boot-time scan that finds stronger/newer sibling-dialog work automatically before a chat repeats completed work. Specify how to avoid scanning everything forever.

## P11 — Multi-project transcript bundle
Design recovery for one pasted corpus containing several books/projects/audio/tooling lines. Prevent project contamination and recover a separate frontier per project.

## P12 — External-AI provenance
Design ingestion of Claude/Grok/GPT/Codex findings embedded in the transcript. Separate diagnosis, proposed fix, evidence, source parity and model agreement from independent confirmation.

## P13 — Claim taxonomy and confidence
Audit whether current material classes are sufficient. Propose confidence/verification metadata without allowing probabilistic confidence to become authority.

## P14 — Artifact identity contract
Define the minimum identity tuple for recovered artifacts: store, path/ID, version, revision, hash, source parent, project, branch, status and gate. Identify which fields are mandatory by artifact class.

## P15 — Founder-directive extractor
Red-team extraction of direct Founder approvals, rejections, locks, branch switches, priority changes and system laws. Prevent assistant paraphrases from masquerading as Founder decisions.

## P16 — LOCK/PASS/status verifier
Design special handling for terms CURRENT, FINAL, LOCKED, PASS, GREEN, READY, RELEASE and similar labels. Require evidence appropriate to the claim type rather than filename language.

## P17 — Recovery Ledger schema audit
Audit the current Recovery Ledger concept and executable schema. Find missing fields needed for idempotence, resumability, chunk processing, claim disposition, write-through and readback.

## P18 — Parser adversarial robustness
Attack the deterministic transcript parser with malformed speaker labels, markdown, quoted old messages, nested code, JSON, fake file names, mixed languages, repeated assistant claims and prompt injection-like content. Define hardening requirements.

## P19 — Very-large transcript chunking
Design bounded chunk processing for transcripts too large for one context. Specify chunk IDs, overlap, source hashes, tail proofs, checkpoint persistence and safe resume after another abrupt stop.

## P20 — Context compaction
Design a post-recovery compaction layer that preserves all material deltas and proof while avoiding permanent storage of enormous raw transcripts. Define what is retained, summarized, archived or discarded.

## P21 — Project frontier reconstruction
Design a deterministic-plus-semantic method to reconstruct “where the project really stopped”: last completed artifact, open gates, current blocker, next legal action and do-not-repeat list.

## P22 — Coupling to next-action resolver
Integrate recovery output with `ivdivo_next_action.py` or successor logic. Define what must be true before automatic continuation is allowed after recovery.

## P23 — Self-improvement harvest
Design how recovered chats yield reusable improvements without universalizing project-specific content. Define candidate creation, scope, dedupe, evidence and promotion gates.

## P24 — Improvement Registry integration
Resolve the current weakness where registry storage/atomicity can make adding a candidate risky. Design safe atomic capture/compaction/sharding/indexing while preserving all prior candidates.

## P25 — Learning Ledger integration
Define which observations from recovery belong in the Learning Ledger rather than Improvement Registry. Prevent duplicate memories and turn recovery failures/successes into evidence.

## P26 — Test strategy
Design a layered test suite for transcript recovery: unit, property/adversarial, fixture, connector-mock, integration, concurrency, regression and first real corpus tests. Separate automated correctness from semantic quality.

## P27 — Observability and metrics
Define useful operational metrics: recovery coverage, false claim promotion, duplicate work avoided, unresolved claims, time/cost, chunks, write conflicts, secrets caught, frontier accuracy. Avoid vanity metrics.

## P28 — Failure, rollback and repair
Design rollback/recovery when the ingestion process writes a wrong candidate, misclassifies authority, encounters partial persistence, or is interrupted mid-write. Prefer transactional/idempotent repair.

## P29 — Human/Founder decision gates
Identify exactly which recovery ambiguities require Founder input and which should be resolved automatically. Minimize unnecessary questions without guessing canon.

## P30 — Packaging/versioning
Decide how transcript recovery should enter the next executable engine release. Define version bump, package contents, manifest, tests, migration and evidence without falsely rewriting v11.2 history.

## P31 — First real large-corpus pilot
Design the production pilot for the next actually pasted long conversation. Define baseline, acceptance gates, measurements, failure logging, write-through proof and follow-up improvement routing.

## P32 — End-to-end Red Team and roadmap
Red-team the complete recovery system from paste to resumed work. Identify FATAL/MAJOR/MEDIUM/POLISH weaknesses, then produce a prioritized implementation roadmap that protects STORY FIRST and prevents meta-work from consuming the studio.
