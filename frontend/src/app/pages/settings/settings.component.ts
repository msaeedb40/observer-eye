import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Platform Settings</h1>
        <p class="text-slate-400">Manage global observability configurations and data retention</p>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-1 space-y-4">
          <div *ngFor="let group of settingGroups" 
               class="glass-panel p-4 cursor-pointer hover:bg-white/5 transition-colors border-l-2"
               [ngClass]="activeGroup === group.id ? 'border-sky-500 bg-white/5' : 'border-transparent'">
            <h3 class="font-bold text-white text-sm">{{group.label}}</h3>
            <p class="text-[10px] text-slate-500 mt-1">{{group.description}}</p>
          </div>
        </div>

        <div class="lg:col-span-2 space-y-6">
          <div class="glass-panel p-8">
            <h3 class="text-xl font-bold mb-6 text-white">General Configuration</h3>
            
            <div class="space-y-8">
              <div class="flex justify-between items-center group">
                <div>
                  <div class="font-bold text-slate-200">Real-time Telemetry</div>
                  <div class="text-xs text-slate-500 mt-1">Streaming data updates every 5 seconds via WebSockets.</div>
                </div>
                <div class="w-12 h-6 rounded-full bg-sky-500/20 border border-sky-500/30 p-1 cursor-pointer">
                  <div class="w-4 h-4 rounded-full bg-sky-400 ml-auto"></div>
                </div>
              </div>

              <div class="flex justify-between items-center group">
                <div>
                  <div class="font-bold text-slate-200">Anomalies Detection (AI)</div>
                  <div class="text-xs text-slate-500 mt-1">Enable automated pattern recognition and forecasting.</div>
                </div>
                <div class="w-12 h-6 rounded-full bg-sky-500/20 border border-sky-500/30 p-1 cursor-pointer">
                  <div class="w-4 h-4 rounded-full bg-sky-400 ml-auto"></div>
                </div>
              </div>

              <div class="flex justify-between items-center group">
                <div>
                  <div class="font-bold text-slate-200">Debug Verbosity</div>
                  <div class="text-xs text-slate-500 mt-1">Include trace-level logs in the Log Explorer (increases storage usage).</div>
                </div>
                <div class="w-12 h-6 rounded-full bg-white/5 border border-white/10 p-1 cursor-pointer">
                  <div class="w-4 h-4 rounded-full bg-slate-600"></div>
                </div>
              </div>

              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-3">Retention Policy (Days)</label>
                <div class="flex gap-4">
                  <div *ngFor="let d of [7, 14, 30, 90]" 
                       class="flex-1 p-4 rounded-xl border border-white/5 text-center cursor-pointer hover:bg-white/5 transition-colors"
                       [ngClass]="d === 30 ? 'bg-sky-500/10 border-sky-500/30 text-sky-400' : 'text-slate-400'">
                    <div class="text-lg font-bold">{{d}}</div>
                    <div class="text-[8px] uppercase font-bold text-slate-500">Days</div>
                  </div>
                </div>
              </div>

              <div class="pt-6 flex justify-end gap-3 border-t border-white/5">
                <button class="px-6 py-2 rounded-xl text-xs font-bold text-slate-400 hover:text-white transition-colors">Discard</button>
                <button class="btn-premium px-8 py-2 text-xs">Save Changes</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class SettingsComponent implements OnInit {
  activeGroup = 'gen';
  settingGroups = [
    { id: 'gen', label: 'General', description: 'Appearance and core platform behavior.' },
    { id: 'data', label: 'Data & Storage', description: 'Retention, indexing, and aggregation rules.' },
    { id: 'sec', label: 'Security & Access', description: 'Auth providers, API keys, and RBAC.' },
    { id: 'notif', label: 'Notifications', description: 'Alert channels, webhooks, and SMTP.' },
    { id: 'billing', label: 'Usage & Billing', description: 'Ingestion limits and subscription.' }
  ];

  ngOnInit(): void { }
}
