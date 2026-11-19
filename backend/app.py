import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Page configuration
st.set_page_config(
    page_title="RideOps Support Hub | Smart Triage & Gatekeeper",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom HookScene Design System CSS Injection
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global Base */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
    }
    
    .stApp {
        background-color: #FAFAFC;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Code / Monospace */
    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* HookScene App Header Bar */
    .hook-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 16px 24px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.02);
    }
    .hook-title {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .hook-badge-amber {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .hook-badge-green {
        background-color: #DCFCE7;
        color: #166534;
        border: 1px solid #BBF7D0;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .hook-badge-red {
        background-color: #FEE2E2;
        color: #991B1B;
        border: 1px solid #FECACA;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .hook-badge-slate {
        background-color: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
    }

    /* HookScene Content Cards */
    .hook-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.02);
    }
    .hook-card-subtle {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        margin-top: 14px;
    }

    /* KPI Metric Card */
    .hook-metric {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        border-top: 4px solid #E8A72D;
    }
    .hook-metric-title {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .hook-metric-val {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.03em;
    }
    .hook-metric-sub {
        font-size: 12px;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Diagnostic Callout Boxes */
    .hook-diagnostic-warning {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 5px solid #E8A72D;
        border-radius: 10px;
        padding: 16px;
        color: #92400E;
    }
    .hook-diagnostic-info {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 5px solid #0284C7;
        border-radius: 10px;
        padding: 16px;
        color: #0369A1;
    }
    .hook-diagnostic-success {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 5px solid #16A34A;
        border-radius: 10px;
        padding: 16px;
        color: #166534;
    }

    /* Primary Buttons Styled like HookScene Amber Primary */
    .stButton>button[kind="primary"] {
        background-color: #E8A72D !important;
        color: #0F172A !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        transition: all 0.15s ease !important;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #D9941E !important;
        color: #000000 !important;
        box-shadow: 0 4px 6px -1px rgba(232, 167, 45, 0.3) !important;
    }

    /* Secondary Buttons */
    .stButton>button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #334155 !important;
        font-weight: 600 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    .stButton>button[kind="secondary"]:hover {
        background-color: #F8FAFC !important;
        border-color: #94A3B8 !important;
        color: #0F172A !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-weight: 600 !important;
        color: #334155 !important;
    }

    /* Input Fields */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px !important;
        border-color: #E2E8F0 !important;
    }
</style>
""", unsafe_allow_html=True)

import os

# 1. Load Data
@st.cache_data
def load_data():
    candidates = [
        os.path.join(os.path.dirname(__file__), 'data', 'rideops_support_tickets.csv'),
        'rideops_support_tickets.csv',
        os.path.join('backend', 'data', 'rideops_support_tickets.csv')
    ]
    for p in candidates:
        if os.path.exists(p):
            df = pd.read_csv(p)
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['final_closed_at'] = pd.to_datetime(df['final_closed_at'])
            df['resolution_hrs'] = (df['final_closed_at'] - df['created_at']).dt.total_seconds() / 3600.0
            return df
    raise FileNotFoundError("Could not locate rideops_support_tickets.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading CSV file: {e}. Please ensure rideops_support_tickets.csv is present.")
    st.stop()

# Session State for tracking user actions
if 'deflected_count' not in st.session_state:
    st.session_state.deflected_count = 0
if 'escalated_count' not in st.session_state:
    st.session_state.escalated_count = 0
if 'resolved_tickets' not in st.session_state:
    st.session_state.resolved_tickets = set()

# Sidebar: HookScene Style
st.sidebar.markdown("""
<div style="padding: 10px 0 20px 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 15px;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 28px;">🚕</span>
        <div>
            <div style="font-weight: 800; font-size: 17px; color: #0F172A; letter-spacing: -0.02em;">RideOps Support</div>
            <div style="font-size: 11px; font-weight: 600; color: #E8A72D; letter-spacing: 0.05em; text-transform: uppercase;">Intelligence Desk</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

app_mode = st.sidebar.radio(
    "WORKSPACE NAVIGATION",
    ["🛡️ Review Desk (Smart Triage)", "📊 Analytics & Command Center", "⚙️ Client Quick-Fix Tools"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Live Session Impact")
st.sidebar.markdown(f"""
<div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
    <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">Deflected Escalations</div>
    <div style="font-size: 24px; font-weight: 800; color: #16A34A;">{st.session_state.deflected_count} tickets</div>
    <div style="font-size: 11px; color: #64748B; margin-top: 4px;">Saved Eng: <b>{st.session_state.deflected_count * 5.5:.1f} hrs</b></div>
</div>
""", unsafe_allow_html=True)

st.sidebar.caption("RideOps Enterprise Transport • Built for Ritika, Meera & Sandeep")

# Top Header Bar (HookScene Style)
st.markdown("""
<div class="hook-header">
    <div class="hook-title">
        <span>🚕</span>
        <span>RideOps Support Intelligence Hub</span>
        <span class="hook-badge-amber">v0.9 Active</span>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <span class="hook-badge-slate">1,444 Total Tickets</span>
        <span class="hook-badge-green">Target: -40% Backlog</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# TAB 1: REVIEW DESK (SMART TRIAGE)
# ==========================================
if app_mode == "🛡️ Review Desk (Smart Triage)":
    
    # Filter Controls Toolbar
    st.markdown('<div class="hook-card" style="padding: 16px 20px; margin-bottom: 20px;">', unsafe_allow_html=True)
    c_f1, c_f2, c_f3 = st.columns([2, 2, 2])
    with c_f1:
        category_filter = st.selectbox(
            "Category Scope:",
            ["All Top Categories", "Roster / booking not syncing", "Live tracking / GPS incorrect", "Report export failing", "OTP / boarding issue", "Login / access issue"]
        )
    with c_f2:
        risk_filter = st.selectbox(
            "Triage Priority Filter:",
            ["All Tickets", "⚠️ High Risk of Bad Escalation", "Open Tickets Only"]
        )
    with c_f3:
        agent_filter = st.selectbox(
            "Assigned Agent:",
            ["All Agents"] + sorted(df['assigned_agent'].unique().tolist())
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Filter Query
    filtered_df = df.copy()
    if category_filter != "All Top Categories":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    if agent_filter != "All Agents":
        filtered_df = filtered_df[filtered_df['assigned_agent'] == agent_filter]
    if risk_filter == "Open Tickets Only":
        filtered_df = filtered_df[filtered_df['status'] != 'Closed']
    elif risk_filter == "⚠️ High Risk of Bad Escalation":
        filtered_df = filtered_df[
            filtered_df['description'].str.contains('cutoff|stuck at loading|date range|insurance|duplicate|Excel|15 days', case=False, na=False)
        ]

    ticket_options = [
        f"{row['ticket_id']} — {row['client_name']} | {row['category']} | {row['description'][:42]}..."
        for _, row in filtered_df.head(60).iterrows()
    ]

    if not ticket_options:
        st.info("No tickets match the selected filters.")
        st.stop()

    selected_option = st.selectbox("Select Ticket from Queue to Inspect:", ticket_options)
    selected_ticket_id = selected_option.split(" — ")[0]
    ticket = df[df['ticket_id'] == selected_ticket_id].iloc[0]

    # Two Column Layout (HookScene Style)
    col_left, col_right = st.columns([1.1, 1.4])

    with col_left:
        st.markdown('<div class="hook-card">', unsafe_allow_html=True)
        st.markdown(f"### 📋 Ticket Inspection: `{ticket['ticket_id']}`")

        # Badges
        p_badge = {"P1": "hook-badge-red", "P2": "hook-badge-amber", "P3": "hook-badge-slate", "P4": "hook-badge-slate"}.get(ticket['priority'], "hook-badge-slate")
        st.markdown(f"""
        <div style="display: flex; gap: 8px; margin-bottom: 16px;">
            <span class="{p_badge}">{ticket['priority']} Criticality</span>
            <span class="hook-badge-slate">{ticket['client_tier']} Tier</span>
            <span class="hook-badge-slate">Via {ticket['channel']}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**Corporate Client:** `{ticket['client_id']}` — **{ticket['client_name']}**")
        st.markdown(f"**Category Tagged:** `{ticket['category']}`")
        st.markdown(f"**Assigned Owner:** `{ticket['assigned_agent']}`")
        st.markdown(f"**Inflow Timestamp:** `{ticket['created_at']}`")

        st.markdown('<div class="hook-card-subtle">', unsafe_allow_html=True)
        st.markdown("**User Problem Description:**")
        st.markdown(f"*{ticket['description']}*")
        st.markdown('</div>', unsafe_allow_html=True)

        if ticket['escalated_to_eng'] == 'Yes':
            st.markdown(f"""
            <div style="margin-top: 16px; padding: 12px; background: #FFF1F2; border: 1px solid #FECDD3; border-radius: 8px; font-size: 13px; color: #9F1239;">
                <b>Historical Benchmark for {ticket['ticket_id']}:</b><br>
                • Escalated to Eng: <b>Yes ({ticket['eng_ticket_id']})</b><br>
                • Eng Verdict: <b>{ticket['eng_outcome']}</b><br>
                • Bounce Handoffs: <b>{ticket['eng_handoffs']} times</b><br>
                • Resolution Duration: <b>{ticket['resolution_hrs']:.1f} hours ({ticket['resolution_hrs']/24:.1f} days)</b>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="hook-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 Diagnostic Brain & Pre-Escalation Gatekeeper")

        desc_lower = str(ticket['description']).lower()
        is_config_issue = False
        diagnosis_title = ""
        diagnosis_desc = ""
        action_guide = ""

        # Smart Heuristic Classifier
        if "cutoff" in desc_lower:
            is_config_issue = True
            diagnosis_title = "🛑 Known Client Configuration Issue: Shift Cutoff Mismatch"
            diagnosis_desc = "Client admin updated shift cutoff settings in the HR portal, but bookings occurred past the cutoff window. This is NOT a software bug."
            action_guide = "1. Advise admin to approve late exception in portal.\n2. Or click 'Apply Cutoff Sync' below to resolve immediately."

        elif "date range" in desc_lower or "> 15 days" in desc_lower or "stuck at loading" in desc_lower:
            is_config_issue = True
            diagnosis_title = "⚠️ Known System Capacity Limit: Export Date Range"
            diagnosis_desc = "Database join timeout caused by requesting >14 days of raw GPS coordinates. Operational usage limit, not an engineering crash."
            action_guide = "Advise client admin to export report in 7-day or 10-day intervals. Downloads finish in under 8 seconds."

        elif "insurance expired" in desc_lower or "compliance" in desc_lower:
            is_config_issue = True
            diagnosis_title = "📋 Vendor Compliance Block: Vehicle Document Expired"
            diagnosis_desc = "Vehicle blocked by RideOps safety engine due to expired fitness/insurance certificates. Engineering cannot override safety rules."
            action_guide = "Notify Vendor Ops team to upload renewed insurance document in Vendor Portal."

        elif "cab location frozen" in desc_lower or "gps" in desc_lower or "tracking link" in desc_lower:
            diagnosis_title = "🔍 Potential Telemetry Issue: Missing Diagnostics"
            diagnosis_desc = "Telemetry ping missing. Historically, 89% of GPS tickets escalated without driver phone & vehicle ID are rejected by Sandeep's team."
            action_guide = "Collect driver phone number, cab license plate, and check driver app battery saver setting."

        else:
            diagnosis_title = "🛠️ Potential Code Bug: Pre-Flight Verification Required"
            diagnosis_desc = "Legitimate bug investigation. Complete mandatory checklist before handoff to Engineering."
            action_guide = "Attach client error screenshots and exact reproduction steps."

        # Diagnostic Alert Box
        if is_config_issue:
            st.markdown(f"""
            <div class="hook-diagnostic-warning">
                <div style="font-weight: 700; font-size: 14px; margin-bottom: 4px;">{diagnosis_title}</div>
                <div style="font-size: 13px; line-height: 1.4;">{diagnosis_desc}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top:10px; font-size:13px;'><b>Recommended L1 Action:</b><br>{action_guide}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="hook-diagnostic-info">
                <div style="font-weight: 700; font-size: 14px; margin-bottom: 4px;">{diagnosis_title}</div>
                <div style="font-size: 13px; line-height: 1.4;">{diagnosis_desc}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top:10px; font-size:13px;'><b>Pre-Flight Protocol:</b><br>{action_guide}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🔒 Mandatory Gatekeeper Checklist")
        st.caption("Sandeep's engineering queue is protected. All checks required to unlock escalation.")

        ch1 = st.checkbox("1. Verified Client Shift & Roster Configuration rules", value=False)
        ch2 = st.checkbox("2. Confirmed not a duplicate of active company-wide outage", value=False)
        ch3 = st.checkbox("3. Attached Driver/Vehicle IDs, Error Screenshot & Reproduction Steps", value=False)

        can_escalate = ch1 and ch2 and ch3 and (not is_config_issue)

        btn_c1, btn_c2 = st.columns(2)

        with btn_c1:
            if can_escalate:
                if st.button("🟢 Escalate to Engineering", type="primary", use_container_width=True):
                    st.session_state.escalated_count += 1
                    st.success(f"Ticket {ticket['ticket_id']} successfully sent to Sandeep's team with verified logs!")
            else:
                st.button("🔒 Escalate to Eng (Locked)", disabled=True, use_container_width=True)
                if is_config_issue:
                    st.caption("⚠️ Escalation disabled: This is a configuration/how-to issue. Resolve via L1 action.")
                else:
                    st.caption("⚠️ Complete all 3 checklist items above to unlock.")

        with btn_c2:
            if st.button("✅ Resolve Directly via L1 Guide", type="secondary", use_container_width=True):
                st.session_state.deflected_count += 1
                st.session_state.resolved_tickets.add(ticket['ticket_id'])
                st.balloons()
                st.success(f"Ticket {ticket['ticket_id']} resolved at L1 in 8 mins! Saved ~128 hours of engineering bounce-back.")

        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 2: ANALYTICS & COMMAND CENTER
# ==========================================
elif app_mode == "📊 Analytics & Command Center":
    st.markdown("### 📊 Executive Support & Escalation Command Center")
    st.markdown("<div style='color: #64748B; font-size: 14px; margin-bottom: 20px;'>Strategic evidence dashboard for Ritika (Head of Ops), Meera (Support Lead) and Sandeep (Eng Manager).</div>", unsafe_allow_html=True)

    # 4 HookScene Style Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="hook-metric" style="border-top-color: #3B82F6;">
            <div class="hook-metric-title">Total Inflow Volume</div>
            <div class="hook-metric-val">1,444</div>
            <div class="hook-metric-sub" style="color: #DC2626;">▲ +51.8% surge since July</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="hook-metric" style="border-top-color: #E8A72D;">
            <div class="hook-metric-title">Escalation Rate</div>
            <div class="hook-metric-val">33.7%</div>
            <div class="hook-metric-sub" style="color: #64748B;">486 tickets sent to Eng</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="hook-metric" style="border-top-color: #EF4444;">
            <div class="hook-metric-title">Avoidable Escalations</div>
            <div class="hook-metric-val">56.6%</div>
            <div class="hook-metric-sub" style="color: #DC2626;">275 non-bugs returned to L1</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
        <div class="hook-metric" style="border-top-color: #10B981;">
            <div class="hook-metric-title">Cycle Time Delay Penalty</div>
            <div class="hook-metric-val">128.6 hrs</div>
            <div class="hook-metric-sub" style="color: #64748B;">5.4 days vs 12.6h at L1</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Simulator Card
    st.markdown('<div class="hook-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Backlog Reduction & Headcount ROI Simulator (Zero Budget)")
    st.markdown("<div style='font-size: 13px; color: #64748B; margin-bottom: 16px;'>Simulate how deflecting avoidable escalations satisfies Ritika's mandate without hiring new agents or engineers.</div>", unsafe_allow_html=True)

    sim1, sim2 = st.columns([1, 1.8])
    with sim1:
        target_pct = st.slider("Target Deflection Rate (%):", 20, 90, 60, 5)
        avoidable_annual = 275 * 4
        deflected = int(avoidable_annual * (target_pct / 100))
        hrs_saved = deflected * 5.5
        fte_eng = hrs_saved / 1800

        st.metric("Annual Tickets Deflected", f"{deflected:,}")
        st.metric("Engineering Hours Saved", f"{hrs_saved:,.0f} hrs")
        st.metric("Equivalent Engineer Capacity Saved", f"{fte_eng:.1f} Engineers")

    with sim2:
        st.markdown("""
        **Operational Wins Delivered:**
        * **Backlog Reduction:** Open backlog drops from **~50 tickets down to < 18** within 4 weeks.
        * **Cycle Time Acceleration:** Median resolution drops by **62%** on top categories.
        * **CSAT Recovery:** Average customer rating recovers from **3.11 $\\to$ 4.15**.
        * **Ritika's Constraint Met:** 100% process and software-driven with **$0 hiring spend**.
        """)
        
        sim_data = pd.DataFrame({
            "Metric": ["Current Reality", "With Smart Gatekeeper v0"],
            "Median Turnaround (Hours)": [86.8, 18.5],
            "Escalation Rejection (%)": [56.6, 12.0]
        }).set_index("Metric")
        st.bar_chart(sim_data)

    st.markdown('</div>', unsafe_allow_html=True)

    # Agent Table
    st.markdown('<div class="hook-card">', unsafe_allow_html=True)
    st.markdown("### 👥 Agent Discrepancy & Coaching Opportunities")
    agent_summary = df.groupby('assigned_agent').agg(
        Tickets=('ticket_id', 'count'),
        Escalation_Rate=('escalated_to_eng', lambda x: f"{(x=='Yes').mean()*100:.1f}%"),
        Reopen_Rate=('reopen_count', lambda x: f"{x.mean():.2f}"),
        CSAT=('csat_score', lambda x: f"{x.mean():.2f}")
    ).reset_index()
    st.dataframe(agent_summary, use_container_width=True)
    st.caption("Key Insight: Coach Rahul T on pre-flight checks (escalates 61.6%). Coach Karan B on verification before closing (0.36 reopens/ticket).")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 3: CLIENT QUICK-FIX TOOLS
# ==========================================
elif app_mode == "⚙️ Client Quick-Fix Tools":
    st.markdown('<div class="hook-card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ L1 Self-Service Quick Configuration Center")
    st.markdown("<div style='font-size: 13px; color: #64748B; margin-bottom: 20px;'>Empowering L1 support agents to resolve common client configuration discrepancies in 2 minutes without waiting for engineering.</div>", unsafe_allow_html=True)

    tool_choice = st.selectbox(
        "Select Quick-Fix Utility:",
        ["1. Shift Booking Cutoff Sync & Override", "2. Bulk Report Date-Range Partitioner", "3. Address Geocode Validation"]
    )

    if "1. Shift Booking Cutoff" in tool_choice:
        st.markdown("#### 🕒 Shift Booking Cutoff Sync")
        q1, q2 = st.columns(2)
        with q1:
            cl = st.selectbox("Corporate Client:", df['client_name'].unique()[:10])
            shift = st.selectbox("Target Shift:", ["Morning Shift (06:00 AM)", "General Shift (09:00 AM)", "Night Shift (10:00 PM)"])
        with q2:
            cutoff = st.time_input("Shift Cutoff Window:", datetime.time(17, 0))
            allow_exc = st.checkbox("Allow 30-Minute Grace Period Exception for Today's Roster", value=True)

        if st.button("Apply Cutoff Sync to Client Roster", type="primary"):
            st.success(f"✅ Roster cutoff synced for {cl}. 16 pending employee bookings successfully injected into tomorrow's roster. Ticket resolved!")

    elif "2. Bulk Report" in tool_choice:
        st.markdown("#### 📄 Automated Report Date-Range Partitioner")
        d_range = st.date_input("Requested Report Range:", [datetime.date(2026, 8, 1), datetime.date(2026, 8, 31)])
        if st.button("Partition into Fast Batches", type="primary"):
            st.info("Report partitioned into 3 batches: [Aug 1 - Aug 10], [Aug 11 - Aug 20], [Aug 21 - Aug 31]. Export links generated in 4 seconds!")

    elif "3. Address Geocode" in tool_choice:
        st.markdown("#### 📍 Address & Society Pin Validator")
        st.text_input("Enter Society / Landmark Name:", "Greenfield Heights, Sector 62")
        if st.button("Fetch & Re-anchor Geocode Coordinates", type="primary"):
            st.success("Coordinates updated: Lat 12.9716, Long 77.5946. Updated for 33 linked employee profiles.")

    st.markdown('</div>', unsafe_allow_html=True)
