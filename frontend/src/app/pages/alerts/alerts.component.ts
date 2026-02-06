import { Component, OnInit, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AlertsService } from '../../services/alerts.service';

@Component({
  selector: 'app-alerts',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-end bg-gradient-to-r from-rose-500/10 to-transparent p-6 rounded-2xl border border-white/5 shadow-xl relative overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-rose-500 to-transparent"></div>
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Alert Center</h1>
          <p class="text-slate-400">Manage incident lifecycle and rule configurations</p>
        </div>
        <div class="flex gap-4">
          <div class="glass-panel px-6 py-2 border border-rose-500/20 shadow-[0_0_15px_rgba(244,63,94,0.1)]">
            <div class="text-[10px] text-slate-500 uppercase font-extrabold tracking-widest mb-1">Active Now</div>
            <div class="text-2xl font-black text-rose-500">{{alertsService.activeAlertCount()}}</div>
          </div>
          <button class="btn-premium px-8 py-2.5 flex items-center gap-2 group" (click)="refresh()">
            <span class="group-hover:rotate-180 transition-transform duration-500">🔄</span> 
            <span>Refresh</span>
          </button>
        </div>
      </header>

      <div class="bento-grid">
        <!-- Summary Card -->
        <div class="glass-panel p-6 col-span-12 md:col-span-4 row-span-1 border-l-4 border-l-sky-500 bg-white/[0.01]">
          <h3 class="text-sm font-bold text-slate-500 uppercase tracking-wider mb-4">Integrity Status</h3>
          <div class="flex items-center gap-4">
            <div class="text-4xl font-black text-white">98.2%</div>
            <div class="text-[10px] text-emerald-400 font-bold bg-emerald-400/10 px-2 py-1 rounded border border-emerald-400/20">+0.5% (24h)</div>
          </div>
          <p class="text-xs text-slate-400 mt-2">Platform monitoring sub-systems are all nominal.</p>
        </div>

        <div class="glass-panel p-6 col-span-12 md:col-span-4 row-span-1 border-l-4 border-l-amber-500 bg-white/[0.01]">
          <h3 class="text-sm font-bold text-slate-500 uppercase tracking-wider mb-4">Mean Time to Detect (MTTD)</h3>
          <div class="flex items-center gap-4">
            <div class="text-4xl font-black text-white">4.2m</div>
            <div class="text-[10px] text-rose-400 font-bold bg-rose-400/10 px-2 py-1 rounded border border-rose-400/20">-12% (7d)</div>
          </div>
          <p class="text-xs text-slate-400 mt-2">Average detection time across all priority tiers.</p>
        </div>

        <div class="glass-panel p-6 col-span-12 md:col-span-4 row-span-1 border-l-4 border-l-rose-500 bg-white/[0.01]">
          <h3 class="text-sm font-bold text-slate-500 uppercase tracking-wider mb-4">Open Incidents</h3>
          <div class="flex items-center gap-4">
            <div class="text-4xl font-black text-white">{{alertsService.activeAlertCount()}}</div>
            <div class="text-[10px] text-slate-400 font-bold bg-white/5 px-2 py-1 rounded border border-white/10 uppercase tracking-tighter">Real-time Signal</div>
          </div>
          <p class="text-xs text-slate-400 mt-2">Currently being triaged by SRE teams.</p>
        </div>

        <!-- Alerts List -->
        <div class="col-span-12 flex flex-col gap-4 mt-6">
          <div *ngFor="let alert of alertsService.activeAlerts()" 
               class="glass-panel p-6 border-l-4 card-hover-effect group border-white/5 relative overflow-hidden" 
               [ngClass]="getSeverityBorder(alert.severity)">
            
            <div class="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                 [ngClass]="getSeverityGradient(alert.severity)"></div>

            <div class="flex justify-between items-start relative z-10">
              <div class="flex gap-6">
                <div class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center text-3xl shadow-inner border border-white/5 group-hover:scale-110 transition-transform">
                  {{alert.icon || '🔔'}}
                </div>
                <div>
                  <div class="flex items-center gap-4 mb-2">
                    <h3 class="text-xl font-black text-white tracking-tight">{{alert.title}}</h3>
                    <span class="px-2.5 py-0.5 rounded-full text-[9px] font-black uppercase tracking-widest border" 
                          [ngClass]="getSeverityBadge(alert.severity)">
                      {{alert.severity}}
                    </span>
                  </div>
                  <p class="text-slate-400 text-sm max-w-3xl leading-relaxed">{{alert.description}}</p>
                  <div class="mt-5 flex items-center gap-8">
                    <div class="flex items-center gap-2">
                      <span class="text-slate-500 text-[10px] uppercase font-black tracking-widest">Triggered</span>
                      <span class="text-[11px] text-slate-300 font-mono">{{alert.triggeredAt}}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-slate-500 text-[10px] uppercase font-black tracking-widest">Topology Node</span>
                      <span class="text-[11px] text-sky-400 font-black uppercase border-b border-sky-500/30">{{alert.service}}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex flex-col gap-2 opacity-0 group-hover:opacity-100 translate-x-4 group-hover:translate-x-0 transition-all duration-300">
                <button class="py-2.5 px-6 rounded-xl bg-white/5 hover:bg-white/10 text-xs font-black text-white transition-all border border-white/5 backdrop-blur-md">
                  Acknowledge
                </button>
                <button class="py-2.5 px-6 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-xs font-black text-rose-400 transition-all border border-rose-500/20 backdrop-blur-md">
                  Escalate
                </button>
              </div>
            </div>
          </div>

          <div *ngIf="alertsService.activeAlertCount() === 0" class="glass-panel p-20 text-center border-dashed border-white/10 bg-transparent">
            <div class="text-6xl mb-6 animate-bounce">🛡️</div>
            <h3 class="text-2xl font-black text-white mb-2 tracking-tight">Perimeter Secure</h3>
            <p class="text-slate-500 text-sm max-w-xs mx-auto">No active threats or anomalies detected in the current observability window.</p>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class AlertsComponent implements OnInit {
  protected readonly alertsService = inject(AlertsService);

  ngOnInit(): void {
    this.refresh();
  }

  refresh(): void {
    this.alertsService.refreshActiveAlerts();
  }

  getSeverityBorder(severity: string) {
    severity = (severity || '').toUpperCase();
    if (severity === 'CRITICAL') return 'border-l-rose-600';
    if (severity === 'HIGH') return 'border-l-rose-500';
    if (severity === 'WARNING') return 'border-l-amber-500';
    return 'border-l-sky-500';
  }

  getSeverityBadge(severity: string) {
    severity = (severity || '').toUpperCase();
    if (severity === 'CRITICAL') return 'bg-rose-500/10 text-rose-500 border-rose-500/30';
    if (severity === 'HIGH') return 'bg-rose-400/10 text-rose-400 border-rose-400/30';
    if (severity === 'WARNING') return 'bg-amber-400/10 text-amber-500 border-amber-500/30';
    return 'bg-sky-400/10 text-sky-400 border-sky-400/30';
  }

  getSeverityGradient(severity: string) {
    severity = (severity || '').toUpperCase();
    if (severity === 'CRITICAL') return 'from-rose-500/5 to-transparent';
    if (severity === 'HIGH') return 'from-rose-400/5 to-transparent';
    if (severity === 'WARNING') return 'from-amber-400/5 to-transparent';
    return 'from-sky-400/5 to-transparent';
  }
}
