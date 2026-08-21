# PROVIDER EXECUTION STATE CONTRACT v1

## Purpose
Convert already-admissible provider evidence into a deterministic next action without creating missing external evidence.

## States owned by this resolver
- `NO_ADMISSIBLE_PROVIDER_EVIDENCE` -> run authenticated provider workflow;
- `AUTH_PROVIDER_VERIFIED` -> acquire second read-only snapshot;
- `CAPABILITY_DRIFT_REVALIDATION_REQUIRED` -> revalidate bindings, no substitution;
- `INVENTORY_READY` -> bind provisional candidates from current inventory;
- `CAST_NOT_AUDITION_READY` -> repair structural candidate/model binding;
- `AUDITION_REQUIRED` -> obtain real pronunciation/multi-state/pair/fatigue human/audio evidence.

## Explicit non-authority
This resolver cannot issue:
- human/Founder voice lock;
- pronunciation lock;
- pre-spend GO;
- paid dispatch authorization;
- production-ready status.

Those remain under existing receipt-based Human Review, Studio Evidence, production-control and Founder authority surfaces. Caller booleans may not substitute for those evidence classes.
