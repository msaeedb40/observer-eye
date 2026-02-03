import { Component, OnInit } from '@angular/core';
import { CommonModule, NgClass, NgIf } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ChartComponent } from '../../components';
import { ChartConfiguration, ChartType } from 'chart.js';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, ChartComponent, NgClass, NgIf],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Platform Overview</h1>
        <p class="text-slate-400">Real-time health monitoring across all observability pillars</p>
      </header>

      <div class="dashboard-grid">
        <!-- Health Score Card -->
        <div class="glass-panel p-6 card-hover-effect flex flex-col items-center justify-center">
          <h3 class="text-slate-400 text-sm font-semibold uppercase tracking-wider mb-4">System Health</h3>
          <div class="relative w-32 h-32 flex items-center justify-center">
            <svg class="w-full h-full transform -rotate-90">
              <circle cx="64" cy="64" r="58" stroke="currentColor" stroke-width="8" fill="transparent" class="text-slate-800" />
              <circle cx="64" cy="64" r="58" stroke="currentColor" stroke-width="8" fill="transparent" 
                      [attr.stroke-dasharray]="364" [attr.stroke-dashoffset]="364 * (1 - healthScore / 100)"
                      class="text-sky-400 transition-all duration-1000 ease-out" />
            </svg>
            <span class="absolute text-3xl font-bold">{{ healthScore }}%</span>
          </div>
          <p class="mt-4 text-sm" [ngClass]="healthScore > 90 ? 'text-emerald-400' : 'text-amber-400'">
            {{ healthScore > 90 ? 'Optimal Performance' : 'Attention Required' }}
          </p>
        </div>

        <!-- Metric Summary Cards -->
        <div class="glass-panel p-6 card-hover-effect">
          <div class="flex flex-col h-full justify-between">
            <div class="flex justify-between items-start mb-4">
              <h3 class="text-slate-400 text-xs font-bold uppercase">Active Users</h3>
              <span class="px-2 py-1 rounded-md bg-emerald-500/10 text-emerald-400 text-[10px] font-bold">+12%</span>
            </div>
            <div class="flex items-baseline gap-2">
              <div class="text-3xl font-bold tracking-tight">{{ activeUsers | number }}</div>
              <div class="text-xs text-slate-500 font-medium">vs last hour</div>
            </div>
          </div>
        </div>

        <div class="glass-panel p-6 card-hover-effect">
          <div class="flex flex-col h-full justify-between">
            <div class="flex justify-between items-start mb-4">
              <h3 class="text-slate-400 text-xs font-bold uppercase">Request Rate</h3>
              <span class="px-2 py-1 rounded-md bg-sky-500/10 text-sky-400 text-[10px] font-bold">Stable</span>
            </div>
            <div class="flex items-baseline gap-2">
              <div class="text-3xl font-bold tracking-tight">{{ requestRate | number }} ops/s</div>
              <div class="text-xs text-slate-500 font-medium">across 12 nodes</div>
            </div>
          </div>
        </div>

        <div class="glass-panel p-6 card-hover-effect">
          <div class="flex flex-col h-full justify-between">
            <div class="flex justify-between items-start mb-4">
              <h3 class="text-slate-400 text-xs font-bold uppercase">Error Rate</h3>
              <span class="px-2 py-1 rounded-md bg-rose-500/10 text-rose-400 text-[10px] font-bold">-2% improvement</span>
            </div>
            <div class="flex items-baseline gap-2">
              <div class="text-3xl font-bold tracking-tight">{{ errorRate }}%</div>
              <div class="text-xs text-slate-500 font-medium">99.9% success rate</div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <!-- Live Traffic Chart -->
        <div class="glass-panel p-6">
          <h3 class="font-bold mb-6 flex items-center justify-between">
            <span>Live Traffic Trends</span>
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          </h3>
          <div class="h-64 bg-slate-900/50 rounded-xl border border-slate-800 flex items-center justify-center">
            <app-chart [chartType]="'line'"></app-chart>
          </div>
        </div>

        <!-- System Resource Chart -->
        <div class="glass-panel p-6">
          <h3 class="font-bold mb-6">System Resource Allocation</h3>
          <div class="h-64 bg-slate-900/50 rounded-xl border border-slate-800">
            <app-chart [chartType]="'bar'"></app-chart>
          </div>
        </div>
      </div>

      <!-- Critical Anomalies List -->
      <div class="mt-8 glass-panel p-6">
        <h3 class="font-bold mb-6 text-rose-400">Critical Anomalies</h3>
        <div class="space-y-4">
          <div *ngFor="let anomaly of criticalAnomalies" 
               class="flex items-center justify-between p-4 rounded-xl bg-slate-900/40 border border-slate-800/50 hover:border-rose-500/30 transition-colors">
            <div class="flex items-center gap-4">
              <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse shadow-[0_0_8px_rgba(244,63,94,0.5)]"></span>
              <div>
                <div class="font-bold text-sm">{{ anomaly.title }}</div>
                <div class="text-[10px] text-slate-500">{{ anomaly.timestamp }}</div>
              </div>
            </div>
            <button class="btn-premium py-1 px-4 text-xs font-bold rounded-lg border-white/5 bg-white/5 active:scale-95 group">
              Investigate <span class="group-hover:translate-x-1 transition-transform inline-block">→</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      min-height: 100vh;
      background: radial-gradient(circle at top left, #0f172a 0%, #020617 100%);
    }
  `]
})
export class DashboardComponent implements OnInit {
  healthScore = 94;
  activeUsers = 12450;
  requestRate = 840;
  errorRate = 0.04;

  criticalAnomalies = [
    { title: 'Spike in payment-service error rate (API-v1)', timestamp: '2 mins ago' },
    { title: 'Auth-service latency degraded (Node-04)', timestamp: '7 mins ago' },
    { title: 'Cross-region replication lag exceeded (DB-Main)', timestamp: '15 mins ago' }
  ];

  ngOnInit(): void { }
}
