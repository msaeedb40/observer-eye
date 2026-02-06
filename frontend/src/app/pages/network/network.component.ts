import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { PerformanceService } from '../../services/performance.service';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-network',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 p-8 glass-panel border-l-4 border-l-sky-400">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Network Observer</h1>
        <p class="text-slate-400">Real-time traffic analysis and connection mapping</p>
      </header>

      <div class="bento-grid mb-8">
        <!-- Main Stats Summary - Span 12 -->
        <div class="col-span-12 glass-panel p-6 mb-4 flex justify-between items-center bg-gradient-to-r from-sky-500/10 to-transparent">
            <div>
                <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Total Bandwidth Utilization</h3>
                <div class="flex items-baseline gap-4">
                    <span class="text-4xl font-black text-white">{{ formatBytes((summary?.total_sent_bytes || 0) + (summary?.total_received_bytes || 0)) }}</span>
                    <span class="text-xs text-emerald-400 font-bold uppercase tracking-tighter">↑ Active</span>
                </div>
            </div>
            <div class="text-right">
                <span class="text-xs text-slate-500 font-bold uppercase block mb-1">Hosts Monitored</span>
                <span class="text-2xl font-bold text-sky-400">{{ summary?.hosts_monitored || 0 }}</span>
            </div>
        </div>

        <!-- Bandwidth Sent - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Bandwidth Sent</h3>
          <div class="text-3xl font-bold text-sky-400">{{ formatBytes(summary?.total_sent_bytes || 0) }}</div>
          <div class="mt-4 h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-sky-400" [style.width.%]="65"></div>
          </div>
        </div>

        <!-- Bandwidth Received - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Bandwidth Received</h3>
          <div class="text-3xl font-bold text-indigo-400">{{ formatBytes(summary?.total_received_bytes || 0) }}</div>
          <div class="mt-4 h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-indigo-400" [style.width.%]="45"></div>
          </div>
        </div>

        <!-- Avg Latency - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Avg Latency</h3>
          <div class="text-3xl font-bold text-purple-400">{{ summary?.avg_latency_ms?.toFixed(2) || 0 }} ms</div>
          <div class="mt-4 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span class="text-[10px] text-emerald-400 font-bold uppercase">System Stable</span>
          </div>
        </div>

        <!-- Large Bandwidth Chart - Span 8 -->
        <div class="col-span-8 glass-panel p-6 row-span-2">
          <h3 class="font-bold mb-6 flex items-center gap-2 text-slate-200">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span> Bandwidth Performance Trends
          </h3>
          <div class="h-80">
            <app-chart [chartType]="'line'" [chartData]="bandwidthData"></app-chart>
          </div>
        </div>

        <!-- Connection Distribution - Span 4 -->
        <div class="col-span-4 glass-panel p-6 row-span-2">
          <h3 class="font-bold mb-6 flex items-center gap-2 text-slate-200">
            <span class="w-2 h-2 rounded-full bg-purple-400"></span> Load Distribution
          </h3>
          <div class="h-80">
            <app-chart [chartType]="'bar'" [chartData]="connectionData"></app-chart>
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
  summary: any = null;
  connections: any = null;

  bandwidthData: ChartConfiguration['data'] = {
    datasets: [
      { data: [65, 59, 80, 81, 56, 55, 40], label: 'Inbound', borderColor: '#38bdf8', backgroundColor: 'rgba(56, 189, 248, 0.1)', fill: true, tension: 0.4 },
      { data: [28, 48, 40, 19, 86, 27, 90], label: 'Outbound', borderColor: '#818cf8', backgroundColor: 'rgba(129, 140, 248, 0.1)', fill: true, tension: 0.4 }
    ],
    labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30']
  };

  connectionData: ChartConfiguration['data'] = {
    datasets: [
      { data: [450, 520, 480, 610], label: 'Established', backgroundColor: '#38bdf8' },
      { data: [120, 150, 110, 180], label: 'TIME_WAIT', backgroundColor: '#fbbf24' }
    ],
    labels: ['node-01', 'node-02', 'db-cluster', 'proxy-01']
  };

  constructor(private readonly performanceService: PerformanceService) { }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.performanceService.getNetworkSummary().subscribe({
      next: (data) => this.summary = data,
      error: (err) => console.error('Failed to load network summary:', err)
    });

    this.performanceService.getNetworkConnections().subscribe({
      next: (data) => {
        this.connections = data;
      },
      error: (err) => console.error('Failed to load connection metrics:', err)
    });
  }

  formatBytes(bytes: number): string {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}
