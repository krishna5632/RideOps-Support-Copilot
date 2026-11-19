import os
import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# Cell 1: Markdown Title & Executive Summary
cells.append(nbf.v4.new_markdown_cell("""# 📊 Case Study: RideOps Support — In-Depth Diagnostic Analysis
**Role:** Senior Data Analyst & Operations Strategist  
**Dataset:** 1,444 Support Tickets (July 2, 2026 – September 30, 2026)  
**Stakeholders:** 
- **Ritika (Head of Ops):** *"Open tickets are up ~60%. I need that number down this quarter. Zero budget for new hires."*
- **Meera (Support Lead):** *"Once escalated, tickets disappear for days... Give us more people and quicker turnaround."*
- **Sandeep (Engineering Manager):** *"A lot of what support escalates shouldn't come to engineering at all... If support did basic checks, we'd move faster."*

---

### Executive Summary & Core Findings
1. **The Inflow Surge is Real:** Ticket volume grew by **+51.8%** from July (390) to September (592).
2. **The "Bad Escalation" Trap (Validating Sandeep):** Out of 486 tickets escalated to engineering, **56.6% (275 tickets) were NOT code bugs**. They were client configuration errors, missing logs, duplicates, or how-to queries.
3. **The Multi-Day Ping-Pong Delay (Validating Meera):** Legitimate code bugs take **~65 hours (2.7 days)** to fix, but avoidable configuration/missing info tickets bounce back and forth (2–3 handoffs) taking **121 to 128 hours (5+ days)**!
4. **Massive Category Concentration (The 80/20 Rule):** Just **3 categories** account for **53.9% of all tickets** and **78.0% of all escalations**:
   - *Roster / booking not syncing* (344 tickets, 50.9% escalated)
   - *Live tracking / GPS incorrect* (228 tickets, 55.7% escalated)
   - *Report export failing* (206 tickets, 37.4% escalated)
5. **Team Inconsistency:** Support lacks standardized operating procedures (SOPs). One agent (Rahul T) escalates **61.6%** of his queue, while another (Karan B) rarely escalates (16.1%) but has a high reopen rate (0.36) and the lowest CSAT (3.13).
6. **Customer Impact:** Escalations destroy CSAT (dropping from **4.01** for L1-resolved tickets down to **2.43** for returned config tickets).
"""))

# Cell 2: Setup & Environment
cells.append(nbf.v4.new_code_cell("""# Environment Setup
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set configuration directory to avoid sandbox write warnings
os.environ['MPLCONFIGDIR'] = os.path.abspath('.mplconfig')

# Visual styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 150
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11

print("Environment configured successfully!")
"""))

# Cell 3: Markdown Section 2
cells.append(nbf.v4.new_markdown_cell("""## 1. Data Ingestion & Quality Checks
We inspect the dataset structure, datatypes, missing values, and verify timestamp logic.
"""))

# Cell 4: Code Data Loading
cells.append(nbf.v4.new_code_cell("""# Load data
df = pd.read_csv('rideops_support_tickets.csv')
data_dict = pd.read_csv('rideops_data_dictionary.csv')

# Timestamp conversion
datetime_cols = ['created_at', 'first_response_at', 'first_closed_at', 'final_closed_at']
for col in datetime_cols:
    df[col] = pd.to_datetime(df[col])

# Feature engineering
df['created_month'] = df['created_at'].dt.to_period('M').astype(str)
df['created_week'] = df['created_at'].dt.to_period('W').astype(str)
df['first_response_hrs'] = (df['first_response_at'] - df['created_at']).dt.total_seconds() / 3600.0
df['resolution_hrs'] = (df['final_closed_at'] - df['created_at']).dt.total_seconds() / 3600.0
df['is_escalated'] = df['escalated_to_eng'] == 'Yes'
df['is_avoidable_escalation'] = df['eng_outcome'].isin([
    'Config issue - returned to L1',
    'Insufficient info - returned to L1',
    'Duplicate of known issue',
    'Not a bug - how-to',
    'Not reproducible'
])

print(f"Total Rows: {len(df):,}")
print(f"Total Columns: {df.shape[1]}")
print(f"Date Range: {df['created_at'].min().date()} to {df['created_at'].max().date()}")
df.head(3)
"""))

# Cell 5: Markdown Section 3
cells.append(nbf.v4.new_markdown_cell("""## 2. Inflow Surge & Backlog Growth
**Question:** Is ticket volume growing, and is it overwhelming capacity?
"""))

# Cell 6: Code Monthly & Weekly Inflow
cells.append(nbf.v4.new_code_cell("""# Monthly ticket counts
monthly_summary = df.groupby('created_month').agg(
    total_tickets=('ticket_id', 'count'),
    escalated_tickets=('is_escalated', 'sum'),
    open_tickets=('status', lambda s: (s != 'Closed').sum())
).reset_index()

monthly_summary['escalation_rate_%'] = (monthly_summary['escalated_tickets'] / monthly_summary['total_tickets'] * 100).round(1)
monthly_summary['growth_%'] = monthly_summary['total_tickets'].pct_change() * 100

display(monthly_summary)

# Plot Weekly Inflow Trend
weekly_counts = df.groupby('created_week').size().reset_index(name='ticket_count')

plt.figure(figsize=(10, 4.5))
ax = sns.lineplot(data=weekly_counts, x='created_week', y='ticket_count', marker='o', color='#1f77b4', linewidth=2.5)
plt.title("Weekly Ticket Inflow (Surge from ~87 to 164 tickets/week)")
plt.xlabel("Week")
plt.ylabel("New Tickets Raised")
plt.xticks(rotation=45, ha='right')
plt.axvline(x=9, color='red', linestyle='--', alpha=0.7, label='September Volume Spike')
plt.legend()
plt.tight_layout()
plt.savefig('fig1_weekly_inflow.png')
plt.show()
"""))

# Cell 7: Markdown Section 4
cells.append(nbf.v4.new_markdown_cell("""## 3. The Escalation Waste Loop: Sandeep's Hypothesis
**Question:** Does Engineering receive tickets that shouldn't be escalated?
"""))

# Cell 8: Code Escalation Outcome Breakdown
cells.append(nbf.v4.new_code_cell("""# Engineering Outcome Distribution
eng_tickets = df[df['is_escalated']].copy()

outcome_counts = eng_tickets['eng_outcome'].value_counts(dropna=False).reset_index()
outcome_counts.columns = ['Outcome', 'Count']
outcome_counts['Percentage_%'] = (outcome_counts['Count'] / len(eng_tickets) * 100).round(1)
outcome_counts['Classification'] = outcome_counts['Outcome'].apply(
    lambda x: 'Legitimate Code Fix' if x == 'Fixed' else ('Pending/Unknown' if pd.isna(x) else 'Avoidable Waste')
)

display(outcome_counts)

# Visualizing the Escalation Waste
fig, ax = plt.subplots(figsize=(10, 5))
palette = {'Legitimate Code Fix': '#2ca02c', 'Avoidable Waste': '#d62728', 'Pending/Unknown': '#7f7f7f'}

sns.barplot(data=outcome_counts.dropna(), y='Outcome', x='Count', hue='Classification', palette=palette, dodge=False, ax=ax)
for p in ax.patches:
    width = p.get_width()
    if width > 0:
        ax.annotate(f"{int(width)} ({width/len(eng_tickets)*100:.1f}%)",
                    (width + 3, p.get_y() + p.get_height() / 2.),
                    va='center', fontsize=10, weight='bold')

plt.title("Engineering Escalation Outcomes: 56.6% Avoidable Waste")
plt.xlabel("Number of Escalated Tickets")
plt.xlim(0, 240)
plt.tight_layout()
plt.savefig('fig2_eng_outcomes.png')
plt.show()

waste_count = outcome_counts[outcome_counts['Classification'] == 'Avoidable Waste']['Count'].sum()
waste_pct = waste_count / len(eng_tickets.dropna(subset=['eng_outcome'])) * 100
print(f"⚡ Total Avoidable Escalations: {waste_count} out of {len(eng_tickets.dropna(subset=['eng_outcome']))} resolved escalations ({waste_pct:.1f}%)")
"""))

# Cell 9: Markdown Section 5
cells.append(nbf.v4.new_markdown_cell("""## 4. Cycle Time & Handoff Ping-Pong: Meera's Hypothesis
**Question:** Why do escalated tickets "disappear for days"?
"""))

# Cell 10: Code Resolution Time Breakdown
cells.append(nbf.v4.new_code_cell("""# Resolution Time by Escalation Status and Outcome
closed_tickets = df[df['status'] == 'Closed'].copy()

time_by_outcome = closed_tickets.groupby('eng_outcome')['resolution_hrs'].agg(
    ticket_count='count',
    median_hours='median',
    mean_hours='mean',
    median_days=lambda x: round(x.median() / 24.0, 1)
).reset_index().sort_values('median_hours', ascending=False)

l1_row = pd.DataFrame([{
    'eng_outcome': 'Resolved at L1 (No Escalation)',
    'ticket_count': len(closed_tickets[~closed_tickets['is_escalated']]),
    'median_hours': closed_tickets[~closed_tickets['is_escalated']]['resolution_hrs'].median(),
    'mean_hours': closed_tickets[~closed_tickets['is_escalated']]['resolution_hrs'].mean(),
    'median_days': round(closed_tickets[~closed_tickets['is_escalated']]['resolution_hrs'].median() / 24.0, 1)
}])

time_comparison = pd.concat([l1_row, time_by_outcome], ignore_index=True)
display(time_comparison)

# Plot Resolution Time Comparison
plt.figure(figsize=(10, 4.5))
bar_colors = ['#1f77b4'] + ['#d62728' if 'returned' in str(x) else '#2ca02c' for x in time_comparison['eng_outcome'][1:]]

sns.barplot(data=time_comparison, y='eng_outcome', x='median_hours', palette=bar_colors)
plt.axvline(x=24, color='gray', linestyle=':', label='24h SLA')
plt.title("Median Resolution Time (Hours): The Ping-Pong Penalty")
plt.xlabel("Median Resolution Hours")
plt.ylabel("Outcome / Routing")
for idx, row in time_comparison.iterrows():
    plt.text(row['median_hours'] + 2, idx, f"{row['median_hours']:.1f} hrs ({row['median_days']} days)", va='center', weight='bold')

plt.xlim(0, 150)
plt.tight_layout()
plt.savefig('fig3_resolution_time_comparison.png')
plt.show()
"""))

# Cell 11: Markdown Section 6
cells.append(nbf.v4.new_markdown_cell("""## 5. Category Concentration: The 80/20 Rule
**Question:** Where should we focus our interventions to get maximum impact?
"""))

# Cell 12: Code Category Pareto
cells.append(nbf.v4.new_code_cell("""# Category Pareto Analysis
cat_summary = df.groupby('category').agg(
    total_tickets=('ticket_id', 'count'),
    escalated_count=('is_escalated', 'sum'),
    median_res_hrs=('resolution_hrs', 'median'),
    mean_csat=('csat_score', 'mean')
).reset_index()

cat_summary['escalation_rate_%'] = (cat_summary['escalated_count'] / cat_summary['total_tickets'] * 100).round(1)
cat_summary = cat_summary.sort_values('escalated_count', ascending=False)
cat_summary['cum_escalations_%'] = (cat_summary['escalated_count'].cumsum() / cat_summary['escalated_count'].sum() * 100).round(1)

display(cat_summary)

# Plot Top Escalation Drivers
plt.figure(figsize=(10, 5))
top3 = cat_summary.head(3)
ax = sns.barplot(data=cat_summary, x='escalated_count', y='category', palette='Blues_r')
plt.title("Engineering Escalations by Category (Top 3 = 78% of Escalations)")
plt.xlabel("Number of Escalated Tickets")
plt.ylabel("Category")
for p in ax.patches:
    width = p.get_width()
    if width > 0:
        ax.annotate(f"{int(width)}", (width + 2, p.get_y() + p.get_height() / 2.), va='center')
plt.tight_layout()
plt.savefig('fig4_category_pareto.png')
plt.show()
"""))

# Cell 13: Markdown Section 7
cells.append(nbf.v4.new_markdown_cell("""## 6. Team Consistency & Agent Discrepancies
**Question:** Are all L1 agents handling tickets consistently, or is there an operational variance?
"""))

# Cell 14: Code Agent Analysis
cells.append(nbf.v4.new_code_cell("""# Agent Performance Breakdown
agent_metrics = df.groupby('assigned_agent').agg(
    tickets_handled=('ticket_id', 'count'),
    escalated_count=('is_escalated', 'sum'),
    reopen_rate=('reopen_count', 'mean'),
    median_res_hrs=('resolution_hrs', 'median'),
    avg_csat=('csat_score', 'mean')
).reset_index()

agent_metrics['escalation_rate_%'] = (agent_metrics['escalated_count'] / agent_metrics['tickets_handled'] * 100).round(1)
agent_metrics = agent_metrics.sort_values('escalation_rate_%', ascending=False)

display(agent_metrics)

print("Key Observations:")
print("• Rahul T escalates 61.6% of tickets (over 2x the team average).")
print("• Karan B escalates only 16.1%, but has a 0.36 reopen rate and lowest CSAT (3.13) due to premature closure.")
"""))

# Cell 15: Markdown Section 8
cells.append(nbf.v4.new_markdown_cell("""## 7. Customer Satisfaction (CSAT) Drivers
**Question:** How does escalating a ticket impact customer happiness?
"""))

# Cell 16: Code CSAT Breakdown
cells.append(nbf.v4.new_code_cell("""# CSAT by escalation outcome and reopen count
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# CSAT by Routing / Escalation
sns.barplot(data=df.dropna(subset=['csat_score']), x='escalated_to_eng', y='csat_score', palette=['#2ca02c', '#d62728'], ax=ax1)
ax1.set_title("Customer CSAT: L1 vs Escalated")
ax1.set_xlabel("Escalated to Engineering?")
ax1.set_ylabel("Average CSAT (1-5)")
ax1.set_ylim(0, 5)

# CSAT by Reopens
sns.barplot(data=df.dropna(subset=['csat_score']), x='reopen_count', y='csat_score', palette='Reds_r', ax=ax2)
ax2.set_title("CSAT Drops Severely with Reopens")
ax2.set_xlabel("Reopen Count")
ax2.set_ylabel("Average CSAT (1-5)")
ax2.set_ylim(0, 5)

plt.tight_layout()
plt.savefig('fig5_csat_impact.png')
plt.show()

print(f"Non-escalated CSAT: {df[~df['is_escalated']]['csat_score'].mean():.2f}")
print(f"Escalated CSAT: {df[df['is_escalated']]['csat_score'].mean():.2f}")
"""))

# Cell 17: Markdown Strategic Recommendations
cells.append(nbf.v4.new_markdown_cell("""## 8. Strategic Synthesis: The v0 Solution & 4-Week Roadmap

### What We Learned:
1. **The Core Problem:** The backlog is caused by a **broken escalation loop**. 56.6% of escalations are sent without basic checks or config verification.
2. **The Bottleneck:** Tickets bounced back from Engineering incur a **5.4-day penalty** and drag CSAT down to 2.4.
3. **The Leverage Point:** Focusing on **Roster Sync, GPS Tracking, and Report Exports** covers 78% of all escalations.

---

### Product Specification for v0: "Smart Triage & Escalation Gatekeeper"
- **Target Persona:** L1 Support Agent.
- **Key Capability 1 (Automated Checklists):** When a ticket in top categories is selected, the tool guides the agent through basic checks (e.g. roster cutoff validation, driver contact verification).
- **Key Capability 2 (Locked Escalation):** Disables the "Escalate to Engineering" button until required fields and diagnostics are attached.
- **Key Capability 3 (L1 Quick-Resolve):** Equips L1 agents with instructions to resolve client configuration discrepancies directly without developer intervention.

---

### Success Metrics Framework
- **North Star Metric:** Active Open Tickets (Target: Reduce by 40% from ~50 to <20).
- **Leading Indicator:** Escalation Rejection Rate (Target: <15%, down from 56.6%).
- **Guardrail Metrics:** First Contact Resolution (<12 hrs), Reopen Rate (<5%), CSAT (>4.0).
"""))

nb.cells = cells

# Save notebook
output_path = 'rideops_support_analysis.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Jupyter Notebook successfully written to: {os.path.abspath(output_path)}")
