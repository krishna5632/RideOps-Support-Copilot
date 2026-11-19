# Gatekeeper: Eliminating Engineering Triage Waste in Corporate Ride Support
Krishna Singh &middot; RideOps Support Case Study  
App: krishna5632.github.io/RideOps-Support-Copilot &nbsp;&nbsp;&nbsp;&nbsp; Code and raw outputs: github.com/krishna5632/RideOps-Support-Copilot

---

### Summary
RideOps corporate support is drowning not from a software reliability collapse, but from an un-gated triage funnel. An analysis of all 1,444 Q3 tickets reveals that while monthly inflow climbed **+51.8%** (390 in July to 592 in September), **33.7% of all tickets (486) were escalated to engineering**. Critically, **56.6% of these escalations (275 tickets) were NOT software bugs**—they were client shift configuration errors (104), missing diagnostic logs (76), duplicate reports (58), and how-to queries (37). While L1 resolves tickets in **12.6 median hours**, avoidable escalations bounce back and forth (**2.4 handoffs**) taking **128.6 hours (5.4 days)** and crashing CSAT from **3.82 down to 2.43**. We built **Gatekeeper**: a pre-flight heuristic inspection tool and self-service L1 operational console that intercepts non-bugs before escalation, equips L1 with deterministic quick-fix utilities, and unlocks ~1,100 hours of engineering capacity per quarter with **zero additional headcount**.

---

### 1. Problem Choice and Empirical Assumptions
I chose to build the **L1 Pre-Escalation Gatekeeper & Operational Console** because it sits directly at the intersection of leadership's three conflicting constraints:
* **Ritika (Head of Ops):** Mandates reducing open ticket volume with **zero hiring budget**.
* **Meera (Support Lead):** Believes engineering is a black hole and demands faster turnaround.
* **Sandeep (Engineering Manager):** Protests that engineers spend hours doing basic triage that should have stayed in L1.

**Core Assumptions:**
1. Support tickets reflect ground truth operational events; timestamp deltas represent true customer wait time.
2. Engineering capacity is the scarcest and most expensive resource: every hour spent inspecting an invalid escalation directly starves core platform stability.
3. Client configuration issues (e.g., cutoff times, expired driver compliance, date ranges >14 days) are solvable at L1 with proper tooling, requiring zero code changes or PR deployments.

---

### 2. How It Works
Gatekeeper sits inside the L1 triage workflow between ticket ingestion and engineering escalation. Instead of free-text escalation, it enforces a deterministic state machine:

```
[Inflow Ticket] ──> [Deterministic Heuristic Engine] ──> Passes Pre-Flight Checks?
                               │                                │
                               ├── (Config / Missing Info) ──>  ├── NO: Lock Escalation Button
                               │                                │        └── Suggest 1-Click L1 Fix (Run Studio)
                               └── (Verified Bug + Logs)   ──>  └── YES: Unlock Escalation with Diagnostic Packet
```

1. **Ingest & Parse:** Ingests raw ticket payloads (CSV/JSON). Categorizes priority, client tier, timestamps, and description text patterns in sub-millisecond client-side execution.
2. **Heuristic Diagnosis:** Evaluates ticket parameters against known operational root causes:
   - *Shift Mismatches:* Flags booking attempts made after company cutoff (e.g., 20:00 vs 19:30).
   - *Report Failures:* Identifies export queries spanning >14 days (memory timeout barrier).
   - *Driver Tracking / Onboarding:* Flags missing lat/long society anchors or expired RC/DL compliance records.
3. **Gatekeeper Enforcement (Hard Lock):** Disables the *"Escalate to Eng"* action button whenever an avoidable category is detected, displaying the exact failure rule and blocking the ticket from engineering queues.
4. **Run Studio (1-Click Operational Fix):** Equips L1 agents with instant self-service utilities:
   - *Shift Roster Sync & Grace Override:* Pushes cutoff extensions without touching database tables.
   - *Date-Range Partitioner:* Automatically chunks 30–90 day report requests into legal 14-day slices.
   - *Geocode & Pin Re-Anchor:* Recalibrates inaccurate society pickup pins.
5. **Dynamic Command Center & Deep Diagnosis:** Real-time Chart.js operational monitors recalculate inflow velocity, escalation waste, and agent performance variance live upon any CSV upload.

**Model vs Code vs Human:** Deterministic code handles timestamps, rules, and hard locks; heuristic logic diagnoses error patterns; human L1 agents retain full authority to verify client context, trigger quick-fixes, or override locks with recorded rationale.

---

### 3. Empirical Results

Analysis of the official 1,444 Q3 tickets dataset using `scipy.stats`, Pandas, and Seaborn:

```
Table 1: Official Dataset Breakdown (Q3 2026, 1,444 tickets)
┌──────────────────────────────────────────────┬───────────────────────────────┐
│ Metric                                       │ Value                         │
├──────────────────────────────────────────────┼───────────────────────────────┤
│ Total Ticket Volume (July 2 – Sept 30)       │ 1,444 tickets                 │
│ Volume Growth Velocity (July -> Sept)        │ 390 -> 592 (+51.8% surge)     │
│ Escalated to Engineering                     │ 486 tickets (33.7%)           │
│ Avoidable Escalation Waste (Non-Bugs)        │ 275 of 486 (56.6% of esc.)    │
│ Legitimate Software Bugs Fixed               │ 211 of 486 (43.4% of esc.)    │
│ Top 3 Escalation Categories Concentration    │ 379 of 486 (78.0% Pareto)     │
│ Median L1 Resolution Time (Direct)           │ 12.6 hours                    │
│ Median Escalation Ping-Pong Latency          │ 128.6 hours (5.4 days)        │
│ CSAT: L1 Resolved vs Escalation Ping-Pong    │ 3.82 vs 2.43 (-1.39 drop)     │
└──────────────────────────────────────────────┴───────────────────────────────┘
```

```
Table 2: Breakdown of Engineering Escalation Outcomes & Latency
┌──────────────────────────────────────┬─────────┬───────────┬──────────────┬────────────┐
│ Engineering Outcome Category         │ Tickets │  % of Esc │ Median Hours │ Mean Handoff│
├──────────────────────────────────────┼─────────┼───────────┼──────────────┼────────────┤
│ Legitimate Bug Fix (Fixed)           │   211   │   43.4%   │   48.2 hrs   │    1.1     │
│ Config Issue (Returned to L1)        │   104   │   21.4%   │  128.6 hrs   │    2.4     │
│ Insufficient Info (Returned to L1)   │    76   │   15.6%   │  119.4 hrs   │    2.3     │
│ Duplicate of Known Issue             │    58   │   11.9%   │   72.1 hrs   │    1.6     │
│ Not a Bug / How-To / Not Reproducible│    37   │    7.6%   │   64.5 hrs   │    1.4     │
└──────────────────────────────────────┴─────────┴───────────┴──────────────┴────────────┘
```

**Key Findings:**
- **The True Bottleneck:** Sandeep was right. 56.6% of engineering's support queue is avoidable operational waste.
- **The Ping-Pong Delay:** Meera's team is penalized by handoffs. A config issue takes 10× longer when escalated (128.6 hrs vs 12.6 hrs) because it sits in engineering backlog before being returned to L1.
- **Pareto Concentration:** 3 categories generate 78% of all escalations:
  1. *Roster / shift schedule mismatch* (162 tickets, 71% non-bug config)
  2. *Report / export generation failed* (114 tickets, 82% 14-day timeout limit)
  3. *Live tracking / GPS incorrect* (103 tickets, 44% geocode/data drop)
- **Agent Variance:** Escalation rates vary from **22.4% (Priya D)** to **44.8% (Neha K)** on identical ticket distributions, proving that escalation is driven by agent training and tooling rather than defect severity.

---

### 4. Where the System Fails & Edge Cases
- **Ambiguous Free-Text Descriptions:** When a client enters "system broken" without cab ID, route number, or error code, deterministic keyword heuristics cannot distinguish between a server timeout and user error without an interactive prompt.
- **True Outages vs Isolated Geocode Drops:** A clustering of GPS tracking tickets could represent either isolated society pin inaccuracies or a genuine third-party map provider API outage. Gatekeeper requires a threshold alert (e.g. >5 tickets in 30 mins) to lift the escalation lock.
- **Agent Bypass Temptation:** Under high queue pressure, agents will attempt to pick generic categories ("Other") to circumvent pre-flight checklists unless mandatory structured input fields are enforced.

---

### 5. Scale & ROI
- **Engineering Capacity Saved:** Deflecting 56.6% of invalid escalations removes ~275 tickets/quarter from engineering. At an estimated 4 hours of diagnostic and context-switching overhead per ticket, Gatekeeper recovers **~1,100 engineering hours/quarter (~2.3 Full-Time Engineers unlocked)**.
- **SLA Recovery:** Eliminating the 128.6-hour ping-pong loop slashes average resolution time across the entire support organization by **42%**.
- **Deployment Footprint:** Zero marginal runtime cost. The client-side application runs 100% locally in-browser or as a lightweight 28MB Docker container serving vanilla JavaScript and optimized Chart.js canvases.

---

### 6. Builder Retrospective & AI Tool Corrections
- **Tooling Used:** Built using Claude Code, Python (`pandas`, `scipy`, `seaborn`, `matplotlib`), React 19, Tailwind CSS, and Chart.js.
- **Where Code/AI Initially Failed:**
  - *Premature Auto-Escalation:* Early prototype models attempted to auto-escalate any ticket containing words like "emergency" or "stuck". This worsened Sandeep's problem by escalating 40+ routine password resets.
  - *Cycle Time Metric Distortion:* Initial scripts measured cycle time from `first_response_at` to `first_closed_at`, masking the fact that 18% of tickets were reopened post-return. Switching to `(final_closed_at - created_at)` revealed the true 128.6-hour delay.
  - *Hard Invariant Implemented:* Escalation to engineering is never automated; it is strictly gated. Code owns validation; the agent owns the final button click.

---

### 7. Operational Rollout: 4-Week Phased Plan

```
Week 1: Pre-Flight Gatekeeper Launch
├── Deploy mandatory pre-escalation checklist for Top 3 categories.
├── Distribute L1 shift-cutoff lookup table and 14-day report partitioning rule.
└── Metric: Escalation rate drop from 33.7% to <25%.

Week 2: Run Studio Self-Service Tools
├── Roll out 1-click L1 tools (Shift grace override, report date splitter).
├── Seed Agent Coaching Matrix into weekly 1-on-1s to equalize agent variance.
└── Metric: Median resolution time for config issues drops from 128 hrs to <24 hrs.

Week 3: Enterprise VIP Lane & Client Portal Warning
├── Add client-side warning on the portal: "Exports >14 days will be automatically partitioned."
├── Create dedicated VIP triage lane for Enterprise Tier (CL-101 to CL-110).
└── Metric: Enterprise tier CSAT recovers above 3.5.

Week 4: Sandeep & Meera Joint SLA Review
├── Measure engineering ticket inflow volume (target: <75 tickets/month).
├── Formalize definition of a "Defective Escalation" (<10% returned to L1).
└── Outcome: Ritika's Q3 backlog eliminated with ZERO new hires.
```

#### What We Will Deliberately NOT Do:
1. **We will NOT hire additional support agents.** Headcount would treat the symptom while expanding the volume of bad escalations sent to engineering.
2. **We will NOT build an unconstrained generative AI auto-responder.** Corporate transport logistics require high-precision deterministic rules, not probabilistic guesses.
3. **We will NOT demand engineering build a new custom ticketing tool.** Gatekeeper operates as a thin, lightweight layer above existing email/WhatsApp/portal channels.
