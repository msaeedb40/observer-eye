import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-logs',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-end">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Log Explorer</h1>
          <p class="text-slate-400">Centralized log aggregation and semantic search</p>
        </div>
        <div class="flex gap-4 mb-1">
          <div class="glass-panel px-4 py-2 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="text-xs font-bold text-slate-300">Live Stream</span>
          </div>
        </div>
      </header>

      <div class="glass-panel overflow-hidden">
        <div class="bg-slate-900/50 p-4 border-b border-white/5 flex gap-4">
          <input type="text" placeholder="Search logs (e.g. service:auth level:error)..." 
                 class="bg-slate-900 border border-white/10 rounded-lg px-4 py-2 text-sm w-full focus:outline-none focus:border-sky-500/50 transition-colors">
          <button class="btn-premium py-2 px-6 text-sm">Search</button>
        </div>
        
        <div class="p-0 font-mono text-xs leading-relaxed max-h-[600px] overflow-y-auto custom-scrollbar bg-[#020617]/80">
          <div *ngFor="let log of mockLogs" class="group flex border-b border-white/5 hover:bg-white/[0.02] transition-colors">
            <div class="py-2 px-4 border-r border-white/5 text-slate-500 whitespace-nowrap w-48">{{log.timestamp}}</div>
            <div class="py-2 px-4 border-r border-white/5 w-24 font-bold uppercase" 
                 [ngClass]="{'text-rose-400': log.level === 'ERROR', 'text-amber-400': log.level === 'WARN', 'text-sky-400': log.level === 'INFO'}">
              {{log.level}}
            </div>
            <div class="py-2 px-4 flex-1 text-slate-300 group-hover:text-white transition-colors">
              <span class="text-sky-400/80 mr-2">[{{log.service}}]</span>
              {{log.message}}
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
    .custom-scrollbar::-webkit-scrollbar { width: 6px; }
    .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
  `]
})
export class LogsComponent implements OnInit {
  mockLogs = [
    { timestamp: '2026-02-03 06:42:01', level: 'INFO', service: 'auth-srv', message: 'Successfully validated JWT for user: admin_01' },
    { timestamp: '2026-02-03 06:42:05', level: 'WARN', service: 'api-gateway', message: 'Rate limit threshold approaching for 192.168.1.45' },
    { timestamp: '2026-02-03 06:42:12', level: 'ERROR', service: 'payment-srv', message: 'Connection timeout: database cluster unreachable' },
    { timestamp: '2026-02-03 06:42:15', level: 'INFO', service: 'worker-04', message: 'Job 8842af complete. Total processing time: 452ms' },
    { timestamp: '2026-02-03 06:42:22', level: 'INFO', service: 'ingress', message: 'GET /api/v1/metrics 200 OK (latency: 12ms)' },
    { timestamp: '2026-02-03 06:42:25', level: 'ERROR', service: 'identity', message: 'Failed login attempt for user: guest. Origin: RU' },
    { timestamp: '2026-02-03 06:42:30', level: 'INFO', service: 'auth-srv', message: 'Refreshing session token for user: dev_tester' },
    { timestamp: '2026-02-03 06:42:31', level: 'INFO', service: 'system-srv', message: 'Health check passed for node-cluster-B' }
  ];

  ngOnInit(): void { }
}
