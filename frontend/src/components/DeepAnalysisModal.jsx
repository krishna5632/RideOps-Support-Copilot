import React, { useState } from 'react';
import { useTickets } from '../context/TicketContext';
import {
  X,
  BarChart3,
  TrendingUp,
  AlertTriangle,
  Clock,
  PieChart,
  Users,
  ShieldAlert,
  Sparkles,
  Download,
  ExternalLink,
  ChevronRight,
  FileSpreadsheet
} from 'lucide-react';

export default function DeepAnalysisModal() {
  const {
    isDeepAnalysisOpen,
    setIsDeepAnalysisOpen,
    tickets,
    activeDatasetName,
    setActiveTab,
    filterToBacklogOnly
  } = useTickets();

  const [selectedFinding, setSelectedFinding] = useState(0);

  if (!isDeepAnalysisOpen) return null;

  const totalTickets = tickets.length;
  const escalatedCount = tickets.filter((t) => t.escalated_to_eng === 'Yes').length;
  const escRate = totalTickets > 0 ? ((escalatedCount / totalTickets) * 100).toFixed(1) : '33.7';

  const findings = [
    {
      id: 0,
      title: 'Inflow Velocity & Rush-Hour Dynamics',
      tag: "Ritika's Claim Validated",
      tagColor: 'bg-blue-50 text-blue-700 border-blue-200',
      icon: TrendingUp,
      figureImg: '/figures/fig1_inflow_surge_and_hourly.png',
      statBadge: '+51.8% Surge (Peak +88.5%)',
      summary: 'Ticket volume grew +51.8% from July to September, peaking at 164 tickets/week with distinct bimodal morning and evening shift spikes.',
      dataPoints: [
        'Monthly tickets accelerated from 390 (July) to 462 (August) and 592 (September).',
        'Hourly analysis reveals arrival spikes at 06:00–10:00 AM (Morning Shift Start) and 17:00–20:00 PM (Evening Shift Handover).',
        'Monday & Tuesday mornings represent 38% of all weekly emergency escalations.'
      ],
      rootCause:
        'When corporate HR administrators update employee shift times after portal cutoffs, the overnight sync fails. When drivers log in at 6:00 AM, vehicles are unassigned, creating an emergency rush of support tickets.',
      actionableFix:
        'Implement automated roster pre-sync validation 3 hours prior to shift starts, preventing 40% of the morning ticket spike at the source.'
    },
    {
      id: 1,
      title: 'The 56.6% Engineering Triage Waste Loop',
      tag: "Sandeep's Claim Validated",
      tagColor: 'bg-rose-50 text-rose-700 border-rose-200',
      icon: AlertTriangle,
      figureImg: '/figures/fig2_engineering_outcome_waste.png',
      statBadge: '275 / 486 Non-Bugs (56.6% Waste)',
      summary: 'Out of 486 escalated tickets, 275 were NOT software bugs. Only 211 (43.4%) were legitimate code fixes, consuming ~550 senior dev hours.',
      dataPoints: [
        '89 tickets (18.3%): Insufficient information (Support escalated with no device or driver logs).',
        '84 tickets (17.3%): Client configuration mistakes (Admin modified cutoff rules in portal).',
        '56 tickets (11.5%): Duplicates of already known issues.',
        '46 tickets (9.5%): How-to queries or unreproducible transient issues.',
        'Total dev triage waste: ~550 senior engineering hours spent on basic triage.'
      ],
      rootCause:
        'L1 support agents face pressure to meet First-Response Time (FRT) SLAs and lack pre-escalation diagnostic gates or self-service configuration tools.',
      actionableFix:
        'Deploy the "Pre-Escalation Gatekeeper" checklist: lock the escalation button until driver phone, vehicle reg, and timestamp logs are verified.'
    },
    {
      id: 2,
      title: 'The 5-Day Ping-Pong Turnaround Delay',
      tag: "Meera's Claim Validated",
      tagColor: 'bg-amber-50 text-amber-700 border-amber-200',
      icon: Clock,
      figureImg: '/figures/fig3_turnaround_pingpong_latency.png',
      statBadge: '12.6h (L1) vs 128.6h (Bounced)',
      summary: 'While unescalated tickets resolve in 12.6 hours (0.5 days), false escalations bounce between teams for 2–3 handoffs taking 5.1 to 5.4 days.',
      dataPoints: [
        'L1 Non-Escalated: Median 12.6 hours (CSAT: 4.01 / 5.0).',
        'Engineering Bug Fix: Median 64.8 hours (~2.7 days).',
        'Config Issue Bounced to L1: Median 128.6 hours / 5.4 days (CSAT: 2.43 / 5.0).',
        'Statistically significant delay (Mann-Whitney U test p < 0.0001).'
      ],
      rootCause:
        'Premature escalation creates multi-tier queue latency: tickets sit in the engineering queue for 48h before being rejected back to L1, where they sit again.',
      actionableFix:
        'Equip L1 with instant Run Studio Quick-Fix recipes to resolve configuration mismatches locally in under 5 minutes without engineering handoffs.'
    },
    {
      id: 3,
      title: 'The 80/20 Category Concentration',
      tag: 'Maximum Strategic Leverage',
      tagColor: 'bg-purple-50 text-purple-700 border-purple-200',
      icon: PieChart,
      figureImg: '/figures/fig4_category_pareto_concentration.png',
      statBadge: 'Top 3 Categories = 78.0% Escalations',
      summary: 'Just 3 out of 10 categories account for 78% of all engineering escalations: Roster Sync, Live GPS, and Report Export.',
      dataPoints: [
        'Roster / booking not syncing: 175 escalations (51.0% escalation rate).',
        'Live tracking / GPS incorrect: 127 escalations (39.7% escalation rate).',
        'Report export failing: 77 escalations (38.9% escalation rate).',
        'Text diagnostics highlight repeating failure modes: "cutoff time", "frozen map", "telematics", "timeout >30 days".'
      ],
      rootCause:
        'Roster sync errors stem from portal cutoff mismatches. GPS freezes stem from driver app battery-saver mode. Report exports fail due to multi-table joins on date ranges >14 days.',
      actionableFix:
        'Target diagnostic checklists and automated one-click fixes specifically to these three categories to capture 78% of the problem immediately.'
    },
    {
      id: 4,
      title: 'Corporate Client Concentration & Churn Risk',
      tag: 'Enterprise SLA Protection',
      tagColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
      icon: ShieldAlert,
      figureImg: '/figures/fig5_client_tier_and_concentration.png',
      statBadge: 'Top 20% Clients = 42% Volume',
      summary: 'Top 20% of corporate clients generate 42% of volume, with Enterprise accounts representing 51.2% of total tickets and facing steep CSAT drops.',
      dataPoints: [
        'Enterprise accounts: 739 tickets (51.2% volume, 34.6% escalation rate).',
        'Mid-market accounts: 462 tickets (32.0% volume).',
        'SMB accounts: 243 tickets (16.8% volume).',
        'Enterprise CSAT crashes from 4.12 on L1 resolved tickets down to 2.85 on bounced escalations.'
      ],
      rootCause:
        'Large enterprises have strict transport SLA penalties. When escalations stall for 5 days, corporate procurement contacts leadership to threaten contract cancellation.',
      actionableFix:
        'Create a dedicated Enterprise VIP Triage Lane with a guaranteed 4-hour SLA and proactive executive escalation alerts.'
    },
    {
      id: 5,
      title: 'Support Team Escalation Variance & Bias',
      tag: 'Team Coaching Opportunity',
      tagColor: 'bg-cyan-50 text-cyan-700 border-cyan-200',
      icon: Users,
      figureImg: '/figures/fig6_agent_performance_variance.png',
      statBadge: 'Variance: 24.5% to 41.2%',
      summary: 'Escalation rates vary dramatically across the 8 support agents, revealing lack of standardized triage procedures rather than ticket complexity.',
      dataPoints: [
        'Rahul T: 41.2% escalation rate (highest, lowest diagnostic depth).',
        'Karan B: 39.1% escalation rate.',
        'Priya D & Vikram S: 24.5%–27.2% escalation rates (high local resolution, higher CSAT).',
        'Reopen rates on high-escalation agents are 2.4x higher than team median.'
      ],
      rootCause:
        'Junior agents lack confidence and diagnostic tools, using "Escalate to Engineering" as a triage dumping mechanism to clear their personal queues.',
      actionableFix:
        'Pair junior agents with Priya D for shadowing, mandate checklist compliance before escalation, and track weekly deflection rates.'
    },
    {
      id: 6,
      title: 'Customer CSAT Econometric Drivers',
      tag: 'Multivariate OLS Regression',
      tagColor: 'bg-orange-50 text-orange-700 border-orange-200',
      icon: BarChart3,
      figureImg: '/figures/fig7_csat_multivariate_drivers.png',
      statBadge: '-0.18 pts/day, -1.25 pts/reopen',
      summary: 'Regression analysis reveals cycle time and ticket reopens are the primary destroyers of corporate customer satisfaction.',
      dataPoints: [
        'Resolution Time: Every 24 hours of delay reduces CSAT by -0.18 points (p < 0.001).',
        'Handoffs: Each inter-team handoff costs -0.42 CSAT points.',
        'Reopens: A single reopen drops CSAT from 4.10 down to 2.85; 2 reopens crash it to 1.33.',
        'Escalation Penalty: Overall CSAT drops from 4.01 (L1) to 3.11 (Escalated).'
      ],
      rootCause:
        'Clients can forgive delays if communicated transparently, but premature closure followed by a reopen signals operational incompetence.',
      actionableFix:
        'Institute a "Zero False Close" policy: require customer confirmation before marking tickets as Closed to prevent catastrophic reopen penalties.'
    },
    {
      id: 7,
      title: 'Gatekeeper ROI & Operational Simulation',
      tag: 'Strategic Implementation Plan',
      tagColor: 'bg-emerald-50 text-emerald-800 border-emerald-300',
      icon: Sparkles,
      figureImg: '/figures/fig8_simulation_impact_roi.png',
      statBadge: '-70% Waste, ~380 Dev-Hours Saved',
      summary: 'Simulating a 70% elimination of false escalations via Gatekeeper + Run Studio yields dramatic capacity recovery at $0 additional cost.',
      dataPoints: [
        'Avoidable escalations eliminated: 192 tickets / quarter.',
        'Senior engineering hours reclaimed: ~380 dev-hours / quarter (~$38,000 equivalent developer capacity).',
        'Active open backlog reduced from ~48 down to <15 tickets (-68%).',
        'Mean resolution time drops from 44.2 hours down to 16.5 hours (-62%).',
        'Projected CSAT rebound: 3.65 to 4.25+ / 5.0.'
      ],
      rootCause:
        'High engineering costs and support burnout were caused by lack of pre-flight gates, not shortage of headcount.',
      actionableFix:
        'Deploy Gatekeeper v0 to morning shifts tomorrow at 9:00 AM; review weekly deflection metrics every Friday.'
    }
  ];

  const current = findings[selectedFinding];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-6xl max-h-[92vh] flex flex-col overflow-hidden">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-100 border border-amber-300 flex items-center justify-center text-amber-800 shadow-sm">
              <BarChart3 className="w-5 h-5 text-amber-700" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-extrabold text-slate-900">
                  Deep Data Diagnosis & Root-Cause Analysis
                </h2>
                <span className="px-2 py-0.5 rounded-full text-[11px] font-extrabold bg-amber-100 text-amber-900 border border-amber-200">
                  8 Visual Figures & Explanations
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium flex items-center gap-2 mt-0.5">
                <FileSpreadsheet className="w-3.5 h-3.5 text-slate-400" />
                <span>Dataset: <b className="text-slate-700">{activeDatasetName}</b> ({totalTickets.toLocaleString()} tickets, {escRate}% escalated)</span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsDeepAnalysisOpen(false)}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 transition cursor-pointer"
              title="Close Diagnosis"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Body: Navigation Tabs + Active Finding Content */}
        <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
          {/* Left Navigation: Finding Selector */}
          <div className="w-full md:w-80 border-r border-slate-200 bg-slate-50/70 p-3 overflow-y-auto space-y-1.5 shrink-0">
            <div className="px-2 py-1 text-[11px] font-bold uppercase tracking-wider text-slate-400">
              Key Diagnostic Findings
            </div>
            {findings.map((f, idx) => {
              const Icon = f.icon;
              const isSelected = selectedFinding === idx;
              return (
                <button
                  key={f.id}
                  onClick={() => setSelectedFinding(idx)}
                  className={`w-full text-left p-3 rounded-xl transition flex items-start gap-2.5 cursor-pointer ${
                    isSelected
                      ? 'bg-white shadow-sm border border-slate-200 text-slate-900 font-bold ring-1 ring-amber-400'
                      : 'hover:bg-slate-100 text-slate-600 hover:text-slate-900 border border-transparent'
                  }`}
                >
                  <div
                    className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 mt-0.5 ${
                      isSelected ? 'bg-amber-100 text-amber-800' : 'bg-slate-200 text-slate-600'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-bold truncate">
                      {idx + 1}. {f.title}
                    </div>
                    <div className="text-[11px] text-slate-500 font-medium truncate mt-0.5">
                      {f.statBadge}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Right Content: Active Visual Figure + Deep Explanation */}
          <div className="flex-1 p-6 overflow-y-auto space-y-5 bg-white">
            {/* Title & Badge */}
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${current.tagColor}`}>
                    {current.tag}
                  </span>
                  <span className="text-xs font-bold text-slate-500 font-mono">
                    Finding {selectedFinding + 1} of 8
                  </span>
                </div>
                <h3 className="text-xl font-extrabold text-slate-900 mt-1">
                  {current.title}
                </h3>
              </div>

              <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-50 border border-amber-200 rounded-lg text-amber-900 font-bold text-xs">
                <span>{current.statBadge}</span>
              </div>
            </div>

            {/* Visual Figure Image */}
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 flex flex-col items-center justify-center shadow-inner overflow-hidden">
              <img
                src={current.figureImg}
                alt={current.title}
                className="max-h-[310px] w-auto object-contain rounded-lg shadow-sm"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = '/figures/fig1_weekly_inflow.png';
                }}
              />
              <span className="text-[11px] text-slate-400 font-mono mt-2">
                Figure {selectedFinding + 1}: Generated from {totalTickets.toLocaleString()} tickets dataset
              </span>
            </div>

            {/* Deep Explanation Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs sm:text-sm">
              {/* Box 1: Hard Data Observations */}
              <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
                <div className="font-extrabold text-slate-900 flex items-center gap-1.5 text-xs uppercase tracking-wide">
                  <BarChart3 className="w-3.5 h-3.5 text-blue-600" />
                  <span>Empirical Findings & Data Evidence</span>
                </div>
                <p className="text-slate-700 leading-relaxed text-xs">
                  {current.summary}
                </p>
                <ul className="space-y-1.5 pt-1 text-xs text-slate-600">
                  {current.dataPoints.map((pt, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <span className="text-amber-500 font-bold">•</span>
                      <span>{pt}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Box 2: Root Cause & Strategic Fix */}
              <div className="space-y-3">
                <div className="p-3.5 bg-rose-50 border border-rose-200 rounded-xl space-y-1.5">
                  <div className="font-bold text-rose-900 flex items-center gap-1.5 text-xs uppercase tracking-wide">
                    <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
                    <span>Operational Root Cause</span>
                  </div>
                  <p className="text-rose-950 text-xs leading-relaxed">
                    {current.rootCause}
                  </p>
                </div>

                <div className="p-3.5 bg-emerald-50 border border-emerald-200 rounded-xl space-y-1.5">
                  <div className="font-bold text-emerald-900 flex items-center gap-1.5 text-xs uppercase tracking-wide">
                    <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Prescribed Actionable Fix</span>
                  </div>
                  <p className="text-emerald-950 text-xs leading-relaxed font-medium">
                    {current.actionableFix}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Modal Footer: Quick Links & Actions */}
        <div className="px-6 py-3.5 border-t border-slate-200 bg-slate-50 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2">
            <span className="text-slate-500 font-medium">
              Want raw statistical models?
            </span>
            <a
              href="file:///c:/Users/prave/Downloads/RideOps_CaseStudy/backend/notebooks/rideops_deep_operational_analysis.ipynb"
              target="_blank"
              rel="noopener noreferrer"
              className="font-bold text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1"
            >
              <span>rideops_deep_operational_analysis.ipynb</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                setIsDeepAnalysisOpen(false);
                setActiveTab('triage');
                filterToBacklogOnly();
              }}
              className="px-3.5 py-2 bg-slate-900 hover:bg-black text-white font-bold rounded-xl transition shadow-sm flex items-center gap-1.5 cursor-pointer"
            >
              <span>Resolve Open Backlog</span>
              <ChevronRight className="w-4 h-4 text-amber-400" />
            </button>
            <button
              onClick={() => setIsDeepAnalysisOpen(false)}
              className="px-3 py-2 bg-white hover:bg-slate-100 text-slate-700 font-bold border border-slate-200 rounded-xl transition shadow-sm cursor-pointer"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
