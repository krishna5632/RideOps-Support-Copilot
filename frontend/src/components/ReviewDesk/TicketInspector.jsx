import React from 'react';
import { useTickets } from '../../context/TicketContext';
import DiagnosticCard from './DiagnosticCard';
import GatekeeperCard from './GatekeeperCard';
import { Building2 } from 'lucide-react';

export default function TicketInspector() {
  const { selectedTicket } = useTickets();

  if (!selectedTicket) {
    return (
      <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center text-slate-400">
        No ticket selected.
      </div>
    );
  }

  const pBadgeColor =
    selectedTicket.priority === 'P1'
      ? 'bg-rose-50 text-rose-700 border-rose-200'
      : selectedTicket.priority === 'P2'
      ? 'bg-amber-50 text-amber-800 border-amber-200'
      : 'bg-slate-100 text-slate-700 border-slate-200';

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-7 shadow-sm space-y-5 sticky top-20">
      {/* Top Badges Row */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span className="font-mono text-base font-bold text-slate-900 bg-slate-100 px-3 py-1 rounded-lg border border-slate-200">
            {selectedTicket.ticket_id}
          </span>
          <span className={`text-xs font-bold px-3 py-1 rounded-lg border ${pBadgeColor}`}>
            {selectedTicket.priority} Priority
          </span>
          <span
            className={`text-xs font-bold px-3 py-1 rounded-lg border ${
              selectedTicket.isResolvedLive
                ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
                : 'bg-slate-100 text-slate-700 border-slate-200'
            }`}
          >
            {selectedTicket.isResolvedLive ? '✅ Resolved at L1 (Deflected)' : selectedTicket.status}
          </span>
        </div>
        <span className="text-xs text-slate-500 font-mono font-semibold">
          Assigned: {selectedTicket.assigned_agent}
        </span>
      </div>

      {/* Hero Problem Quote Title */}
      <div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight leading-snug">
          "{selectedTicket.description}"
        </h2>

        {/* Metadata Line */}
        <div className="flex flex-wrap items-center gap-2 text-sm text-slate-600 font-medium mt-2.5">
          <span className="flex items-center gap-1.5 text-slate-800 font-bold">
            <Building2 className="w-4 h-4 text-slate-400" />
            <span>
              {selectedTicket.client_name} ({selectedTicket.client_id})
            </span>
          </span>
          <span>•</span>
          <span>
            Tier: <b className="text-slate-800">{selectedTicket.client_tier}</b>
          </span>
          <span>•</span>
          <span className="px-2.5 py-0.5 rounded bg-slate-100 text-slate-700 font-mono text-xs font-bold">
            {selectedTicket.category}
          </span>
        </div>
      </div>

      {/* Diagnostic intelligence callout */}
      <DiagnosticCard ticket={selectedTicket} />

      {/* Gatekeeper checklist & action buttons */}
      <GatekeeperCard ticket={selectedTicket} />
    </div>
  );
}
