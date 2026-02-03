import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-traffic',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-end">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Traffic Explorer</h1>
          <p class="text-slate-400">L7 Analysis, endpoint throughput, and regional payload distribution</p>
        </div>
        <div class="glass-panel px-4 py-2 flex items-center gap-2">
           <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
           <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Live Flow</span>
        </div>
      </header>

      <div class="dashboard-grid mb-8">
        <div class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Requests Per Second</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold text-sky-400">142.8</div>
            <div class="text-[10px] font-bold text-slate-500 uppercase">req/s</div>
          </div>
          <div class="mt-4 w-full h-8 opacity-30">
             <app-chart [chartType]="'line'" [chartData]="sparklineData" [height]="'32px'"></app-chart>
          </div>
        </div>
        <div class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Avg Payload Size</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold text-indigo-400">42.5</div>
             <div class="text-[10px] font-bold text-slate-500 uppercase">KB</div>
          </div>
          <div class="mt-4 w-full h-8 opacity-30">
             <app-chart [chartType]="'line'" [chartData]="sparklineData" [height]="'32px'"></app-chart>
          </div>
        </div>
        <div class="glass-panel p-6 card-hover-effect border-l-4 border-l-rose-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Error Rate (5xx)</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold text-rose-500">0.12</div>
            <div class="text-[10px] font-bold text-slate-500 uppercase">%</div>
          </div>
          <p class="mt-4 text-[10px] text-rose-400 font-bold uppercase tracking-widest flex items-center gap-1">
             <span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></span>
             Awaiting Review
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div class="lg:col-span-2 glass-panel p-6">
          <h3 class="font-bold mb-6 flex items-center gap-2">
             <span class="w-2 h-2 rounded-full bg-sky-400"></span>
             L7 Protocol Distribution (Ops/sec)
          </h3>
          <div class="h-[300px]">
            <app-chart [chartType]="'bar'" [chartData]="protocolData"></app-chart>
          </div>
        </div>
        <div class="glass-panel p-6">
           <h3 class="font-bold mb-6 flex items-center gap-2">
             <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
             Geographic Traffic
          </h3>
          <div class="space-y-4">
            <div *ngFor="let region of regions" class="space-y-2">
              <div class="flex justify-between text-xs">
                <span class="text-slate-400 font-bold uppercase">{{region.name}}</span>
                <span class="text-white font-mono">{{region.traffic}}%</span>
              </div>
              <div class="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-indigo-500" [style.width.%]="region.traffic"></div>
              </div>
            </div>
          </div>
          <div class="mt-8 pt-8 border-t border-white/5">
             <div class="flex items-center gap-4 p-4 rounded-xl bg-indigo-500/5 border border-indigo-500/10">
                <div class="text-2xl">🌍</div>
                <div>
                   <p class="text-xs font-bold text-white">Dominant Region</p>
                   <p class="text-[10px] text-slate-500 uppercase">US-EAST-1 (Northern Virginia)</p>
                </div>
             </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="glass-panel p-6">
          <h3 class="text-lg font-bold text-white mb-6">Top Resource Endpoints</h3>
          <div class="space-y-6">
            <div *ngFor="let ep of topEndpoints" class="space-y-2">
              <div class="flex justify-between items-center text-xs">
                <code class="text-sky-400 bg-slate-900 border border-white/5 px-2 py-0.5 rounded">{{ep.path}}</code>
                <span class="font-bold text-slate-300">{{ep.calls}} ops</span>
              </div>
              <div class="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-sky-500 to-indigo-500" [style.width.%]="ep.width"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="glass-panel p-6">
          <h3 class="text-lg font-bold text-white mb-6">Active Traffic Bottlenecks</h3>
          <div class="space-y-4">
            <div *ngFor="let b of bottlenecks" class="p-4 rounded-xl bg-slate-900/50 border border-white/5 flex gap-4 card-hover-effect">
              <div class="mt-1 w-2 h-2 rounded-full shrink-0" 
                   [ngClass]="b.impact === 'High' ? 'bg-rose-500' : 'bg-amber-500'"></div>
              <div>
                <h4 class="font-bold text-slate-200 text-sm mb-1">{{b.endpoint}}</h4>
                <p class="text-xs text-slate-500 leading-relaxed">{{b.cause}}</p>
                <div class="mt-2 text-[10px] font-bold uppercase tracking-widest" 
                     [ngClass]="b.impact === 'High' ? 'text-rose-400' : 'text-amber-400'">
                  {{b.impact}} Impact
                </div>
              </div>
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
  topEndpoints = [
    { path: '/api/v1/telemetry', calls: '150k', width: 95 },
    { path: '/api/v1/auth/login', calls: '45k', width: 40 },
    { path: '/api/v1/analytics', calls: '12k', width: 15 }
  ];

  bottlenecks = [
    { endpoint: '/api/v1/reports/export', cause: 'PDF generation CPU bound during heavy serialization', impact: 'High' },
    { endpoint: '/api/v1/users/search', cause: 'Missing index on email field in production schema', impact: 'Medium' }
  ];

  regions = [
    { name: 'N. Virginia (us-east-1)', traffic: 45 },
    { name: 'Frankfurt (eu-central-1)', traffic: 28 },
    { name: 'Tokyo (ap-northeast-1)', traffic: 15 },
    { name: 'Ireland (eu-west-1)', traffic: 12 },
  ];

  protocolData: ChartConfiguration['data'] = {
    datasets: [
      { data: [850, 720, 910, 680, 740, 800], label: 'HTTPS (REST)', backgroundColor: '#38bdf8' },
      { data: [120, 140, 110, 130, 150, 120], label: 'gRPC', backgroundColor: '#818cf8' },
      { data: [45, 52, 48, 61, 55, 67], label: 'WebSocket', backgroundColor: '#f472b6' }
    ],
    labels: ['10:00', '10:10', '10:20', '10:30', '10:40', '10:50']
  };

  sparklineData: ChartConfiguration['data'] = {
    datasets: [{
      data: [42, 45, 43, 48, 47, 45, 46],
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
