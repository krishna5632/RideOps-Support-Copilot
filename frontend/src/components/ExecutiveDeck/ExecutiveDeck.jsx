import React from 'react';
import { useTickets } from '../../context/TicketContext';
import { ChevronLeft, ChevronRight, Printer } from 'lucide-react';

export default function ExecutiveDeck() {
  const { currentSlide, setCurrentSlide, totalSlides } = useTickets();

  const prevSlide = () => setCurrentSlide((s) => Math.max(1, s - 1));
  const nextSlide = () => setCurrentSlide((s) => Math.min(totalSlides, s + 1));

  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Executive Presentation Master</h1>
          <p className="text-sm text-slate-500 font-medium mt-1">
            8-Slide Briefing Prepared for Ritika, Meera and Sandeep
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => window.print()}
            className="hidden sm:flex items-center gap-1.5 px-3 py-2 border border-slate-200 rounded-lg bg-white hover:bg-slate-50 text-slate-700 text-xs font-bold transition shadow-sm cursor-pointer"
            title="Print or Save Deck as PDF"
          >
            <Printer className="w-3.5 h-3.5 text-slate-500" />
            <span>Print / PDF</span>
          </button>
          <button
            onClick={prevSlide}
            className="p-2.5 border border-slate-200 rounded-lg bg-white hover:bg-slate-50 text-slate-600 transition shadow-sm cursor-pointer"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="font-mono text-sm font-bold px-3.5 py-1.5 bg-white border border-slate-200 rounded-lg text-slate-800 shadow-sm">
            Slide {currentSlide} of {totalSlides}
          </span>
          <button
            onClick={nextSlide}
            className="p-2.5 border border-slate-200 rounded-lg bg-white hover:bg-slate-50 text-slate-600 transition shadow-sm cursor-pointer"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-8 sm:p-10 shadow-sm min-h-[480px]">
        {/* Slide 1 */}
        {currentSlide === 1 && (
          <div className="space-y-5">
            <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded uppercase">
              Slide 1: Executive Dilemma
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              Breaking the Deadlock: Solving Support's Backlog Without Adding Headcount
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm pt-2">
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
                <b className="text-slate-900 block text-sm">Meera (Support Lead)</b>
                <p className="text-slate-600 italic leading-relaxed text-sm">
                  "Engineering is a black hole. Tickets disappear for days and clients scream for updates."
                </p>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
                <b className="text-slate-900 block text-sm">Sandeep (Eng Manager)</b>
                <p className="text-slate-600 italic leading-relaxed text-sm">
                  "Support sends us junk with no logs. More than half are client config mistakes."
                </p>
              </div>
              <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl space-y-1.5">
                <b className="text-amber-900 block text-sm">Ritika (Head of Ops)</b>
                <p className="text-amber-900 font-semibold leading-relaxed text-sm">
                  "No finger-pointing. Bring open backlog down this quarter with ZERO hiring budget."
                </p>
              </div>
            </div>
            <p className="text-sm sm:text-base text-slate-700 leading-relaxed pt-2">
              <b>Strategic Assessment:</b> The surge (+51.8% in Q3) caused support to escalate 33.7% of tickets. But 56.6% of those escalations are not code bugs! Stopping bad escalations at L1 unlocks 2 full-time engineers' bandwidth and solves the backlog at $0 cost.
            </p>
          </div>
        )}

        {/* Slide 2 */}
        {currentSlide === 2 && (
          <div className="space-y-5">
            <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded uppercase">
              Slide 2: Diagnosis
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              The Data Proves Sandeep is Right: 56.6% of Escalations Are Waste
            </h2>
            <div className="text-sm sm:text-base space-y-3 text-slate-800">
              <div className="p-3.5 bg-rose-50 border border-rose-200 rounded-lg text-rose-900 font-bold">
                Out of 486 engineering escalations, 275 tickets were NOT software bugs:
              </div>
              <ul className="space-y-2 pl-2">
                <li>• <b>89 tickets (18.3%):</b> Insufficient info (Support didn't collect basic device logs).</li>
                <li>• <b>84 tickets (17.3%):</b> Client configuration issues (Admin changed cutoff times).</li>
                <li>• <b>56 tickets (11.5%):</b> Duplicate of known issue.</li>
                <li>• <b>46 tickets (9.5%):</b> How-to queries or not reproducible.</li>
                <li>• <b>Only 211 tickets (43.4%):</b> Were legitimate software code fixes!</li>
              </ul>
            </div>
          </div>
        )}

        {/* Slide 3 */}
        {currentSlide === 3 && (
          <div className="space-y-5">
            <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded uppercase">
              Slide 3: Cycle Time Analysis
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              The Data Also Proves Meera is Right: The 5-Day Ping-Pong Delay
            </h2>
            <div className="text-sm sm:text-base space-y-3 text-slate-800">
              <p>When support prematurely escalates without verification, tickets bounce between L1 and Engineering 2 to 3 times:</p>
              <div className="grid grid-cols-2 gap-3.5 pt-1">
                <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg">
                  <b className="text-slate-800">Resolved by L1 (No Escalation):</b>
                  <div className="text-emerald-700 font-bold text-lg mt-1 font-mono">12.6 hrs (CSAT: 4.01)</div>
                </div>
                <div className="p-4 bg-rose-50 border border-rose-200 rounded-lg">
                  <b className="text-rose-900">Config Issue Bounced to L1:</b>
                  <div className="text-rose-700 font-bold text-lg mt-1 font-mono">128.6 hrs / 5.4 days (CSAT: 2.43)</div>
                </div>
              </div>
              <p className="pt-2 text-slate-600 italic">Premature escalation is the #1 driver of customer dissatisfaction.</p>
            </div>
          </div>
        )}

        {/* Slide 4 */}
        {currentSlide === 4 && (
          <div className="space-y-5">
            <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded uppercase">
              Slide 4: Focus Strategy
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              Where to Focus: 3 Categories Drive 78% of All Escalations
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5 text-sm pt-1">
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
                <b className="text-slate-900 block text-sm">1. Roster Sync (175 Escalated)</b>
                <p className="text-slate-600 leading-relaxed text-sm">
                  Root cause: Cutoff times changed in portal. Solvable in 2 mins via L1 sync tool.
                </p>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
                <b className="text-slate-900 block text-sm">2. Live Tracking / GPS (127 Escalated)</b>
                <p className="text-slate-600 leading-relaxed text-sm">
                  Root cause: Missing telemetry & battery saver mode. Mandatory diagnostic gatekeeper stops 89% of rejections.
                </p>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
                <b className="text-slate-900 block text-sm">3. Report Export (77 Escalated)</b>
                <p className="text-slate-600 leading-relaxed text-sm">
                  Root cause: &gt;14 day database joins. Automated batch partitioner finishes in 4s.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Slide 5 */}
        {currentSlide === 5 && (
          <div className="space-y-5">
            <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded uppercase">
              Slide 5: Metrics
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              The Week-to-Week Success Framework
            </h2>
            <div className="text-sm sm:text-base space-y-3.5">
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <b>North Star Metric:</b> Active Open Support Backlog (Target: -40% in 4 weeks, from ~50 down to &lt;20).
              </div>
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <b>Primary Leading Indicator:</b> Escalation Rejection Rate (Target: reduce from 56.6% down to &lt;15%).
              </div>
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <b>Guardrails:</b> L1 Turnaround &lt; 12 hrs, CSAT ≥ 4.2, Reopen Rate &lt; 5%.
              </div>
            </div>
          </div>
        )}

        {/* Slide 6 */}
        {currentSlide === 6 && (
          <div className="space-y-5">
            <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded uppercase">
              Slide 6: Tool Capabilities
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              The Working v0 Tool: Smart Triage & Pre-Escalation Gatekeeper
            </h2>
            <p className="text-sm sm:text-base text-slate-700 leading-relaxed">
              Equips L1 agents with automated root-cause detection, locks premature engineering escalations behind a 3-question checklist, and provides instant self-service configuration overrides.
            </p>
          </div>
        )}

        {/* Slide 7 */}
        {currentSlide === 7 && (
          <div className="space-y-5">
            <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded uppercase">
              Slide 7: 4-Week Schedule & Non-Goals
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              Execution Schedule and What We Will NOT Do
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm pt-2">
              <div className="space-y-2.5">
                <b className="text-slate-900 uppercase text-xs block">4-Week Phased Rollout:</b>
                <div className="p-2.5 bg-slate-50 rounded border border-slate-200">Week 1: Deploy Gatekeeper for Top 3 categories; coach Rahul T.</div>
                <div className="p-2.5 bg-slate-50 rounded border border-slate-200">Week 2: Release Self-Service Cutoff Sync to L1 team.</div>
                <div className="p-2.5 bg-slate-50 rounded border border-slate-200">Week 3: Automated ticket status tracking on portal/WhatsApp.</div>
                <div className="p-2.5 bg-slate-50 rounded border border-slate-200">Week 4: Support-Engineering SLA contracts (auto-reject in 2h).</div>
              </div>
              <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl space-y-2">
                <b className="text-rose-900 uppercase text-xs block">What We Deliberately Will NOT Do:</b>
                <ul className="space-y-2 text-rose-900 leading-relaxed text-sm">
                  <li>❌ Do NOT hire new agents or engineers (Zero-budget mandate).</li>
                  <li>❌ Do NOT rewrite core backend software (quarterly crisis).</li>
                  <li>❌ Do NOT deploy a generic customer chatbot (causes B2B friction).</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Slide 8 */}
        {currentSlide === 8 && (
          <div className="space-y-5">
            <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded uppercase">
              Slide 8: Immediate Next Steps
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              Action Plan for Tomorrow at 09:00 AM
            </h2>
            <div className="space-y-3.5 text-sm pt-1">
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">1. Sign-off with Ritika, Meera, and Sandeep on gatekeeper checklist.</div>
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">2. Deploy v0 to Rahul T and Karan B on the morning shift.</div>
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">3. Review first Friday deflection metrics toward the -40% backlog reduction goal.</div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
