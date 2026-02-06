import { Component, OnInit, inject, ChangeDetectionStrategy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SettingsService } from '../../../services/settings.service';

@Component({
   selector: 'app-settings-integrations',
   standalone: true,
   imports: [CommonModule],
   changeDetection: ChangeDetectionStrategy.OnPush,
   template: `
    <div class="space-y-6 page-transition">
      <header class="flex justify-between items-end mb-8 bg-gradient-to-r from-sky-500/10 to-transparent p-6 rounded-2xl border border-white/5 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-sky-500 to-transparent"></div>
        <div>
          <h2 class="text-2xl font-black text-white mb-1 uppercase tracking-tighter">Third-party Integrations</h2>
          <p class="text-xs text-slate-500">Connect and manage external data sources and observability tools</p>
        </div>
        <button class="btn-premium px-6 py-2.5 text-[10px] group">
          <span class="group-hover:scale-125 transition-transform inline-block mr-2">+</span>
          Add Integration
        </button>
      </header>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div *ngFor="let integration of integrations()" 
             class="glass-panel p-6 border-t-4 transition-all hover:scale-[1.02] cursor-pointer group relative overflow-hidden"
             [ngClass]="integration.color">
          
          <div class="absolute inset-0 bg-white/[0.01] opacity-0 group-hover:opacity-100 transition-opacity"></div>

          <div class="flex justify-between items-start mb-6 relative z-10">
             <div class="w-14 h-14 rounded-2xl bg-white/5 flex items-center justify-center text-3xl shadow-inner border border-white/5 group-hover:rotate-6 transition-transform">
               {{integration.icon}}
             </div>
             <span class="px-2.5 py-1 bg-white/5 rounded-full text-[8px] font-black uppercase border border-white/5 tracking-widest"
                   [ngClass]="integration.status === 'Active' ? 'text-emerald-400 border-emerald-500/20' : 'text-slate-500'">
               {{integration.status}}
             </span>
          </div>
          <h3 class="font-black text-white mb-1 tracking-tight">{{integration.name}}</h3>
          <p class="text-[10px] text-slate-500 mb-8 font-mono tracking-tighter uppercase">{{integration.type}}</p>
          
          <div class="flex justify-between items-center pt-4 border-t border-white/5 relative z-10">
             <span class="text-[9px] text-slate-600 font-bold uppercase tracking-tighter italic">Synced {{integration.lastSync}}</span>
             <button class="text-sky-400 text-[10px] font-black uppercase tracking-widest hover:text-white transition-colors">Configure</button>
          </div>
        </div>

        <!-- Add Integration Card -->
        <div class="glass-panel p-6 border-2 border-dashed border-white/10 flex flex-col items-center justify-center gap-4 hover:border-sky-500/30 group transition-all cursor-pointer bg-white/[0.01]">
           <div class="w-14 h-14 rounded-full bg-white/5 flex items-center justify-center text-3xl text-slate-500 group-hover:text-sky-400 group-hover:scale-110 transition-all border border-white/5 shadow-inner">
             +
           </div>
           <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest group-hover:text-slate-300">Browse Marketplace</span>
        </div>
      </div>

      <!-- Webhooks Section -->
      <div class="glass-panel mt-10 border border-white/5 shadow-2xl relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-sky-500/30"></div>
        <div class="p-8 border-b border-white/5 flex justify-between items-center bg-white/[0.01]">
           <div>
             <h3 class="font-black text-white uppercase tracking-tight">Incoming Webhooks</h3>
             <p class="text-[10px] text-slate-500 mt-1">Direct ingest points for external system events</p>
           </div>
           <button class="px-5 py-2.5 bg-sky-500/10 border border-sky-500/20 rounded-xl text-[10px] font-black text-sky-400 hover:bg-sky-500/20 transition-all uppercase tracking-widest shadow-lg">
              Generate Hook
           </button>
        </div>
        <div class="divide-y divide-white/5">
           <div *ngFor="let hook of webhooks()" class="p-8 flex items-center justify-between hover:bg-white/[0.02] transition-all group">
              <div class="flex items-center gap-6">
                 <div class="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.6)] animate-pulse"></div>
                 <div>
                    <div class="font-bold text-slate-200 mb-1">{{hook.name}}</div>
                    <div class="text-[10px] font-mono text-slate-500 truncate max-w-[400px] border-b border-white/5 pb-1 select-all">{{hook.url}}</div>
                 </div>
              </div>
              <div class="flex items-center gap-10">
                 <div class="text-right">
                    <div class="text-[9px] font-black text-slate-600 uppercase tracking-widest mb-1">Requests (24h)</div>
                    <div class="text-lg font-black text-white tabular-nums">{{hook.requests}}</div>
                 </div>
                 <button class="p-3 rounded-xl hover:bg-rose-500/10 text-slate-600 hover:text-rose-400 transition-all group-hover:translate-x-0 translate-x-4 opacity-0 group-hover:opacity-100">
                   <span class="text-sm">🗑️</span>
                 </button>
              </div>
           </div>
        </div>
      </div>
    </div>
  `,
   styles: [`
    :host { display: block; }
    .border-orange { border-top-color: #f97316; }
    .border-blue { border-top-color: #3b82f6; }
    .border-red { border-top-color: #ef4444; }
    .border-indigo { border-top-color: #6366f1; }
    .border-emerald { border-top-color: #10b981; }
  `]
})
export class SettingsIntegrationsComponent implements OnInit {
   private readonly settingsService = inject(SettingsService);

   // Reactive signals for state
   readonly integrations = signal<any[]>([
      { name: 'AWS CloudWatch', type: 'Infra Metrics', status: 'Active', icon: '🟠', color: 'border-orange', lastSync: '2m ago' },
      { name: 'Sentry', type: 'Error Tracking', status: 'Healthy', icon: '🟣', color: 'border-indigo', lastSync: '15m ago' },
      { name: 'Datadog Ingest', type: 'APM Sync', status: 'Active', icon: '🟢', color: 'border-emerald', lastSync: '1h ago' },
      { name: 'PagerDuty', type: 'Incident Response', status: 'Active', icon: '🔴', color: 'border-red', lastSync: '12m ago' }
   ]);

   readonly webhooks = signal<any[]>([
      { name: 'production-ci-cd', url: 'https://api.observer-eye.io/v1/hooks/prod-8472-x283', requests: '1,240' },
      { name: 'security-scanner', url: 'https://api.observer-eye.io/v1/hooks/sec-947f-w192', requests: '42' }
   ]);

   ngOnInit(): void {
      this.loadIntegrations();
   }

   loadIntegrations(): void {
      // In a real app, fetch from backend via settingsService
      // this.settingsService.getSettingsByCategory('integrations').subscribe(...)
   }
}
