import React, { useState } from 'react';
import { useTickets } from '../../context/TicketContext';
import { Layers } from 'lucide-react';

export default function ReportPartitionTool() {
  const { selectedTicket, resolveTicketLive, showToast } = useTickets();
  const [resultMsg, setResultMsg] = useState('');

  const handlePartition = () => {
    const msg = '✅ Query split into 3 batches: [Aug 1-10], [Aug 11-20], [Aug 21-31]. Export links generated in 4s!';
    setResultMsg(msg);
    showToast('Report Partitioned', '3 batches generated in 4 seconds.');
    if (selectedTicket) {
      resolveTicketLive(selectedTicket.ticket_id);
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div className="flex items-center gap-2.5 border-b border-slate-100 pb-3">
        <span className="w-7 h-7 rounded-full border border-slate-300 text-slate-800 text-sm font-bold flex items-center justify-center">
          2
        </span>
        <h3 className="text-base font-bold text-slate-900">Bulk Report Partitioner & Async Join Streamer</h3>
      </div>

      <p className="text-sm text-slate-600 max-w-xl leading-relaxed">
        Splits queries exceeding the 14-day database join limit into 3 chunked micro-batches to eliminate PostgreSQL 504 timeouts.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 text-sm pt-1">
        <div>
          <label className="block font-semibold text-slate-700 mb-1.5 text-sm">Requested Date Range:</label>
          <input
            type="text"
            readOnly
            value="Aug 01, 2026 - Aug 31, 2026 (31 Days)"
            className="w-full p-2.5 bg-slate-100 border border-slate-200 rounded-lg font-mono text-slate-700 text-sm"
          />
        </div>
        <div>
          <label className="block font-semibold text-slate-700 mb-1.5 text-sm">Partition Scheme:</label>
          <select defaultValue="3 Chunks (10 Days Each) - Recommended" className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-medium text-sm">
            <option>3 Chunks (10 Days Each) - Recommended</option>
            <option>5 Chunks (6 Days Each)</option>
          </select>
        </div>
      </div>

      <div className="pt-2 flex items-center gap-3">
        <button
          onClick={handlePartition}
          className="py-2.5 px-4 bg-slate-900 hover:bg-black text-white font-bold text-sm rounded-xl transition shadow-sm flex items-center gap-2 cursor-pointer"
        >
          <Layers className="w-4 h-4 text-white" />
          <span>Partition Query & Download Links</span>
        </button>
        <span className="text-xs text-slate-400">⚡ Eliminates 77 report export engineering escalations</span>
      </div>

      {resultMsg && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 text-sm font-semibold">
          {resultMsg}
        </div>
      )}
    </div>
  );
}
