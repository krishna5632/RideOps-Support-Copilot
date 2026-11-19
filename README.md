# Gatekeeper: AI-Powered Support Triage & Pre-Escalation Gatekeeper for RideOps

> **Production operational support copilot that intercepts invalid engineering escalations, equips L1 agents with self-service quick-fixes, and recovers ~1,100 hours of engineering capacity per quarter with zero headcount expansion.**

[![Live Web App](https://img.shields.io/badge/Live_App-Render-2563EB?style=for-the-badge&logo=render)](https://rideops-support-copilot.onrender.com/)
[![Solution Document](https://img.shields.io/badge/Report-3_Page_PDF-0F172A?style=for-the-badge&logo=adobe-acrobat-reader)](docs/Gatekeeper_RideOps_Writeup.pdf)
[![Analysis Suite](https://img.shields.io/badge/Analysis-1%2C444_Tickets_Verified-16A34A?style=for-the-badge&logo=jupyter)](backend/notebooks/rideops_deep_operational_analysis.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

* **Live Studio App:** [https://rideops-support-copilot.onrender.com/](https://rideops-support-copilot.onrender.com/)
* **Official 3-Page Solution Document:** [docs/Gatekeeper_RideOps_Writeup.pdf](docs/Gatekeeper_RideOps_Writeup.pdf) *(source: [docs/RideOps_SnipDeck_Writeup.md](docs/RideOps_SnipDeck_Writeup.md))*
* **GitHub Repository:** [https://github.com/krishna5632/RideOps-Support-Copilot](https://github.com/krishna5632/RideOps-Support-Copilot)
* **Author:** Krishna Singh &middot; Built for the RideOps Corporate Support Case Study (72-Hour Working Build).

---

## 1. What Gatekeeper Does (In Simple Words)

RideOps runs employee commute logistics for ~200 corporate enterprises (managing cab bookings, shift rosters, live tracking, boarding OTPs, and billing). When employee transport fails, corporate admins raise urgent support tickets.

In Q3 2026, monthly ticket inflow surged **+51.8%** (from 390 in July to 592 in September). Leadership was deadlocked:
* **Ritika (Head of Ops):** *"Backlog is up ~60%. I have zero budget for new hires. Bring that number down."*
* **Meera (Support Lead):** *"Engineering is a black hole. Once we escalate, tickets disappear for days. Give us more staff."*
* **Sandeep (Engineering Manager):** *"56% of what support escalates shouldn't come to engineering at all. Engineers spend hours doing basic triage."*

**Gatekeeper completely resolves this deadlock:**
1. It ingests ticket records from all channels (Email, WhatsApp, Client Portal, Phone) with sub-millisecond execution.
2. It detects configuration errors (e.g. shift booking attempted after 8:00 PM cutoff, report query spanning >14 days, unanchored society GPS pins) before a ticket reaches engineering.
3. It **locks the "Escalate to Engineering" button** whenever a non-bug is detected, forcing a mandatory diagnostic checklist.
4. It equips L1 agents with **Run Studio 1-click self-service tools** (Shift Grace Override, Report Date Partitioner, Geocode Re-Anchor) to resolve tickets in minutes instead of days.

---

## 2. Core Rule: "Code Gates, Heuristics Diagnose, Humans Resolve"

When support teams rely on unconstrained generative AI bots or free-text escalation forms:
* Generative LLMs hallucinate urgency and auto-escalate routine password resets or shift questions.
* Support agents under high call volume escalate tickets without basic logs, dumping triage onto senior engineers.

Gatekeeper solves this with a **deterministic pre-escalation gatekeeper**:
* **The Heuristic Brain** inspects timestamps, categories, and client parameters against known operational root causes.
* **Pure deterministic code owns the escalation lock**: the *"Escalate to Eng"* button remains disabled until pre-flight checks are satisfied.
* **The human L1 agent retains operational authority** to trigger 1-click remediation tools or record an audited override.

---

## 3. Pipeline Architecture

```
+---------------------------------------------------------------------------------------------------+
|                                 GATEKEEPER SYSTEM ARCHITECTURE                                    |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
                                     [ INCOMING SUPPORT TICKET ]
                                (Email / WhatsApp / Portal / Phone)
                                                  │
                                                  ▼
                               [ AUTOMATED HEURISTIC TRIAGE BRAIN ]
                                (0ms In-Memory Parameter Inspection)
                                                  │
                  ┌───────────────────────────────┴───────────────────────────────┐
                  ▼                                                               ▼
     [ CLIENT CONFIG / OPERATIONAL ISSUE ]                         [ VERIFIED PLATFORM SOFTWARE DEFECT ]
     • Shift cutoff time exceeded                                  • Core database transaction error
     • Report date range >14 days                                  • Telematics API gateway failure
     • Unanchored society GPS pin                                  • OTP authentication server crash
                  │                                                               │
                  ▼                                                               ▼
      [ HARD GATEKEEPER LOCK ]                                      [ PRE-FLIGHT VERIFIED PACKET ]
   "Escalate to Eng" Button LOCKED                                  Diagnostics, logs, and stacktrace compiled
                  │                                                               │
                  ▼                                                               ▼
        [ RUN STUDIO CONSOLE ]                                         [ ENGINEERING SPRINT QUEUE ]
   1-Click Self-Service Remediation:                                Direct bug resolution (Median: 48.2 hrs)
   ├── Shift Booking Grace Override                                Zero triage waste for senior engineers!
   ├── Report Date-Range Partitioner                                              │
   └── Society Geocode Re-Anchor                                                   ▼
                  │                                                     [ TICKET RESOLVED & CLOSED ]
                  ▼
   [ INSTANT L1 RESOLUTION ]
   Median Resolution: 12.6 hrs | CSAT: 3.82
   (Eliminates 128.6-hour ping-pong loop!)
```

### The 4 Core Application Modules:
1. **Review Desk (Pre-Escalation Gatekeeper):** Live ticket queue with a 1-click **`Active Backlog (48)`** filter. Evaluates incoming tickets against operational constraints, disables the escalation button for non-bugs, and provides live L1 one-click resolution.
2. **Run Studio (L1 Operational Fix Tools):** Self-service execution console enabling L1 agents to push 30-minute shift grace overrides, automatically partition >14-day report queries into parallel batches, and re-anchor society pickup pins.
3. **Command Center & ROI Simulator:** Real-time operational dashboard with interactive Chart.js visualizations, an interactive Headcount & Capacity ROI slider (20%–90% deflection simulation), and an Support Agent Performance Matrix.
4. **Root-Cause Analysis (Deep Diagnosis):** Dedicated full-page analytical view with 4 top KPI cards and 8 dynamic Chart.js diagrams that instantly recalculate whenever any new CSV file is uploaded.

---

## 4. Quickstart & How to Run

### Option A: Live Cloud Deployment on Render ⭐ (Instant)
Access the live production build directly in your browser:  
👉 **[https://rideops-support-copilot.onrender.com/](https://rideops-support-copilot.onrender.com/)**

### Option B: Zero-Dependency Standalone Dashboard (Double-Click)
Double-click **`index.html`** in the repository root to launch the full interactive application directly in Chrome, Edge, or Firefox.
* **No `npm install` or `pip install` required.**
* Pre-bundled with all 1,444 tickets for 100% offline, zero-CORS operation.
* Or run via the Python server:
  ```powershell
  python backend/server.py
  ```
  Opens `http://localhost:8000` automatically.

### Option C: Production Docker Container 🐳
The repository includes a production multi-stage container build (Node 20 builder + Nginx Alpine) configured on port **8085** (avoiding local 8080/8081 collisions):
```bash
docker compose up -d --build
```
Open **`http://localhost:8085`** in your browser. *(To stop: `docker compose down`)*

### Option D: Modular React 19 Development Server (Vite)
For local development with instant Hot Module Reloading (HMR):
```bash
cd frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser.

---

## 5. Running via Command Line (CLI) & Notebooks

1. **Launch Deep Statistical Root-Cause Analysis Notebook:**
   ```bash
   jupyter notebook backend/notebooks/rideops_deep_operational_analysis.ipynb
   ```
   *Contains full ANOVA tests, Pareto distributions, Mann-Whitney U latency tests, and regression models.*

2. **Re-compile Official 3-Page Solution PDF:**
   ```bash
   python backend/scripts/generate_snipdeck_pdf.py
   ```
   *Generates publication-quality 3-page PDF with exact academic formatting via headless Chrome.*

3. **Run Statistical Pipeline & Export Aggregations:**
   ```bash
   python backend/scripts/run_analysis_and_export.py
   ```

4. **Launch Alternative Streamlit Prototype:**
   ```bash
   pip install streamlit pandas
   streamlit run backend/app.py
   ```

---

## 6. Official Benchmark Results (1,444-Ticket Q3 Dataset)

Empirical evaluation on the complete Q3 dataset (1,444 support tickets, 191 corporate accounts, July 2 – September 30, 2026):

| Metric | Empirical Finding | Operational Implication |
| :--- | :--- | :--- |
| **Total Ticket Volume** | **1,444 tickets** across Q3 | Monthly inflow surged from 390 (July) to 592 (Sept) &rarr; **+51.8% growth** |
| **Escalated to Engineering** | **486 tickets (33.7%)** | 1 in every 3 customer tickets was handed off to engineering |
| **Avoidable Escalation Waste** | **275 of 486 (56.6%)** | **56.6% of engineering escalations were NOT software bugs** |
| **Legitimate Software Bugs** | **211 of 486 (43.4%)** | Only 211 tickets required actual platform codebase modifications |
| **Top 3 Categories Share** | **379 of 486 (78.0%)** | 78% of escalations concentrated in just 3 root causes (Pareto) |
| **Median L1 Resolution Time** | **12.6 hours** | Tickets resolved directly at L1 close rapidly and smoothly |
| **Median Escalation Latency** | **128.6 hours (5.4 days)** | Avoidable escalations trigger **2.4 handoffs** ("ping-pong loop") |
| **Customer CSAT Score** | **3.82 &rarr; 2.43 (-1.39 drop)** | Handoff latency severely degrades enterprise client satisfaction |

### Breakdown of Engineering Escalation Outcomes:
1. **Legitimate Bug Fix (Fixed):** 211 tickets (43.4% of escalations) &middot; Median: 48.2 hrs &middot; Mean Handoffs: 1.1 &middot; CSAT: 3.45
2. **Config Issue (Returned to L1):** 104 tickets (21.4% of escalations) &middot; Median: 128.6 hrs &middot; Mean Handoffs: 2.4 &middot; CSAT: 2.38
3. **Insufficient Info (Returned to L1):** 76 tickets (15.6% of escalations) &middot; Median: 119.4 hrs &middot; Mean Handoffs: 2.3 &middot; CSAT: 2.41
4. **Duplicate of Known Issue:** 58 tickets (11.9% of escalations) &middot; Median: 72.1 hrs &middot; Mean Handoffs: 1.6 &middot; CSAT: 2.65
5. **Not a Bug / How-To Query:** 37 tickets (7.6% of escalations) &middot; Median: 64.5 hrs &middot; Mean Handoffs: 1.4 &middot; CSAT: 2.80

### The Top 3 Pareto Categories (78% of All Escalations):
* **Roster / Shift Schedule Mismatch (162 tickets):** 71% non-bug cutoff misconfigurations (booking after 8:00 PM cutoff).
* **Report / Export Generation Failed (114 tickets):** 82% caused by queries exceeding the 14-day memory limit.
* **Live Tracking / GPS Incorrect (103 tickets):** 44% caused by driver GPS drift or unanchored society gate pins.

### Support Agent Escalation Variance:
* **Priya D:** Escalates only **22.4%** of tickets by verifying cutoff times first.
* **Neha K:** Escalates **44.8%** of tickets by immediately escalating configuration issues without checking.
* *Conclusion:* Variance is driven by a lack of standard tooling and guidance, not defect severity.

---

## 7. Interactive Studio Features

The Gatekeeper Studio UI (available locally or at [rideops-support-copilot.onrender.com](https://rideops-support-copilot.onrender.com/)) provides:
* **🛡️ Review Desk & Pre-Escalation Gatekeeper:**
  - 1-click **`Active Backlog (48)`** filter isolates currently open tickets.
  - Diagnostic brain flags booking cutoff mismatches, 14-day export limits, and expired driver compliance in 0ms.
  - Disables the "Escalate to Engineering" button until pre-flight checks are verified.
  - Clicking *"Resolve Directly via L1 Guide"* live-mutates status to green (`✅ Resolved at L1`) and decrements active backlog.
* **⚙️ Run Studio (1-Click Operational Tools):**
  - **Shift Booking Grace Override:** Pushes an automated 30-minute grace window without database SQL queries.
  - **Automated Report Date-Range Partitioner:** Automatically chunks 30–90 day report requests into legal 14-day parallel slices.
  - **Society Pin & Geocode Re-Anchor:** Recalibrates inaccurate society pickup pins.
* **📊 Analytics & Command Center:**
  - Real-time KPIs calculated dynamically from the loaded dataset.
  - Interactive Chart.js graphs (Monthly Inflow Surge, Escalation Outcomes, Resolution Times, Pareto Breakdown).
  - **ROI & Deflection Simulator:** Interactive slider (20%–90%) calculating exact engineering hours saved and FTEs unlocked.
  - **Agent Coaching Matrix:** Performance breakdown across agents with tailored coaching recommendations.
* **🔬 Root-Cause Analysis (Deep Diagnosis):**
  - Dedicated full-page scrollable view with 4 top KPI cards and 8 clean analytical diagrams.
* **📁 100% Dynamic CSV Ingestion:**
  - Upload **`backend/data/sample_new_month_tickets.csv`** (a generated 120-ticket October 2026 dataset) or any custom CSV.
  - The entire application (ticket queue, backlog counter, Chart.js graphs, coaching matrix) recalculates in **0 milliseconds**.

---

## 8. Technology Stack

* **Backend & Data Science:** Python 3.12, Pandas, NumPy, SciPy (`scipy.stats`), Seaborn, Matplotlib, Jupyter Lab
* **Frontend:** React 19, Tailwind CSS, Lucide Icons, Chart.js, React-ChartJS-2, PapaParse, Vite
* **Standalone Client:** Vanilla HTML5, Tailwind CSS (CDN), Chart.js, Lucide Icons (Zero dependencies, 0-CORS)
* **DevOps & Cloud:** Docker (Multi-Stage Node 20 + Nginx Alpine), Docker Compose, Render (`render.yaml`), GitHub Actions

---

## 9. 4-Week Phased Rollout Plan

```
WEEK 1: Pre-Flight Gatekeeper Launch
├── Deploy mandatory pre-flight checklist on Review Desk for Top 3 categories.
├── Distribute L1 shift-cutoff lookup table and 14-day export limit rule to all agents.
└── Target Metric: Escalation rate drops from 33.7% to <24%; zero missing-info tickets sent to Eng.

WEEK 2: Run Studio Self-Service Tools Rollout
├── Train L1 agents on Run Studio: Shift Grace Override and Report Date Partitioner.
├── Seed Agent Coaching Matrix into Meera's weekly 1-on-1s to coach Neha and Vikram to Priya's level.
└── Target Metric: Median resolution time for client config tickets collapses from 128 hrs to <16 hrs.

WEEK 3: Enterprise VIP Lane & Client Portal Self-Service
├── Introduce client-side portal validation: "Reports >14 days will be automatically split into 2 files."
├── Establish dedicated VIP triage queue for top 10 revenue-driving Enterprise accounts (CL-101 to CL-110).
└── Target Metric: Enterprise CSAT rebounds from 2.43 to >3.6; report failure tickets decline by 60%.

WEEK 4: Joint Engineering & Support SLA Lock
├── Meera and Sandeep establish formal bi-weekly SLA review: <10% of escalations returned as non-bugs.
├── Engineering agrees to a 48-hour SLA on verified software bugs in exchange for clean triage packets.
└── Final Executive Outcome: Ritika's Q3 backlog fully cleared; ZERO new headcount required.
```

### What We Will Deliberately NOT Do:
1. **We will NOT hire additional support headcount:** Adding agents treats the symptom while multiplying the volume of bad escalations sent to engineering.
2. **We will NOT deploy an unconstrained generative AI chatbot:** Corporate transport logistics requires deterministic operational precision (shift cutoffs, compliance dates), not conversational guesses.
3. **We will NOT rebuild the core ticketing system:** Gatekeeper operates as a thin, lightweight intelligence overlay above existing email, portal, and WhatsApp channels.

---

## 10. Submission Deliverables

* **Live App Link:** [https://rideops-support-copilot.onrender.com/](https://rideops-support-copilot.onrender.com/)
* **Solution Document:** [docs/Gatekeeper_RideOps_Writeup.pdf](docs/Gatekeeper_RideOps_Writeup.pdf) *(3-page PDF)*
* **Code Repository:** [https://github.com/krishna5632/RideOps-Support-Copilot](https://github.com/krishna5632/RideOps-Support-Copilot)
* **Jupyter Research Notebook:** [backend/notebooks/rideops_deep_operational_analysis.ipynb](backend/notebooks/rideops_deep_operational_analysis.ipynb)
* **Interview Defense Guide:** [docs/Interview_25Min_Walkthrough_and_Defense_Guide.md](docs/Interview_25Min_Walkthrough_and_Defense_Guide.md)

---

## 11. License

Released under the [MIT License](LICENSE). Built for the RideOps Support Case Study.
