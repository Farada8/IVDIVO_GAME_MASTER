# BOOK INTELLIGENCE ENGINE — TARGETED SOURCE PASS
## ITU-R BS.1116-3 — SUBJECTIVE AUDIO TEST METHODOLOGY

**Date:** 2026-08-22  
**Source ID:** `OPEN-ITU-BS1116-3`  
**Source:** Recommendation ITU-R BS.1116-3, *Methods for the subjective assessment of small impairments in audio systems*  
**Official source:** ITU Recommendation page / official PDF  
**Rights:** ACCESS_ONLY / ITU copyrighted publication; do not redistribute raw source through GitHub  
**Integrity:** VERIFIED official source  
**Read coverage:** PARTIAL_TARGETED  
**Extraction stage:** MECHANISMS_EXTRACTED  
**FULL_READ:** false

## Why this source was opened
D04 `SEVEN NIGHTS BEFORE CODE BLUE` already had a real blind-listener packet for the NORMAL TRANSFER vs SECOND TRANSFER cue. The packet was about to be used as human evidence, so the decision could materially change based on listening-test design quality.

This pass asks one bounded question:

`CAN THE CURRENT D04 BLIND A/B PROCEDURE SUPPORT ITS CLAIM OF RELIABLE HUMAN RECOGNITION?`

## Located claims used

### ITU-C01 — presentation order is a confound if not controlled
**Locator:** Annex 1, §2 Experimental design, official PDF pp. 3–4.

Mechanism-level paraphrase: if all subjects receive the same sequence, judgements may be partly caused by order rather than the intended experimental factor. Test conditions should therefore control/order-randomize presentation so the independent factor is what is being measured.

### ITU-C02 — listener-panel size limits the strength/generalizability of conclusions
**Locator:** Annex 1, §3.3 Size of listening panel, official PDF p. 5.

Mechanism-level paraphrase: adequate panel size depends on variance and required resolution; under tightly controlled conditions, substantially more than one listener is normally used for formal conclusions. A small internal screen must therefore be labelled as a small internal screen rather than a standards-grade perceptual validation.

### ITU-C03 — blinded test-object assignment should vary by trial
**Locator:** Annex 1, §4 Test method, official PDF p. 6.

Mechanism-level paraphrase: the recommended small-impairment method uses hidden/random assignment of the test object and reference across trials. For D04 we do not copy the exact BS.1116 method, but we adopt the bias-control principle: A/B identity must not be predictable from fixed labels or a fixed modality sequence.

### ITU-C04 — listening level / alignment is a controlled variable
**Locator:** Annex 1, §8.4 Listening level, official PDF pp. 17–18; programme level guidance in §6.

Mechanism-level paraphrase: reproduced level is part of the test condition and should be controlled/reported. D04 therefore must not let listeners change volume separately to hunt for the extra cue.

### ITU-C05 — subjective conclusions are statistical and must state their evidence limits
**Locator:** Annex 1, §10.4 and §11, official PDF pp. 23–24.

Mechanism-level paraphrase: subjective results require explicit treatment of significance/confidence and sufficiently detailed reporting for critique/replication. D04's small-N production screen cannot claim formal statistical validity.

## Extracted mechanisms

### BI-ITU-M01 — ORDER_COUNTERBALANCE
For a multi-condition perceptual screen, vary modality order across independent listeners and vary which physical item receives the visible A/B label. Do not allow one fixed sequence to become a hidden experimental factor.

### BI-ITU-M02 — REPLICATE_BEFORE_RELIABLE
One forced-choice response from one listener is evidence of one response, not reliable recognition. Reliability language requires independent replication appropriate to the production decision.

### BI-ITU-M03 — FIX_LEVEL_WITHIN_SESSION
Set a comfortable playback level before the scored trials and keep it fixed within that listener's session. Record device/path; do not allow per-trial volume hunting to become the cue.

### BI-ITU-M04 — EVIDENCE_SCOPE_LABEL
A lightweight production screen may be useful without pretending to be a formal standards-conformant listening experiment. Label the result `INTERNAL_REPLICATED_SCREEN`, not `ITU_VALIDATED`, unless the actual standard method/panel/statistics are performed.

## Applicability boundary

This source pass **does not claim**:
- that D04 is or will be compliant with BS.1116-3;
- that three internal listeners equal the formal panel guidance in the Recommendation;
- that A/B discriminability proves artistic quality;
- that machine metrics prove perception;
- that a human screen replaces provider, cast or release evidence.

It only supplies bias-control and evidence-scope mechanisms for the current production gate.

## D04 pre-change diagnosis

Current v1 packet had three important weaknesses:
1. one listener could produce the entire `HUMAN PASS`;
2. STEREO → MONO → PHONE order was fixed, so later responses could be influenced by learning from earlier formats;
3. forced `A_or_B` gave no explicit `CAN'T_TELL`, making guessing indistinguishable from perceived discriminability.

The v1 packet also used the phrase `reliable recognition`, which exceeded the evidence produced by one three-choice session.

## Disposition

`SOURCE = VERIFIED / PARTIAL_TARGETED / MECHANISMS_EXTRACTED / NOT_FULL_READ`

`D04 BLIND PROTOCOL v1 = METHODologically INSUFFICIENT FOR RELIABLE_HUMAN_PASS CLAIM`

Next action: create a counterbalanced, replicated internal production screen that preserves the existing WAV assets and keeps the formal human/perceptual claim scoped correctly.