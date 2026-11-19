import os
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# Section 1
cells.append(nbf.v4.new_markdown_cell("""# 📊 Case Study: RideOps Support — Root Cause & Strategic Analysis
**Author:** Senior Product & Operations Data Analyst  
**Scope:** 1,444 Support Tickets (July 2, 2026 – September 30, 2026)  
**Target Audience:** Ritika (Head of Ops), Meera (Support Lead), Sandeep (Engineering Manager)  

---

## 🎯 Executive Summary & The Core Conflict
The leadership team at RideOps is facing an operational crisis:
* **Ritika (Head of Ops):** *"Open tickets are up ~60% since July and our clients are noticing. I have no budget for new hires."*
* **Meera (Support Lead):** *"Engineering is the bottleneck. Escalated tickets disappear for days. Give us more people and faster turnaround."*
* **Sandeep (Engineering Manager):** *"A lot of what support escalates shouldn't come to engineering at all. Engineers spend hours doing basic triage."*

### 📌 Summary of Hard Findings from the Data:
1. **The Inflow Surge is Real:** Monthly ticket volume rose **+51.8%** from July (390) to September (592).
2. **Sandeep's Claim is Validated (56.6% Waste):** Out of 486 tickets escalated to Engineering, **275 (56.6%) were NOT software bugs**. They were client config issues (84), missing information (89), duplicate tickets (56), or how-to queries (24).
3. **Meera's Claim is Validated (The 5-Day Ping-Pong Delay):** While L1 resolves non-escalated tickets in **12.6 hours**, tickets escalated with configuration issues or missing info bounce back and forth (2 to 3 handoffs) taking **121 to 128 hours (5+ days)**.
4. **The 80/20 Concentration:** Just **3 categories** account for **78.0% of all escalations** (*Roster Sync*, *Live GPS*, and *Report Export*).
5. **CSAT Destruction:** Escalating a ticket drops customer satisfaction from **4.01** to **3.11**, and returned config errors crash satisfaction to **2.43**.
"""))

# Section 2: Code Loading
cells.append(nbf.v4.new_code_cell("""# 1. Environment Setup & Data Loading
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 140

df = pd.read_csv('rideops_support_tickets.csv')
data_dict = pd.read_csv('rideops_data_dictionary.csv')

# Timestamp conversion & Feature Engineering
for col in ['created_at', 'first_response_at', 'first_closed_at', 'final_closed_at']:
    df[col] = pd.to_datetime(df[col])

df['created_month'] = df['created_at'].dt.to_period('M').astype(str)
df['created_week'] = df['created_at'].dt.to_period('W').astype(str)
df['resolution_hrs'] = (df['final_closed_at'] - df['created_at']).dt.total_seconds() / 3600.0
df['is_escalated'] = df['escalated_to_eng'] == 'Yes'

print(f"Dataset successfully loaded: {len(df):,} tickets across {df['client_id'].nunique()} corporate clients.")
"""))

# Section 3: Monthly Inflow
cells.append(nbf.v4.new_markdown_cell("""## 2. Inflow Surge Analysis: Is Support Truly Drowning?
We first test Ritika's observation that ticket volume is overwhelming support.
"""))

cells.append(nbf.v4.new_code_cell("""# Monthly ticket trend
monthly_inflow = df.groupby('created_month').agg(
    total_tickets=('ticket_id', 'count'),
    escalated_tickets=('is_escalated', 'sum'),
    open_tickets=('status', lambda s: (s != 'Closed').sum())
).reset_index()

monthly_inflow['escalation_pct'] = (monthly_inflow['escalated_tickets'] / monthly_inflow['total_tickets'] * 100).round(1)
monthly_inflow['growth_vs_prior_month_%'] = monthly_inflow['total_tickets'].pct_change() * 100
monthly_inflow
"""))

cells.append(nbf.v4.new_markdown_cell("""### 📈 Visualizing Weekly Ticket Inflow
Between July and September, weekly ticket creation jumped from **87 tickets/week to a peak of 164 tickets/week (+88.5% peak surge)**.

![Weekly Ticket Inflow](fig1_weekly_inflow.png)
"""))

# Section 4: Escalation Waste Loop
cells.append(nbf.v4.new_markdown_cell("""## 3. Sandeep's Hypothesis: The 56.6% Escalation Waste Loop
Sandeep claimed: *"A lot of what support escalates shouldn't be coming to engineering at all."*
We evaluate `eng_outcome` across all 486 escalated tickets.
"""))

cells.append(nbf.v4.new_code_cell("""# Breakdown of engineering outcomes
eng_tickets = df[df['is_escalated']].copy()
outcome_table = eng_tickets['eng_outcome'].value_counts(dropna=False).reset_index()
outcome_table.columns = ['Engineering Outcome', 'Count']
outcome_table['Percentage_%'] = (outcome_table['Count'] / len(eng_tickets) * 100).round(1)

outcome_table['Verdict'] = outcome_table['Engineering Outcome'].apply(
    lambda x: 'Legitimate Bug Fix' if x == 'Fixed' else ('In-Progress / Open' if pd.isna(x) else 'Avoidable Escalation (Waste)')
)
outcome_table
"""))

cells.append(nbf.v4.new_markdown_cell("""### 📊 Escalation Outcome Chart
**Key Takeaway:** Only **43.4%** of escalations were legitimate software bugs. **56.6%** were avoidable waste that clogged engineering bandwidth.

![Escalation Outcomes](fig2_eng_outcomes.png)
"""))

# Section 5: Turnaround Time
cells.append(nbf.v4.new_markdown_cell("""## 4. Meera's Hypothesis: The 5-Day Ping-Pong Delay
Meera stated: *"Once we escalate a ticket, it disappears for days."*
We compare median resolution times between non-escalated tickets and escalated tickets by outcome.
"""))

cells.append(nbf.v4.new_code_cell("""# Turnaround comparison
closed_df = df[df['status'] == 'Closed'].copy()

res_stats = closed_df.groupby('eng_outcome')['resolution_hrs'].agg(
    tickets=('count'),
    median_hrs=('median'),
    mean_hrs=('mean'),
    median_days=(lambda x: round(x.median() / 24, 1))
).reset_index().sort_values('median_hrs', ascending=False)

l1_baseline = pd.DataFrame([{
    'eng_outcome': 'Resolved by L1 (No Escalation)',
    'tickets': len(closed_df[~closed_df['is_escalated']]),
    'median_hrs': closed_df[~closed_df['is_escalated']]['resolution_hrs'].median(),
    'mean_hrs': closed_df[~closed_df['is_escalated']]['resolution_hrs'].mean(),
    'median_days': round(closed_df[~closed_df['is_escalated']]['resolution_hrs'].median() / 24, 1)
}])

cycle_time_table = pd.concat([l1_baseline, res_stats], ignore_index=True)
cycle_time_table
"""))

cells.append(nbf.v4.new_markdown_cell("""### ⏱️ Turnaround Delay Chart
* A non-escalated ticket takes **12.6 hours**.
* A real bug takes **64.8 hours (~2.7 days)**.
* A bounced config error or missing info ticket takes **121 to 128 hours (5+ days)** due to multiple handoffs!

![Turnaround Comparison](fig3_resolution_time_comparison.png)
"""))

# Section 6: Category Pareto
cells.append(nbf.v4.new_markdown_cell("""## 5. Category Concentration: The 80/20 Rule
To fix the problem fast without new hires, where should we focus?
"""))

cells.append(nbf.v4.new_code_cell("""# Category Analysis
cat_df = df.groupby('category').agg(
    total_volume=('ticket_id', 'count'),
    escalated_volume=('is_escalated', 'sum'),
    median_resolution_hrs=('resolution_hrs', 'median'),
    average_csat=('csat_score', 'mean')
).reset_index().sort_values('escalated_volume', ascending=False)

cat_df['escalation_rate_%'] = (cat_df['escalated_volume'] / cat_df['total_volume'] * 100).round(1)
cat_df['cum_escalations_%'] = (cat_df['escalated_volume'].cumsum() / cat_df['escalated_volume'].sum() * 100).round(1)
cat_df
"""))

cells.append(nbf.v4.new_markdown_cell("""### 🎯 Top 3 Categories Account for 78% of Escalations
1. **Roster / booking not syncing:** 175 escalations
2. **Live tracking / GPS incorrect:** 127 escalations
3. **Report export failing:** 77 escalations

![Category Pareto](fig4_category_pareto.png)
"""))

# Section 7: Agent Performance & CSAT
cells.append(nbf.v4.new_markdown_cell("""## 6. Team Variance & Customer CSAT Impact
We examine whether all agents are performing uniformly and how routing decisions affect client CSAT.
"""))

cells.append(nbf.v4.new_code_cell("""# Agent breakdown
agent_df = df.groupby('assigned_agent').agg(
    tickets_assigned=('ticket_id', 'count'),
    escalated_count=('is_escalated', 'sum'),
    avg_reopens_per_ticket=('reopen_count', 'mean'),
    median_hrs=('resolution_hrs', 'median'),
    avg_csat=('csat_score', 'mean')
).reset_index()

agent_df['escalation_rate_%'] = (agent_df['escalated_count'] / agent_df['tickets_assigned'] * 100).round(1)
agent_df.sort_values('escalation_rate_%', ascending=False)
"""))

cells.append(nbf.v4.new_markdown_cell("""### 📉 CSAT Impact of Escalations & Reopens
* Escalating a ticket drops CSAT from **4.01 down to 3.11**.
* Reopening a ticket twice crashes CSAT to **1.33**.

![CSAT Impact](fig5_csat_impact.png)
"""))

# Section 8: Recommendations & Action Plan
cells.append(nbf.v4.new_markdown_cell("""## 7. Strategic Recommendations & v0 Specification

### 🛠️ What We Are Building: The "Smart Triage & Escalation Gatekeeper"
Instead of hiring new staff (Ritika's constraint), we equip L1 Support Agents with an interactive tool:
1. **Automated Diagnostic Checklist:** Instantly checks if a ticket is a known config issue (e.g. roster cutoff mismatch) before it ever reaches engineering.
2. **Escalation Gatekeeper:** Locks the "Escalate to Engineering" button until required logs (vehicle registration, driver phone, app version) are attached.
3. **L1 Quick-Fix Recipes:** Allows L1 to fix client configuration errors on the spot in under 15 minutes.

### 📐 Success Metrics
* **North Star Metric:** Active Open Backlog (Target: -40% reduction within 30 days).
* **Primary Operational Driver:** Escalation Rejection Rate (Target: reduce from 56.6% down to <15%).
* **Guardrails:** Keep CSAT $\ge 4.0$ and Reopen Rate $< 5\%$.
"""))

nb.cells = cells

with open('rideops_support_analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Updated rideops_support_analysis.ipynb with complete Senior Data Analyst content!")
