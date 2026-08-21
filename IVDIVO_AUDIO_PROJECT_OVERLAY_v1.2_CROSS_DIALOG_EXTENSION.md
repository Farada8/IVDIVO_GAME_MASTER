# IVDIVO — AUDIO PROJECT OVERLAY v1.2 CROSS-DIALOG EXTENSION

**Status:** ADDITIVE EXTENSION to `IVDIVO_AUDIO_PROJECT_OVERLAY_TEMPLATE_v1.1.md`.
**Rule:** v1.1 fields remain valid. This extension adds execution continuity and stronger voice-audition gates; it does not alter project story canon.

## A. PERSISTED EXECUTION STATE

Every active project must bind a machine-readable `CURRENT_EXECUTION_STATE` or equivalent.

Required fields:

- `project / project_id`
- `active_branch`
- `story_status`
- `delivery_mode`
- `build_id`
- `authority_refs`
- `source file/version/hash/text_protection_mode`
- `last_completed_artifact`
- `completed_action`
- `parent_artifacts`
- `open_gates`
- `current_blocker`
- `next_action`
- `required_evidence`
- `hard_stops`
- `allowed_actions`
- `prohibited_actions`
- `working_downstream_artifacts`
- `continuation_policy`

A new/resumed chat must read this state before interpreting `continue`.

### Continuation policy fields

```yaml
continuation_policy:
  default_continue_when_unblocked: true
  require_repeated_continuation_word: false
  safe_zero_cost_reversible_only: true
```

For an action to auto-continue, project state should explicitly resolve:

```yaml
next_action:
  stage:
  action:
  safe: true|false
  zero_cost: true|false
  reversible: true|false
  tool_executable_here: true|false
```

Missing flags fail closed.

## B. CROSS_DIALOG_SYNC

Before resumed work:
1. current Drive router;
2. active project execution state;
3. relevant newer Drive/GitHub artifacts and repository deltas;
4. project source/hash/branch/overlay/locks;
5. open gates and blocker;
6. highest unblocked next obligation.

Do not recreate a module until this sync proves it is absent or obsolete.

## C. VOICE AUDITION / CASTING GATE

For each role add:

```yaml
audition_protocol:
  candidate_slots: []
  candidate_labels_anonymous_where_practical: true
  loudness_matched: true
  music: OFF
  reverb: OFF
  heavy_processing: OFF
  minimum_take_types:
    - NATURAL_RESTRAINED
    - DIRECTED_CHANGE
  functional_test_blocks: {}
  direction_change_test:
    first_direction:
    second_direction:
    pass_condition:
  hard_fails: []
  weighted_scorecard: {}
  device_translation:
    headphones: REQUIRED
    mono: REQUIRED
    phone: REQUIRED
  long_form_fatigue_minutes:
  status: CANDIDATE|HOLD|CALLBACK|PROVISIONAL_PILOT_LOCK|LOCKED|REJECTED
```

### Casting laws

- Never cast from one best line.
- One precise direction must create an audible useful change without breaking character law.
- Hard fail overrides attractive timbre or high average score.
- Important leads require a pair/chemistry gate when relationship dynamics matter.
- Chemistry must not be manufactured through flirtation if the story relationship state is earlier/more constrained.
- Season lock requires long-form fatigue/listenability evidence and project-required performed multi-episode evidence.

Project-specific numeric thresholds belong in the project overlay; generic universal layer does not force one score threshold across all genres.

## D. PAIR / RELATIONSHIP PERFORMANCE GATE

For every relationship-critical pair:

```yaml
pair_gate:
  pair: []
  exact_pair_blocks: []
  current_relationship_state:
  extra_attention_allowed:
  romantic_pressure_allowed:
  status_asymmetry:
  pass_conditions: []
  hard_fails: []
```

Test the relationship actually written, not the relationship expected later in the season.

## E. MULTI-AI RUN CARD

Every AI must restore:

`project_id / branch / story_status / delivery_mode / authority_refs / source file-version-hash / build_id / overlay / last_completed_artifact / parent_artifacts / open_gates / blocker / next obligation / allowed / prohibited / evidence / outputs / produced IDs+hashes / next_action`.

Parallel AI work is allowed only on independent DAG branches with upstream PASS. Merge through artifacts/manifests.

## F. WORKING DOWNSTREAM ARTIFACTS

A project may contain useful later-stage artifacts created before the current upstream gate is satisfied. Record them explicitly rather than letting them hijack current execution:

```yaml
working_downstream_artifacts:
  - artifact:
    status: WORKING
    stage:
    blocked_by:
    note:
```

Downstream work never bypasses a current upstream real-evidence/voice/canon/release gate.

## G. CONTINUATION COMMAND REPLACEMENT

Replace v1.1 section 25 semantics with:

**CONTINUATION DEFAULT**

Once the Founder authorizes active work:
1. restore current universal + project authority;
2. read persisted project execution state;
3. inspect newer cross-dialog deltas;
4. execute the highest unblocked safe/zero-cost/reversible/tool-executable obligation;
5. save/version result;
6. update execution state;
7. if the next obligation also qualifies, continue immediately;
8. stop only at a defined real blocker and report `DONE / STATUS / BLOCKER / EXACT NEXT ACTION`.

`и / дальше / продолжай / делай / работай` remain shorthand but are not required between consecutive authorized steps.

**NO SILENT CANON CHANGES. FAIL CLOSED ON AUTHORITY AMBIGUITY.**
