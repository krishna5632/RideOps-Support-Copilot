import React from 'react';
import RosterSyncTool from './RosterSyncTool';
import ReportPartitionTool from './ReportPartitionTool';
import GeocodeValidatorTool from './GeocodeValidatorTool';

export default function RunStudio() {
  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Run Studio</h1>
        <p className="text-sm text-slate-500 font-medium mt-1">
          L1 Self-Service Execution Engine & Client Configuration Fixes
        </p>
      </div>

      <div className="space-y-6">
        <RosterSyncTool />
        <ReportPartitionTool />
        <GeocodeValidatorTool />
      </div>
    </section>
  );
}
