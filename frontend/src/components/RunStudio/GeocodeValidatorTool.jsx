import React, { useState } from 'react';
import { useTickets } from '../../context/TicketContext';
import { MapPin } from 'lucide-react';

export default function GeocodeValidatorTool() {
  const { selectedTicket, resolveTicketLive, showToast } = useTickets();
  const [resultMsg, setResultMsg] = useState('');

  const handleReanchor = () => {
    const msg = '✅ Coordinates re-anchored: Lat 12.9716, Long 77.5946 for 33 linked profiles.';
    setResultMsg(msg);
    showToast('Coordinates Updated', 'Re-anchored Lat 12.9716, Long 77.5946.');
    if (selectedTicket) {
      resolveTicketLive(selectedTicket.ticket_id);
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div className="flex items-center gap-2.5 border-b border-slate-100 pb-3">
        <span className="w-7 h-7 rounded-full border border-slate-300 text-slate-800 text-sm font-bold flex items-center justify-center">
          3
        </span>
        <h3 className="text-base font-bold text-slate-900">Address Geocode Re-Anchor & Society Pin Fix</h3>
      </div>

      <p className="text-sm text-slate-600 max-w-xl leading-relaxed">
        Re-anchors inaccurate reverse-geocoded coordinates for cluster housing societies directly on Mapbox/OSM maps.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 text-sm pt-1">
        <div>
          <label className="block font-semibold text-slate-700 mb-1.5 text-sm">Target Society Address:</label>
          <input
            type="text"
            readOnly
            value="Greenfield Society Gate 2, Outer Ring Rd"
            className="w-full p-2.5 bg-slate-100 border border-slate-200 rounded-lg text-slate-700 text-sm"
          />
        </div>
        <div>
          <label className="block font-semibold text-slate-700 mb-1.5 text-sm">Updated Lat / Long Coordinates:</label>
          <input
            type="text"
            readOnly
            value="12.9716° N, 77.5946° E (Verified)"
            className="w-full p-2.5 bg-slate-100 border border-slate-200 rounded-lg font-mono text-slate-700 text-sm"
          />
        </div>
      </div>

      <div className="pt-2 flex items-center gap-3">
        <button
          onClick={handleReanchor}
          className="py-2.5 px-4 bg-slate-900 hover:bg-black text-white font-bold text-sm rounded-xl transition shadow-sm flex items-center gap-2 cursor-pointer"
        >
          <MapPin className="w-4 h-4 text-white" />
          <span>Re-Anchor Society Pin</span>
        </button>
        <span className="text-xs text-slate-400">⚡ Fixes 30+ employees in 1 click</span>
      </div>

      {resultMsg && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 text-sm font-semibold">
          {resultMsg}
        </div>
      )}
    </div>
  );
}
