import React from 'react';
import { useTickets } from '../../context/TicketContext';

export default function AgentMatrix() {
  const { tickets } = useTickets();

  const agentMap = {};
  tickets.forEach((t) => {
    const a = t.assigned_agent || 'General Support';
    if (!agentMap[a]) agentMap[a] = { count: 0, esc: 0, reopens: 0, csatSum: 0, csatCount: 0 };
    agentMap[a].count++;
    if (t.escalated_to_eng === 'Yes') agentMap[a].esc++;
    agentMap[a].reopens += Number(t.reopen_count) || 0;
    const csat = Number(t.csat_score) || 0;
    if (csat > 0) {
      agentMap[a].csatSum += csat;
      agentMap[a].csatCount++;
    }
  });

  const agentRows = Object.keys(agentMap)
    .sort((a, b) => agentMap[b].count - agentMap[a].count)
    .map((agentName) => {
      const d = agentMap[agentName];
      const escP = ((d.esc / d.count) * 100).toFixed(1);
      const reopenP = (d.reopens / d.count).toFixed(2);
      const csatAvg = d.csatCount > 0 ? (d.csatSum / d.csatCount).toFixed(2) : '3.80';

      let coachingTag = <span className="text-slate-500 font-medium">Standard guidance</span>;
      let rowClass = '';
      if (Number(escP) > 50) {
        coachingTag = (
          <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-rose-100 text-rose-800 border border-rose-200">
            High Escalation: Train on pre-flight checks
          </span>
        );
        rowClass = 'bg-amber-50/40';
      } else if (Number(reopenP) > 0.20) {
        coachingTag = (
          <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-amber-100 text-amber-800 border border-amber-200">
            High Reopen: Coach on root cause verification
          </span>
        );
        rowClass = 'bg-amber-50/40';
      } else if (Number(csatAvg) >= 3.90) {
        coachingTag = (
          <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
            High CSAT Leader
          </span>
        );
      }

      return {
        agentName,
        count: d.count,
        escP,
        reopenP,
        csatAvg,
        coachingTag,
        rowClass
      };
    });

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900">
            Support Agent Discrepancy & Coaching Matrix
          </h3>
          <p className="text-xs text-slate-500">
            Root-cause identification of training gaps (Rahul T & Karan B coaching priorities)
          </p>
        </div>
        <span className="text-xs font-mono font-bold bg-slate-100 text-slate-700 px-3 py-1 rounded-lg">
          {agentRows.length} Agents
        </span>
      </div>

      <div className="overflow-x-auto text-sm">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-200 text-slate-600 font-bold uppercase text-xs">
              <th className="py-3 px-3.5">Agent</th>
              <th className="py-3 px-3.5">Tickets</th>
              <th className="py-3 px-3.5">Escalation Rate</th>
              <th className="py-3 px-3.5">Reopen Rate</th>
              <th className="py-3 px-3.5">Avg CSAT</th>
              <th className="py-3 px-3.5">Target Coaching Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 font-medium">
            {agentRows.map((r) => (
              <tr key={r.agentName} className={r.rowClass}>
                <td className="py-3 px-3.5 font-bold text-slate-900">{r.agentName}</td>
                <td className="py-3 px-3.5 font-mono text-slate-700">{r.count}</td>
                <td
                  className={`py-3 px-3.5 font-mono font-bold ${
                    Number(r.escP) > 50 ? 'text-rose-600' : 'text-slate-800'
                  }`}
                >
                  {r.escP}%
                </td>
                <td
                  className={`py-3 px-3.5 font-mono ${
                    Number(r.reopenP) > 0.20 ? 'font-bold text-rose-600' : 'text-slate-700'
                  }`}
                >
                  {r.reopenP}
                </td>
                <td className="py-3 px-3.5 font-mono font-bold text-slate-800">{r.csatAvg}</td>
                <td className="py-3 px-3.5">{r.coachingTag}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
