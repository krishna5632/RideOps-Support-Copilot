# 🚕 RideOps Support Copilot & Pre-Escalation Gatekeeper

A production-grade operational support intelligence hub, pre-escalation gatekeeper, and empirical root-cause diagnostic system built for the **RideOps Corporate Support Case Study**.

---

## 🏛️ Project Architecture & Directory Structure

The repository is structured with strict separation of concerns between frontend, backend services, data science artifacts, and deployment orchestration:

```
RideOps_CaseStudy/
├── backend/                                # Python services, data pipelines & analytics
│   ├── app.py                              # Streamlit operational prototype portal
│   ├── server.py                           # Zero-dependency local web server (Python stdlib)
│   ├── data/                               # Canonical datasets
│   │   ├── rideops_support_tickets.csv     # Primary Q3 dataset (1,444 corporate tickets)
│   │   ├── rideops_data_dictionary.csv     # Schema & column definitions
│   │   ├── sample_new_month_tickets.csv    # 120-ticket dataset for dynamic upload testing
│   │   ├── tickets.json                    # Pre-parsed JSON payload
│   │   └── data.js                         # Zero-CORS pre-bundled browser data store
│   ├── notebooks/                          # Jupyter research & statistical models
│   │   ├── rideops_deep_operational_analysis.ipynb  # 9-section root-cause modeling notebook
│   │   └── *.png                           # Matplotlib & Seaborn analytical figures
│   └── scripts/                            # Operational utility & pipeline scripts
│       ├── build_and_execute_notebook.py   # Automated notebook build pipeline
│       ├── populate_notebook_outputs.py    # Process-level notebook output generator
│       ├── run_analysis_and_export.py      # Statistical aggregation & export script
│       └── generate_data_js.py             # Generates universal browser data.js
│
├── frontend/                               # Production React 19 SPA
│   ├── public/                             # Static public assets, icons, figures
│   ├── src/
│   │   ├── components/
│   │   │   ├── ReviewDesk/                 # L1 Gatekeeper, active backlog, ticket triage
│   │   │   ├── RunStudio/                  # L1 self-service operational fix tools
│   │   │   ├── CommandCenter/              # Command analytics, ROI simulator, coaching matrix
│   │   │   ├── DeepDiagnosis/              # Dynamic root-cause diagnosis charts
│   │   │   ├── Header.jsx                  # Top navigation, CSV file uploader, live status
│   │   │   ├── Sidebar.jsx                 # Collapsible 4-module navigation sidebar
│   │   │   └── Toast.jsx                   # Notification dispatch system
│   │   ├── context/                        # Centralized TicketContext state management
│   │   ├── data/                           # Inlined default dataset (defaultTickets.js)
│   │   ├── App.jsx                         # Main layout container
│   │   └── main.jsx                        # React root entry point
│   ├── package.json                        # Frontend dependencies (React 19, Tailwind, Chart.js)
│   └── vite.config.js                      # Vite compiler configuration
│
├── docs/                                   # Executive documentation & interview defense
│   ├── RideOps_Writeup_and_Presentation_Deck.md        # 4-page writeup + 8-slide executive deck
│   └── Interview_25Min_Walkthrough_and_Defense_Guide.md # 15-min walkthrough script & Q&A defense
│
├── figures/                                # High-resolution analytical figures for reports
├── index.html                              # Standalone, zero-dependency interactive dashboard
├── Dockerfile                              # Multi-stage production container build (Node + Nginx)
├── docker-compose.yml                      # Container orchestration (Port 8085:80)
├── nginx.conf                              # Production SPA routing configuration
├── .gitignore                              # Clean repository exclusions
└── README.md                               # Project documentation
```

---

## 🚀 How to Run the Application

You can evaluate the system using any of the following methods:

### Option 1: Standalone Dashboard (Instant / Zero Dependencies) ⭐
Double-click **`index.html`** in the root directory to open the full interactive application directly in Chrome, Edge, or Firefox.
* **No `npm install` or `pip install` required.**
* Works 100% locally with all 1,444 tickets pre-bundled.
* Or run via the Python server:
  ```powershell
  python backend/server.py
  ```
  Opens `http://localhost:8000` automatically.

---

### Option 2: React 19 Development Server (Vite)
For modern engineering evaluation with hot-module reloading:
```powershell
cd frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser.

To compile a minified production bundle:
```powershell
cd frontend
npm run build
npm run preview
```

---

### Option 3: Docker Container (Production Nginx Build) 🐳
The container is pre-configured on port **8085** (avoiding local 8080/8081 collisions):
```powershell
docker compose up -d --build
```
Open **`http://localhost:8085`** in your browser.

*(To stop the container: `docker compose down`)*

---

### Option 4: Jupyter Notebook (Deep Statistical Root-Cause Modeling)
To inspect the underlying statistical hypotheses, ANOVA tests, Pareto distributions, and regression models:
```powershell
jupyter notebook backend/notebooks/rideops_deep_operational_analysis.ipynb
```

---

### Option 5: Streamlit Prototype Portal
To run the quick Python Streamlit dashboard:
```powershell
pip install streamlit pandas
streamlit run backend/app.py
```

---

## 🎯 The 4 Navigation Modules in the Sidebar

The sidebar provides clean, one-click access across four core operational views:

| Module | Purpose | Key Features |
| :--- | :--- | :--- |
| **1. Review Desk** | Pre-Escalation Gatekeeper | Isolates active backlog (48 tickets), detects config/doc issues before escalation, enables 1-click L1 resolution. |
| **2. Run Studio** | L1 Self-Service Tools | Fixes recurring issues without engineering: shift cutoff overrides, report date-range splitters, and geocode re-anchoring. |
| **3. Command Center** | Operational Analytics | Real-time KPI cards, volume/outcome trends, interactive ROI & Deflection Simulator, and Support Agent Coaching Matrix. |
| **4. Root-Cause Analysis** | Empirical Deep Diagnosis | Dedicated scrollable dashboard with 4 core metrics and 8 clean Chart.js diagrams explaining operational bottlenecks. |

> **Note:** The sidebar has been streamlined to focus exclusively on operational tools and empirical diagnosis. The Executive Deck slides remain documented in [`docs/RideOps_Writeup_and_Presentation_Deck.md`](file:///c:/Users/prave/Downloads/RideOps_CaseStudy/docs/RideOps_Writeup_and_Presentation_Deck.md).

---

## 📁 Dynamic CSV Upload Testing

The application is **100% dynamic**. You can verify how the dashboard handles new data at runtime:

1. Click the **`📁 Upload CSV`** button in the top right header.
2. Select **`backend/data/sample_new_month_tickets.csv`** (a 120-ticket October 2026 dataset) or any custom CSV matching the RideOps schema.
3. Every KPI card, chart, active backlog counter, coaching matrix, and root-cause diagram immediately recalculates in **0 milliseconds**.

---

## 📊 Core Case Study Findings & Metrics

* **Volume Growth:** +51.8% surge in ticket inflow between July (390) and September (592).
* **Escalation Volume:** 33.7% of all tickets are escalated to Engineering (486 tickets).
* **The Root Cause:** **56.6% (275 of 486) of escalations are NOT software bugs** (configuration errors, missing logs, duplicate reports, how-to queries).
* **Cycle Time Penalty:** L1 resolves tickets in **12.6 median hours**, whereas configuration tickets escalated to engineering bounce back and forth (2–3 handoffs), taking **128.6 hours (5.4 days)** and driving CSAT down to **2.43**.
* **Zero-Budget Solution:** Implementing the Pre-Escalation Gatekeeper deflects ~56% of unnecessary escalations, saving ~1,100 hours of engineering capacity per quarter without adding support headcount.
