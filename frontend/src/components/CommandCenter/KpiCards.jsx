import React from 'react';
import { useTickets } from '../../context/TicketContext';

export default function KpiCards() {
  const { tickets } = useTickets();

  const total = tickets.length;
  const escTickets = tickets.filter((t) => t.escalated_to_eng === 'Yes');
  const escCount = escTickets.length;
  const escRate = total > 0 ? ((escCount / total) * 100).toFixed(1) : '0';

  const avoidableTickets = escTickets.filter((t) => t.eng_outcome && t.eng_outcome !== 'Fixed');
  const avoidableCount = avoidableTickets.length;
  const avoidableRate = escCount > 0 ? ((avoidableCount / escCount) * 100).toFixed(1) : '0';

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
          Total Q3 Volume
        </span>
        <div className="text-3xl font-extrabold text-slate-900 mt-1 font-mono tracking-tight">
          {total.toLocaleString()}
        </div>
        <p className="text-xs text-rose-600 mt-1 font-semibold">+51.8% Surge (Jul-Sep)</p>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
          Escalation Rate
        </span>
        <div className="text-3xl font-extrabold text-slate-900 mt-1 font-mono tracking-tight">
          {escRate}%
        </div>
        <p className="text-xs text-slate-500 mt-1 font-medium">{escCount} tickets sent to Eng</p>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
          Avoidable Rejections
        </span>
        <div className="text-3xl font-extrabold text-rose-600 mt-1 font-mono tracking-tight">
          {avoidableRate}%
        </div>
        <p className="text-xs text-rose-600 mt-1 font-semibold">{avoidableCount} not legitimate bugs</p>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
          Ping-Pong Bounce Loop
        </span>
        <div className="text-3xl font-extrabold text-amber-600 mt-1 font-mono tracking-tight">
          128.6 hrs
        </div>
        <p className="text-xs text-slate-500 mt-1 font-medium">5.4 days cycle time delay</p>
      </div>
    </div>
  );
}
