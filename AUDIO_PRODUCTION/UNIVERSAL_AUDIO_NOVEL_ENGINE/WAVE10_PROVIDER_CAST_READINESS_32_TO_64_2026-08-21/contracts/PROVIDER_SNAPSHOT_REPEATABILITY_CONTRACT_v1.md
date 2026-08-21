# PROVIDER SNAPSHOT REPEATABILITY CONTRACT v1

Status: WORKING engineering contract. Does not create provider truth.

## Purpose
Compare two independently validated secret-free ProviderSnapshots from the same provider account and separate capability drift from ordinary volatile usage drift.

## Preconditions
1. Each input independently PASSes `provider_snapshot_contract.validate_provider_snapshot`.
2. Expected provider is explicit.
3. Account fingerprint is present and equal across snapshots.
4. Freshness is enforced when the consumer supplies a max-age.

## Outputs
- source snapshot hashes;
- same-account proof;
- model added/removed/changed sets;
- voice added/removed/changed sets;
- account-metadata change flag;
- volatile-usage change flag;
- `dispatch_revalidation_required` when capability inventory changed;
- `auto_substitution=false` always.

## Fail-closed
Different account fingerprints -> `FAIL_ACCOUNT_IDENTITY_DRIFT`.
Invalid first/second snapshot -> `FAIL_FIRST_SNAPSHOT` / `FAIL_SECOND_SNAPSHOT`.

## Evidence ceiling
Repeatability proves only observed consistency/drift of authenticated snapshot data. It does not prove voice quality, pronunciation, performance, human preference, price, future availability, successful synthesis or release readiness.
