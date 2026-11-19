import React, { useState } from 'react';
import { useTickets } from '../context/TicketContext';
import {
  Columns2,
  Zap,
  BarChart3,
  FileText,
  Inbox,
  UserCheck,
  PanelLeftClose,
  PanelLeftOpen
} from 'lucide-react';

export default function Sidebar() {
  const { activeTab, setActiveTab, openBacklogCount, filterToBacklogOnly } = useTickets();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const navItems = [
    { id: 'triage', label: 'Review Desk', icon: Columns2 },
    { id: 'quickfix', label: 'Run Studio (Quick-Fix)', icon: Zap },
    { id: 'analytics', label: 'Command Center', icon: BarChart3 },
    { id: 'deck', label: 'Executive Deck', icon: FileText }
  ];

  return (
    <aside
      className={`${
        isCollapsed ? 'w-20' : 'w-64'
      } shrink-0 bg-white border-r border-slate-200 flex flex-col justify-between h-screen sticky top-0 z-30 select-none transition-all duration-200`}
    >
      <div>
        {/* Brand Header */}
        <div
          className={`h-16 flex items-center border-b border-slate-100 ${
            isCollapsed ? 'justify-center px-2' : 'justify-between px-5'
          }`}
        >
          {isCollapsed ? (
            <button
              onClick={() => setIsCollapsed(false)}
              className="w-10 h-10 rounded-xl bg-slate-900 text-white font-extrabold text-sm flex items-center justify-center hover:bg-black transition shadow-sm cursor-pointer"
              title="Expand Sidebar"
            >
              RO
            </button>
          ) : (
            <>
              <span className="font-extrabold text-xl tracking-tight text-slate-900">RideOps</span>
              <button
                onClick={() => setIsCollapsed(true)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition cursor-pointer"
                title="Collapse Sidebar"
              >
                <PanelLeftClose className="w-5 h-5" />
              </button>
            </>
          )}
        </div>

        <div className="p-3.5 space-y-3">
          {/* Active Backlog Button */}
          {isCollapsed ? (
            <button
              onClick={() => {
                setActiveTab('triage');
                filterToBacklogOnly();
              }}
              className="relative w-full h-11 bg-slate-900 hover:bg-black text-white rounded-xl flex items-center justify-center shadow-sm transition cursor-pointer"
              title={`Active Backlog (${openBacklogCount})`}
            >
              <Inbox className="w-5 h-5 text-amber-400" />
              <span className="absolute -top-1.5 -right-1.5 bg-rose-500 text-white text-[10px] font-extrabold px-1.5 py-0.5 rounded-full border border-white">
                {openBacklogCount}
              </span>
            </button>
          ) : (
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
          )}

          {/* Navigation Links */}
          <nav className="space-y-1.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  title={isCollapsed ? item.label : undefined}
                  className={`w-full flex items-center rounded-xl text-sm transition cursor-pointer ${
                    isCollapsed ? 'justify-center h-11 px-0' : 'justify-between px-3.5 py-3'
                  } ${
                    isActive
                      ? 'bg-slate-100 text-slate-900 font-bold'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50 font-semibold'
                  }`}
                >
                  {!isCollapsed && <span>{item.label}</span>}
                  <Icon className={`w-4 h-4 ${isActive ? 'text-slate-900' : 'text-slate-400'}`} />
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Footer Area: Persona & Bottom Collapse Toggle Button */}
      <div className="border-t border-slate-100 p-3 space-y-2">
        {!isCollapsed && (
          <div className="px-2 py-1 text-xs text-slate-500 font-medium space-y-0.5">
            <div className="flex items-center gap-1.5 font-bold text-slate-700 text-xs">
              <UserCheck className="w-4 h-4 text-amber-600" />
              <span>User: L1 Support</span>
            </div>
            <div className="text-[11px] text-slate-400">Gatekeeper v1.0</div>
          </div>
        )}

        {/* Bottom Collapse Button (matching HookScene) */}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className={`w-full flex items-center rounded-xl py-2.5 text-xs font-bold text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer ${
            isCollapsed ? 'justify-center px-0' : 'justify-between px-3'
          }`}
          title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
        >
          {!isCollapsed && <span>Collapse</span>}
          {isCollapsed ? <PanelLeftOpen className="w-4 h-4" /> : <PanelLeftClose className="w-4 h-4" />}
        </button>
      </div>
    </aside>
  );
}
