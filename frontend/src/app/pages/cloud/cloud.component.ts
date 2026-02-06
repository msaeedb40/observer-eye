import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { CloudResourceInventoryComponent } from '../../features/cloud';
import { PerformanceService } from '../../services/performance.service';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-cloud',
  standalone: true,
  imports: [CommonModule, ChartComponent, CloudResourceInventoryComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 p-8 glass-panel border-l-4 border-l-orange-500 relative overflow-hidden">
        <div class="relative z-10">
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Cloud Monitoring</h1>
          <p class="text-slate-400">Multi-cloud resource tracking and performance orchestration</p>
        </div>
        <div class="absolute top-0 right-0 p-12 opacity-10 transform rotate-12">
            <span class="text-9xl">☁️</span>
        </div>
      </header>

      <div class="bento-grid mb-8">
        <!-- AWS Metric Summary - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect border-t-2 border-t-orange-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">AWS Metric (Avg)</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold text-white">{{ (metricsData?.[0]?.value || 0).toFixed(2) }}</div>
            <div class="text-[10px] font-bold text-slate-500 uppercase">{{ metricsData?.[0]?.unit }}</div>
          </div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold text-emerald-400">Real-time telemetry</span>
          </div>
        </div>

        <!-- Total Cost Card - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect border-t-2 border-t-blue-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Total Cloud Cost</h3>
          <div class="text-3xl font-bold text-white">$ {{ costsData?.[0]?.cost || '0.00' }}</div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold text-sky-400">Projected spend</span>
          </div>
        </div>

        <!-- Metric Count Card - Span 4 -->
        <div class="col-span-4 glass-panel p-6 card-hover-effect border-t-2 border-t-red-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Active Cloud Metrics</h3>
          <div class="text-3xl font-bold text-white">{{ metricsData?.length || 0 }}</div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold text-rose-400">Monitoring resources</span>
          </div>
        </div>

        <!-- Performance Trends Chart - Span 8 -->
        <div class="col-span-8 glass-panel p-6 row-span-2">
          <h3 class="font-bold mb-6 flex items-center gap-2 text-slate-200">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            Cloud Performance Trends (Aggregate)
          </h3>
          <div class="h-80">
            <app-chart [chartType]="'line'" [chartData]="cloudUtilizationData"></app-chart>
          </div>
        </div>

        <!-- Cost Distribution Chart - Span 4 -->
        <div class="col-span-4 glass-panel p-6 row-span-2 flex flex-col items-center justify-center">
          <h3 class="font-bold mb-6 self-start flex items-center gap-2 text-slate-200">
            <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
            Provider Cost Ratio
          </h3>
          <div class="h-64 flex items-center justify-center">
            <app-chart [chartType]="'doughnut'" [chartData]="costDistributionData"></app-chart>
          </div>
        </div>

        <!-- Resource Inventory - Span 12 -->
        <div class="col-span-12">
            <app-cloud-resource-inventory [resources]="cloudResources"></app-cloud-resource-inventory>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class CloudComponent implements OnInit {
  metricsData: any[] = [];
  costsData: any[] = [];

  cloudResources = [
    { name: 'prod-api-cluster', provider: 'AWS', region: 'us-east-1', type: 'EKS Cluster', utilization: 65, status: 'Healthy' },
    { name: 'db-primary-replica', provider: 'Azure', region: 'west-europe', type: 'SQL Managed Instance', utilization: 42, status: 'Healthy' },
    { name: 'ml-training-node', provider: 'GCP', region: 'us-central1', type: 'Compute Engine', utilization: 88, status: 'Active' },
    { name: 'static-cdn-assets', provider: 'AWS', region: 'global', type: 'CloudFront', utilization: 12, status: 'Steady' }
  ];

  cloudUtilizationData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [65, 68, 62, 70, 64, 67, 69, 72, 68, 65, 66, 70],
        label: 'Compute Utilization (All Clouds)',
        borderColor: '#38bdf8',
        backgroundColor: 'rgba(56, 189, 248, 0.1)',
        tension: 0.4,
        pointRadius: 0,
        fill: true
      }
    ],
    labels: ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
  };

  costDistributionData: ChartConfiguration['data'] = {
    datasets: [{
      data: [60, 25, 15],
      backgroundColor: ['#f97316', '#3b82f6', '#ef4444'],
      hoverOffset: 4,
      borderWidth: 0
    }],
    labels: ['AWS', 'Azure', 'GCP']
  };

  constructor(private readonly performanceService: PerformanceService) { }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.performanceService.getCloudMetrics().subscribe({
      next: (data) => this.metricsData = data,
      error: (err) => console.error('Failed to load cloud metrics:', err)
    });

    this.performanceService.getCloudCosts().subscribe({
      next: (data) => this.costsData = data,
      error: (err) => console.error('Failed to load cloud costs:', err)
    });
  }
}
