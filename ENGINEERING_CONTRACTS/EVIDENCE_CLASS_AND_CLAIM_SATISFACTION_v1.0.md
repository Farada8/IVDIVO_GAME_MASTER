# EVIDENCE CLASS + CLAIM SATISFACTION CONTRACT v1.0

**Status:** ENGINEERING CONTRACT / ANTI-INFLATION GATE  
**Date:** 2026-08-21  
**Authority boundary:** evidence classification only; never automatic promotion, Founder lock, canon, or release authorization.

## Problem

IVDIVO now produces many legitimate proof types: tests, AI reviews, source hashes, provider artifacts, human listens, specialist reviews, market data and Founder decisions. The risk is not lack of evidence but **cross-class substitution**: treating one class as if it satisfied another.

Examples that MUST fail:
- model review -> Human Signal;
- unit test -> provider evidence;
- source hash -> market validation;
- story gate -> specialist legal/technical release clearance;
- two reports derived from one root source -> two independent evidence families;
- Human Signal -> Founder lock.

## Evidence classes

Canonical v1 classes:
- `DETERMINISTIC_MACHINE`
- `INTERNAL_AI_REVIEW`
- `SOURCE_PROVENANCE`
- `PRODUCTION_OBSERVATION`
- `PROVIDER`
- `HUMAN_SIGNAL`
- `SPECIALIST`
- `MARKET`
- `FOUNDER_AUTHORITY`

These are **orthogonal classes, not a total ranking**.

## Evidence record

Each evidence record requires:
- `evidence_id` — unique in packet;
- `evidence_class`;
- `source_locator`;
- `source_family` — root provenance family, not model/report count;
- `status = PASS | FAIL | HOLD | BLOCKED`.

Unknown or unmeasured values remain unknown/null. They are never rewritten as zero or PASS.

## Claim record

Each claim requires:
- `claim_id`;
- human-readable `claim_text`;
- explicit `required_evidence_classes[]`;
- optional `minimum_independent_source_families{class: n}`.

A claim without a required evidence class is invalid for machine promotion/release routing.

## Satisfaction law

By default a class satisfies only itself. Cross-class substitution is forbidden unless a future contract explicitly defines a narrow safe substitution for that exact claim type.

Current hard firewalls:
- `INTERNAL_AI_REVIEW != HUMAN_SIGNAL`
- `DETERMINISTIC_MACHINE != PROVIDER`
- `DETERMINISTIC_MACHINE != HUMAN_SIGNAL`
- `SOURCE_PROVENANCE != MARKET`
- `SOURCE_PROVENANCE != SPECIALIST`
- `PROVIDER != HUMAN_SIGNAL`
- `HUMAN_SIGNAL != FOUNDER_AUTHORITY`
- AI/machine evidence never implies `FOUNDER_AUTHORITY`.

## Evidence-family law

Independence follows root provenance. Five model summaries of one underlying document are one source family. Two human listeners are independent only if they are actually distinct human evidence sources under the human protocol. A transformed mirror is not a new evidence family.

## Gate output

The executable gate returns claim-level:
- `PASS | FAIL`;
- satisfied evidence IDs by required class;
- missing classes;
- forbidden impersonation attempts;
- independence failures;
- malformed-evidence errors.

It ALWAYS emits:
`authority_mutation_authorized = false`.

Passing evidence requirements means only that this particular claim has the requested evidence classes. Promotion/lock/release still belongs to the controlling lifecycle/authority gate.

## Integration examples

### Audio
A real provider WAV may satisfy `PROVIDER`; it does not satisfy `HUMAN_SIGNAL`. A prepared listener packet satisfies neither until a human actually performs it.

### Books
Book Engine deterministic sensors may satisfy `DETERMINISTIC_MACHINE` or `PRODUCTION_OBSERVATION`. They cannot establish literary superiority without the explicitly required live/human evidence.

### Story locks
Final Story Gate can be source/provenance and internal review evidence. `FOUNDER LOCKED` requires actual Founder authority if the project gate says so.

### Specialist holds
D07/D08 story lock does not clear finance/legal/product-safety specialist holds.

## Acceptance

Required negative fixtures:
1. AI for human -> FAIL;
2. machine for provider -> FAIL;
3. source provenance for market -> FAIL;
4. machine/story gate for specialist -> FAIL;
5. same source family counted twice -> FAIL;
6. human evidence for Founder authority -> FAIL.

Required positive fixture:
- exact required class present with required independent source families -> PASS, while automatic promotion remains false.
