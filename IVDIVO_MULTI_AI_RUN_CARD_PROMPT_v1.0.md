# IVDIVO — MULTI-AI RUN CARD PROMPT v1.0

**Status:** PROPOSED UNIVERSAL EXECUTION/HANDOFF STANDARD
**Parent:** `IVDIVO_NARRATIVE_OS/13_CONTINUOUS_MULTI_MODEL_STUDIO_PROTOCOL_v1.0.md`

## Purpose

Give ChatGPT, Claude, Grok, Gemini or another production AI the same recoverable state before it writes, audits, tests or produces anything.

AI brand is not authority. Functional role + loaded authority + evidence determine the value of the output.

## Mandatory startup

Before substantive work, restore the newest governing authority and active project's persisted execution state. Do not treat the current chat transcript as the primary source of truth when a newer valid Drive/GitHub state exists.

Resolve this run card:

```yaml
project_id:
active_project:
active_branch:
story_status:
delivery_mode:
current_authority_refs: []
source_file:
source_version:
source_sha256:
text_protection_mode:
build_id:
project_overlay_version:
voice_binding_ledger_version:
acoustic_identity_ledger_version:
last_completed_artifact:
parent_artifacts: []
open_gates: []
current_blocker:
highest_unblocked_next_obligation:
allowed_actions: []
prohibited_actions: []
required_evidence: []
expected_outputs: []
working_downstream_artifacts: []
next_action:
```

If authority/source/branch is ambiguous, fail closed. Do not invent missing canon.

## Delta boot

Before redesigning a module:
1. inspect the current project's persisted frontier;
2. inspect relevant newer GitHub/Drive deltas since `last_completed_artifact`;
3. inspect neighboring IVDIVO work only for stronger generic mechanisms;
4. classify any discovered item as `PROJECT_ONLY / GENRE_OVERLAY_CANDIDATE / UNIVERSAL_CANDIDATE / REFERENCE_ONLY / SUPERSEDED / REJECTED`;
5. strip project-specific content before any portability test.

Never transfer names, provider voice IDs, culprit/solution, clue chains, signature motifs, chronology or relationship timing.

## Execution rule

Once the Founder has authorized active work, continue through consecutive **SAFE + ZERO-COST + REVERSIBLE + TOOL-EXECUTABLE** unblocked actions without waiting for repeated `и / дальше` messages.

Stop only at a real blocker: unresolved authority, missing evidence/human signal, paid/authenticated action unavailable in the current environment, user-side credential step, irreversible/high-impact action requiring approval, explicit lock/release gate, missing tool, or Founder STOP/HOLD.

Do not manufacture planning documents when the next real gate is external execution/evidence.

## Artifact provenance

Every material returned artifact should expose or allow recovery of:

```yaml
artifact_id:
artifact_version:
status: CANON|LOCKED|WORKING|OPTION|REFERENCE_ONLY|SUPERSEDED|REJECTED
project_id:
build_id:
parent_artifacts: []
source_sha256:
producer_system:
functional_role:
created_for_stage:
completed_action:
open_gates_after: []
blocker_after:
next_action_after:
```

No secrets/API keys in artifacts.

## Parallel multi-AI law

Different AIs may work concurrently only on independent DAG branches whose upstream gates PASS. They converge by artifact IDs, hashes, manifests and explicit gate outcomes, not conversational summaries.

No AI may silently change canon, protected text, locked voice identity, clue causality or release state.

## External-model report

Record where possible:
`MODEL/PROVIDER / FUNCTIONAL ROLE / MATERIAL+VERSION / AUTHORITY LOADED / EXACT QUESTION / FINDINGS / SEVERITY / EVIDENCE / PROPOSED FIX / DISPOSITION PENDING|ACCEPT|MODIFY|REJECT|HOLD / CHANGED ARTIFACTS / TESTS / BLOCKERS / NEXT ACTION`.

No model may promote its own recommendation to CURRENT/CANON.

## End-of-action update

After every substantive completed action update the active project's persisted execution state with:
`last_completed_artifact / completed_action / open_gates / blocker / next_action / required_evidence / hard_stops / working_downstream_artifacts`.

If `next_action` is safe, zero-cost, reversible and executable with available tools, continue immediately. Otherwise stop at the real blocker and report:
`DONE / STATUS / BLOCKER / EXACT NEXT ACTION`.
