import React from 'react';
import { useTickets } from '../../context/TicketContext';

export default function TicketCard({ ticket, isSelected }) {
  const { setSelectedTicketId } = useTickets();

  let cardBgBorder = isSelected
    ? 'bg-white border-slate-900 ring-1 ring-slate-900'
    : 'bg-white hover:border-slate-300 border-slate-200';

  if (ticket.isResolvedLive) {
    cardBgBorder = isSelected
      ? 'bg-emerald-50 border-emerald-600 ring-1 ring-emerald-600'
      : 'bg-emerald-50/40 border-emerald-200 hover:border-emerald-300';
  }

  const pBadgeColor = ticket.isResolvedLive
    ? 'bg-emerald-100 text-emerald-800 border-emerald-300 font-bold'
    : ticket.priority === 'P1'
    ? 'bg-rose-50 text-rose-700 border-rose-200'
    : ticket.priority === 'P2'
    ? 'bg-amber-50 text-amber-800 border-amber-200'
    : 'bg-slate-100 text-slate-700 border-slate-200';

  const statusTag = ticket.isResolvedLive ? '✅ Resolved at L1' : ticket.priority;

  return (
    <div
      onClick={() => setSelectedTicketId(ticket.ticket_id)}
      className={`rounded-2xl border transition p-4 cursor-pointer text-xs space-y-2.5 shadow-sm ${cardBgBorder}`}
    >
      {/* Top Row */}
      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center gap-2 font-semibold text-slate-800">
          <span className="px-2.5 py-1 rounded-lg bg-slate-100 border border-slate-200 font-mono font-bold text-xs text-slate-900">
            {ticket.ticket_id}
          </span>
          <span className="px-2 py-0.5 rounded-lg bg-slate-100 text-slate-600 text-xs">
            {ticket.channel || 'Portal'}
          </span>
        </div>
        <span className={`px-2.5 py-1 rounded-lg border font-bold uppercase text-xs ${pBadgeColor}`}>
          {statusTag}
        </span>
      </div>

      {/* Hero Problem Description Quote */}
      <div className="font-bold text-slate-900 text-sm line-clamp-2 leading-snug">
        "{ticket.description}"
      </div>

      {/* Bottom: Client Name + Category */}
      <div className="flex items-center justify-between pt-1 text-xs text-slate-500">
        <span className="font-bold text-slate-800 truncate max-w-[200px]">{ticket.client_name}</span>
        <span className="text-slate-500 font-medium">{(ticket.category || '').split('/')[0]}</span>
      </div>
    </div>
  );
}
