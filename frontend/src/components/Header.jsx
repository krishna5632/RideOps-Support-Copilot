import React, { useRef } from 'react';
import { useTickets } from '../context/TicketContext';
import { Upload, Download, RotateCcw, FileSpreadsheet, BarChart3 } from 'lucide-react';

export default function Header() {
  const {
    activeTab,
    tickets,
    isCustomDataset,
    activeDatasetName,
    setIsDeepAnalysisOpen,
    resetToDefault,
    handleFileUpload,
    exportQueueCsv
  } = useTickets();

  const fileInputRef = useRef(null);

  const tabLabels = {
    triage: 'Review Desk',
    quickfix: 'Run Studio',
    analytics: 'Command Center',
    deck: 'Executive Deck'
  };

  const onFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file);
      e.target.value = '';
    }
  };

  return (
    <header className="h-16 bg-white border-b border-slate-200 sticky top-0 z-20 px-6 flex items-center justify-between select-none">
      <div className="flex items-center gap-3 text-sm">
        <span className="font-bold text-slate-900 text-sm">RideOps</span>
        <span className="text-slate-400">/</span>
        <span className="font-semibold text-slate-700 text-sm">{tabLabels[activeTab]}</span>

        {/* Status Pill */}
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-semibold">
          <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span>{tickets.length.toLocaleString()} Tickets Active</span>
        </span>

        {/* Custom Dataset Active Pill + 1-Click Reset Button */}
        {isCustomDataset && (
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 text-amber-900 border border-amber-300 text-xs font-bold">
              <FileSpreadsheet className="w-3.5 h-3.5 text-amber-600" />
              <span>{activeDatasetName}</span>
            </span>
            <button
              onClick={resetToDefault}
              className="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-300 text-xs font-bold transition flex items-center gap-1 shadow-sm cursor-pointer"
              title="Restore original 1,444 Q3 tickets"
            >
              <RotateCcw className="w-3 h-3 text-slate-500" />
              <span>Reset to Default (1,444)</span>
            </button>
          </div>
        )}
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3">
        {/* Export Queue Button */}
        <button
          onClick={exportQueueCsv}
          className="hidden sm:flex items-center gap-2 px-3.5 py-2 rounded-xl border border-slate-200 hover:bg-slate-50 text-xs font-bold text-slate-700 transition shadow-sm cursor-pointer"
          title="Download active filtered queue as CSV"
        >
          <Download className="w-4 h-4 text-slate-500" />
          <span>Export Queue</span>
        </button>

        {/* Hidden File Input */}
        <input
          type="file"
          ref={fileInputRef}
          accept=".csv"
          onChange={onFileChange}
          className="hidden"
        />

        {/* Diagnostic Findings Button */}
        <button
          onClick={() => setIsDeepAnalysisOpen(true)}
          className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-xs font-bold text-slate-700 transition shadow-sm cursor-pointer"
          title="Open Root-Cause Diagnostic Findings (8 Clean Diagrams)"
        >
          <BarChart3 className="w-4 h-4 text-amber-500" />
          <span className="hidden sm:inline">Diagnostic Findings</span>
          <span className="px-1.5 py-0.5 rounded-full bg-slate-100 text-slate-800 text-[10px] font-bold">8</span>
        </button>

        {/* Upload Custom CSV Button */}
        <button
          onClick={() => fileInputRef.current?.click()}
          className="flex items-center gap-2 px-3.5 py-2 rounded-xl border border-slate-200 hover:bg-slate-50 text-xs font-bold text-slate-700 transition shadow-sm cursor-pointer"
        >
          <Upload className="w-4 h-4 text-slate-500" />
          <span>Upload CSV</span>
        </button>

        {/* User Avatar */}
        <div
          className="w-9 h-9 rounded-full bg-amber-200 border border-amber-300 text-amber-950 font-bold text-xs flex items-center justify-center shadow-sm"
          title="Active Session: L1 Support"
        >
          RO
        </div>
      </div>
    </header>
  );
}
