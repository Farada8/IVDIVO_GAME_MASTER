# IVDIVO Production System

Canonical machine-readable production workflow for the IVDIVO long-form audio-fiction / book-series project.

## Purpose
This directory is the operational bridge from research corpus to finished episode. It is designed so ChatGPT/Codex can resume work later without relying on chat memory.

## Source-of-truth order
1. `project_state.json` — current pipeline state and next action.
2. `workflow.yaml` — stage order, gates, inputs, outputs.
3. `agent_registry.yaml` — which AI role does what and which source schools it may use.
4. `handoff_schemas.json` — required data contracts between stages.
5. `source_routing.md` — where to take what from reference authors/corpora and what must not be copied.
6. `prompt_library.md` — professional prompts for each stage.
7. `../library_audit/` — source completeness, priority sources, mechanism indexes and dedupe data.
8. Google Drive folder `03_IVDIVO_STORY_ENGINE` — human-readable workbooks and long-form working documents.

## Evidence labels
- `[SOURCE BOOK]` — supported by uploaded literary source.
- `[IVDIVO CANON]` — supported by IVDIVO corpus.
- `[OUR SYNTHESIS]` — new synthesis/deduction.

Never silently promote synthesis to canon.

## Non-negotiable gates
- No full-book claims from fragments.
- No prose before episode passport and scene map pass.
- Every scene changes position, information, relationship, danger, decision or price.
- Every major revelation changes the next action, allowed option or mission definition.
- Every moral choice has a measurable cost.
- Local episode closes a real human problem; mythology may remain open.
- Reference books provide mechanisms, never copied surface, scene sequence or author voice.
- Only IVDIVO corpus defines IVDIVO canon.

## Resume instruction
When resuming work, read `project_state.json` first, then run only the stage named in `next_action`. After completing it, update `project_state.json` with artifacts created, gates passed/failed, unresolved questions and the next stage.
