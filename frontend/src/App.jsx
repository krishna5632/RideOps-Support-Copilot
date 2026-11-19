import React from 'react';
import { useTickets } from './context/TicketContext';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Toast from './components/Toast';
import ReviewDesk from './components/ReviewDesk/ReviewDesk';
import RunStudio from './components/RunStudio/RunStudio';
import CommandCenter from './components/CommandCenter/CommandCenter';
import DeepDiagnosis from './components/DeepDiagnosis/DeepDiagnosis';
import ExecutiveDeck from './components/ExecutiveDeck/ExecutiveDeck';

export default function App() {
  const { activeTab } = useTickets();

  return (
    <div className="min-h-screen flex bg-[#F8FAFC] text-slate-900 text-sm">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header />
        <main className="flex-1 p-6 max-w-7xl w-full mx-auto">
          {activeTab === 'triage' && <ReviewDesk />}
          {activeTab === 'quickfix' && <RunStudio />}
          {activeTab === 'analytics' && <CommandCenter />}
          {activeTab === 'diagnosis' && <DeepDiagnosis />}
          {activeTab === 'deck' && <ExecutiveDeck />}
        </main>
      </div>
      <Toast />
    </div>
  );
}
