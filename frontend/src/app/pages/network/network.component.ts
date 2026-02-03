import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-network',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Network Observer</h1>
        <p class="text-slate-400">Real-time traffic analysis and connection mapping</p>
      </header>

      <div class="dashboard-grid mb-8">
        <div class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Ingress Traffic</h3>
          <div class="text-3xl font-bold text-sky-400">1.2 GB/s</div>
          <div class="mt-2 h-1 w-full bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-sky-400" style="width: 65%"></div>
          </div>
        </div>
        <div class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Egress Traffic</h3>
          <div class="text-3xl font-bold text-indigo-400">850 MB/s</div>
          <div class="mt-2 h-1 w-full bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-indigo-400" style="width: 45%"></div>
          </div>
        </div>
        <div class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Active Connections</h3>
          <div class="text-3xl font-bold text-purple-400">24.5k</div>
          <div class="text-xs text-emerald-400 mt-2 font-bold">Stable connectivity</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-panel p-6">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span> Bandwidth Performance
          </h3>
          <div class="h-64 bg-slate-900/50 rounded-xl border border-slate-800 flex items-center justify-center">
            <app-chart [chartType]="'line'"></app-chart>
          </div>
        </div>
        <div class="glass-panel p-6">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-purple-400"></span> Connection Distribution
          </h3>
          <div class="h-64 bg-slate-900/50 rounded-xl border border-slate-800 flex items-center justify-center">
            <app-chart [chartType]="'bar'"></app-chart>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class NetworkComponent implements OnInit {
  ngOnInit(): void { }
  bandwidthData: ChartConfiguration['data'] = {
    datasets: [
      { data: [65, 59, 80, 81, 56, 55, 40], label: 'Inbound', borderColor: '#4e73df', tension: 0.4 },
      { data: [28, 48, 40, 19, 86, 27, 90], label: 'Outbound', borderColor: '#1cc88a', tension: 0.4 }
    ],
    labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30']
  };

  connectionData: ChartConfiguration['data'] = {
    datasets: [
      { data: [450, 520, 480, 610], label: 'Established', backgroundColor: '#4e73df' },
      { data: [120, 150, 110, 180], label: 'TIME_WAIT', backgroundColor: '#f6c23e' }
    ],
    labels: ['node-01', 'node-02', 'db-cluster', 'proxy-01']
  };
}
