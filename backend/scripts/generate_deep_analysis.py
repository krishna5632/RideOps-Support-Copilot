import os
import sys
import json
import base64
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import nbformat as nbf

base_dir = r"c:\Users\prave\Downloads\RideOps_CaseStudy"
notebooks_dir = os.path.join(base_dir, "backend", "notebooks")
os.makedirs(notebooks_dir, exist_ok=True)
os.environ['MPLCONFIGDIR'] = os.path.join(base_dir, '.matplotlib_cache')
os.makedirs(os.path.join(base_dir, '.matplotlib_cache'), exist_ok=True)

# Visual styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 140
plt.rcParams['font.sans-serif'] = 'Arial'

# 1. Load Data
csv_path = os.path.join(base_dir, 'rideops_support_tickets.csv')
dict_path = os.path.join(base_dir, 'rideops_data_dictionary.csv')
df = pd.read_csv(csv_path)

# Datetime & Feature Engineering
for col in ['created_at', 'first_response_at', 'first_closed_at', 'final_closed_at']:
    df[col] = pd.to_datetime(df[col])

df['created_month'] = df['created_at'].dt.to_period('M').astype(str)
df['created_week'] = df['created_at'].dt.to_period('W').astype(str)
df['created_hour'] = df['created_at'].dt.hour
df['created_dow'] = df['created_at'].dt.day_name()
df['resolution_hrs'] = (df['final_closed_at'] - df['created_at']).dt.total_seconds() / 3600.0
df['frt_hrs'] = (df['first_response_at'] - df['created_at']).dt.total_seconds() / 3600.0
df['is_escalated'] = df['escalated_to_eng'] == 'Yes'
df['is_closed'] = df['status'] == 'Closed'

# Classification of engineering outcome
def classify_outcome(row):
    if not row['is_escalated']:
        return 'L1 Resolved'
    outcome = str(row['eng_outcome']).strip()
    if outcome == 'Fixed':
        return 'Legitimate Bug (Fixed)'
    elif outcome in ['Configuration error', 'Missing information', 'Duplicate', 'Not a bug / How-to']:
        return f'Escalation Waste ({outcome})'
    else:
        return 'Eng In-Progress / Open'

df['escalation_classification'] = df.apply(classify_outcome, axis=1)

print(f"Data Loaded: {len(df)} tickets, {df['client_id'].nunique()} clients.")

# --- FIGURE GENERATION ---
# Fig 1: Inflow Surge & Hourly Distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
weekly = df.groupby('created_week')['ticket_id'].count()
ax1.plot(range(len(weekly)), weekly.values, marker='o', color='#2563eb', linewidth=2.5, markersize=6)
ax1.set_xticks(range(len(weekly)))
ax1.set_xticklabels([w.split('/')[-1] for w in weekly.index], rotation=45, ha='right', fontsize=9)
ax1.set_title('Weekly Ticket Inflow (+88% Peak Surge)', fontsize=12, fontweight='bold', pad=10)
ax1.set_ylabel('New Tickets Created')
ax1.set_xlabel('Calendar Week (July - Sept 2026)')
ax1.axvline(x=len(weekly)-2, color='#e11d48', linestyle='--', alpha=0.7, label='Peak Surge Week')
ax1.legend(loc='upper left', frameon=True)

hourly = df.groupby('created_hour')['ticket_id'].count()
bars = ax2.bar(hourly.index, hourly.values, color='#3b82f6', width=0.7, edgecolor='none')
for h in [6, 7, 8, 9, 17, 18, 19]:
    if h in hourly.index:
        bars[h].set_color('#f59e0b')
ax2.set_title('Hourly Ticket Arrival (AM & PM Shift Spikes)', fontsize=12, fontweight='bold', pad=10)
ax2.set_xlabel('Hour of Day (24h UTC/Local)')
ax2.set_ylabel('Total Tickets')
ax2.set_xticks(range(0, 24, 2))
fig.tight_layout()
fig1_path = os.path.join(notebooks_dir, 'fig1_inflow_surge_and_hourly.png')
fig.savefig(fig1_path, bbox_inches='tight')
plt.close(fig)

# Fig 2: Engineering Outcome Waste Breakdown
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
eng_df = df[df['is_escalated']].copy()
outcomes = eng_df['eng_outcome'].value_counts(dropna=False)
outcome_labels = [str(x) if pd.notna(x) else 'Open / In-Progress' for x in outcomes.index]

colors = ['#10b981', '#ef4444', '#f97316', '#eab308', '#8b5cf6', '#64748b']
ax1.pie(outcomes.values, labels=outcome_labels, autopct='%1.1f%%', startangle=140, colors=colors,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
ax1.set_title('Escalated Tickets Breakdown (n=486)\n56.6% Avoidable Triage Waste', fontsize=12, fontweight='bold')

waste_counts = eng_df['escalation_classification'].value_counts()
categories_waste = eng_df[eng_df['eng_outcome'].isin(['Configuration error', 'Missing information', 'Duplicate', 'Not a bug / How-to'])]
waste_by_cat = categories_waste['category'].value_counts()
bars2 = ax2.barh(waste_by_cat.index, waste_by_cat.values, color='#ef4444', edgecolor='none')
ax2.set_title('Avoidable Engineering Waste by Category (n=275)', fontsize=12, fontweight='bold', pad=10)
ax2.set_xlabel('Number of False Escalations')
for bar in bars2:
    w = bar.get_width()
    ax2.text(w + 2, bar.get_y() + bar.get_height()/2, f'{int(w)}', va='center', fontsize=10, fontweight='bold')
ax2.set_xlim(0, max(waste_by_cat.values) * 1.15)
fig.tight_layout()
fig2_path = os.path.join(notebooks_dir, 'fig2_engineering_outcome_waste.png')
fig.savefig(fig2_path, bbox_inches='tight')
plt.close(fig)

# Fig 3: Resolution Time Comparison (Ping-Pong Latency)
fig, ax = plt.subplots(figsize=(10, 5))
closed_df = df[df['is_closed']].copy()
outcome_order = ['L1 Resolved (No Escalation)', 'Fixed', 'Duplicate', 'Not a bug / How-to', 'Configuration error', 'Missing information']
closed_df['display_outcome'] = closed_df.apply(
    lambda r: 'L1 Resolved (No Escalation)' if not r['is_escalated'] else str(r['eng_outcome']), axis=1
)
medians = closed_df.groupby('display_outcome')['resolution_hrs'].median().reindex(outcome_order)
colors_res = ['#10b981', '#3b82f6', '#f59e0b', '#f59e0b', '#ef4444', '#ef4444']
bars = ax.barh(outcome_order, medians.values, color=colors_res, edgecolor='none', height=0.6)
ax.set_title('Median Resolution Time by Resolution Path\n(False Escalations Trigger 5-Day Ping-Pong Delay)', fontsize=12, fontweight='bold', pad=15)
ax.set_xlabel('Median Resolution Time (Hours)')
for bar in bars:
    w = bar.get_width()
    days = w / 24.0
    ax.text(w + 2, bar.get_y() + bar.get_height()/2, f'{w:.1f} hrs ({days:.1f} days)', va='center', fontsize=9.5, fontweight='bold')
ax.set_xlim(0, 150)
ax.axvline(x=24, color='#64748b', linestyle=':', label='24-Hour SLA Marker')
ax.legend(loc='lower right', frameon=True)
fig.tight_layout()
fig3_path = os.path.join(notebooks_dir, 'fig3_turnaround_pingpong_latency.png')
fig.savefig(fig3_path, bbox_inches='tight')
plt.close(fig)

# Fig 4: Category Pareto & Cumulative Escalation Concentration
fig, ax1 = plt.subplots(figsize=(11, 5))
cat_agg = df.groupby('category').agg(
    total=('ticket_id', 'count'),
    escalated=('is_escalated', 'sum')
).sort_values('escalated', ascending=False)
cat_agg['cum_pct'] = cat_agg['escalated'].cumsum() / cat_agg['escalated'].sum() * 100

x = range(len(cat_agg))
ax1.bar(x, cat_agg['escalated'], color='#1e293b', width=0.55, label='Escalated to Engineering')
ax1.set_xticks(x)
ax1.set_xticklabels(cat_agg.index, rotation=35, ha='right', fontsize=9.5)
ax1.set_ylabel('Escalated Ticket Volume', fontweight='bold')
ax1.set_title('Category Pareto: Top 3 Categories Account for 78.0% of All Escalations', fontsize=12, fontweight='bold', pad=12)

ax2 = ax1.twinx()
ax2.plot(x, cat_agg['cum_pct'], color='#f59e0b', marker='s', linewidth=2.5, markersize=6, label='Cumulative Escalation %')
ax2.set_ylabel('Cumulative % of Escalations', color='#d97706', fontweight='bold')
ax2.set_ylim(0, 110)
ax2.axhline(y=80, color='#ef4444', linestyle='--', alpha=0.6, label='80% Pareto Cutoff')
for i, txt in enumerate(cat_agg['cum_pct']):
    ax2.annotate(f"{txt:.1f}%", (i, txt + 3), ha='center', fontsize=9, fontweight='bold', color='#b45309')
fig.tight_layout()
fig4_path = os.path.join(notebooks_dir, 'fig4_category_pareto_concentration.png')
fig.savefig(fig4_path, bbox_inches='tight')
plt.close(fig)

# Fig 5: Client Tier Analysis & Concentration
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
tier_df = df.groupby('client_tier').agg(
    total_tickets=('ticket_id', 'count'),
    escalation_rate=('is_escalated', lambda x: x.mean() * 100),
    avg_csat=('csat_score', 'mean')
).reindex(['Enterprise', 'Mid-market', 'SMB'])

ax1.bar(tier_df.index, tier_df['total_tickets'], color=['#0f172a', '#3b82f6', '#94a3b8'], width=0.5)
ax1.set_title('Ticket Volume by Client Tier', fontsize=12, fontweight='bold')
ax1.set_ylabel('Total Tickets')
for i, v in enumerate(tier_df['total_tickets']):
    ax1.text(i, v + 15, f'{v} ({v/len(df)*100:.1f}%)', ha='center', fontweight='bold', fontsize=9.5)

client_vol = df.groupby('client_id')['ticket_id'].count().sort_values(ascending=False)
cum_clients = np.linspace(0, 100, len(client_vol))
cum_vol = np.cumsum(client_vol.values) / client_vol.sum() * 100
ax2.plot(cum_clients, cum_vol, color='#2563eb', linewidth=2.5, label='Actual Distribution')
ax2.plot([0, 100], [0, 100], color='#94a3b8', linestyle='--', label='Perfect Equality (Baseline)')
ax2.fill_between(cum_clients, cum_vol, cum_clients, alpha=0.15, color='#3b82f6')
ax2.set_title('Client Concentration (Top 20% Clients = 42% Volume)', fontsize=12, fontweight='bold')
ax2.set_xlabel('% of Corporate Clients')
ax2.set_ylabel('Cumulative % of Tickets')
ax2.legend(loc='lower right', frameon=True)
fig.tight_layout()
fig5_path = os.path.join(notebooks_dir, 'fig5_client_tier_and_concentration.png')
fig.savefig(fig5_path, bbox_inches='tight')
plt.close(fig)

# Fig 6: Agent Performance & Escalation Variance
fig, ax = plt.subplots(figsize=(10, 5))
agent_stats = df.groupby('assigned_agent').agg(
    total=('ticket_id', 'count'),
    escalation_rate=('is_escalated', lambda x: x.mean() * 100),
    avg_csat=('csat_score', 'mean')
).sort_values('escalation_rate', ascending=True)

y_pos = range(len(agent_stats))
bars = ax.barh(y_pos, agent_stats['escalation_rate'], color='#3b82f6', height=0.55)
ax.set_yticks(y_pos)
ax.set_yticklabels(agent_stats.index, fontsize=10, fontweight='bold')
ax.axvline(x=df['is_escalated'].mean() * 100, color='#e11d48', linestyle='--', linewidth=2, label=f"Team Average ({df['is_escalated'].mean()*100:.1f}%)")
ax.set_title('Escalation Rate Variance Across Support Agents\n(Significant Variance: 24.5% to 41.2%)', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Escalation Rate (%)')
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.8, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', fontsize=9.5, fontweight='bold')
ax.set_xlim(0, 50)
ax.legend(loc='lower right', frameon=True)
fig.tight_layout()
fig6_path = os.path.join(notebooks_dir, 'fig6_agent_performance_variance.png')
fig.savefig(fig6_path, bbox_inches='tight')
plt.close(fig)

# Fig 7: CSAT Impact & Reopens
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
csat_by_esc = df.dropna(subset=['csat_score']).groupby('is_escalated')['csat_score'].agg(['mean', 'median', 'count'])
bars_esc = ax1.bar(['Resolved by L1\n(No Escalation)', 'Escalated to\nEngineering'], csat_by_esc['mean'],
                   color=['#10b981', '#ef4444'], width=0.45)
ax1.set_title('Impact of Escalation on CSAT Score', fontsize=12, fontweight='bold', pad=10)
ax1.set_ylabel('Mean CSAT Score (1.0 to 5.0)')
ax1.set_ylim(0, 5)
for bar in bars_esc:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, h + 0.15, f'{h:.2f} / 5.0', ha='center', fontweight='bold', fontsize=10)

csat_by_reopen = df.dropna(subset=['csat_score']).groupby('reopen_count')['csat_score'].mean()
bars_reopen = ax2.bar(csat_by_reopen.index.astype(str), csat_by_reopen.values, color=['#10b981', '#f59e0b', '#ef4444', '#7f1d1d'], width=0.45)
ax2.set_title('The Reopen Penalty on Customer CSAT', fontsize=12, fontweight='bold', pad=10)
ax2.set_xlabel('Number of Ticket Reopens')
ax2.set_ylabel('Mean CSAT Score')
ax2.set_ylim(0, 5)
for bar in bars_reopen:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, h + 0.15, f'{h:.2f}', ha='center', fontweight='bold', fontsize=10)
fig.tight_layout()
fig7_path = os.path.join(notebooks_dir, 'fig7_csat_multivariate_drivers.png')
fig.savefig(fig7_path, bbox_inches='tight')
plt.close(fig)

# Fig 8: Simulation / ROI Model of L1 Gatekeeper + QuickFix
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
baseline_waste = 275
reclaimed_waste = int(baseline_waste * 0.70)
remaining_waste = baseline_waste - reclaimed_waste

ax1.bar(['Current Baseline\n(Q3 Actual)', 'With Gatekeeper\n(Projected)'], [baseline_waste, remaining_waste],
        color=['#ef4444', '#10b981'], width=0.45)
ax1.set_title('Escalation Waste Volume Reduction\n(-70% False Escalations Eliminated)', fontsize=12, fontweight='bold', pad=10)
ax1.set_ylabel('Total Avoidable Escalations / Quarter')
ax1.text(0, baseline_waste + 6, f'{baseline_waste} tickets', ha='center', fontweight='bold', fontsize=10)
ax1.text(1, remaining_waste + 6, f'{remaining_waste} tickets (-70%)', ha='center', fontweight='bold', fontsize=10, color='#047857')

dev_hrs_baseline = baseline_waste * 2.0
dev_hrs_projected = remaining_waste * 2.0
hrs_saved = dev_hrs_baseline - dev_hrs_projected
ax2.bar(['Dev Triage Time\n(Baseline)', 'Dev Triage Time\n(With Gatekeeper)'], [dev_hrs_baseline, dev_hrs_projected],
        color=['#f97316', '#3b82f6'], width=0.45)
ax2.set_title(f'Engineering Bandwidth Reclaimed\n(~{int(hrs_saved)} Senior Dev Hours Saved / Quarter)', fontsize=12, fontweight='bold', pad=10)
ax2.set_ylabel('Engineering Triage Hours')
ax2.text(0, dev_hrs_baseline + 10, f'{int(dev_hrs_baseline)} hrs', ha='center', fontweight='bold', fontsize=10)
ax2.text(1, dev_hrs_projected + 10, f'{int(dev_hrs_projected)} hrs', ha='center', fontweight='bold', fontsize=10, color='#1d4ed8')
fig.tight_layout()
fig8_path = os.path.join(notebooks_dir, 'fig8_simulation_impact_roi.png')
fig.savefig(fig8_path, bbox_inches='tight')
plt.close(fig)

print("All 8 figures generated successfully in backend/notebooks!")
