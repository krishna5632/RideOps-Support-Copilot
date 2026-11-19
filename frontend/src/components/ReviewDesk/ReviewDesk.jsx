import React from 'react';
import { useTickets } from '../../context/TicketContext';
import FilterBar from './FilterBar';
import TicketFeed from './TicketFeed';
import TicketInspector from './TicketInspector';
import { Database, Star, ShieldCheck, FileCheck2, RotateCcw } from 'lucide-react';

export default function ReviewDesk() {
  const {
    tickets,
    deflectedCount,
    isCustomDataset,
    activeDatasetName,
    resetToDefault
  } = useTickets();

  const escCount = tickets.filter((t) => t.escalated_to_eng === 'Yes').length;
  const escRate = tickets.length > 0 ? Math.round((escCount / tickets.length) * 100) : 0;

  return (
    <section className="space-y-6">
      {/* Header Row: Title + 3 Summary KPI Cards */}
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1.5">
            <span className="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-200">
              Built for L1 Agent Persona
            </span>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Support Review Desk</h1>
          <p className="text-sm text-slate-500 font-medium mt-1">
            Pre-Escalation Gatekeeper & Instant L1 Resolution Workspace
          </p>
        </div>

        {/* 3 Summary KPI Cards */}
        <div className="flex items-center gap-3">
          <div className="bg-white border border-slate-200 rounded-2xl px-4 py-3 flex items-center gap-3 shadow-[0_1px_2px_rgba(0,0,0,0.02)] min-w-[135px]">
            <Database className="w-5 h-5 text-slate-500" />
            <div>
              <div className="text-2xl font-extrabold text-slate-900 font-mono tracking-tight leading-none">
                {tickets.length.toLocaleString()}
              </div>
              <div className="text-xs font-semibold text-slate-500 mt-1">Total Inflow</div>
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl px-4 py-3 flex items-center gap-3 shadow-[0_1px_2px_rgba(0,0,0,0.02)] min-w-[145px]">
            <Star className="w-5 h-5 fill-amber-400 text-amber-500" />
            <div>
              <div className="text-2xl font-extrabold text-slate-900 font-mono tracking-tight leading-none">
                {escCount}
              </div>
              <div className="text-xs font-semibold text-slate-500 mt-1">Escalations ({escRate}%)</div>
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl px-4 py-3 flex items-center gap-3 shadow-[0_1px_2px_rgba(0,0,0,0.02)] min-w-[155px]">
            <ShieldCheck className="w-5 h-5 text-emerald-600" />
            <div>
              <div className="text-2xl font-extrabold text-emerald-600 font-mono tracking-tight leading-none">
                {deflectedCount}
              </div>
              <div className="text-xs font-semibold text-slate-500 mt-1">Resolved by L1</div>
            </div>
          </div>
        </div>
      </div>

      {/* Dynamic Dataset Alert Banner (when custom CSV is active) */}
      {isCustomDataset && (
        <div className="p-4 rounded-2xl bg-amber-50/90 border border-amber-300 text-amber-950 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-sm shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-amber-200 text-amber-950 flex items-center justify-center font-bold flex-shrink-0">
              <FileCheck2 className="w-5 h-5 text-amber-900" />
            </div>
            <div>
              <div className="font-bold text-slate-900 flex flex-wrap items-center gap-2">
                <span>Active Dataset:</span>
                <span className="font-mono text-xs font-extrabold bg-white px-2.5 py-0.5 rounded border border-amber-300 text-amber-950">
                  {activeDatasetName}
                </span>
                <span className="text-xs font-semibold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded border border-emerald-300">
                  {tickets.length} tickets loaded
                </span>
              </div>
              <p className="text-xs text-amber-800 mt-0.5 font-medium">
                The default 1,444 tickets are completely unloaded. The queue below displays <b>only</b> the tickets from your uploaded CSV.
              </p>
            </div>
          </div>
          <button
            onClick={resetToDefault}
            className="self-start sm:self-auto px-3.5 py-2 rounded-xl bg-white hover:bg-amber-100 border border-amber-300 text-amber-950 text-xs font-bold transition flex items-center gap-1.5 shadow-sm whitespace-nowrap cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5 text-amber-700" />
            <span>Switch Back to Default Q3 (1,444)</span>
          </button>
        </div>
      )}

      {/* Filter Bar */}
      <FilterBar />

      {/* Split Feed & Inspector View */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        <TicketFeed />
        <div className="lg:col-span-7">
          <TicketInspector />
        </div>
      </div>
    </section>
  );
}
