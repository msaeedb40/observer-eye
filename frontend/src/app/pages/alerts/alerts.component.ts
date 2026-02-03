import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-alerts',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-end">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Alert Center</h1>
          <p class="text-slate-400">Manage incident lifecycle and rule configurations</p>
        </div>
        <div class="flex gap-4">
          <div class="glass-panel px-6 py-2">
            <div class="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1">Active Now</div>
            <div class="text-2xl font-bold text-rose-500">3</div>
          </div>
          <button class="btn-premium px-6 flex items-center gap-2">
            <span>+</span> Create Rule
          </button>
        </div>
      </header>

      <div class="grid grid-cols-1 gap-6">
        <div *ngFor="let alert of activeAlerts" class="glass-panel p-6 border-l-4 card-hover-effect group" 
             [ngClass]="getSeverityBorder(alert.severity)">
          <div class="flex justify-between items-start">
            <div class="flex gap-5">
              <div class="w-14 h-14 rounded-2xl bg-white/5 flex items-center justify-center text-2xl">
                {{alert.icon}}
              </div>
              <div>
                <div class="flex items-center gap-3 mb-1">
                  <h3 class="text-xl font-bold text-white">{{alert.title}}</h3>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase" 
                        [ngClass]="getSeverityBadge(alert.severity)">
                    {{alert.severity}}
                  </span>
                </div>
                <p class="text-slate-400 text-sm max-w-2xl">{{alert.description}}</p>
                <div class="mt-4 flex items-center gap-6">
                  <div class="flex items-center gap-2">
                    <span class="text-slate-600 text-[10px] uppercase font-bold">Triggered</span>
                    <span class="text-xs text-slate-300">{{alert.triggeredAt}}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-slate-600 text-[10px] uppercase font-bold">Service</span>
                    <span class="text-xs text-sky-400 font-mono">{{alert.service}}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <button class="py-2 px-5 rounded-xl bg-white/5 hover:bg-white/10 text-xs font-bold text-white transition-colors border border-white/5">
                Acknowledge
              </button>
              <button class="py-2 px-5 rounded-xl bg-sky-500/10 hover:bg-sky-500/20 text-xs font-bold text-sky-400 transition-colors border border-sky-500/20">
                Silence
              </button>
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
export class AlertsComponent implements OnInit {
  activeAlerts = [
    {
      title: 'High 5xx Error Rate',
      description: 'The payment-service is experiencing a spike in 500 Internal Server Errors (currently 12.4%).',
      severity: 'CRITICAL',
      triggeredAt: '4 mins ago',
      service: 'payment-srv',
      icon: '🔥'
    },
    {
      title: 'Database Latency Spike',
      description: 'P95 latency for db-cluster-main queries exceeded 2.5s threshold for over 5 minutes.',
      severity: 'WARNING',
      triggeredAt: '12 mins ago',
      service: 'postgresql',
      icon: '⏳'
    },
    {
      title: 'Unauthorized Login Burst',
      description: '150+ failed login attempts detected within 60 seconds from suspicious IPs.',
      severity: 'HIGH',
      triggeredAt: '25 mins ago',
      service: 'auth-srv',
      icon: '🛡️'
    }
  ];

  ngOnInit(): void { }

  getSeverityBorder(severity: string) {
    if (severity === 'CRITICAL') return 'border-l-rose-500';
    if (severity === 'HIGH') return 'border-l-rose-400';
    if (severity === 'WARNING') return 'border-l-amber-400';
    return 'border-l-sky-400';
  }

  getSeverityBadge(severity: string) {
    if (severity === 'CRITICAL') return 'bg-rose-500/20 text-rose-500';
    if (severity === 'HIGH') return 'bg-rose-400/20 text-rose-400';
    if (severity === 'WARNING') return 'bg-amber-400/20 text-amber-400';
    return 'bg-sky-400/20 text-sky-400';
  }
}
