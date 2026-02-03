import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-integrations',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Integrations & Data Sources</h1>
        <p class="text-slate-400">Connect external telemetry streams and manage system-wide data ingestion</p>
      </header>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <div *ngFor="let source of dataSources" class="glass-panel p-6 card-hover-effect">
          <div class="flex items-center justify-between mb-6">
            <div class="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center text-2xl">
              {{source.type === 'postgres' ? '🗄️' : '📈'}}
            </div>
            <span class="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-[10px] font-bold rounded-full uppercase tracking-wider border border-emerald-500/20">
              {{source.status}}
            </span>
          </div>
          <h3 class="text-xl font-bold text-white mb-2">{{source.name}}</h3>
          <p class="text-slate-500 text-xs mb-6">Type: <span class="text-sky-400 font-mono">{{source.type}}</span> | Ingestion: <span class="text-slate-300">Active</span></p>
          
          <div class="flex gap-3">
            <button class="flex-1 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-xs font-bold text-white transition-colors border border-white/5">Configure</button>
            <button class="py-2 px-4 rounded-xl bg-white/5 hover:bg-white/10 text-xs text-slate-400 border border-white/5">Test</button>
          </div>
        </div>

        <div class="glass-panel border-2 border-dashed border-white/5 flex flex-col items-center justify-center p-6 cursor-pointer hover:bg-white/[0.02] transition-colors min-h-[220px]">
          <div class="w-12 h-12 rounded-full bg-sky-500/10 flex items-center justify-center text-sky-400 text-2xl mb-4">+</div>
          <div class="text-sm font-bold text-white">Add Data Source</div>
          <div class="text-[10px] text-slate-500 mt-1 uppercase tracking-widest font-bold">Postgres, Prometheus, gRPC</div>
        </div>
      </div>

      <section>
        <div class="flex items-center gap-4 mb-6">
          <h2 class="text-xl font-bold text-white">Configured Webhooks</h2>
          <div class="h-px flex-1 bg-white/5"></div>
        </div>

        <div class="glass-panel overflow-hidden">
          <div class="space-y-px">
            <div *ngFor="let hook of ['Alert Dispatcher', 'Slack Connector', 'PagerDuty Sink']" 
                 class="flex items-center justify-between p-5 bg-slate-900/30 hover:bg-white/[0.02] transition-colors border-b border-white/5 last:border-0">
              <div class="flex items-center gap-6">
                <div class="w-8 h-8 rounded-lg bg-orange-500/10 flex items-center justify-center text-orange-400 text-sm">🔗</div>
                <div>
                  <div class="font-bold text-slate-200">{{hook}}</div>
                  <div class="text-xs font-mono text-slate-500 mt-1">https://api.observereye.io/hooks/v1/internal-sink</div>
                </div>
              </div>
              <div class="flex items-center gap-4">
                <span class="px-2 py-0.5 bg-sky-500/10 text-sky-400 text-[10px] font-bold rounded border border-sky-500/20">PRODUCTION</span>
                <button class="p-2 hover:bg-white/5 rounded-lg transition-colors text-slate-500 hover:text-white">⚙️</button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class IntegrationsComponent implements OnInit {
  dataSources = [
    { name: 'Primary PostgreSQL', type: 'postgres', status: 'connected' },
    { name: 'Identity Store', type: 'postgres', status: 'connected' },
    { name: 'Prometheus Cluster', type: 'prometheus', status: 'connected' }
  ];

  ngOnInit(): void { }
}
