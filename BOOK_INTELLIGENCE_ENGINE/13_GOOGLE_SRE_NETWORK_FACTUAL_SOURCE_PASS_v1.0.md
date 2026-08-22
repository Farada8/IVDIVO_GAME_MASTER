# BOOK INTELLIGENCE ENGINE — TARGETED SOURCE PASS
## Google SRE → B03 relay/failover factual hold

**Date:** 2026-08-22  
**Source ID:** `OPEN-GOOGLE-SRE-HUB`  
**Source:** official Google SRE book pages, especially *Addressing Cascading Failures* and *Managing Critical State: Distributed Consensus for Reliability*  
**License/access:** official Google SRE book; CC BY-NC-ND 4.0 indicated by official book portal  
**Source state:** `VERIFIED / PARTIAL_TARGETED / MECHANISMS_EXTRACTED / FULL_READ=false`  
**Target:** B03 / SMITH I / THE EMPTY RESCUE — P72 M2 network/relay terminology hold.

## Decision
Question: do current CH23–29 relay/failover/segmentation terms contain a concrete factual defect requiring minimal repair before factual lock?

Current manuscript authority inspected:
- CH23 `52_B03 — MANUSCRIPT CH23 — FAILOVER v0.1` / Drive `13khiS1NdVndiGNDqQiHY_TRlhsiLme2HRY-2C3-7Zr0`;
- CH24 `54_B03 — MANUSCRIPT CH24 — GO TO THE RELAY v0.1` / Drive `1r4kteDwkxb5LnQ5pPj2zTtrexCMN-gdzdq_dl6FPCzA`;
- CH26 `59_B03 — MANUSCRIPT CH26 — THE RELAY v0.2` / Drive `1Q_1QM5Y5SExp6clbk_EJW9J6m5T_Gjec4Uuux0njCPY`;
- CH27 `61_B03 — MANUSCRIPT CH27 — THE BEST WARNING YET v0.2` / Drive `18bdNCKq1FaT1lrAreL1ec5VMuyDLWeU3L6UlHfeIWwo`;
- CH28 `63_B03 — MANUSCRIPT CH28 — THE THIRD ROUTE v0.1` / Drive `1EzrMOjPldszs-iEl3pCUuEKnyN17yUniMvnDrZWIExw`;
- CH29 `65_B03 — MANUSCRIPT CH29 — WHAT WE DID WITH THE WARNING v0.1` / Drive `1LZPRkR89wAkdcWJqUOv6dYdUUSimtDm3b1PpxEUydpM`.

## Source claims
### SRE-NET-C01 — Failover can concentrate load and reduce failure-domain diversity
**Locator:** Google SRE, *Addressing Cascading Failures*, Server Overload / triggering and recovery discussion.  
Failure or removal of one serving path can push work onto remaining paths; automated balancing/retry/failover can amplify load and contribute to cascading failure. Capacity and failure-domain effects must be considered.

### SRE-NET-C02 — Degraded modes should preserve useful work while shedding nonessential load
**Locator:** Google SRE, *Addressing Cascading Failures*, Load Shedding and Graceful Degradation; *Production Services Best Practices*.  
A robust system can deliberately reduce less important work while retaining critical service rather than treating availability as all-or-nothing.

### SRE-NET-C03 — Redundancy does not eliminate network-partition/failover risk
**Locator:** Google SRE, *Managing Critical State*, placement/redundancy/failover discussion.  
Redundancy and failover improve availability only within capacity/topology constraints; failover may cause abrupt traffic redistribution and create new risk.

### SRE-NET-C04 — Shared network path does not itself synchronize clocks
**Locator:** Google SRE, *Managing Critical State*, timestamps/clock drift discussion; RFC 5905 NTP specification for clock synchronization.  
Distributed clocks can drift. Clock synchronization requires a time-synchronization mechanism; routing several application feeds over one fallback path does not by itself place them on “one clock”.

## Mechanisms
### BI-SRE-NET-M01 — FAILOVER_CHANGES_FAILURE_DOMAIN_AND_LOAD
When redundancy moves traffic onto fewer shared paths, record both availability benefit and changed load/failure-domain exposure.

### BI-SRE-NET-M02 — PRESERVE_CRITICAL_SERVICE_SHED_NONESSENTIAL_STATE
For a fictional/emergency application-control layer, it is technically plausible to preserve priority voice/status while suppressing nonessential mirrored detail, provided this is framed as configured service/application behavior rather than a universal property of networking.

### BI-SRE-NET-M03 — DELIVERY_COHERENCE_NEQ_CLOCK_SYNCHRONIZATION
A more stable/common transport/feed may reduce delayed, duplicated or inconsistently routed updates. It must not be described as synchronizing independent clocks unless a time-sync mechanism is established.

## Current manuscript findings
### PASS — CH23/24/26–29 overall architecture
- automatic failover to a shared fallback path is plausible at story abstraction level;
- increased shared load / reduced path diversity / potential recovery-path risk is explicitly acknowledged;
- CH24/26 distinguish local voice/status from nonessential central mirrors and keep network ownership with Luka/Eva;
- CH26 limits the change, observes results, preserves reversibility and notes that another failure can alter recovery behavior;
- CH27 correctly presents restoring a high-resolution rescue mirror as technically possible but not risk-free;
- CH29 keeps isolated relationships under local engineering review before ordinary restoration.

These are fictional implementation details, not claims that a named real telecom protocol behaves exactly this way. No broad rewrite is justified.

### REPAIR REQUIRED — CH23 clock language
Current CH23 contains three linked statements that overclaim what failover itself can do:
1. `Cleaner timestamp consistency.`
2. `Hydro control’s engineering channel and lower-service status sat on the same clock.`
3. `...given hydro one clock.`

A shared fallback path can plausibly improve delivery consistency and reduce delayed/duplicated updates, but it does not itself synchronize clocks. These three lines require a minimal terminology repair only.

## Authorized minimal repair
Preserve story function — improved regional visibility after failover — while removing unsupported clock-sync causality:
1. `Less packet loss. Fewer delayed or duplicated updates.`
2. replace the “same clock” clause with a statement that both streams appear in the same regional event feed;
3. replace “given hydro one clock” with reliable regional feed/status wording.

No CH24/26/27/28/29 prose change is authorized by this source pass unless readback after CH23 repair exposes a dependent contradiction.

## Evidence boundary
This is a targeted factual/technical source pass, not a FULL_READ of Google SRE and not a telecom certification. It can close the specific terminology defect only after:
`SOURCE -> CLAIM -> MECHANISM -> STORY ADAPTER -> CURRENT CH23 REPAIR -> READBACK -> CH23-29 DEPENDENCY REGRESSION -> FACTUAL HOLD DISPOSITION`.
