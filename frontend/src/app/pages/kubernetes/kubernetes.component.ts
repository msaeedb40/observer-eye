import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { PodInventoryComponent } from '../../features/k8s';
import { ChartConfiguration } from 'chart.js';

interface K8sPod {
  name: string;
  namespace: string;
  status: 'Running' | 'Pending' | 'Failed' | 'Succeeded';
  cpu: string;
  memory: string;
  restarts: number;
  age: string;
}

@Component({
  selector: 'app-kubernetes',
  standalone: true,
  imports: [CommonModule, ChartComponent, PodInventoryComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 p-8 glass-panel border-l-4 border-l-sky-500 relative overflow-hidden">
        <div class="relative z-10 flex justify-between items-end">
          <div>
            <h1 class="text-4xl font-extrabold gradient-text mb-2">Kubernetes Observability</h1>
            <p class="text-slate-400">Cluster health, pod orchestration, and resource lifecycle tracking</p>
          </div>
          <div class="flex gap-4">
            <div class="glass-panel px-4 py-2 flex items-center gap-3">
               <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
               <span class="text-xs font-bold text-slate-300">Cluster: production-main</span>
            </div>
            <div class="glass-panel px-4 py-2 flex items-center gap-3">
               <span class="text-xs font-bold text-slate-300 capitalize">Nodes: 12 Active</span>
            </div>
          </div>
        </div>
        <div class="absolute top-0 right-0 p-12 opacity-10 transform rotate-45">
            <span class="text-9xl">⎈</span>
        </div>
      </header>

      <div class="bento-grid mb-8">
        <!-- Pod Summary - Span 3 -->
        <div class="col-span-3 glass-panel p-6 card-hover-effect border-t-2 border-t-indigo-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Total Pods</h3>
          <div class="text-3xl font-bold text-white">248</div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold text-emerald-400">242 Running</span>
            <span class="text-[10px] text-rose-400">6 Pending</span>
          </div>
        </div>

        <!-- CPU Usage - Span 3 -->
        <div class="col-span-3 glass-panel p-6 card-hover-effect border-t-2 border-t-sky-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">CPU Usage</h3>
          <div class="text-3xl font-bold text-white">68.4%</div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold text-sky-400">84.2 Cores</span>
            <span class="text-[10px] text-slate-500 uppercase">Limit: 120 Cores</span>
          </div>
        </div>

        <!-- Memory Usage - Span 3 -->
        <div class="col-span-3 glass-panel p-6 card-hover-effect border-t-2 border-t-emerald-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Memory Usage</h3>
          <div class="text-3xl font-bold text-white">42.1 GB</div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold text-emerald-400">Stable</span>
            <span class="text-[10px] text-slate-500 uppercase">Limit: 64 GB</span>
          </div>
        </div>

        <!-- Net Throughput - Span 3 -->
        <div class="col-span-3 glass-panel p-6 card-hover-effect border-t-2 border-t-amber-500">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Net Throughput</h3>
          <div class="text-3xl font-bold text-white">1.8 Gbps</div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold text-amber-400">Normal Traffic</span>
            <span class="text-[10px] text-slate-500 uppercase">Across 3 AZs</span>
          </div>
        </div>

        <!-- Resource Requests Chart - Span 6 -->
        <div class="col-span-6 glass-panel p-6 row-span-2">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            Resource Requests vs Limits
          </h3>
          <div class="h-80">
            <app-chart [chartType]="'bar'" [chartData]="resourceData"></app-chart>
          </div>
        </div>

        <!-- Pod Status Line Chart - Span 6 -->
        <div class="col-span-6 glass-panel p-6 row-span-2">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-rose-400"></span>
            Pod Status Trends (24h)
          </h3>
          <div class="h-80">
            <app-chart [chartType]="'line'" [chartData]="podStatusData"></app-chart>
          </div>
        </div>

        <!-- Pod Inventory - Span 12 -->
        <div class="col-span-12">
            <app-pod-inventory [pods]="pods"></app-pod-inventory>
        </div>
      </div>
    </div>
  `,
  styles: [`
    @reference "tailwindcss";
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class KubernetesComponent implements OnInit {
  pods: K8sPod[] = [
    { name: 'api-gateway-748df74-xs9j', namespace: 'production', status: 'Running', cpu: '12.5%', memory: '442MB', restarts: 0, age: '12d' },
    { name: 'auth-service-984bf4-m2kd', namespace: 'production', status: 'Running', cpu: '4.2%', memory: '280MB', restarts: 0, age: '4h' },
    { name: 'telemetry-worker-12948-pl7q', namespace: 'processing', status: 'Running', cpu: '42.1%', memory: '1024MB', restarts: 2, age: '2d' },
    { name: 'db-migration-pod-v12', namespace: 'infra', status: 'Pending', cpu: '0%', memory: '0MB', restarts: 0, age: '5m' },
    { name: 'frontend-app-84724-sh0n', namespace: 'production', status: 'Running', cpu: '2.1%', memory: '154MB', restarts: 1, age: '3d' },
    { name: 'anomaly-detector-94hf8', namespace: 'ml', status: 'Failed', cpu: '0%', memory: '0MB', restarts: 5, age: '1h' },
  ];

  resourceData: ChartConfiguration['data'] = {
    labels: ['Compute', 'Storage', 'Network', 'IOPS'],
    datasets: [
      { data: [65, 59, 80, 81], label: 'Requests', backgroundColor: 'rgba(56, 189, 248, 0.4)' },
      { data: [85, 75, 95, 88], label: 'Limits', backgroundColor: 'rgba(56, 189, 248, 0.1)' }
    ]
  };

  podStatusData: ChartConfiguration['data'] = {
    labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
    datasets: [
      { data: [240, 242, 238, 245, 241, 248], label: 'Running', borderColor: '#10b981', tension: 0.4 },
      { data: [5, 3, 8, 4, 7, 6], label: 'Pending', borderColor: '#f59e0b', tension: 0.4 },
      { data: [2, 1, 4, 3, 2, 5], label: 'Failed', borderColor: '#ef4444', tension: 0.4 }
    ]
  };

  constructor() { }

  ngOnInit(): void {
    console.log('Kubernetes Monitoring Initialized');
  }
}
