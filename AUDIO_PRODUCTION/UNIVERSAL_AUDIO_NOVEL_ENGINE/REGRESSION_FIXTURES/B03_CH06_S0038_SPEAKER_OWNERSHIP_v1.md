# Speaker Attribution Regression Fixture — B03 CH06 S0038

**Expected speaker:** `SMITH`  
**Failure class:** `ACTION_RESPONSE_OWNERSHIP_WITH_EXPLICIT_NEXT_SPEAKER_ENTRY`

Context sequence:
1. Nika: `Or easier to blame the operator.`
2. `Smith looked at her.`
3. Target: `Then every escalated decision gets the evidence state and authorizing person logged with it.`
4. `Jana said,`
5. Jana: `Mine included.`

## Rule
The target belongs to Smith. The named action establishes Smith as the responder, while the immediately following explicit `Jana said` marks Jana's later entry. Assigning the target to Jana collapses two distinct ownership signals.

Any future speaker-attribution engine that assigns this segment to Jana fails promotion. UNKNOWN is safer than a contradictory assignment.
