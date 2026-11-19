import os
import io
import base64
import contextlib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import nbformat as nbf

os.environ['MPLCONFIGDIR'] = os.path.abspath('.mplconfig')
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 140

print("Running senior data analyst workflow...")

# 1. Load data
df = pd.read_csv('rideops_support_tickets.csv')
data_dict = pd.read_csv('rideops_data_dictionary.csv')

# Conversions
datetime_cols = ['created_at', 'first_response_at', 'first_closed_at', 'final_closed_at']
for col in datetime_cols:
    df[col] = pd.to_datetime(df[col])

df['created_month'] = df['created_at'].dt.to_period('M').astype(str)
df['created_week'] = df['created_at'].dt.to_period('W').astype(str)
df['first_response_hrs'] = (df['first_response_at'] - df['created_at']).dt.total_seconds() / 3600.0
df['resolution_hrs'] = (df['final_closed_at'] - df['created_at']).dt.total_seconds() / 3600.0
df['is_escalated'] = df['escalated_to_eng'] == 'Yes'

# Chart 1: Inflow Trend
plt.figure(figsize=(9, 4.2))
weekly_counts = df.groupby('created_week').size().reset_index(name='ticket_count')
sns.lineplot(data=weekly_counts, x='created_week', y='ticket_count', marker='o', color='#1f77b4', linewidth=2.5)
plt.title("Weekly Ticket Inflow (Surge from ~87 to 164 tickets/week)", fontsize=13, weight='bold')
plt.xlabel("Week", fontsize=10)
plt.ylabel("New Tickets Raised", fontsize=10)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.axvline(x=9, color='#d62728', linestyle='--', alpha=0.7, label='September Volume Spike (+51.8%)')
plt.legend(frameon=True)
plt.tight_layout()
fig1_path = 'fig1_weekly_inflow.png'
plt.savefig(fig1_path)
plt.close()

# Chart 2: Escalation Outcomes (Waste vs Legitimate)
eng_tickets = df[df['is_escalated']].copy()
outcome_counts = eng_tickets['eng_outcome'].value_counts(dropna=False).reset_index()
outcome_counts.columns = ['Outcome', 'Count']
outcome_counts['Classification'] = outcome_counts['Outcome'].apply(
    lambda x: 'Legitimate Code Fix' if x == 'Fixed' else ('Pending' if pd.isna(x) else 'Avoidable Waste')
)

plt.figure(figsize=(9, 4.8))
palette = {'Legitimate Code Fix': '#2ca02c', 'Avoidable Waste': '#d62728', 'Pending': '#7f7f7f'}
ax2 = sns.barplot(data=outcome_counts.dropna(), y='Outcome', x='Count', hue='Classification', palette=palette, dodge=False)
for p in ax2.patches:
    w = p.get_width()
    if w > 0:
        ax2.annotate(f"{int(w)} ({w/len(eng_tickets)*100:.1f}%)",
                     (w + 3, p.get_y() + p.get_height() / 2.),
                     va='center', fontsize=9, weight='bold')
plt.title("Engineering Escalation Outcomes: 56.6% Avoidable Waste", fontsize=13, weight='bold')
plt.xlabel("Number of Escalated Tickets", fontsize=10)
plt.xlim(0, 245)
plt.tight_layout()
fig2_path = 'fig2_eng_outcomes.png'
plt.savefig(fig2_path)
plt.close()

# Chart 3: Cycle Time Penalty
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

plt.figure(figsize=(9, 4.5))
bar_colors = ['#1f77b4'] + ['#d62728' if 'returned' in str(x) else '#2ca02c' for x in time_comparison['eng_outcome'][1:]]
sns.barplot(data=time_comparison, y='eng_outcome', x='median_hours', palette=bar_colors)
plt.title("Median Resolution Time (Hours): The 5-Day Ping-Pong Penalty", fontsize=13, weight='bold')
plt.xlabel("Median Resolution Hours", fontsize=10)
plt.ylabel("Outcome / Route", fontsize=10)
for idx, row in time_comparison.iterrows():
    plt.text(row['median_hours'] + 2, idx, f"{row['median_hours']:.1f} hrs ({row['median_days']} d)", va='center', weight='bold', fontsize=9)
plt.xlim(0, 155)
plt.tight_layout()
fig3_path = 'fig3_resolution_time_comparison.png'
plt.savefig(fig3_path)
plt.close()

# Chart 4: Category Pareto
cat_summary = df.groupby('category').agg(
    total_tickets=('ticket_id', 'count'),
    escalated_count=('is_escalated', 'sum'),
    median_res_hrs=('resolution_hrs', 'median'),
    mean_csat=('csat_score', 'mean')
).reset_index().sort_values('escalated_count', ascending=False)
cat_summary['escalation_rate_%'] = (cat_summary['escalated_count'] / cat_summary['total_tickets'] * 100).round(1)

plt.figure(figsize=(9, 4.5))
ax4 = sns.barplot(data=cat_summary, x='escalated_count', y='category', palette='Blues_r')
plt.title("Engineering Escalations by Category (Top 3 = 78% of Escalations)", fontsize=13, weight='bold')
plt.xlabel("Number of Escalated Tickets", fontsize=10)
for p in ax4.patches:
    w = p.get_width()
    if w > 0:
        ax4.annotate(f"{int(w)}", (w + 2, p.get_y() + p.get_height() / 2.), va='center', fontsize=9)
plt.tight_layout()
fig4_path = 'fig4_category_pareto.png'
plt.savefig(fig4_path)
plt.close()

# Chart 5: CSAT Impact
fig, (ax_c1, ax_c2) = plt.subplots(1, 2, figsize=(10, 4.2))
sns.barplot(data=df.dropna(subset=['csat_score']), x='escalated_to_eng', y='csat_score', palette=['#2ca02c', '#d62728'], ax=ax_c1)
ax_c1.set_title("CSAT Drops from 4.01 to 3.11 on Escalation", fontsize=11, weight='bold')
ax_c1.set_ylabel("Average CSAT (1-5)", fontsize=10)
ax_c1.set_ylim(0, 5)

sns.barplot(data=df.dropna(subset=['csat_score']), x='reopen_count', y='csat_score', palette='Reds_r', ax=ax_c2)
ax_c2.set_title("CSAT Crashes to 1.33 on 2 Reopens", fontsize=11, weight='bold')
ax_c2.set_ylabel("Average CSAT (1-5)", fontsize=10)
ax_c2.set_ylim(0, 5)
plt.tight_layout()
fig5_path = 'fig5_csat_impact.png'
plt.savefig(fig5_path)
plt.close()

print("All charts generated and saved successfully!")
