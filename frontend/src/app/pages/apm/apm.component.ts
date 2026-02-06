import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-apm',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-center">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Application Performance</h1>
          <p class="text-slate-400">Transaction latency, throughput, and distributed performance signals</p>
        </div>
        <div class="flex gap-4">
          <div class="glass-panel px-4 py-2 text-center">
            <p class="text-[10px] font-bold text-slate-500 uppercase">Services</p>
            <p class="text-xl font-black text-white">24</p>
          </div>
          <div class="glass-panel px-4 py-2 text-center">
            <p class="text-[10px] font-bold text-slate-500 uppercase">Endpoints</p>
            <p class="text-xl font-black text-white">156</p>
          </div>
        </div>
      </header>

      <div class="dashboard-grid mb-8">
        <div *ngFor="let stat of apmStats" class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">{{stat.label}}</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold" [ngClass]="stat.color">{{stat.value}}</div>
            <div class="text-[10px] uppercase font-bold text-slate-500">{{stat.unit}}</div>
          </div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold" [ngClass]="stat.trend === 'up' ? 'text-emerald-400' : 'text-rose-400'">
              {{stat.trend === 'up' ? '↑' : '↓'}} {{stat.trendValue}}%
            </span>
            <div class="w-16 h-4 opacity-30">
               <app-chart [chartType]="'line'" [chartData]="sparklineData" [height]="'20px'"></app-chart>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div class="lg:col-span-2 glass-panel p-6">
          <div class="flex justify-between items-center mb-6">
            <h3 class="font-bold flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-sky-400"></span>
              Global Response Time (P95)
            </h3>
            <div class="text-[10px] font-bold text-slate-500 uppercase">Target: &lt;200ms</div>
          </div>
          <div class="h-[300px]">
            <app-chart [chartType]="'line'" [chartData]="latencyHistoryData"></app-chart>
          </div>
        </div>
        
        <div class="glass-panel p-6 flex flex-col">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            Service Health Status
          </h3>
          <div class="flex-1 space-y-4">
            <div *ngFor="let s of services" class="p-3 rounded-xl bg-white/[0.02] border border-white/5 hover:border-white/10 transition-all group">
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-bold text-white">{{s.name}}</span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded-full" 
                      [ngClass]="s.status === 'Healthy' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'">
                  {{s.status}}
                </span>
              </div>
              <div class="flex items-center gap-2">
                <div class="flex-1 h-1 bg-slate-800 rounded-full overflow-hidden">
                  <div class="h-full bg-sky-400 group-hover:bg-vibrant transition-colors" [style.width.%]="s.score"></div>
                </div>
                <span class="text-[10px] font-mono text-slate-500">{{s.score}}%</span>
              </div>
            </div>
          </div>
          <button class="mt-6 w-full py-2 rounded-lg bg-white/[0.05] border border-white/10 text-[10px] font-bold text-slate-400 hover:bg-white/10 transition-all uppercase tracking-widest">
            View All Services
          </button>
        </div>
      </div>

      <div class="glass-panel overflow-hidden">
        <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
          <h3 class="font-bold">Distributed Transactions</h3>
          <div class="flex gap-2">
             <button class="px-3 py-1 text-[10px] font-bold rounded-lg border border-white/10 bg-white/5 text-white">Slowest</button>
             <button class="px-3 py-1 text-[10px] font-bold rounded-lg hover:bg-white/5 text-slate-500 transition-all">Highest Impact</button>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="text-slate-500 bg-white/[0.01] uppercase font-bold border-b border-white/5">
                <th class="px-6 py-4">Endpoint</th>
                <th class="px-6 py-4">Service</th>
                <th class="px-6 py-4">Throughput</th>
                <th class="px-6 py-4">Latency (P99)</th>
                <th class="px-6 py-4">Error Rate</th>
                <th class="px-6 py-4">Trend</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5 text-slate-300">
              <tr *ngFor="let tx of slowTransactions" class="hover:bg-white/[0.02] transition-colors group">
                <td class="px-6 py-4">
                  <div class="flex flex-col">
                    <span class="font-bold text-white">{{tx.method}} {{tx.endpoint}}</span>
                    <span class="text-[10px] text-slate-500">{{tx.id}}</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span class="px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">{{tx.service}}</span>
                </td>
                <td class="px-6 py-4 font-mono">{{tx.tput}} req/m</td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-2">
                    <span class="font-bold" [ngClass]="tx.latency > 500 ? 'text-rose-400' : 'text-sky-400'">{{tx.latency}}ms</span>
                    <div class="w-12 h-1 bg-slate-800 rounded-full overflow-hidden">
                      <div class="h-full bg-rose-500" [style.width.%]="tx.latency / 10"></div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span class="font-mono" [ngClass]="tx.errors > 1 ? 'text-rose-400' : 'text-emerald-400'">{{tx.errors}}%</span>
                </td>
                <td class="px-6 py-4">
                   <div class="w-16 h-6">
                      <app-chart [chartType]="'line'" [chartData]="sparklineData" [height]="'24px'"></app-chart>
                   </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class ApmComponent implements OnInit {
  apmStats = [
    { label: 'Avg Latency', value: '124', unit: 'ms', color: 'text-sky-400', trend: 'down', trendValue: 12 },
    { label: 'Throughput', value: '1.2k', unit: 'req/s', color: 'text-white', trend: 'up', trendValue: 5 },
    { label: 'Error Rate', value: '0.04', unit: '%', color: 'text-emerald-400', trend: 'down', trendValue: 2 },
    { label: 'Apdex Score', value: '0.96', unit: 'index', color: 'text-amber-400', trend: 'up', trendValue: 1 }
  ];

  services = [
    { name: 'payment-srv', status: 'Healthy', score: 98 },
    { name: 'auth-srv', status: 'Healthy', score: 99 },
    { name: 'catalog-srv', status: 'Degraded', score: 76 },
    { name: 'ai-recommend', status: 'Healthy', score: 92 },
  ];

  slowTransactions = [
    { id: 'tx-8812', method: 'POST', endpoint: '/api/v1/checkout', service: 'payment-srv', latency: 850, tput: 420, errors: 0.1 },
    { id: 'tx-2291', method: 'GET', endpoint: '/api/v1/inventory', service: 'catalog-srv', latency: 420, tput: 1200, errors: 4.2 },
    { id: 'tx-4401', method: 'POST', endpoint: '/api/v1/auth', service: 'auth-srv', latency: 310, tput: 2800, errors: 0.05 },
    { id: 'tx-5512', method: 'GET', endpoint: '/api/v1/recommend', service: 'ai-srv', latency: 1200, tput: 150, errors: 1.2 }
  ];

  latencyHistoryData: ChartConfiguration['data'] = {
    datasets: [{
      data: [142, 138, 145, 128, 132, 124, 130, 122, 128, 124, 120, 124],
      label: 'P95 Latency (ms)',
      borderColor: '#38bdf8',
      backgroundColor: 'rgba(56, 189, 248, 0.05)',
      fill: true,
      tension: 0.4,
      pointRadius: 0
    }],
    labels: ['12:00', '12:05', '12:10', '12:15', '12:20', '12:25', '12:30', '12:35', '12:40', '12:45', '12:50', '12:55']
  };

  sparklineData: ChartConfiguration['data'] = {
    datasets: [{
      data: [10, 15, 12, 18, 14, 20, 16],
      borderColor: '#38bdf8',
      borderWidth: 2,
      pointRadius: 0,
      tension: 0.4,
      fill: false
    }],
    labels: ['', '', '', '', '', '', '']
  };

  ngOnInit(): void { }
}
