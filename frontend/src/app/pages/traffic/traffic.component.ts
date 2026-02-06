import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { PerformanceService } from '../../services/performance.service';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-traffic',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 p-8 glass-panel border-l-4 border-l-emerald-400 relative overflow-hidden">
        <div class="relative z-10">
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Traffic Observer</h1>
          <p class="text-slate-400">Layer 7 protocol analysis and request orchestration</p>
        </div>
        <div class="absolute top-0 right-0 p-12 opacity-10 transform rotate-12">
            <span class="text-9xl">⇄</span>
        </div>
      </header>

      <div class="bento-grid mb-8">
        <!-- Request Rate Card - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Request Rate</h3>
          <div class="flex items-baseline gap-2">
              <div class="text-3xl font-bold text-white">{{ metrics?.requests_per_second || 0 }}</div>
              <div class="text-sm text-slate-500 font-bold uppercase">RPS</div>
          </div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold text-emerald-400">↑ 12% vs last hr</span>
            <span class="text-[10px] text-slate-500 uppercase">Global Ingress</span>
          </div>
        </div>

        <!-- Payload Card - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Avg Payload Size</h3>
          <div class="text-3xl font-bold text-white">{{ metrics?.avg_response_size_kb || 0 }} KB</div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold text-sky-400">Stable</span>
            <span class="text-[10px] text-slate-500 uppercase">JSON Dominant</span>
          </div>
        </div>

        <!-- Error Rate Card - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Error Rate (5xx)</h3>
          <div class="text-3xl font-bold text-rose-500">{{ (metrics?.http_5xx_rate * 100)?.toFixed(2) || 0 }}%</div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold text-rose-400">Threshold: 0.1%</span>
            <span class="text-[10px] text-slate-500 uppercase">Critical metric</span>
          </div>
        </div>

        <!-- Protocol Analysis Chart - Span 8 -->
        <div class="col-span-8 glass-panel p-6 row-span-2">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            Protocol Distribution Over Time
          </h3>
          <div class="h-80">
            <app-chart [chartType]="'bar'" [chartData]="protocolData"></app-chart>
          </div>
        </div>

        <!-- Bottlenecks List - Span 4 -->
        <div class="col-span-4 glass-panel p-6 row-span-2 overflow-y-auto">
          <h3 class="text-lg font-bold text-white mb-6">Active Bottlenecks</h3>
          <div class="space-y-4">
            <div *ngFor="let b of bottlenecks" class="p-4 rounded-xl bg-slate-900/50 border border-white/5 flex gap-4 card-hover-effect">
              <div class="mt-1 w-2 h-2 rounded-full shrink-0" 
                   [ngClass]="b.impact === 'High' ? 'bg-rose-500' : 'bg-amber-500'"></div>
              <div>
                <h4 class="font-bold text-slate-200 text-sm mb-1 truncate w-40">{{b.endpoint}}</h4>
                <p class="text-[10px] text-slate-500 leading-relaxed mb-2">{{b.cause}}</p>
                <div class="text-[9px] font-bold uppercase tracking-widest" 
                     [ngClass]="b.impact === 'High' ? 'text-rose-400' : 'text-amber-400'">
                  {{b.impact}} Impact
                </div>
              </div>
            </div>
            <div *ngIf="!bottlenecks?.length" class="p-8 text-center text-slate-600 italic text-sm">
                No active bottlenecks detected
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
export class TrafficComponent implements OnInit {
  metrics: any = null;
  analysis: any = null;

  topEndpoints = [
    { path: '/api/v1/telemetry', calls: '150k', width: 95 },
    { path: '/api/v1/auth/login', calls: '45k', width: 40 },
    { path: '/api/v1/analytics', calls: '12k', width: 15 }
  ];

  bottlenecks = [
    { endpoint: '/api/v1/reports/export', cause: 'PDF generation CPU bound during heavy serialization', impact: 'High' },
    { endpoint: '/api/v1/users/search', cause: 'Missing index on email field in production schema', impact: 'Medium' }
  ];

  protocolData: ChartConfiguration['data'] = {
    datasets: [
      { data: [850, 720, 910, 680, 740, 800], label: 'HTTPS (REST)', backgroundColor: '#38bdf8' },
      { data: [120, 140, 110, 130, 150, 120], label: 'gRPC', backgroundColor: '#818cf8' },
      { data: [45, 52, 48, 61, 55, 67], label: 'WebSocket', backgroundColor: '#f472b6' }
    ],
    labels: ['10:00', '10:10', '10:20', '10:30', '10:40', '10:50']
  };

  constructor(private readonly performanceService: PerformanceService) { }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.performanceService.getTrafficMetrics().subscribe({
      next: (data) => this.metrics = data,
      error: (err) => console.error('Failed to load traffic metrics:', err)
    });

    this.performanceService.getTrafficAnalysis().subscribe({
      next: (data) => {
        this.analysis = data;
        if (data?.bottlenecks) {
          this.bottlenecks = data.bottlenecks;
        }
      },
      error: (err) => {
        console.error('Failed to load traffic analysis:', err);
        this.analysis = { bottlenecks: this.bottlenecks };
      }
    });
  }
}
