import React from 'react';
import { useTickets } from '../../context/TicketContext';
import { Lock, Unlock, CheckCircle2 } from 'lucide-react';

export default function GatekeeperCard({ ticket }) {
  const { checklist, setChecklist, resolveTicketLive, showToast } = useTickets();

  if (!ticket) return null;

  const desc = (ticket.description || '').toLowerCase();
  const isConfig =
    desc.includes('cutoff') ||
    desc.includes('date range') ||
    desc.includes('> 15 days') ||
    desc.includes('stuck at loading') ||
    desc.includes('insurance expired') ||
    desc.includes('compliance');

  const canEscalate = checklist.c1 && checklist.c2 && checklist.c3 && !isConfig;

  const handleEscalate = () => {
    showToast('Escalated to Engineering', `Ticket ${ticket.ticket_id} submitted with full verified dossier.`);
  };

  return (
    <div className="space-y-5">
      {/* Mandatory Gatekeeper Checklist */}
      <div className="border border-slate-200 rounded-xl p-5 bg-white space-y-3">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-800 flex items-center gap-1.5">
            <Lock className="w-4 h-4 text-slate-500" />
            <span>Mandatory Pre-Flight Checks</span>
          </span>
          <span className="text-xs text-slate-500 font-medium">Protect engineering queue</span>
        </div>

        <label className="flex items-start gap-3 text-sm text-slate-800 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={checklist.c1}
            onChange={(e) => setChecklist({ ...checklist, c1: e.target.checked })}
            className="mt-0.5 w-4 h-4 rounded text-slate-900 focus:ring-slate-900 border-slate-300 cursor-pointer"
          />
          <span>1. Verified Client Shift & Roster rules (confirmed admin cutoff times).</span>
        </label>

        <label className="flex items-start gap-3 text-sm text-slate-800 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={checklist.c2}
            onChange={(e) => setChecklist({ ...checklist, c2: e.target.checked })}
            className="mt-0.5 w-4 h-4 rounded text-slate-900 focus:ring-slate-900 border-slate-300 cursor-pointer"
          />
          <span>2. Confirmed not a duplicate of active platform outage or vendor document block.</span>
        </label>

        <label className="flex items-start gap-3 text-sm text-slate-800 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={checklist.c3}
            onChange={(e) => setChecklist({ ...checklist, c3: e.target.checked })}
            className="mt-0.5 w-4 h-4 rounded text-slate-900 focus:ring-slate-900 border-slate-300 cursor-pointer"
          />
          <span>3. Attached Driver/Vehicle IDs, App error screenshot, and reproduction steps.</span>
        </label>
      </div>

      {/* Action Controls */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-1">
        <div>
          <button
            onClick={handleEscalate}
            disabled={!canEscalate}
            className={`w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl text-sm font-bold border transition shadow-sm ${
              canEscalate
                ? 'bg-emerald-600 hover:bg-emerald-700 text-white border-emerald-700 cursor-pointer'
                : 'bg-slate-100 text-slate-400 border-slate-200 cursor-not-allowed'
            }`}
          >
            {canEscalate ? <Unlock className="w-4 h-4" /> : <Lock className="w-4 h-4" />}
            <span>{canEscalate ? '🟢 Escalate to Eng with Verified Dossier' : '🔒 Escalate to Eng (Locked)'}</span>
          </button>
          <p
            className={`text-xs mt-1.5 text-center ${
              canEscalate
                ? 'text-emerald-700 font-bold'
                : isConfig
                ? 'text-amber-800 font-bold'
                : 'text-slate-500 font-medium'
            }`}
          >
            {canEscalate
              ? "✓ All pre-flight criteria satisfied. Sandeep's queue unlocked."
              : isConfig
              ? '⚠️ Disabled: Configuration issue. Resolve via L1 action.'
              : '⚠️ Complete all 3 checklist items above to unlock.'}
          </p>
        </div>

        <div>
          <button
            onClick={() => resolveTicketLive(ticket.ticket_id)}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl text-sm font-bold bg-amber-500 hover:bg-amber-600 text-slate-950 transition shadow-sm border border-amber-600 cursor-pointer"
          >
            <CheckCircle2 className="w-4 h-4 text-slate-950" />
            <span>Resolve Directly via L1 Guide</span>
          </button>
          <p className="text-xs text-slate-500 mt-1.5 text-center font-medium">
            ⚡ 8 min resolution • Bypasses 5.4-day bounce loop
          </p>
        </div>
      </div>
    </div>
  );
}
