import React from 'react';
import { useTickets } from '../context/TicketContext';
import { Columns2, Zap, BarChart3, FileText, Inbox, UserCheck } from 'lucide-react';

export default function Sidebar() {
  const { activeTab, setActiveTab, openBacklogCount, filterToBacklogOnly } = useTickets();

  const navItems = [
    { id: 'triage', label: 'Review Desk', icon: Columns2 },
    { id: 'quickfix', label: 'Run Studio (Quick-Fix)', icon: Zap },
    { id: 'analytics', label: 'Command Center', icon: BarChart3 },
    { id: 'deck', label: 'Executive Deck', icon: FileText }
  ];

  return (
    <aside className="w-64 shrink-0 bg-white border-r border-slate-200 flex flex-col justify-between h-screen sticky top-0 z-30 select-none">
      <div>
        {/* Brand Header */}
        <div className="h-16 px-5 flex items-center justify-between border-b border-slate-100">
          <span className="font-extrabold text-xl tracking-tight text-slate-900">RideOps</span>
        </div>

        <div className="p-3.5 space-y-3">
          {/* Active Backlog Quick Action Button */}
          <button
            onClick={() => {
              setActiveTab('triage');
              filterToBacklogOnly();
            }}
            className="w-full h-11 bg-slate-900 hover:bg-black text-white font-bold text-sm rounded-xl flex items-center justify-between px-3.5 shadow-sm transition cursor-pointer"
          >
            <span>Active Backlog ({openBacklogCount})</span>
            <Inbox className="w-4 h-4 text-amber-400" />
          </button>

          {/* Navigation Links */}
          <nav className="space-y-1.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center justify-between px-3.5 py-3 rounded-xl text-sm transition cursor-pointer ${
                    isActive
                      ? 'bg-slate-100 text-slate-900 font-bold'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50 font-semibold'
                  }`}
                >
                  <span>{item.label}</span>
                  <Icon className={`w-4 h-4 ${isActive ? 'text-slate-700' : 'text-slate-400'}`} />
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Persona Footer */}
      <div className="p-4 border-t border-slate-100 text-xs text-slate-500 font-medium space-y-1">
        <div className="flex items-center gap-1.5 font-bold text-slate-700 text-xs">
          <UserCheck className="w-4 h-4 text-amber-600" />
          <span>User: L1 Support Agent</span>
        </div>
        <div className="text-xs text-slate-400">Pre-Escalation Gatekeeper v1.0</div>
      </div>
    </aside>
  );
}
