import React from 'react';
import KpiCards from './KpiCards';
import ChartsSection from './ChartsSection';
import RoiSimulator from './RoiSimulator';
import AgentMatrix from './AgentMatrix';

export default function CommandCenter() {
  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Executive Command Center</h1>
        <p className="text-sm text-slate-500 font-medium mt-1">
          Root-Cause Operational Intelligence & Engineering Workload Deflection Analytics
        </p>
      </div>

      <KpiCards />
      <ChartsSection />
      <RoiSimulator />
      <AgentMatrix />
    </section>
  );
}
