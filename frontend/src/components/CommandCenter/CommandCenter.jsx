import React from 'react';
import { useTickets } from '../../context/TicketContext';
import { BarChart3, ArrowRight } from 'lucide-react';
import KpiCards from './KpiCards';
import ChartsSection from './ChartsSection';
import RoiSimulator from './RoiSimulator';
import AgentMatrix from './AgentMatrix';

export default function CommandCenter() {
  const { setIsDeepAnalysisOpen, activeDatasetName } = useTickets();

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Executive Command Center</h1>
        <p className="text-sm text-slate-500 font-medium mt-1">
          Root-Cause Operational Intelligence & Engineering Workload Deflection Analytics
        </p>
      </div>

      {/* Root-Cause Diagnostic Banner */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-xl bg-slate-900 text-white flex items-center justify-center font-bold shadow-sm">
            RO
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-extrabold text-slate-900">
                Root-Cause Diagnostic Findings
              </h2>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-200">
                8 Clean Diagrams
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Empirical insights on inflow surge, 56.6% triage waste, 5-day cycle time delay, and CSAT drivers for <b className="text-slate-800">{activeDatasetName}</b>.
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsDeepAnalysisOpen(true)}
          className="px-4 py-2.5 rounded-xl bg-slate-900 hover:bg-black text-white font-bold text-xs transition flex items-center gap-2 shadow-sm cursor-pointer whitespace-nowrap"
        >
          <span>View 8 Diagnostic Diagrams</span>
          <ArrowRight className="w-4 h-4 text-amber-400" />
        </button>
      </div>

      <KpiCards />
      <ChartsSection />
      <RoiSimulator />
      <AgentMatrix />
    </section>
  );
}
