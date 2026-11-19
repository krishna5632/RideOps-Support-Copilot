import React, { useState } from 'react';
import { Bar } from 'react-chartjs-2';

export default function RoiSimulator() {
  const [targetPct, setTargetPct] = useState(60);

  const annualAvoidable = 275 * 4;
  const deflected = Math.round(annualAvoidable * (targetPct / 100));
  const hours = Math.round(deflected * 5.5);
  const fte = (hours / 1800).toFixed(1);
  const backlog = Math.round(50 * (1 - (targetPct / 100) * 0.7));

  const chartData = {
    labels: ['Turnaround (Hours)', 'Rejection Rate (%)'],
    datasets: [
      {
        label: 'Current Reality',
        data: [86.8, 56.6],
        backgroundColor: '#EF4444',
        borderRadius: 6
      },
      {
        label: 'With Gatekeeper v0',
        data: [
          Math.round(86.8 * (1 - (targetPct / 100) * 0.75)),
          Math.max(8, Math.round(56.6 * (1 - targetPct / 100)))
        ],
        backgroundColor: '#10B981',
        borderRadius: 6
      }
    ]
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div className="border-b border-slate-100 pb-3">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900">
          Executive Headcount ROI & Deflection Simulator
        </h3>
        <p className="text-xs text-slate-500">
          Simulate how eliminating avoidable engineering escalations unlocks capacity with $0 hiring.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        <div className="lg:col-span-5 space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2 font-bold">
              <span className="text-slate-800 text-sm">Target Deflection Rate:</span>
              <span className="font-mono text-sm text-amber-700 bg-amber-50 px-2.5 py-1 rounded border border-amber-200">
                {targetPct}%
              </span>
            </div>
            <input
              type="range"
              min="20"
              max="90"
              step="5"
              value={targetPct}
              onChange={(e) => setTargetPct(Number(e.target.value))}
              className="w-full accent-slate-900 cursor-pointer h-2 bg-slate-200 rounded-lg"
            />
            <div className="flex justify-between text-xs text-slate-500 font-semibold mt-1.5">
              <span>Conservative (20%)</span>
              <span>Balanced (60%)</span>
              <span>Aggressive (90%)</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3.5 pt-1">
            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl">
              <span className="text-xs font-bold uppercase text-slate-500 block">Annual Deflected</span>
              <span className="font-mono text-xl font-extrabold text-slate-900">{deflected}</span>
            </div>
            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl">
              <span className="text-xs font-bold uppercase text-slate-500 block">Eng Hours Saved</span>
              <span className="font-mono text-xl font-extrabold text-emerald-700">{hours.toLocaleString()} hrs</span>
            </div>
            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl">
              <span className="text-xs font-bold uppercase text-slate-500 block">FTE Eng Unlocked</span>
              <span className="font-mono text-xl font-extrabold text-slate-900">{fte} Eng</span>
            </div>
            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl">
              <span className="text-xs font-bold uppercase text-slate-500 block">Backlog Drop</span>
              <span className="font-mono text-xl font-extrabold text-blue-700">50 → {backlog}</span>
            </div>
          </div>
        </div>

        <div className="lg:col-span-7 bg-slate-50 border border-slate-200 rounded-xl p-4">
          <div className="h-56">
            <Bar
              data={chartData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } } },
                scales: {
                  y: { grid: { color: '#E2E8F0' }, ticks: { font: { size: 11 } } },
                  x: { grid: { display: false }, ticks: { font: { size: 11, weight: 'bold' } } }
                }
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
