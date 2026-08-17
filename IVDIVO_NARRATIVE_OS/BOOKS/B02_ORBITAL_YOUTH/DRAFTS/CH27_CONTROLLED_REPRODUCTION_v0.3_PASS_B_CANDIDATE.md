# ORBITAL YOUTH

## Chapter 27 — CONTROLLED REPRODUCTION

Ollie was allowed into Test Rig Four because Test Rig Four was not Ring Six.

His temporary band made the distinction once, clearly enough.

TEST RIG 4 — OBSERVER / ANALYSIS PARTICIPANT.

RING SIX COMMISSIONING — REVIEW HOLD UNCHANGED.

Ren read the second line over Ollie’s shoulder.

“They know you.”

“I know what the scope is.”

“Emotionally?”

“That is not a scope category.”

Ren handed him a service pouch.

“Good. Carry this.”

“The rig window opens in twenty-seven minutes.”

“This panel exists now.”

The last ordinary maintenance ticket before the test was a differential panel with a stiff latch.

Ollie reached for the hinge.

Ren said, “Ticket it.”

Ollie logged the latch instead of fixing something outside the task.

The differential passed.

Ren closed the housing.

“Done.”

Twenty-two minutes remained.

They reached the transfer spine together. Ren continued toward filter inventory; Ollie turned toward the rig.

“Good luck,” Ren called.

“With what?”

“Not touching anything.”

Ollie kept walking.

* * *

Test Rig Four was less impressive than Ring Six and more useful for today.

Its environmental loop was real hardware, but nobody lived in the spaces it served. One side held instrumented air paths, pressure buffers and controllable service-door loads. The other was an equipment volume designed to behave badly under controlled conditions.

If Ollie was wrong, nobody had to be evacuated.

A transparent wall separated the observer desk from the main console.

Ollie’s band opened the observer desk.

It did not open control.

He tested that once.

CONTROL AUTHORITY — NOT ASSIGNED.

Mara saw.

“You needed the interface to agree with the band?”

“I prefer failures that are explicit.”

A test engineer at the main console looked over.

“Is he always like this?”

“Sometimes more,” Mara said.

The engineer gave Ollie the rules instead of a biography.

“Hard stop at twelve percent deviation from rig baseline. Unexpected cross-loop rise outside the registered envelope, we abort. Predictions lock before each run. You do not touch control, revise a prediction after the run begins or ask me to try one extra thing.”

“Understood.”

Iri arrived with the percussion-frame clamp that had been travelling between work and rehearsal all week.

They took the empty observer seat and opened the run list.

RUN N0 — FULL BASELINE / ORDINARY SERVICE TRANSITION.

RUN C1 — RETURN CORRECTION WITH RESIDUAL SETTLING / PERMITTED SERVICE LOAD.

RUN C2 — APPARENTLY EQUIVALENT VISIBLE SEQUENCE AFTER FULL PHYSICAL BASELINE.

RUN C3 — RESERVED PENDING C1/C2 RESULT.

Iri pointed at C1.

“Residual settling?”

Ollie opened the preregistered range.

“Return paths inside occupied tolerance but still two to five percent off aggregate pre-transition balance.”

“Why two to five?”

“Below two, ordinary noise eats the separation. Above five, we leave the safe bounded range we are trying to reproduce.”

“And C2?”

“Same visible sequence labels. Full physical baseline first.”

Iri traced the two definitions.

“So controller-closed is not enough to call C2 baseline.”

“Correct.”

That was the question they had come for.

Iri checked the time.

“I have rehearsal.”

“N0 starts in eight minutes.”

“Yes.”

“You could stay for the boring run.”

“That is an excellent advertisement.”

They stood.

Before leaving, Iri tapped the preregistration.

“Do not move baseline after you see the result.”

Ollie left the file locked.

Iri went to rehearsal.

The test engineer glanced at the door.

“Relationship workshop over?”

“Control run,” Mara said.

* * *

N0 was exactly as boring as Ollie had hoped.

The rig returned to full physical baseline.

Not controller-closed.

Baseline.

A2 and A3 return paths sat within half a percent of their pre-run state. Buffer neutral. No residual correction demand.

The engineer ran an ordinary service-door transition with a short hold.

Local air curtain compensated. Return balance moved. The shared-loop estimator stayed below the preregistered entry threshold. Fixed display followed normally.

No coupled state.

The engineer ended the run.

“N0?”

“Predicted no candidate entry. No entry observed.”

She saved the result and reset.

Ollie watched the traces settle.

He wanted C1 sooner and kept the want to himself.

“You can blink during reset,” the engineer said.

“I am blinking.”

“Statistically, perhaps.”

C1 began nine minutes later.

A low-amplitude return correction shifted A2 and A3 against each other. The formal controller event closed while the physical return pair continued settling inside the preregistered two-to-five-percent residual window.

The control display changed:

CORRECTION CLOSED.

The physical traces were not at baseline.

At 3.1 percent aggregate imbalance the engineer called the C1 state window valid.

Mara asked, “Prediction?”

“Permitted service transition during residual recovery enters the candidate shared-loop relationship without exceeding the abort envelope.”

“Dangerous oscillation?”

“Not predicted or tested.”

The engineer opened the permitted service load.

One simulated access door held.

The local buffer compensated.

A2 recovery slowed. A3 compensation rose.

The shared-loop estimator crossed the preregistered threshold.

CANDIDATE STATE ENTRY — YES.

The fixed display updated 3.8 seconds later.

Then the rig recovered cleanly.

No oscillation. No runaway correction. No alarm.

The engineer ended the run.

Ollie’s pulse was more dramatic than the data.

“Interpretation,” Mara said.

“C1 reproduced the candidate state relationship at low amplitude. A visible sequence outside the original partition-overlap family can enter the same control-state relationship when residual recovery is present.”

He stopped there.

The engineer saved the run.

No dangerous incident mechanism had been reproduced.

Reset began.

C1 had worked.

Ollie allowed himself forty seconds of satisfaction before remembering C2.

* * *

C2 looked almost identical on the visible run list.

That was deliberate.

The rig executed the same initial correction. The controller closed it.

This time the team waited.

A2 returned.

A3 returned.

Buffer neutralized.

Physical baseline reached.

RETURN CORRECTION — CLOSED.

SERVICE TRANSITION — READY.

LOCAL BUFFER — NORMAL.

The preregistration said:

C2 — EXPECT STATE ENTRY.

The engineer looked at Ollie.

“Still yes?”

“Yes.”

She ran the service transition.

The access door held. The local buffer compensated. Return demand shifted.

The estimator rose.

Stopped below threshold.

A2 corrected. A3 followed. Fixed display updated normally.

No candidate state entry.

The engineer waited ten more seconds.

Nothing changed.

RUN C2 — NO CANDIDATE STATE ENTRY.

Ollie’s first thought was that C2 was not equivalent because the starting state differed.

True.

Also exactly the sort of sentence that could rescue a failed model after the fact.

He left it unspoken.

“Prediction?” the engineer asked.

“State entry.”

“Result?”

“No entry.”

“Interpretation?”

Ollie looked at the locked preregistration.

“Model too broad.”

Nobody rewarded him for saying it.

Good.

He overlaid C1 and C2.

The visible service labels were almost the same.

The difference sat before them.

C1 started with the return pair still inside ordinary residual settling.

C2 started from full physical baseline.

The controller had said CORRECTION CLOSED in both cases.

The air had not meant the same thing.

Ollie enlarged the return traces and created a derived variable.

RETURN RECOVERY STATE.

He deleted it.

Too vague.

RESIDUAL RETURN IMBALANCE.

The engineer glanced over.

“That is measurable.”

Ollie aligned N0, C1 and C2 by physical state instead of only by controller closure.

N0 and C2 now looked like two negative cases rather than one control and one embarrassing exception.

“C1 is candidate evidence for service transition plus residual return state,” he said. “Not for service-transition equivalence alone.”

“Candidate,” the engineer said.

“Candidate.”

Mara asked, “What would damage that?”

“Repeat the residual window and fail under the registered condition.”

One run would not settle the general question. But one remaining run today could decide whether C1 deserved to guide the next test phase.

Thirty-one minutes, reset included.

Ollie opened C3.

Repeating C1 exactly would test simple repeatability.

He chose something harder.

RESIDUAL RETURN IMBALANCE: 2.5–4.0%.

SERVICE ROUTE: DIFFERENT PERMITTED LOAD PATH.

LOCAL BUFFER: SAME SHARED LOOP / DIFFERENT VISIBLE DEVICE SEQUENCE.

Mara read it.

“Why change the visible route?”

“If one exact service device is required, we are still naming hardware instead of state.”

The engineer checked the rig map.

“Path D can do it inside the same abort envelope.”

C3 locked as:

EXPECT CANDIDATE SHARED-LOOP ENTRY ONLY IF RESIDUAL RETURN IMBALANCE IS WITHIN PREREGISTERED WINDOW.

ALTERNATE VISIBLE SERVICE PATH.

NO PREDICTION OF DANGEROUS OSCILLATION.

Once the engineer locked it, Ollie could no longer improve the answer after seeing the result.

That helped.

* * *

Reset took eleven minutes.

Ollie used nine to eat something from the test-room vending unit.

It was bad.

Mara ate the same thing without complaint.

“That does not make it acceptable,” Ollie said.

“The food?”

“Yes.”

“I have eaten bad food before.”

“That is not a quality standard.”

The engineer looked up from C3 setup.

“Please keep debating food. It is the safest variable in the room.”

Ollie’s band vibrated.

IRI: rehearsal break. did you break physics yet

He typed:

OLLIE: C1 entered state. C2 failed.

Then remembered the result package was still review-owned and deleted it.

OLLIE: test in progress. authorized summary later.

IRI: disgusting growth

C3 reached baseline.

The initial correction was slightly smaller than C1.

Controller closed.

Physical return pair remained offset.

3.4 percent.

Inside the preregistered residual window.

“C3 entry condition valid,” the engineer said.

“Prediction?” Mara asked.

“Candidate state entry through alternate permitted service path.”

Path D opened.

Different service door. Different buffer controller. Same adaptive return pair beneath them.

The first trace rose.

The second moved against it.

The shared-loop estimator crossed threshold.

CANDIDATE STATE ENTRY — YES.

Fixed display updated 4.1 seconds later.

The rig recovered.

No oscillation. No abort.

Nobody moved until the traces returned to baseline.

Then Mara said, “Result.”

Ollie looked at all four runs.

“Safe-amplitude distributed equivalence reproduced under two visible service paths when the shared return loop began inside the preregistered residual-recovery window. C2 did not enter from full physical baseline.”

“Dangerous oscillation?” the engineer asked.

“Not reproduced.”

“Human or support timing?”

“Not tested.”

“Ring Six clearance?” Mara asked.

“No.”

The answer came easily.

The engineer saved N0, C1, C2 and C3 in the same result package.

C2 stayed in the main result.

Ollie noticed and left it there.

* * *

The debrief happened standing because the next team was waiting outside with equipment cases.

The engineer put the preliminary result on the wall.

PHASE 1 — CONTROL-STATE REPRODUCTION.

N0: NEGATIVE CONTROL — NO ENTRY.

C1: CANDIDATE — ENTRY.

C2: EXPECTED ENTRY — NO ENTRY.

C3: NARROWED CANDIDATE — ENTRY.

She added:

RESIDUAL RETURN IMBALANCE / RECOVERY STATE REQUIRED FOR CURRENT RIG REPRODUCTION — CANDIDATE NECESSARY CONDITION, NOT SUFFICIENT CAUSE OF INCIDENT ESCALATION.

Ollie read it.

“Required is too strong.”

The engineer waited.

“Required for the successful reproductions under today’s tested conditions.”

She changed the line.

The next question was operational.

The simplest control direction was obvious: wait for deeper physical return recovery instead of trusting controller closure before permitting certain service combinations.

Mara asked for cost.

The engineer pulled up cycle timing.

Enough waiting to matter in an occupied ring.

At peak occupancy it reduced flexibility, lengthened service queues, increased some door holds and compressed maintenance windows.

The other direction preserved more capacity: estimate residual recovery state in real time and inhibit only combinations entering the candidate shared-loop window.

More selective.

More model dependence.

And the model still did not explain escalation or resident/support timing.

Mara put both on the debrief.

FULL-RECOVERY INTERLOCK.

STATE-AWARE CONTROL DEVELOPMENT.

NO RECOMMENDATION YET.

Ollie looked at C2 before looking at the second option again.

The failed run was still there.

The test engineer cleared observer access.

TEST RIG 4 — SESSION COMPLETE.

RING SIX COMMISSIONING — REVIEW HOLD UNCHANGED.

Ollie read the second line once and followed Mara out because the next team needed the room.

* * *

Iri’s rehearsal was ending when the authorized summary cleared.

Ollie sent only the released result.

PHASE 1: SAFE-AMPLITUDE DISTRIBUTED EQUIVALENCE REPRODUCED UNDER TWO VISIBLE SERVICE PATHS WHEN RESIDUAL RETURN RECOVERY STATE PRESENT.

ONE APPARENTLY EQUIVALENT RUN FROM FULL PHYSICAL BASELINE DID NOT ENTER STATE.

NO DANGEROUS OSCILLATION REPRODUCED.

NO HUMAN / SUPPORT TIMING TESTED.

Five minutes later:

IRI: C2 stayed in main result?

OLLIE: yes

IRI: good

OLLIE: two operational directions now

IRI: train in 4 minutes

Ollie started typing the options anyway.

Then deleted them.

The options would exist tomorrow.

A separate maker-team message from Earth waited underneath.

JUNE: we broke the rover bracket again. not urgent. when free tell me why our fix is stupid

Ollie read it.

His transfer home arrived.

He put the band away.

The bracket could wait until tomorrow too.
