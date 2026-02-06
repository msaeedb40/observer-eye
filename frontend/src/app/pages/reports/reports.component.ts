import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-reports',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-center">
        <div>
           <h1 class="text-4xl font-extrabold gradient-text mb-2">Reports & Exports</h1>
           <p class="text-slate-400">Scheduled analytics and on-demand PDF summaries</p>
        </div>
        <button class="btn-primary">
            <span class="mr-2">+</span> Create Schedule
        </button>
      </header>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
         <div *ngFor="let tmpl of templates" class="glass-panel p-6 card-hover-effect">
            <div class="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center text-2xl mb-4">
              {{tmpl.icon}}
            </div>
            <h3 class="font-bold text-lg mb-2">{{tmpl.name}}</h3>
            <p class="text-slate-400 text-sm mb-6">{{tmpl.desc}}</p>
            <button class="w-full py-2 bg-white/5 hover:bg-white/10 border border-white/5 rounded-lg text-sm font-bold transition-all flex items-center justify-center gap-2 text-indigo-300">
               Generate PDF
            </button>
         </div>
      </div>

      <div class="glass-panel overflow-hidden">
        <div class="p-6 border-b border-white/5 bg-white/[0.02]">
           <h3 class="font-bold">Recent Generated Reports</h3>
        </div>
        <div class="divide-y divide-white/5">
           <div *ngFor="let r of recentReports" class="p-4 flex items-center justify-between hover:bg-white/[0.02] transition-colors">
              <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-lg bg-slate-800 flex items-center justify-center text-slate-400">
                     <span class="font-black text-[10px] uppercase">PDF</span>
                  </div>
                  <div>
                     <h4 class="font-bold text-slate-200">{{r.name}}</h4>
                     <p class="text-xs text-slate-500">{{r.date}} • {{r.size}}</p>
                  </div>
              </div>
              <button class="text-xs font-bold text-sky-400 uppercase hover:text-white transition-colors">Download</button>
           </div>
        </div>
      </div>
    </div>
  `,
    styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class ReportsComponent implements OnInit {
    templates = [
        { name: 'Executive Summary', desc: 'High-level overview of system health and SLAs.', icon: '📊' },
        { name: 'Security Audit', desc: 'Detailed threat analysis and vulnerability report.', icon: '🛡️' },
        { name: 'Cost Analysis', desc: 'Resource utilization and estimated cloud costs.', icon: '💰' },
        { name: 'Incident Post-Mortem', desc: 'Logs and traces from recent critical alerts.', icon: '🔥' },
        { name: 'Traffic Insights', desc: 'Geographic and protocol traffic breakdown.', icon: '🌍' }
    ];

    recentReports = [
        { name: 'Weekly System Health - W42', date: 'Oct 24, 2024 09:00 AM', size: '2.4 MB' },
        { name: 'Security Incident #9921 Report', date: 'Oct 23, 2024 04:15 PM', size: '1.1 MB' },
        { name: 'Monthly Cost Forecast', date: 'Oct 01, 2024 00:00 AM', size: '850 KB' }
    ];

    ngOnInit(): void { }
}
