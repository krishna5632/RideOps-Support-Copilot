import React from 'react';
import { useTickets } from '../context/TicketContext';

export default function Toast() {
  const { toast } = useTickets();

  if (!toast) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 transition-all duration-300">
      <div className="flex items-center gap-3 bg-slate-900 text-white px-4 py-3 rounded-2xl shadow-xl border border-slate-800 text-xs">
        <div className="w-6 h-6 rounded-lg bg-amber-500 text-slate-950 flex items-center justify-center font-bold">
          ✓
        </div>
        <div>
          <div className="font-bold">{toast.title}</div>
          <div className="text-slate-300">{toast.msg}</div>
        </div>
      </div>
    </div>
  );
}
