# IVDIVO NARRATIVE OS — OUTPUT SCHEMAS

**Status:** CANONICAL DATA CONTRACT  
**Version:** 1.0

---

# 1. AGENT_PACKET

Use this to brief every specialist.

```yaml
AGENT_PACKET:
  task_id:
  project:
  book_or_line:
  version:
  mode:
  phase:
  founder_instruction:
  decision_needed:
  governing_canon:
  locked_facts:
  source_material:
  relevant_prior_reports:
  forbidden_changes:
  independence_required: true|false
  output_schema:
  gate:
```

Do not include irrelevant saga lore merely because it exists.

---

# 2. ROUTE_PLAN

```yaml
ROUTE_PLAN:
  active_project:
  active_book_or_line:
  mode:
  current_phase:
  unresolved_decision:
  selected_agents:
    - id:
      reason:
      depends_on:
      independent_from:
  canon_inputs:
  source_inputs:
  forbidden_changes:
  gate:
  stop_condition:
```

---

# 3. AGENT_REPORT

All specialist reports use a shared header.

```yaml
AGENT_REPORT:
  agent_id:
  task_id:
  verdict: GREEN|YELLOW|RED
  confidence: HIGH|MEDIUM|LOW
  summary:
  findings:
    - issue_or_strength:
      classification: CANON_FACT|TEXT_EVIDENCE|INFERENCE|OPTION|UNKNOWN
      severity: FATAL|MAJOR|MEDIUM|POLISH|NONE
      evidence:
      cause:
      reader_or_story_effect:
      recommendation:
      repair_scope:
      regression_risk:
  unanswered_questions:
  dependencies:
```

Agents may use domain-specific fields after this header.

---

# 4. STORY_CORE

```yaml
STORY_CORE:
  title:
  hero:
  want:
  why_now:
  opposition:
  wrong_strategy:
  stakes:
  price:
  midpoint:
  low_point:
  climax_choice:
  climax_action:
  resolution:
  permanent_change:
  series_hook_after_resolution:
```

No field may be filled with abstract theme when a concrete dramatic answer is required.

---

# 5. CHARACTER_ENGINE

```yaml
CHARACTER_ENGINE:
  name:
  age:
  external_goal:
  private_desire:
  fear:
  shame:
  strength:
  flaw:
  contradiction:
  defensive_strategy:
  ordinary_life:
  family_pressure:
  peer_pressure:
  work_school_money:
  moral_boundary:
  line_they_may_cross:
  lie_to_self:
  book_price:
  book_change:
  unresolved_saga_pressure:
  voice_cognition:
```

---

# 6. RELATIONSHIP_EDGE

```yaml
RELATIONSHIP_EDGE:
  a:
  b:
  type: FRIENDSHIP|LOVE|FAMILY|RIVALRY|MENTOR|DUTY|FEAR|DEPENDENCY
  a_wants:
  b_wants:
  attraction_or_respect:
  resentment_or_fear:
  status_asymmetry:
  secret:
  boundary:
  rupture_condition:
  repair_condition:
  start_state:
  midpoint_state:
  end_state:
```

---

# 7. MYSTERY_LEDGER

```yaml
MYSTERY_LEDGER:
  question:
  truth_status: KNOWN_TO_AUTHOR|WORKING|UNKNOWN_BY_DESIGN
  initial_model:
  clues:
    - clue:
      location:
      visibility:
      immediate_interpretation:
      false_interpretation:
      actual_meaning:
      action_caused:
      payoff:
  partial_answers:
  false_hypotheses:
  allowed_open_question:
  forbidden_premature_reveal:
```

---

# 8. CONTINUITY_LEDGER

```yaml
CONTINUITY_LEDGER:
  timeline:
    - date_time:
      event:
      participants:
      consequence:
  character_knowledge:
    - character:
      fact:
      source:
      learned_when:
      false_version_if_any:
  relationship_state:
  injuries:
  objects:
  technology_state:
  institution_state:
  unresolved_setups:
  contradictions:
    - description:
      label: HARD_CONTRADICTION|SOFT_CONTRADICTION|POSSIBLE_RETCON|INTENTIONAL_MYSTERY|UNKNOWN
      required_action:
```

---

# 9. CHAPTER_CARD

```yaml
CHAPTER_CARD:
  chapter:
  title:
  pov:
  date_time:
  entering_state:
  immediate_want:
  obstacle:
  chapter_function:
  key_actions:
  new_information:
  turn:
  price:
  relationship_delta:
  knowledge_delta:
  institutional_or_world_delta:
  setup_used:
  payoff_created:
  exit_state:
  exit_pull:
  forbidden_inventions:
```

---

# 10. SCENE_CARD

```yaml
SCENE_CARD:
  scene_id:
  pov:
  date_time:
  place:
  who_wants_what:
  why_now:
  obstacle:
  first_tactic:
  countermove:
  escalation:
  unexpected_information:
  choice:
  action:
  turn:
  price:
  relationship_delta:
  knowledge_delta:
  resource_or_status_delta:
  setup_used:
  payoff_created:
  exit_condition:
  forbidden_inventions:
```

---

# 11. GREENLIGHT_DECISION

```yaml
GREENLIGHT_DECISION:
  gate:
  verdict: GREEN|YELLOW|RED
  blocking_issues:
  nonblocking_issues:
  protected_strengths:
  conditions_to_advance:
  writer_authorized: true|false
```

---

# 12. INTEGRATED_DECISION

```yaml
INTEGRATED_DECISION:
  decision_id:
  issue:
  positions:
    - source_agent:
      recommendation:
      evidence:
      cost:
  priority_rule_applied:
  decision:
  reason:
  rejected_options:
  regression_risk:
  validation_test:
  canon_effect: NONE|WORKING|REQUIRES_FOUNDER_APPROVAL
```

---

# 13. WRITER_BRIEF

The Primary Writer receives this, not the raw committee reports.

```yaml
WRITER_BRIEF:
  target:
  purpose:
  pov:
  entering_state:
  must_preserve:
  must_change:
  causal_turns:
  character_requirements:
  relationship_requirements:
  world_system_requirements:
  continuity_locks:
  setup_payoff_requirements:
  forbidden_inventions:
  desired_exit_state:
  prose_constraints:
  acceptance_tests:
```

A Writer Brief should be compact enough to write from.

---

# 14. MANUSCRIPT_PATCH

```yaml
MANUSCRIPT_PATCH:
  target_version:
  range:
  prose_or_scene_text:
  self_check:
    brief_satisfied:
    new_canon_introduced: true|false
    continuity_uncertainty:
    factual_verification_needed:
```

---

# 15. RED_TEAM_REPORT

```yaml
RED_TEAM_REPORT:
  verdict: PASS|PASS_WITH_REWRITE|STRUCTURAL_REWRITE|REBUILD
  fatal:
  major:
  medium:
  polish:
  close_the_book_risks:
  protected_strengths:
  false_alarms:
```

For each issue:

`SYMPTOM -> EVIDENCE -> CAUSE -> READER EFFECT -> REPAIR CLASS`.

---

# 16. REVISION_PLAN

```yaml
REVISION_PLAN:
  source_red_team:
  approved_issues:
    - issue:
      level: L1|L2|L3|L4|L5
      preserve:
      change:
      reason:
      scope:
      dependencies:
      expected_effect:
      regression_risk:
      validation:
  rejected_recommendations:
```

---

# 17. PATCH_INSTRUCTION

```yaml
PATCH_INSTRUCTION:
  location:
  problem:
  preserve:
  change:
  do_not_change:
  desired_reader_effect:
  continuity_locks:
  verification:
```

---

# 18. READER_REPORT

```yaml
READER_REPORT:
  reader_segment:
  first_curiosity:
  first_boredom:
  first_confusion:
  stop_or_skim_point:
  most_interesting_character:
  emotional_wait:
  expected_payoff:
  payoff_received:
  wonder_points:
  homework_points:
  next_chapter_desire: YES|MAYBE|NO
  next_book_desire: YES|MAYBE|NO
  classification: CONSENSUS_FAILURE|SEGMENT_ISSUE|PERSONAL_TASTE|INTENTIONAL_FRICTION
```

---

# 19. REGRESSION_REPORT

```yaml
REGRESSION_REPORT:
  patch_id:
  original_problem:
  solved: YES|PARTIAL|NO
  new_causality_issue:
  new_character_issue:
  new_voice_issue:
  new_continuity_issue:
  new_pacing_issue:
  setup_payoff_changed:
  local_story_still_closes:
  series_hook_still_secondary:
  verdict: PASS|PARTIAL|REGRESSION
```

---

# 20. LOCK_DECISION

```yaml
LOCK_DECISION:
  book:
  version:
  status: DEVELOPMENT_LOCKED|CANON_LOCKED|EXTERNAL_FEEDBACK
  story_gate:
  unresolved_nonblocking_threads:
  allowed_future_hooks:
  prohibited_reopens:
  reopen_conditions:
  inherited_consequences_for_next_book:
```

---

# 21. DECISION_LOG ENTRY

```yaml
DECISION_LOG:
  date:
  founder_instruction:
  affected_book_or_system:
  previous_state:
  new_decision:
  status: CANON|WORKING|OPTION|SUPERSEDED|REJECTED
  files_affected:
  downstream_consequences:
```

---

# 22. BOOK_STUDIO_REPORT

```yaml
BOOK_STUDIO_REPORT:
  manuscript_version:
  development_locked: true|false
  reader_validation:
  acquisition_positioning:
  word_count_risk:
  genre_category:
  query_status:
  synopsis_status:
  copyedit_status:
  continuity_status:
  audio_status:
  screen_status:
  reopen_story_recommended: true|false
  evidence_for_reopen:
```

---

# FINAL SCHEMA LAW

Schemas serve decisions. Do not fill fields mechanically when they are irrelevant.

Do not omit a required causal/character field merely to keep the report short.
