# IVDIVO — DURABLE MULTI-STORE TRANSACTION CONTRACT v1.0

**Status:** ENGINEERING CANDIDATE / SI-0014  
**Date:** 2026-08-21

## Contract boundary
This contract governs recovery decisions for a logical transaction spanning more than one durable/external store. It does not execute external actions.

## Required inputs
- transaction ID;
- project/work-unit identity;
- fresh authority snapshot (`repo_main_sha`, `state_revision`);
- one or more actions;
- effect class per action;
- side-effect state per action;
- deterministic idempotency key;
- intended/observed identity when available;
- readback status.

## Required invariants
1. `action_id` unique within transaction.
2. idempotency key unique within transaction.
3. credentials/secrets forbidden.
4. blocker outranks all recovery work.
5. authority/state drift outranks action replay.
6. confirmed identity mismatch = STOP.
7. ambiguous paid/irreversible effect = quarantine, never automatic retry.
8. ambiguous reversible effect = store verification before retry.
9. confirmed write is incomplete until readback is verified.
10. unstarted paid/irreversible action requires its existing explicit dispatch/approval gate.
11. only safe missing actions may be returned for automatic continuation.
12. transaction completion requires all actions terminal and verified.

## Proof obligations
A candidate implementation must have deterministic regression fixtures for:
- blocker + ambiguous paid action;
- authority drift + ambiguous action;
- identity mismatch;
- paid unknown quarantine;
- reversible unknown verify-before-retry;
- confirmed without readback;
- safe missing action;
- unstarted paid action;
- full completion;
- secret rejection;
- duplicate action rejection;
- deterministic idempotency/hash behavior.

## Evidence boundary
Passing fixtures prove only tested machine-routing behavior. They do not prove external provider completion, market/human quality, canon correctness, or lossless behavior under every real distributed-system failure.
