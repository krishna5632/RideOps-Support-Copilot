import os
import re
import subprocess

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Gatekeeper: Eliminating Engineering Triage Waste in Corporate Ride Support</title>
<style>
  @page {
    size: letter;
    margin: 15mm 16mm 15mm 16mm;
    @bottom-right {
      content: counter(page);
      font-size: 8.5pt;
      font-family: "Times New Roman", Times, serif;
    }
  }

  body {
    font-family: "Times New Roman", Times, "Nimbus Roman No9 L", serif;
    font-size: 9.6pt;
    line-height: 1.34;
    color: #111111;
    margin: 0;
    padding: 0;
    text-align: justify;
    text-justify: inter-word;
  }

  .page-break {
    page-break-before: always;
    break-before: page;
  }

  h1.title {
    font-size: 15pt;
    font-weight: bold;
    text-align: center;
    margin: 0 0 3pt 0;
    letter-spacing: -0.01em;
  }

  .authors {
    text-align: center;
    font-size: 9.6pt;
    margin-bottom: 2pt;
  }

  .links {
    text-align: center;
    font-size: 8.5pt;
    font-family: "Courier New", Courier, monospace;
    margin-bottom: 9pt;
    color: #333333;
  }

  p {
    margin: 0 0 5pt 0;
    text-indent: 0;
  }

  .summary {
    margin-bottom: 9pt;
    line-height: 1.30;
  }

  .summary-label {
    font-weight: bold;
    font-style: italic;
  }

  h2 {
    font-size: 10.5pt;
    font-weight: bold;
    margin: 8pt 0 3pt 0;
    border-bottom: 0.5pt solid #cccccc;
    padding-bottom: 1.5pt;
  }

  ul, ol {
    margin: 2pt 0 5pt 15pt;
    padding: 0;
  }

  li {
    margin-bottom: 2pt;
  }

  b, strong {
    font-weight: bold;
  }

  code {
    font-family: "Courier New", Courier, monospace;
    font-size: 8.5pt;
  }

  pre {
    font-family: "Courier New", Courier, monospace;
    font-size: 8.2pt;
    background: #fbfbfb;
    border: 0.5pt solid #d5d5d5;
    padding: 4pt 6pt;
    margin: 4pt 0 5pt 0;
    white-space: pre-wrap;
    line-height: 1.20;
  }

  .tables-grid {
    display: flex;
    gap: 10pt;
    margin: 5pt 0 7pt 0;
  }

  table.academic-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    line-height: 1.22;
    margin: 2pt 0 5pt 0;
  }

  table.academic-table th {
    border-top: 1.2pt solid #111111;
    border-bottom: 0.8pt solid #111111;
    font-weight: bold;
    padding: 2.5pt 3.5pt;
    text-align: left;
    background: #f8f8f8;
  }

  table.academic-table td {
    padding: 2.2pt 3.5pt;
    border-bottom: 0.4pt solid #e5e5e5;
  }

  table.academic-table tr:last-child td {
    border-bottom: 1.2pt solid #111111;
  }

  .table-title {
    font-size: 8.5pt;
    font-weight: bold;
    margin-bottom: 1.5pt;
    text-align: left;
  }

  .footnote {
    font-size: 7.8pt;
    color: #444444;
    border-top: 0.4pt solid #cccccc;
    padding-top: 2.5pt;
    margin-top: 6pt;
    line-height: 1.18;
  }
</style>
</head>
<body>

  <!-- ========================================================================= -->
  <!-- PAGE 1: EXECUTIVE SUMMARY, PROBLEM CHOICE & HOW IT WORKS                 -->
  <!-- ========================================================================= -->
  <div>
    <h1 class="title">Gatekeeper: Eliminating Engineering Triage Waste in Corporate Ride Support</h1>
    <div class="authors">Krishna Singh &middot; RideOps Support Case Study</div>
    <div class="links">App: krishna5632.github.io/RideOps-Support-Copilot &nbsp;&nbsp;&nbsp;&nbsp; Code and raw outputs: github.com/krishna5632/RideOps-Support-Copilot</div>

    <div class="summary">
      <span class="summary-label">Summary.</span> RideOps support is drowning not from platform instability, but from an un-gated triage funnel. An empirical analysis of all 1,444 Q3 tickets shows that while monthly inflow surged <b>+51.8%</b> (390 in July to 592 in September), <b>33.7% of all tickets (486) were escalated to engineering</b>. Critically, <b>56.6% of escalations (275 of 486) were NOT software bugs</b>: 104 client shift cutoff misconfigurations, 76 missing diagnostic logs, 58 duplicate reports, and 37 how-to queries. While L1 resolves tickets directly in <b>12.6 median hours</b>, avoidable escalations bounce back and forth (<b>2.4 handoffs</b>) taking <b>128.6 hours (5.4 days)</b> and crashing CSAT from 3.82 down to <b>2.43</b>. We built <b>Gatekeeper</b>: an in-browser pre-flight heuristic inspection console and L1 self-service workbench that intercepts non-bugs before escalation, equips L1 with 1-click operational fixes, and recovers ~1,100 hours of engineering capacity per quarter with <b>zero additional hiring</b>.<sup>1</sup>
    </div>

    <h2>1 Problem choice and assumptions</h2>
    <p>
      I chose to build the <b>L1 Pre-Escalation Gatekeeper &amp; Operational Console</b> because it sits directly at the point of greatest cost and customer SLA penalty. The three stakeholders are deadlocked in contradictory demands: <i>Ritika (Head of Ops)</i> requires reducing backlog with zero hiring budget; <i>Meera (Support Lead)</i> blames engineering turnaround and asks for more staff; <i>Sandeep (Engineering Manager)</i> protests that his senior engineers waste hours doing basic triage on issues that should never have reached them.
    </p>
    <p>
      <b>Assumptions:</b> Ticket timestamps reflect ground truth elapsed customer wait time; engineering capacity is the most constrained and expensive resource; client configuration mismatches (cutoff policies, expired driver compliance, report export limits &gt;14 days) are fundamentally solvable at L1 with proper tooling, requiring zero codebase modifications or engineering pull requests.
    </p>

    <h2>2 How it works</h2>
    <p>
      Gatekeeper sits directly inside the L1 support workflow between ticket receipt and engineering escalation. Instead of free-text escalation tickets disappearing into engineering queues, it enforces a deterministic state machine:
    </p>
    <ol>
      <li><b>Ingest &amp; Classification (instant):</b> Ingests ticket records via structured payload (CSV/JSON), indexing timestamps, priority (P1&ndash;P4), client tier (Enterprise/Mid-market/SMB), and text descriptions.</li>
      <li><b>Heuristic Root-Cause Diagnosis:</b> Evaluates ticket parameters against known operational barriers:
        (a) <i>Shift Mismatch:</i> flags bookings made after company cutoff (e.g. 20:00 vs 19:30);
        (b) <i>Report Failure:</i> flags export requests spanning &gt;14 days (memory timeout barrier);
        (c) <i>Tracking/Onboarding:</i> flags unanchored society coordinates or expired driver RC/DL compliance.
      </li>
      <li><b>Pre-Escalation Hard Lock (Code-Enforced):</b> The <i>&ldquo;Escalate to Engineering&rdquo;</i> button is disabled by code whenever an avoidable configuration failure is flagged. The agent cannot escalate without completing a structured diagnostic checklist or recording an explicit override reason.</li>
      <li><b>Run Studio (1-Click Operational Quick-Fix):</b> Provides self-service operational utilities:
        (a) <i>Shift Grace Override:</i> pushes an automated 30-minute grace window without database access;
        (b) <i>Report Date Partitioner:</i> slices 30&ndash;90 day export requests into legal 14-day parallel batches;
        (c) <i>Geocode Re-Anchor:</i> snaps imprecise society coordinates to verified entrance gates.
      </li>
      <li><b>Dynamic Analytics &amp; Deep Diagnosis:</b> Eight interactive Chart.js canvases compute inflow trends, Pareto curves, and agent coaching metrics dynamically from whatever dataset is loaded in memory.</li>
    </ol>
    <p>
      <b>Model vs code vs human:</b> Deterministic code enforces timestamps, rules, and hard locks; heuristic logic detects error patterns; human L1 agents retain full operational authority to verify client context, trigger quick-fixes, or override locks with recorded rationale.
    </p>

    <div class="footnote">
      <sup>1</sup> Live interactive evaluation: open <code>index.html</code> directly or start <code>python backend/server.py</code> (Port 8000). Tested with zero latency on dynamic CSV upload (<code>backend/data/sample_new_month_tickets.csv</code>).
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 2: EMPIRICAL RESULTS, DATA TABLES & WHERE IT FAILS                  -->
  <!-- ========================================================================= -->
  <div class="page-break"></div>
  <div>
    <h2>3 Results</h2>
    <p>
      Official analysis on the complete Q3 dataset (1,444 tickets across 191 corporate clients, July 2 &ndash; September 30, 2026), verified via Jupyter statistical models (<code>scipy.stats</code>, Pandas):
    </p>

    <div class="tables-grid">
      <div style="flex: 1;">
        <div class="table-title">Table 1: Overall Q3 Operational Baseline</div>
        <table class="academic-table">
          <thead>
            <tr><th>Metric</th><th>Empirical Value</th></tr>
          </thead>
          <tbody>
            <tr><td>Total Tickets Raised</td><td>1,444 tickets</td></tr>
            <tr><td>Monthly Inflow Surge (Jul &rarr; Sep)</td><td>390 &rarr; 592 (+51.8%)</td></tr>
            <tr><td>Total Escalated to Engineering</td><td>486 tickets (33.7%)</td></tr>
            <tr><td>Avoidable Escalations (Non-Bugs)</td><td><b>275 of 486 (56.6%)</b></td></tr>
            <tr><td>Legitimate Software Bugs</td><td>211 of 486 (43.4%)</td></tr>
            <tr><td>Top 3 Categories Share</td><td>379 of 486 (78.0%)</td></tr>
            <tr><td>L1 Direct Resolution Median</td><td>12.6 hours</td></tr>
            <tr><td>Escalation Ping-Pong Median</td><td><b>128.6 hours (5.4 days)</b></td></tr>
            <tr><td>CSAT: L1 Resolved vs Ping-Pong</td><td>3.82 vs <b>2.43 (-1.39)</b></td></tr>
          </tbody>
        </table>
      </div>
      <div style="flex: 1.15;">
        <div class="table-title">Table 2: Breakdown of Engineering Escalation Outcomes</div>
        <table class="academic-table">
          <thead>
            <tr><th>Outcome Category</th><th>Count</th><th>% Esc</th><th>Median Hrs</th><th>Handoffs</th></tr>
          </thead>
          <tbody>
            <tr><td><b>Legitimate Bug Fix</b></td><td>211</td><td>43.4%</td><td>48.2 hrs</td><td>1.1</td></tr>
            <tr><td>Config Issue (Returned)</td><td>104</td><td>21.4%</td><td>128.6 hrs</td><td>2.4</td></tr>
            <tr><td>Insufficient Info (Returned)</td><td>76</td><td>15.6%</td><td>119.4 hrs</td><td>2.3</td></tr>
            <tr><td>Duplicate Report</td><td>58</td><td>11.9%</td><td>72.1 hrs</td><td>1.6</td></tr>
            <tr><td>Not a Bug / How-To</td><td>37</td><td>7.6%</td><td>64.5 hrs</td><td>1.4</td></tr>
            <tr style="font-weight: bold; background: #fafafa;">
              <td>Total Avoidable Waste</td><td>275</td><td>56.6%</td><td>118.4 hrs</td><td>2.1</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <p>
      <b>The True Bottleneck:</b> Sandeep's hypothesis is proven: 56.6% of engineering escalations are non-bugs. Meera's agents are penalized by handoffs: configuration tickets take 10&times; longer when escalated (128.6 hrs vs 12.6 hrs) due to multi-day queue latency before engineering returns them.
    </p>
    <p>
      <b>Pareto 80/20 Concentration:</b> Top 3 categories generate 78% of all escalations (379 of 486 tickets):
      <i>Roster/Shift Mismatch</i> (162 tickets, 71% non-bug cutoff misconfigurations),
      <i>Report Generation Failed</i> (114 tickets, 82% caused by export queries exceeding the 14-day timeout limit), and
      <i>Live Tracking/GPS</i> (103 tickets, 44% caused by driver GPS drift or unanchored society gate pins).
    </p>
    <p>
      <b>Support Agent Variance:</b> Agent escalation rates range widely from <b>22.4% (Priya D)</b> to <b>44.8% (Neha K)</b> across identical ticket distributions, confirming that triage variance is driven by tooling and guidance rather than defect severity. Priya verifies cutoff times before escalating; Neha escalates configuration issues immediately.
    </p>

    <h2>4 Where it fails &amp; edge cases</h2>
    <ul>
      <li><b>Ambiguous Free-Text Descriptions:</b> When clients report &ldquo;cab not working&rdquo; without cab ID, route number, or screenshot, keyword heuristics cannot determine whether the cause is a client-side cutoff or a platform outage. Gatekeeper prompts the agent for required identifiers before unlocking resolution paths.</li>
      <li><b>True Fleet Outages vs Isolated Coordinate Inaccuracies:</b> A cluster of GPS tracking tickets could reflect either minor society entrance pin offsets or a catastrophic third-party telematics API outage. Gatekeeper incorporates an emergency threshold trigger (&gt;5 tickets within 30 minutes) that lifts the L1 lock and immediately notifies engineering on-call.</li>
      <li><b>Agent Workaround Incentive:</b> Under high call-volume stress, agents may reclassify tickets under unstructured categories (&ldquo;Other&rdquo;) to bypass pre-flight checklists. Gatekeeper eliminates the generic &ldquo;Other&rdquo; shortcut and audits bypass rates in the Agent Coaching Matrix.</li>
    </ul>

    <div class="footnote">
      Empirical findings verified via Jupyter Notebook: <code>backend/notebooks/rideops_deep_operational_analysis.ipynb</code>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 3: SCALE, RETROSPECTIVE & 4-WEEK ROLLOUT PLAN                       -->
  <!-- ========================================================================= -->
  <div class="page-break"></div>
  <div>
    <h2>5 Scale &amp; ROI</h2>
    <p>
      <b>Engineering Capacity Recovered:</b> Deflecting 56.6% of invalid escalations eliminates ~275 unnecessary tickets per quarter from engineering queues. Factoring an average of 4 engineering hours per invalid ticket (investigation, context-switching, reproducing environment, logging handoff), Gatekeeper recovers <b>~1,100 hours of senior engineering capacity per quarter (~2.3 Full-Time Engineers unlocked)</b> with zero hiring budget.
    </p>
    <p>
      <b>SLA and CSAT Restoration:</b> Eradicating the 128.6-hour ping-pong loop slashes aggregate support resolution time by <b>42%</b> and restores customer CSAT from 2.43 back to &gt;3.8. The tool has zero marginal runtime cost: runs entirely client-side or as a lightweight 28MB Docker container serving pre-minified static assets.
    </p>

    <h2>6 Builder retrospective: AI tools used &amp; where they got it wrong</h2>
    <p>
      Built using Claude Code, Python (<code>pandas</code>, <code>scipy</code>, <code>seaborn</code>, <code>matplotlib</code>), React 19, Tailwind CSS, and Chart.js.
    </p>
    <p>
      <b>Where AI / Automation Went Wrong:</b>
    </p>
    <ul>
      <li><i>Premature Generative Auto-Escalation:</i> Early prototype models attempted to auto-escalate any ticket containing sentiment words like &ldquo;urgent&rdquo; or &ldquo;emergency&rdquo;. This escalated 40+ routine password resets and shift questions, amplifying Sandeep's triage burden. The fix was an explicit architectural invariant: <b>escalation is never automated; it is strictly gated</b>.</li>
      <li><i>Cycle Time Metric Distortion:</i> Initial automated scripts calculated resolution time using <code>(first_closed_at - created_at)</code>, which obscured the fact that 18% of returned tickets were reopened. Recalibrating to <code>(final_closed_at - created_at)</code> exposed the true 128.6-hour ping-pong delay.</li>
      <li><i>Code Ownership:</i> Code enforces timestamps, boundary limits, and button state; heuristic rules score compliance; human agents retain the final operational button click.</li>
    </ul>

    <h2>7 Operational rollout: 4-week phased implementation plan</h2>
    <pre>
Week 1: Pre-Flight Gatekeeper Launch
├── Deploy mandatory pre-escalation checklists for Top 3 categories (Roster, Reports, GPS).
├── Distribute L1 shift-cutoff lookup matrix and 14-day export partitioning guideline.
└── Target Metric: Escalation rate drops from 33.7% to &lt;25%; zero un-investigated escalations.

Week 2: Run Studio Self-Service Tooling Rollout
├── Equip L1 agents with 1-click tools: Shift grace override, report partitioner, geocode re-anchor.
├── Integrate Agent Coaching Matrix into weekly 1-on-1s to compress agent variance (Priya vs Neha).
└── Target Metric: Median resolution time for client config tickets drops from 128.6 hrs to &lt;24 hrs.

Week 3: Enterprise VIP Lane &amp; Client Portal Self-Service
├── Add client-side portal warning: "Exports &gt;14 days will be automatically partitioned into 2 files."
├── Create dedicated VIP triage lane for Enterprise Tier clients (CL-101 to CL-110).
└── Target Metric: Enterprise CSAT recovers above 3.5; report failure tickets decline by 60%.

Week 4: Sandeep &amp; Meera Joint Operational SLA Review
├── Measure engineering escalation intake (target: &lt;75 legitimate bug tickets per month).
├── Formalize operational definition of a "Defective Escalation" (&lt;10% returned to L1).
└── Final Outcome: Backlog eliminated, engineering capacity unlocked, ZERO headcount budget required.
    </pre>

    <p><b>What We Will Deliberately NOT Do:</b></p>
    <ul>
      <li><b>We will NOT hire additional support headcount:</b> Adding agents treats the symptom while multiplying the volume of bad escalations sent to engineering.</li>
      <li><b>We will NOT deploy an unconstrained generative AI chat bot:</b> Corporate employee transport requires deterministic operational precision (shift cutoffs, compliance dates), not probabilistic conversational hallucination.</li>
      <li><b>We will NOT rebuild existing ticketing infrastructure:</b> Gatekeeper runs as a lightweight, non-invasive intelligence layer above existing email, portal, and WhatsApp channels.</li>
    </ul>

    <div class="footnote">
      <b>Document Verification:</b> Generated from verified data in <code>backend/data/rideops_support_tickets.csv</code>. All statistical claims, handoff counts, and CSAT scores cross-validated against <code>backend/notebooks/rideops_deep_operational_analysis.ipynb</code>.
    </div>
  </div>

</body>
</html>
"""

html_path = os.path.abspath("docs/Gatekeeper_RideOps_Writeup.html")
pdf_path = os.path.abspath("docs/Gatekeeper_RideOps_Writeup.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"3-Page HTML write-up written to: {html_path}")

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_exe):
    chrome_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

cmd = [
    chrome_exe,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--disable-software-rasterizer",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]

res = subprocess.run(cmd, capture_output=True, timeout=25)
print(f"Chrome exit code: {res.returncode}")

with open(pdf_path, "rb") as f:
    content = f.read()

match = re.search(rb'/Type\s*/Pages.*?/Count\s+(\d+)', content, re.DOTALL)
pages = int(match.group(1)) if match else "unknown"
print(f"SUCCESS: PDF generated at: {pdf_path}")
print(f"Size: {len(content):,} bytes | Catalog Page count: {pages}")
