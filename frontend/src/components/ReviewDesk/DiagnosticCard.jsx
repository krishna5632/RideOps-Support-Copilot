import React from 'react';

export default function DiagnosticCard({ ticket }) {
  if (!ticket) return null;

  const desc = (ticket.description || '').toLowerCase();
  let isConfig = false;
  let title = '';
  let text = '';
  let action = '';

  if (desc.includes('cutoff')) {
    isConfig = true;
    title = 'Shift Booking Cutoff Mismatch (Known Client Configuration)';
    text = 'Client admin updated shift cutoff settings in the HR portal, but bookings occurred past the cutoff window. This is NOT a software bug.';
    action = 'Advise corporate admin to approve late exception, or use the Shift Cutoff Sync tool in Run Studio to resolve immediately.';
  } else if (desc.includes('date range') || desc.includes('> 15 days') || desc.includes('stuck at loading')) {
    isConfig = true;
    title = 'Report Export Query Timeout (>14 Day GPS Join)';
    text = 'Database join timeout caused by requesting >14 days of raw GPS coordinate streams. Operational usage limit, not an engineering crash.';
    action = 'Advise client admin to export report in 7-day or 10-day intervals, or partition via Run Studio (finishes in 4s).';
  } else if (desc.includes('insurance expired') || desc.includes('compliance')) {
    isConfig = true;
    title = 'Vendor Vehicle Document Expired / Blocked';
    text = 'Vehicle blocked automatically by RideOps safety engine due to expired fitness/insurance certificates. Engineering cannot override legal safety rules.';
    action = 'Notify Vendor Ops team to upload renewed insurance document in the Vendor Portal.';
  } else if (desc.includes('frozen') || desc.includes('gps') || desc.includes('tracking')) {
    isConfig = false;
    title = 'Missing Device Telemetry Logs';
    text = "Telemetry signal ping missing. Historically, 89% of GPS tickets escalated without driver phone & vehicle ID are returned by Sandeep's team.";
    action = 'Collect driver phone number, cab license plate, and check driver app battery saver setting before escalating.';
  } else {
    isConfig = false;
    title = 'Legitimate Bug Investigation: Mandatory Verification';
    text = 'Potential code issue. Complete all pre-flight verification items before handoff to Engineering.';
    action = 'Attach client error screenshots and exact reproduction steps.';
  }

  return (
    <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-2.5">
      <div className="flex items-center gap-2 text-sm font-bold text-slate-900 uppercase tracking-wide">
        <span className="text-base">💡</span>
        <span>{title}</span>
      </div>
      <p className="text-sm text-slate-700 leading-relaxed font-medium">{text}</p>
      <div className="pt-2.5 border-t border-slate-200 text-sm text-slate-800">
        <span className="font-bold text-slate-900">Recommended Resolution Guide:</span>
        <p className="text-slate-700 mt-1 leading-relaxed">{action}</p>
      </div>
    </div>
  );
}
