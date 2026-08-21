# IVDIVO — CHECKPOINT LINEAGE + RETENTION CONTRACT v1.0

**Status:** ENGINEERING CANDIDATE / SI-0014  
**Date:** 2026-08-21

## Purpose
Prevent checkpoint-file explosion and ambiguous concurrent heads while preserving incident evidence.

## Lineage invariants
- exactly one root per work unit;
- root generation = 0;
- each child names one existing parent in the same work unit;
- child generation = parent generation + 1;
- duplicate `entry_id` forbidden;
- duplicate checkpoint SHA forbidden;
- cycles forbidden;
- appending a child supersedes the previous ACTIVE parent;
- a competing unexplained ACTIVE head fails closed.

## Retention classes
- `EPHEMERAL_RECOVERY_CURRENT` — newest checkpoint needed for current recovery;
- `AUDIT_KEEP` — historical checkpoint tied to a real incident/evidence obligation;
- `GC_ELIGIBLE` — routine superseded checkpoint that is not required for incident evidence.

## Anti-bloat rule
Checkpoint lineage stores hashes/pointers and recovery metadata, not full chat transcripts, model scratchpads, binary asset bytes, or duplicate project-state payloads.

## Proof obligations
Tests must cover root/child append, second-root rejection, cross-work parent rejection, generation mismatch/cycle rejection, duplicate checkpoint rejection, competing head rejection, and retention of incident evidence.

## Authority boundary
Lineage is an audit/recovery index. It never outranks current project authority or restores superseded canon/state by itself.
