# 🚕 RideOps Support Copilot & Pre-Escalation Gatekeeper (v0)

A working operational tool and data diagnostic system built for the **RideOps Support Case Study**.

---

## 🚀 How to Run the Working App

You have three convenient ways to evaluate and run the project:

### Method 1: Modular React Application (Vite + React 19 + Tailwind CSS + Lucide) ⭐ (Recommended for Engineering Evaluation)
The frontend has been completely refactored into a clean, modular component architecture:
```bash
cd frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser. Features instant Hot Module Reloading (HMR), isolated components, and type-safe Context state management.

To compile a minified production bundle:
```bash
cd frontend
npm run build
npm run preview
```

---

### Method 2: Instant Double-Click (Zero Setup)
Simply double-click **`index.html`** in the root directory to open the standalone web application directly in Chrome, Edge, or Firefox.
* **No `npm install` or `pip install` required.**
* Runs 100% locally with all 1,444 tickets pre-loaded.

---

### Method 3: Standard Python Server
Open terminal / PowerShell in the root directory and run:
```bash
python server.py
```
This starts a local server on port 8000 and opens your browser at `http://localhost:8000`.

---

### Method 4: Docker Container (Production Nginx Build) 🐳
Build and run the containerized application with Docker:
```bash
docker build -t rideops-support-copilot .
docker run -d -p 8080:80 --name rideops-app rideops-support-copilot
```
Open **`http://localhost:8080`** in your browser. Powered by multi-stage Node 20 builder and optimized Nginx Alpine static serving with client-side SPA routing.

---

### 📁 Dynamic CSV Upload Testing
The application is **100% dynamic**. You can upload any new ticket CSV anytime:
1. Open the app and click the **`📁 Upload CSV`** button in the top right header.
2. Select **`sample_new_month_tickets.csv`** (a generated 120-ticket October 2026 dataset included in this folder) or any custom CSV.
3. The entire application (ticket queue, open backlog counter, Chart.js graphs, and the agent coaching matrix) recalculates in **0 milliseconds**.

---

### Alternative: Streamlit App
If you prefer running the Python Streamlit prototype:
```bash
pip install streamlit pandas
streamlit run backend/app.py
```

---

## 📂 Repository Structure

```
RideOps_CaseStudy/
├── frontend/                     # Modular React 19 + Tailwind CSS + Lucide Icons Application
│   ├── src/
│   │   ├── components/
│   │   │   ├── ReviewDesk/       # Gatekeeper triage, ticket feed, problem inspector
│   │   │   ├── RunStudio/        # L1 quick-fix self-service execution tools
│   │   │   ├── CommandCenter/    # Analytics charts, ROI simulator, coaching matrix
│   │   │   └── ExecutiveDeck/    # 8-Slide executive presentation viewer
│   │   └── context/              # Centralized TicketContext state management
│   └── package.json
│
├── backend/                      # Python services, data science pipeline, and datasets
│   ├── data/                     # Raw datasets (rideops_support_tickets.csv, sample new month)
│   ├── scripts/                  # Data preparation & analysis Python scripts
│   ├── notebooks/                # rideops_support_analysis.ipynb & PNG figures
│   ├── server.py                 # Backend server
│   └── app.py                    # Streamlit prototype
│
├── docs/                         # Executive briefings & interview prep
│   ├── RideOps_Writeup_and_Presentation_Deck.md     # 4-Page Briefing + 8-Slide deck text
│   └── Interview_25Min_Walkthrough_and_Defense_Guide.md # 15m walkthrough script + Q&A defense
│
├── index.html                    # 0-Dependency standalone double-clickable app
├── server.py                     # Root HTTP server for index.html (python server.py)
└── README.md                     # Project documentation & run guide
```

---

## 📌 Problem Summary
* **Volume Inflow:** +51.8% surge in new tickets between July (390) and September (592).
* **The Escalation Black Hole:** 33.7% of all tickets are escalated to Engineering (486 tickets).
* **The Root Cause:** **56.6% (275 of 486) of escalations are NOT software bugs** (configuration errors, missing diagnostic logs, duplicate tickets, how-to queries).
* **Cycle Time Penalty:** While L1 resolves tickets in **12.6 hours**, tickets escalated with configuration issues bounce back and forth (2–3 handoffs) taking **128.6 hours (5.4 days)** and crashing CSAT down to **2.43**.
* **Constraint:** Zero budget for new hires (Ritika's mandate).

---

## 🛠️ Key Capabilities Built into the Modern App
1. **🛡️ Review Desk & Pre-Escalation Gatekeeper:**
   - 1-click **`Active Backlog (48)`** button isolates currently open tickets.
   - Heuristic diagnostic brain spots shift cutoff mismatches, 14-day export limits, and expired compliance documents.
   - Lock & Key Gatekeeper disables the "Escalate to Engineering" button until pre-flight checks are verified.
   - Clicking *"Resolve Directly via L1 Guide"* mutates ticket status live to green (`✅ Resolved at L1`) and decrements active backlog in real time.
2. **📊 Analytics & Executive Command Center:**
   - Real-time KPIs calculated dynamically from the loaded dataset.
   - Interactive Chart.js graphs (Monthly Inflow Surge, Escalation Outcomes, Resolution Times, Pareto Breakdown).
   - **Real-Time Backlog & Headcount ROI Simulator:** Slider simulates 20%-90% deflection, showing exact engineering hours saved and FTE equivalents unlocked.
   - **Dynamic Agent Coaching Matrix:** Live breakdown across agents with tailored coaching recommendations.
3. **⚙️ L1 Client Quick-Fix Tools:**
   - Shift Booking Cutoff Sync & Grace Override.
   - Automated Report Date-Range Partitioner (>14 day split).
   - Address & Society Pin Re-Anchor.
4. **📑 Executive Presentation Deck:**
   - Interactive 8-slide presentation viewer covering the dilemma, diagnosis, 80/20 Pareto focus, week-to-week metrics, and the 4-week rollout plan (including what we deliberately will NOT do).
5. **🎯 25-Minute Interview Cheat Sheet:**
   - See [Interview_25Min_Walkthrough_and_Defense_Guide.md](file:///c:/Users/prave/Downloads/RideOps_CaseStudy/docs/Interview_25Min_Walkthrough_and_Defense_Guide.md) for the exact 15-minute live demo script and answers to the top 5 challenge questions.
