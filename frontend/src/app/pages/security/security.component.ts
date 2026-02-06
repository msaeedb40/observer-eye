import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { PerformanceService } from '../../services/performance.service';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-security',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 p-8 glass-panel border-l-4 border-l-rose-500 relative overflow-hidden">
        <div class="relative z-10 flex justify-between items-end">
          <div>
            <h1 class="text-4xl font-extrabold gradient-text mb-2">Security Command Center</h1>
            <p class="text-slate-400">Threat monitoring, surface analysis, and real-time security events</p>
          </div>
          <button class="px-4 py-2 rounded-lg bg-rose-500/10 text-rose-400 border border-rose-500/20 text-xs font-black uppercase tracking-widest animate-pulse">Emergency Lockdown</button>
        </div>
        <div class="absolute top-0 right-0 p-12 opacity-10 transform rotate-12">
            <span class="text-9xl">🛡️</span>
        </div>
      </header>

      <div class="bento-grid mb-8">
        <!-- Auth Attempts Summary - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect border-t-2 border-t-sky-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Auth Attempts</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold text-sky-400">{{ stats?.total_auth_attempts || 0 }}</div>
            <div class="text-[10px] font-bold text-slate-500 uppercase">Total Access</div>
          </div>
          <div class="mt-4 h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
             <div class="h-full bg-sky-500" [style.width.%]="75"></div>
          </div>
        </div>

        <!-- Blocked Attacks - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect border-t-2 border-t-rose-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Blocked Attacks</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold text-rose-500">{{ stats?.total_attacks_blocked || 0 }}</div>
            <div class="text-[10px] font-bold text-slate-500 uppercase">Last 24h</div>
          </div>
          <div class="mt-4 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span class="text-[10px] text-emerald-400 font-bold uppercase">Active Mitigation</span>
          </div>
        </div>

        <!-- Auth Failures - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect border-t-2 border-t-amber-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Auth Failures</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold text-amber-500">{{ stats?.total_auth_failures || 0 }}</div>
            <div class="text-[10px] font-bold text-slate-500 uppercase">Critical</div>
          </div>
          <div class="mt-4 flex items-center gap-2 text-amber-400">
              <span class="text-[10px] font-bold uppercase tracking-widest">Monitoring spikes</span>
          </div>
        </div>

        <!-- Threat Surface Chart - Span 8 -->
        <div class="col-span-8 glass-panel p-6 row-span-2">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-rose-500"></span>
            Threat Surface Analysis
          </h3>
          <div class="h-80">
             <app-chart [chartType]="'line'" [chartData]="threatSurfaceData"></app-chart>
          </div>
        </div>
        
        <!-- Attack Vectors - Span 4 -->
        <div class="col-span-4 glass-panel p-6 row-span-2">
           <h3 class="font-bold mb-6 flex items-center gap-2">
             <span class="w-2 h-2 rounded-full bg-amber-400"></span>
             Top Attack Vectors
          </h3>
          <div class="h-80 flex items-center justify-center">
             <app-chart [chartType]="'bar'" [chartData]="attackVectorData"></app-chart>
          </div>
        </div>

        <!-- Event Stream - Span 12 -->
        <div class="col-span-12 glass-panel overflow-hidden border-t-2 border-t-slate-700">
            <div class="p-6 border-b border-white/5 bg-white/[0.02] flex justify-between items-center">
               <h3 class="font-bold">Active Security Event Stream</h3>
               <span class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Real-time enrichment active</span>
            </div>
            <div class="divide-y divide-white/5">
               <div *ngFor="let t of threats?.results" class="p-6 hover:bg-white/[0.02] transition-all group flex items-start gap-6">
                  <div class="w-12 h-12 shrink-0 rounded-2xl flex items-center justify-center border transition-all"
                       [ngClass]="t.severity === 'critical' || t.severity === 'high' ? 'bg-rose-500/5 border-rose-500/20 text-rose-500' : 'bg-sky-500/5 border-sky-500/20 text-sky-500'">
                     <span class="text-xl">{{ t.severity === 'critical' || t.severity === 'high' ? '⚠️' : '🛡️' }}</span>
                  </div>
                  <div class="flex-1">
                     <div class="flex justify-between mb-1">
                        <h4 class="font-bold text-white text-base">{{ t.threat_type }}</h4>
                        <span class="text-xs font-mono text-slate-500">{{ t.timestamp | date:'HH:mm:ss' }}</span>
                     </div>
                     <p class="text-sm text-slate-400 leading-relaxed mb-3">Detected from source {{ t.source_ip }}. Action taken: {{ t.action_taken }}</p>
                     <div class="flex items-center gap-4">
                        <div class="flex items-center gap-2">
                           <span class="text-[10px] font-bold text-slate-500 uppercase">Severity:</span>
                           <span class="px-2 py-0.5 rounded text-[10px] font-black uppercase"
                                 [ngClass]="t.severity === 'critical' ? 'bg-rose-500/20 text-rose-500' : 'bg-amber-500/20 text-amber-500'">
                            {{ t.severity }}
                           </span>
                        </div>
                     </div>
                  </div>
                  <div class="text-right flex flex-col items-end gap-3">
                     <button class="text-[10px] font-black uppercase tracking-widest text-sky-400 hover:text-vibrant transition-colors">Investigate</button>
                  </div>
               </div>
               <div *ngIf="!threats?.results?.length" class="p-12 text-center text-slate-600 italic">
                   No security threats detected in the current window
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
export class SecurityComponent implements OnInit {
  stats: any = null;
  threats: any = null;

  threatSurfaceData: ChartConfiguration['data'] = {
    datasets: [{
      data: [12, 11, 15, 12, 14, 13, 15, 12, 11, 12, 14, 12],
      label: 'Open Threat Surface',
      borderColor: '#f43f5e',
      backgroundColor: 'rgba(244, 63, 94, 0.1)',
      fill: true,
      tension: 0.4,
      pointRadius: 0
    }],
    labels: ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
  };

  attackVectorData: ChartConfiguration['data'] = {
    datasets: [{
      data: [300, 150, 50, 20],
      backgroundColor: ['#fbbf24', '#f87171', '#38bdf8', '#4ade80'],
    }],
    labels: ['SQLi', 'BruteForce', 'DDoS', 'PortScan']
  };

  constructor(private readonly performanceService: PerformanceService) { }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.performanceService.getSecurityStats().subscribe({
      next: (data) => this.stats = data,
      error: (err) => console.error('Failed to load security stats:', err)
    });

    this.performanceService.getSecurityThreats().subscribe({
      next: (data) => this.threats = data,
      error: (err) => console.error('Failed to load security threats:', err)
    });
  }
}
