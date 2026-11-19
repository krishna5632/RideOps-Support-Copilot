import os

index_path = r"c:\Users\prave\Downloads\RideOps_CaseStudy\index.html"

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Modal markup to replace <img> with <canvas>
old_img_block = """          <!-- Figure Image -->
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 flex flex-col items-center justify-center shadow-inner overflow-hidden">
            <img id="deepAnalysisImg" src="" alt="Figure" class="max-h-[300px] w-auto object-contain rounded-lg shadow-sm">
            <span class="text-[11px] text-slate-400 font-mono mt-2" id="deepAnalysisFigureLabel"></span>
          </div>"""

new_canvas_block = """          <!-- Native Chart.js Diagram (Matching Command Center) -->
          <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
            <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center justify-between">
              <span>Analysis Visualization</span>
              <span id="deepAnalysisFigureLabel" class="text-[11px] font-mono text-slate-400 font-normal"></span>
            </div>
            <div class="h-64 sm:h-72 w-full relative">
              <canvas id="deepAnalysisChartCanvas"></canvas>
            </div>
          </div>"""

if old_img_block in html:
    html = html.replace(old_img_block, new_canvas_block)

# 2. Add chart rendering function to selectDeepAnalysisFinding
old_img_js = """      const imgEl = document.getElementById('deepAnalysisImg');
      if (imgEl) {
        imgEl.src = f.figureImg;
        imgEl.alt = f.title;
      }

      const figLabelEl = document.getElementById('deepAnalysisFigureLabel');
      if (figLabelEl) {
        figLabelEl.innerText = `Figure ${idx + 1}: Generated from ${state.tickets.length.toLocaleString()} tickets dataset`;
      }"""

new_canvas_js = """      const figLabelEl = document.getElementById('deepAnalysisFigureLabel');
      if (figLabelEl) {
        figLabelEl.innerText = `Diagram ${idx + 1} of 8 (${state.tickets.length.toLocaleString()} tickets)`;
      }

      // Render native Chart.js diagram matching Command Center
      renderDeepAnalysisDiagram(idx);"""

if old_img_js in html:
    html = html.replace(old_img_js, new_canvas_js)

# 3. Add renderDeepAnalysisDiagram implementation
diagram_fn = """
    function renderDeepAnalysisDiagram(idx) {
      const canvas = document.getElementById('deepAnalysisChartCanvas');
      if (!canvas) return;
      if (state.charts.deepAnalysis) {
        state.charts.deepAnalysis.destroy();
      }
      const ctx = canvas.getContext('2d');

      const fontOpts = { family: 'Inter, system-ui, sans-serif', size: 11 };
      const commonScales = {
        y: { grid: { color: '#F1F5F9' }, ticks: { font: fontOpts } },
        x: { grid: { display: false }, ticks: { font: { ...fontOpts, weight: 'bold' } } }
      };

      let config;
      if (idx === 0) {
        // Inflow
        config = {
          type: 'bar',
          data: {
            labels: ['W1 (Jul)', 'W3 (Jul)', 'W5 (Aug)', 'W7 (Aug)', 'W9 (Sep)', 'W11 (Sep)', 'W13 (Peak)'],
            datasets: [
              { label: 'Weekly Volume', data: [87, 94, 102, 116, 128, 142, 164], backgroundColor: '#0F172A', borderRadius: 6 },
              { label: 'Shift Spikes (6-10 AM & 5-8 PM)', data: [42, 46, 51, 60, 68, 79, 95], backgroundColor: '#E8A72D', borderRadius: 6 }
            ]
          },
          options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top', labels: { boxWidth: 12, font: fontOpts } } }, scales: commonScales }
        };
      } else if (idx === 1) {
        // Waste Doughnut
        config = {
          type: 'doughnut',
          data: {
            labels: ['Genuine Code Bug (43.4%)', 'Missing Logs (18.3%)', 'Client Config (17.3%)', 'Duplicate (11.5%)', 'How-to / Other (9.5%)'],
            datasets: [{ data: [211, 89, 84, 56, 46], backgroundColor: ['#10B981', '#EF4444', '#F59E0B', '#6366F1', '#94A3B8'], borderWidth: 2, borderColor: '#FFF' }]
          },
          options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { boxWidth: 10, font: fontOpts } } } }
        };
      } else if (idx === 2) {
        // Latency
        config = {
          type: 'bar',
          data: {
            labels: ['Resolved by L1 (No Escalation)', 'Engineering Bug Fix', 'Config Issue Bounced to L1', 'Insufficient Info Bounced'],
            datasets: [{ label: 'Median Turnaround (Hours)', data: [12.6, 64.8, 128.6, 121.4], backgroundColor: ['#10B981', '#0F172A', '#EF4444', '#F59E0B'], borderRadius: 6 }]
          },
          options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: '#F1F5F9' }, ticks: { font: fontOpts } }, y: { grid: { display: false }, ticks: { font: { ...fontOpts, weight: 'bold' } } } } }
        };
      } else if (idx === 3) {
        // Category Pareto
        config = {
          type: 'bar',
          data: {
            labels: ['Roster Sync', 'Live Tracking', 'Report Export', 'Cab Complaint', 'Login / Access', 'Other'],
            datasets: [{ label: 'Escalations to Engineering', data: [175, 127, 77, 36, 28, 43], backgroundColor: ['#0F172A', '#0F172A', '#0F172A', '#94A3B8', '#94A3B8', '#CBD5E1'], borderRadius: 6 }]
          },
          options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top', labels: { boxWidth: 12, font: fontOpts } } }, scales: commonScales }
        };
      } else if (idx === 4) {
        // Client Tier
        config = {
          type: 'bar',
          data: {
            labels: ['Enterprise (739 Tickets)', 'Mid-Market (462 Tickets)', 'SMB (243 Tickets)'],
            datasets: [{ label: 'Ticket Volume by Tier', data: [739, 462, 243], backgroundColor: ['#0F172A', '#3B82F6', '#94A3B8'], borderRadius: 6 }]
          },
          options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top', labels: { boxWidth: 12, font: fontOpts } } }, scales: commonScales }
        };
      } else if (idx === 5) {
        // Agent Variance
        config = {
          type: 'bar',
          data: {
            labels: ['Priya D', 'Vikram S', 'Ananya M', 'Rohan P', 'Neha R', 'Amit K', 'Karan B', 'Rahul T'],
            datasets: [{ label: 'Escalation Rate (%)', data: [24.5, 27.2, 30.1, 32.4, 34.8, 36.5, 39.1, 41.2], backgroundColor: ['#10B981', '#10B981', '#3B82F6', '#3B82F6', '#F59E0B', '#F59E0B', '#EF4444', '#EF4444'], borderRadius: 6 }]
          },
          options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top', labels: { boxWidth: 12, font: fontOpts } } }, scales: commonScales }
        };
      } else if (idx === 6) {
        // CSAT
        config = {
          type: 'bar',
          data: {
            labels: ['L1 Direct Solve', 'Bug Fixed by Eng', 'Bounced Config Error', 'Reopened Once', 'Reopened Twice'],
            datasets: [{ label: 'Average CSAT Score (1 to 5)', data: [4.01, 3.42, 2.43, 2.85, 1.33], backgroundColor: ['#10B981', '#3B82F6', '#EF4444', '#F59E0B', '#991B1B'], borderRadius: 6 }]
          },
          options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top', labels: { boxWidth: 12, font: fontOpts } } }, scales: commonScales }
        };
      } else {
        // ROI
        config = {
          type: 'bar',
          data: {
            labels: ['False Escalations', 'Senior Dev Hours', 'Active Open Backlog', 'Mean Turnaround (Hrs)'],
            datasets: [
              { label: 'Current Baseline (Q3)', data: [275, 550, 48, 44.2], backgroundColor: '#EF4444', borderRadius: 6 },
              { label: 'With Gatekeeper v0 (Projected)', data: [83, 166, 15, 16.5], backgroundColor: '#10B981', borderRadius: 6 }
            ]
          },
          options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top', labels: { boxWidth: 12, font: fontOpts } } }, scales: commonScales }
        };
      }

      state.charts.deepAnalysis = new Chart(ctx, config);
    }
"""

if "function renderDeepAnalysisDiagram" not in html:
    html = html.replace("function selectDeepAnalysisFinding(idx) {", diagram_fn + "\n    function selectDeepAnalysisFinding(idx) {")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("index.html upgraded with native Chart.js diagrams!")
