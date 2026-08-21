# PROVIDER EVIDENCE INTAKE CONTRACT v1

## Inputs
- one secret-free `AUTH_PROVIDER` payload emitted by the trusted upstream acquisition/readback workflow;
- exact GitHub repository, triggering `run_id`, and `run_attempt` supplied by trusted workflow event context;
- optionally the separately stored `provider_snapshot.json` from the same artifact;
- optionally one prior authenticated snapshot for repeatability comparison.

## Mandatory validations
1. no forbidden secret-bearing key shapes (`api_key`, authorization, access token, password, private key, bearer token);
2. canonical `validate_provider_auth_receipt(... expected_provider=elevenlabs, max_age_seconds=21600)` PASS;
3. durable receipt transaction ID equals exactly `<run_id>:<run_attempt>`;
4. durable/trust `source_ref` equals exactly `https://github.com/<repository>/actions/runs/<run_id>`;
5. optional separately stored snapshot independently validates and has the same canonical snapshot hash as the packet;
6. provider inventory compiles only from the validated current snapshot;
7. optional prior snapshot independently validates; account fingerprint drift is fatal; capability drift requires downstream revalidation and never auto-substitution.

## Outputs
`PASS_AUTH_PROVIDER_INTAKE` only when every applicable validation passes. Output contains typed lineage, normalized inventory, optional repeatability result, next admissible state, and a deterministic intake hash.

## Invariants
- provider calls performed by intake = 0;
- paid synthesis calls = 0;
- provider dispatch allowed = false;
- machine may auto-lock = false;
- voice lock = false;
- inventory metadata is not artistic evidence;
- no current real provider fact may be inferred when the input artifact is absent.

## Fail closed
Malformed, stale, mismatched, cross-run, cross-account, secret-bearing, or capability-incomplete evidence cannot advance provider/cast state.
