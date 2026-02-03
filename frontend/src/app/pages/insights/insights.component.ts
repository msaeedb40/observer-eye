import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
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
      </header>

      <div class="dashboard-grid mb-8">
        <div class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Anomaly Probability</h3>
          <div class="flex items-end gap-3">
            <div class="text-4xl font-extrabold text-pink-400">12%</div>
            <div class="text-xs text-emerald-400 font-bold mb-1">Low Risk</div>
          </div>
        </div>
        <div class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Predicted Load (1h)</h3>
          <div class="text-3xl font-bold text-sky-400">~450 ops/s</div>
          <div class="text-xs text-slate-400 mt-2">↑ 5% increase expected</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 glass-panel p-6">
          <h3 class="font-bold mb-6">Traffic Forecast vs Actual</h3>
          <div class="h-80 bg-slate-900/50 rounded-xl border border-slate-800 flex items-center justify-center">
             <app-chart [chartType]="'line'"></app-chart>
          </div>
        </div>
        <div class="glass-panel p-6">
          <h3 class="font-bold mb-6">Actionable Insights</h3>
          <div class="space-y-4">
            <div *ngFor="let insight of insights" class="p-4 rounded-xl bg-gradient-to-br from-slate-900/80 to-slate-900/40 border border-slate-800/50">
              <div class="flex items-center gap-2 mb-2">
                <span class="text-sky-400">✦</span>
                <span class="text-sm font-bold">{{insight.title}}</span>
              </div>
              <p class="text-xs text-slate-400 leading-relaxed">{{insight.description}}</p>
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
export class InsightsComponent implements OnInit {
  insights = [
    { title: 'Predictive Scaling', description: 'Anticipated traffic spike in US-East at 09:00 UTC. Recommendation: Pre-provision 3 instances.' },
    { title: 'Pattern Correlation', description: 'Memory leaks in worker-v2 correlate with high-latency traces in processing-queue.' },
    { title: 'Cost Optimization', description: 'Over-provisioned idle resources detected in dev-cluster. Potential savings: $420/month.' }
  ];

  ngOnInit(): void { }
}
