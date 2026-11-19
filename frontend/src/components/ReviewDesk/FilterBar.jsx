import React from 'react';
import { useTickets } from '../../context/TicketContext';
import { Search, AlertCircle, ChevronLeft, ChevronRight } from 'lucide-react';

export default function FilterBar() {
  const {
    tickets,
    filteredTickets,
    selectedTicketId,
    setSelectedTicketId,
    searchQuery,
    setSearchQuery,
    filterCategory,
    setFilterCategory,
    filterPriority,
    setFilterPriority,
    filterRisk,
    setFilterRisk,
    filterAgent,
    setFilterAgent,
    openBacklogCount,
    isBacklogFiltered,
    toggleBacklogFilter,
    prevTicket,
    nextTicket
  } = useTickets();

  const categories = Array.from(new Set(tickets.map((t) => t.category).filter(Boolean))).sort();
  const agents = Array.from(new Set(tickets.map((t) => t.assigned_agent).filter(Boolean))).sort();

  const currentIndex = filteredTickets.findIndex((t) => t.ticket_id === selectedTicketId);
  const total = filteredTickets.length;
  const currentNum = total > 0 && currentIndex >= 0 ? currentIndex + 1 : 0;

  return (
    <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-3 text-sm">
      {/* Search Input */}
      <div className="relative flex-1 max-w-sm">
        <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search by ticket ID, client, text..."
          className="w-full bg-white border border-slate-200 rounded-xl pl-10 pr-3.5 py-2.5 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 text-sm font-medium shadow-sm"
        />
      </div>

      {/* Dropdown Filters + Fast Backlog Toggle */}
      <div className="flex flex-wrap items-center gap-2">
        {/* 1-Click Active Backlog Button */}
        <button
          onClick={toggleBacklogFilter}
          className={`px-3.5 py-2.5 rounded-xl text-sm font-bold transition flex items-center gap-2 shadow-sm cursor-pointer ${
            isBacklogFiltered
              ? 'bg-rose-50 border border-rose-300 text-rose-800 ring-1 ring-rose-400'
              : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
          }`}
        >
          <AlertCircle className="w-4 h-4 text-rose-500" />
          <span>Active Backlog ({openBacklogCount})</span>
        </button>

        <select
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          className="bg-white border border-slate-200 rounded-xl px-3.5 py-2.5 text-slate-700 font-semibold focus:outline-none focus:ring-2 focus:ring-slate-900 shadow-sm cursor-pointer text-sm"
        >
          <option value="ALL">All Categories</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>

        <select
          value={filterPriority}
          onChange={(e) => setFilterPriority(e.target.value)}
          className="bg-white border border-slate-200 rounded-xl px-3.5 py-2.5 text-slate-700 font-semibold focus:outline-none focus:ring-2 focus:ring-slate-900 shadow-sm cursor-pointer text-sm"
        >
          <option value="ALL">All Priorities</option>
          <option value="P1">P1 Critical</option>
          <option value="P2">P2 High</option>
          <option value="P3">P3 Normal</option>
          <option value="P4">P4 Low</option>
        </select>

        <select
          value={filterRisk}
          onChange={(e) => setFilterRisk(e.target.value)}
          className="bg-white border border-slate-200 rounded-xl px-3.5 py-2.5 text-slate-700 font-semibold focus:outline-none focus:ring-2 focus:ring-slate-900 shadow-sm cursor-pointer text-sm"
        >
          <option value="ALL">All Tickets</option>
          <option value="HIGH_RISK">⚠️ High Risk Escalations</option>
          <option value="OPEN">Open Tickets Only</option>
          <option value="ESCALATED">Historical Escalations</option>
          <option value="RESOLVED_L1">Resolved by L1</option>
        </select>

        <select
          value={filterAgent}
          onChange={(e) => setFilterAgent(e.target.value)}
          className="bg-white border border-slate-200 rounded-xl px-3.5 py-2.5 text-slate-700 font-semibold focus:outline-none focus:ring-2 focus:ring-slate-900 shadow-sm cursor-pointer text-sm"
        >
          <option value="ALL">All Agents</option>
          {agents.map((a) => (
            <option key={a} value={a}>
              {a}
            </option>
          ))}
        </select>
      </div>

      {/* Pagination Indicator */}
      <div className="flex items-center gap-2 text-slate-600 font-semibold self-end lg:self-center">
        <span className="font-mono text-sm">
          {currentNum} of {total}
        </span>
        <div className="flex items-center border border-slate-200 rounded-lg bg-white overflow-hidden shadow-sm">
          <button
            onClick={prevTicket}
            className="p-2 hover:bg-slate-50 transition border-r border-slate-200 text-slate-600 cursor-pointer"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button
            onClick={nextTicket}
            className="p-2 hover:bg-slate-50 transition text-slate-600 cursor-pointer"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
