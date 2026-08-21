# WORKFLOW RUN LINEAGE CONTRACT v1

## Authority source
Trusted GitHub `workflow_run` event after successful completion of exactly `ElevenLabs Provider Snapshot Evidence`.

## Exact lineage tuple
`repository + workflow_run.id + workflow_run.run_attempt + artifact_name + transaction_id + source_ref + snapshot_hash`.

The artifact name must resolve to:
`elevenlabs-provider-auth-evidence-<run_id>-<run_attempt>`.
The durable transaction ID must be `<run_id>:<run_attempt>`.
The trusted source ref must be `https://github.com/<repository>/actions/runs/<run_id>`.

## Workflow security
- trigger only on upstream workflow completion;
- execute only if upstream conclusion is `success`;
- `contents: read`, `actions: read`; no repository write permission;
- checkout current trusted default-branch code, never code from the artifact;
- do not execute files downloaded from the evidence artifact;
- download only the exact triggering run artifact;
- independently validate all downloaded JSON before use;
- no provider credential in this workflow;
- no synthesis/provider dispatch in this workflow.

## Fail closed
Multiple/missing expected files, lineage mismatch, invalid receipt, stale snapshot, secret-bearing content, or account mismatch terminates intake and produces no READY/lock/spend state.
