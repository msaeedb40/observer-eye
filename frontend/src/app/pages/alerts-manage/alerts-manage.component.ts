import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-alerts-manage',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-end">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Alert Configuration</h1>
          <p class="text-slate-400">Define monitoring conditions, thresholds, and notification routing</p>
        </div>
        <button class="btn-premium px-6 flex items-center gap-2">
          <span>+</span> Create New Rule
        </button>
      </header>

      <div class="glass-panel overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm">
            <thead>
              <tr class="text-slate-500 border-b border-white/5 bg-slate-900/40">
                <th class="p-4 font-semibold uppercase text-[10px]">Rule Name</th>
                <th class="p-4 font-semibold uppercase text-[10px]">Condition</th>
                <th class="p-4 font-semibold uppercase text-[10px]">Severity</th>
                <th class="p-4 font-semibold uppercase text-[10px]">Channels</th>
                <th class="p-4 font-semibold uppercase text-[10px]">Active</th>
                <th class="p-4 font-semibold uppercase text-[10px]">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr *ngFor="let rule of alertRules" class="hover:bg-white/[0.02] transition-colors">
                <td class="p-4 font-bold text-white">{{rule.name}}</td>
                <td class="p-4 font-mono text-sky-400 text-xs">{{rule.condition}}</td>
                <td class="p-4">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase" 
                        [ngClass]="rule.severity === 'critical' ? 'bg-rose-500/20 text-rose-500' : 'bg-amber-500/20 text-amber-400'">
                    {{rule.severity}}
                  </span>
                </td>
                <td class="p-4 text-slate-400 text-xs">{{rule.channels.join(', ')}}</td>
                <td class="p-4">
                  <div class="w-10 h-5 rounded-full p-0.5 cursor-pointer transition-colors"
                       [ngClass]="rule.enabled ? 'bg-sky-500/40 border border-sky-500/30' : 'bg-slate-800 border border-white/5'">
                    <div class="w-4 h-4 rounded-full bg-white shadow-sm transition-transform"
                         [style.transform]="rule.enabled ? 'translateX(20px)' : 'translateX(0)'"></div>
                  </div>
                </td>
                <td class="p-4">
                  <div class="flex gap-3">
                    <button class="p-2 hover:bg-white/5 rounded-lg text-slate-500 hover:text-sky-400 transition-colors">✏️</button>
                    <button class="p-2 hover:bg-white/5 rounded-lg text-slate-500 hover:text-rose-400 transition-colors">🗑️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class AlertsManageComponent implements OnInit {
  alertRules = [
    { name: 'High CPU Usage', condition: 'cpu.avg_usage > 92%', severity: 'critical', channels: ['Slack', 'Email'], enabled: true },
    { name: 'API Latency Spike', condition: 'http.latency_p95 > 450ms', severity: 'high', channels: ['PagerDuty'], enabled: true },
    { name: 'Memory Leak Detection', condition: 'mem.usage_delta > 15%/hr', severity: 'high', channels: ['Slack'], enabled: false }
  ];

  ngOnInit(): void { }
}
