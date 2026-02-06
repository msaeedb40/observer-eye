import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { PerformanceService } from '../../services/performance.service';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-identity',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 p-8 glass-panel border-l-4 border-l-indigo-500 relative overflow-hidden">
        <div class="relative z-10">
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Identity Monitoring</h1>
          <p class="text-slate-400">Authentication telemetry and session lifecycle tracking</p>
        </div>
        <div class="absolute top-0 right-0 p-12 opacity-10 transform rotate-12">
            <span class="text-9xl">👤</span>
        </div>
      </header>

      <div class="bento-grid mb-8">
        <!-- Login Time Card - Span 3 -->
        <div class="col-span-3 glass-panel p-6 card-hover-effect">
            <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Avg Login Time</h3>
            <div class="text-3xl font-bold text-white">{{ metrics?.avg_login_duration || 0 }}ms</div>
            <div class="mt-4 flex items-center justify-between">
                <span class="text-[10px] font-bold text-emerald-400">Stable latency</span>
            </div>
        </div>

        <!-- Success Rate Card - Span 3 -->
        <div class="col-span-3 glass-panel p-6 card-hover-effect">
            <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Auth Success Rate</h3>
            <div class="text-3xl font-bold text-emerald-400">{{ (metrics?.auth_success_rate * 100)?.toFixed(1) || 0 }}%</div>
            <div class="mt-4 flex items-center justify-between">
                <span class="text-[10px] font-bold text-slate-500 uppercase">Target: 99.9%</span>
            </div>
        </div>

        <!-- Active Sessions Card - Span 3 -->
        <div class="col-span-3 glass-panel p-6 card-hover-effect">
            <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Active Sessions</h3>
            <div class="text-3xl font-bold text-sky-400">{{ metrics?.active_sessions || 0 }}</div>
            <div class="mt-4 flex items-center justify-between">
                <span class="text-[10px] font-bold text-sky-400">↑ live users</span>
            </div>
        </div>

        <!-- MFA Usage Card - Span 3 -->
        <div class="col-span-3 glass-panel p-6 card-hover-effect">
            <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">MFA Usage</h3>
            <div class="text-3xl font-bold text-indigo-400">{{ metrics?.mfa_usage_percent || 0 }}%</div>
            <div class="mt-4 flex items-center justify-between">
                <span class="text-[10px] font-bold text-indigo-400">Compliance high</span>
            </div>
        </div>

        <!-- Auth Lifecycle Chart - Span 8 -->
        <div class="col-span-8 glass-panel p-6 row-span-2">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            Authentication Lifecycle
          </h3>
          <div class="h-80">
             <app-chart [chartType]="'line'" [chartData]="authLifecycleData"></app-chart>
          </div>
        </div>

        <!-- Risk Distribution Chart - Span 4 -->
        <div class="col-span-4 glass-panel p-6 row-span-2 flex flex-col items-center justify-center">
          <h3 class="font-bold mb-6 self-start flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
            Session Risk Distribution
          </h3>
          <div class="h-64 flex items-center justify-center">
             <app-chart [chartType]="'doughnut'" [chartData]="riskScoreData"></app-chart>
          </div>
        </div>

        <!-- Active Sessions List - Span 12 -->
        <div class="col-span-12 glass-panel overflow-hidden border-t-2 border-t-slate-700">
            <div class="p-6 border-b border-white/5 bg-white/[0.02] flex justify-between items-center">
              <h3 class="font-bold text-slate-200">Active Secure Sessions</h3>
              <span class="text-[10px] font-black text-sky-400 bg-sky-500/10 px-2 py-1 rounded border border-sky-500/20">LIVE STREAM</span>
            </div>
            <div class="divide-y divide-white/5 max-h-[400px] overflow-y-auto">
              <div *ngFor="let s of sessionsData?.sessions" class="flex items-center justify-between p-6 hover:bg-white/[0.02] transition-all group">
                <div class="flex items-center gap-5">
                  <div class="relative">
                    <div class="w-12 h-12 rounded-full bg-sky-500/5 border border-white/10 flex items-center justify-center text-sky-400 font-black text-lg">
                      {{ s.user.charAt(0).toUpperCase() }}
                    </div>
                    <div class="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-emerald-500 border-2 border-[#020617]"></div>
                  </div>
                  <div>
                    <div class="font-bold text-slate-200 text-base leading-tight">{{ s.user }}</div>
                    <div class="text-xs font-mono text-slate-500 mt-1 flex items-center gap-2">
                       {{ s.ip }} <span class="text-[8px]">•</span> Status: {{ s.status }}
                    </div>
                  </div>
                </div>
                <div class="text-right flex items-center gap-8">
                  <div class="hidden md:block">
                     <p class="text-[10px] font-bold text-slate-500 uppercase mb-0.5">Duration</p>
                     <p class="text-xs text-slate-300 font-mono">{{ s.duration }}</p>
                  </div>
                  <button class="w-8 h-8 rounded-lg hover:bg-white/5 flex items-center justify-center text-slate-500 hover:text-rose-400 transition-all">✕</button>
                </div>
              </div>
              <div *ngIf="!sessionsData?.sessions?.length" class="p-12 text-center text-slate-600 italic">
                  No active sessions found
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
export class IdentityComponent implements OnInit {
  metrics: any = null;
  sessionsData: any = null;

  authLifecycleData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [120, 145, 110, 160, 130, 155, 125, 140, 135, 145, 115, 150],
        label: 'Successful Logins',
        borderColor: '#38bdf8',
        backgroundColor: 'rgba(56, 189, 248, 0.1)',
        tension: 0.4,
        pointRadius: 0,
        fill: true
      }
    ],
    labels: ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
  };

  riskScoreData: ChartConfiguration['data'] = {
    datasets: [{
      data: [85, 12, 3],
      backgroundColor: ['#4ade80', '#fbbf24', '#f87171'],
      hoverOffset: 4,
      borderWidth: 0
    }],
    labels: ['Low Risk', 'Medium Risk', 'High Risk']
  };

  constructor(private readonly performanceService: PerformanceService) { }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.performanceService.getIdentityMetrics().subscribe({
      next: (data) => this.metrics = data,
      error: (err) => console.error('Failed to load identity metrics:', err)
    });

    this.performanceService.getIdentitySessions().subscribe({
      next: (data) => this.sessionsData = data,
      error: (err) => console.error('Failed to load identity sessions:', err)
    });
  }
}
