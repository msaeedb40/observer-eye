import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { PerformanceService } from '../../services/performance.service';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-insights',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 p-8 glass-panel border-l-4 border-l-pink-400 relative overflow-hidden">
        <div class="relative z-10">
          <h1 class="text-4xl font-extrabold gradient-text mb-2">AI Insights & Forecasting</h1>
          <p class="text-slate-400">Predictive analytics and automated root cause analysis engine</p>
        </div>
        <div class="absolute top-0 right-0 p-12 opacity-10 transform rotate-12">
          <span class="text-9xl">🧠</span>
        </div>
        <div class="absolute bottom-4 right-8 z-20">
           <button class="px-4 py-2 bg-pink-500/10 hover:bg-pink-500/20 border border-pink-500/20 rounded-lg text-pink-300 text-xs font-bold uppercase transition-all flex items-center gap-2" (click)="loadData()">
              <span class="animate-spin-slow">↻</span> Recalibrate Models
           </button>
        </div>
      </header>

      <div class="bento-grid mb-8">
        <!-- Anomaly Probability Card - Span 6 -->
        <div class="col-span-6 glass-panel p-8 card-hover-effect overflow-hidden relative">
          <div class="relative z-10">
            <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Anomaly Probability</h3>
            <div class="flex items-end gap-3">
              <div class="text-5xl font-black text-pink-400">{{ (health?.anomaly_probability * 100)?.toFixed(1) || 0 }}%</div>
              <div class="text-sm text-emerald-400 font-bold mb-1 uppercase tracking-tighter">
                  Status: {{ health?.status || 'Active' }}
              </div>
            </div>
            <div class="mt-6 flex gap-2">
                <span *ngFor="let i of [1,2,3,4,5,6,7,8,9,10]" 
                      class="h-1 flex-1 rounded-full"
                      [ngClass]="i <= ((health?.anomaly_probability || 0) * 10) ? 'bg-pink-500' : 'bg-slate-800'"></span>
            </div>
          </div>
          <div class="absolute -right-4 -bottom-4 opacity-5 pointer-events-none">
              <span class="text-8xl">✦</span>
          </div>
        </div>

        <!-- Health Score Card - Span 6 -->
        <div class="col-span-6 glass-panel p-8 card-hover-effect relative overflow-hidden">
          <div class="relative z-10">
            <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Core System Health Score</h3>
            <div class="flex items-baseline gap-4">
                <div class="text-5xl font-black text-sky-400">{{ health?.health_score || 0 }}<span class="text-lg text-slate-600">/100</span></div>
                <div class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[10px] font-black uppercase">Optimized</div>
            </div>
            <p class="mt-4 text-xs text-slate-400 leading-relaxed max-w-xs">
                AI engine reports system stability within normal deviations of training set.
            </p>
          </div>
          <div class="absolute right-8 top-1/2 -translate-y-1/2 w-24 h-24 rounded-full border-8 border-sky-500/10 flex items-center justify-center">
              <div class="w-16 h-16 rounded-full border-4 border-sky-400/20"></div>
          </div>
        </div>

        <!-- Traffic Forecast Chart - Span 8 -->
        <div class="col-span-8 glass-panel p-6 row-span-2">
          <h3 class="font-bold mb-6 flex items-center gap-2 text-slate-200">
            <span class="w-2 h-2 rounded-full bg-pink-400"></span>
            Traffic Forecast vs Actual Utilization
          </h3>
          <div class="h-80">
             <app-chart [chartType]="'line'" [chartData]="forecastData"></app-chart>
          </div>
        </div>

        <!-- Anomaly List - Span 4 -->
        <div class="col-span-4 glass-panel p-6 row-span-2 flex flex-col">
          <h3 class="font-bold mb-6 flex items-center gap-2 text-slate-200">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            Detected Events
          </h3>
          <div class="space-y-4 overflow-y-auto pr-2 flex-1 max-h-[350px]">
            <div *ngFor="let anomaly of anomalies?.results" class="p-4 rounded-xl bg-gradient-to-br from-slate-900/80 to-slate-900/40 border border-slate-800/50 hover:border-pink-500/30 transition-colors cursor-pointer group">
              <div class="flex items-center gap-2 mb-2">
                <span class="text-sky-400 group-hover:scale-110 transition-transform">✦</span>
                <span class="text-sm font-bold text-slate-200 group-hover:text-white transition-colors truncate">{{ anomaly.anomaly_type }}</span>
              </div>
              <p class="text-[10px] text-slate-500 leading-relaxed mb-3 italic">System: {{ anomaly.system_name }}</p>
              <div class="flex justify-between items-center bg-black/20 p-2 rounded-lg">
                 <span class="text-[9px] font-mono text-slate-500">{{ anomaly.timestamp | date:'HH:mm:ss' }}</span>
                 <button class="text-[9px] uppercase font-black tracking-tighter text-pink-400 hover:text-pink-300">Run RCA</button>
              </div>
            </div>
            <div *ngIf="!anomalies?.results?.length" class="p-12 text-center text-slate-600 italic text-sm">
                No anomalies detected
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
    .animate-spin-slow { animation: spin 3s linear infinite; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
  `]
})
export class InsightsComponent implements OnInit {
  health: any = null;
  anomalies: any = null;

  forecastData: ChartConfiguration['data'] = {
    datasets: [
      { data: [300, 320, 310, 350, 340, 380], label: 'Actual', borderColor: '#38bdf8', backgroundColor: 'rgba(56, 189, 248, 0.1)', fill: true, tension: 0.4 },
      { data: [null, null, null, null, null, 380, 410, 430, 420], label: 'Forecast', borderColor: '#f472b6', borderDash: [5, 5], fill: false, tension: 0.4 }
    ],
    labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40']
  };

  constructor(private readonly performanceService: PerformanceService) { }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.performanceService.getHealthScore().subscribe({
      next: (data) => this.health = data,
      error: (err) => console.error('Failed to load health score:', err)
    });

    this.performanceService.getAnomalies('system.health').subscribe({
      next: (data) => this.anomalies = data,
      error: (err) => console.error('Failed to load anomalies:', err)
    });
  }
}
