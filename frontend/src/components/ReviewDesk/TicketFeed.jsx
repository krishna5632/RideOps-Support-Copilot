import React from 'react';
import { useTickets } from '../../context/TicketContext';
import TicketCard from './TicketCard';

export default function TicketFeed() {
  const { filteredTickets, selectedTicketId } = useTickets();

  const displayList = filteredTickets.slice(0, 50);

  if (displayList.length === 0) {
    return (
      <div className="lg:col-span-5 bg-white border border-slate-200 rounded-2xl p-12 text-center text-slate-400 text-sm">
        No matching tickets in queue.
      </div>
    );
  }

  return (
    <div className="lg:col-span-5 space-y-3.5 max-h-[740px] overflow-y-auto pr-1">
      {displayList.map((ticket) => (
        <TicketCard
          key={ticket.ticket_id}
          ticket={ticket}
          isSelected={ticket.ticket_id === selectedTicketId}
        />
      ))}
    </div>
  );
}
