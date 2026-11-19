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

      {/* Deep Diagnosis Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 rounded-2xl p-5 text-white flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm border border-slate-700">
        <div className="flex items-center gap-3.5">
          <div className="w-11 h-11 rounded-xl bg-amber-400 text-slate-900 flex items-center justify-center font-extrabold shadow-sm">
            <BarChart3 className="w-6 h-6 text-slate-950" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-extrabold text-white">
                Deep Statistical Diagnosis & Jupyter Root-Cause Models
              </h2>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-amber-400/20 text-amber-300 border border-amber-400/30">
                8 Visual Figures Ready
              </span>
            </div>
            <p className="text-xs text-slate-300 mt-0.5">
              Active: <b className="text-amber-300">{activeDatasetName}</b> — Explore 8 empirical figures proving Sandeep's 56.6% waste, Meera's 5-day delay, and CSAT regression models.
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsDeepAnalysisOpen(true)}
          className="px-4 py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-extrabold text-xs transition flex items-center gap-2 shadow-sm cursor-pointer whitespace-nowrap"
        >
          <span>Open 8 Diagnostic Figures</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      <KpiCards />
      <ChartsSection />
      <RoiSimulator />
      <AgentMatrix />
    </section>
  );
}
