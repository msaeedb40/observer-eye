import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-system',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-end">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">System Performance</h1>
          <p class="text-slate-400">Host resource utilization and infrastructure health</p>
        </div>
        <div class="flex gap-3">
          <div class="glass-panel px-4 py-2 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="text-xs font-bold text-slate-300">Agent Connected: node-prod-01</span>
          </div>
        </div>
      </header>

      <div class="dashboard-grid mb-8">
        <div class="glass-panel p-6 card-hover-effect">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xs font-bold text-slate-500 uppercase">CPU Load (Average)</h3>
            <span class="text-sky-400 font-bold">45.2%</span>
          </div>
          <div class="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-sky-400 to-indigo-500" style="width: 45%"></div>
          </div>
          <div class="mt-4 flex justify-between text-[10px] text-slate-500">
            <span>User: 32%</span>
            <span>System: 8%</span>
            <span>I/O Wait: 5.2%</span>
          </div>
        </div>
        <div class="glass-panel p-6 card-hover-effect">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xs font-bold text-slate-500 uppercase">Physical Memory</h3>
            <span class="text-indigo-400 font-bold">72.8%</span>
          </div>
          <div class="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-indigo-400 to-purple-500" style="width: 72%"></div>
          </div>
          <div class="mt-4 flex justify-between text-[10px] text-slate-500">
            <span>Total: 64 GB</span>
            <span>Cached: 12 GB</span>
            <span>Swap: 0%</span>
          </div>
        </div>
        <div class="glass-panel p-6 card-hover-effect">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xs font-bold text-slate-500 uppercase">Storage I/O</h3>
            <span class="text-pink-400 font-bold">12.5 MB/s</span>
          </div>
          <div class="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-pink-400 to-rose-500" style="width: 12%"></div>
          </div>
          <div class="mt-4 flex justify-between text-[10px] text-slate-500">
            <span>Read: 8.2 MB/s</span>
            <span>Write: 4.3 MB/s</span>
            <span>IOPS: 1.2k</span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div class="lg:col-span-2 glass-panel p-6 relative overflow-hidden">
          <div class="absolute top-0 right-0 p-4">
             <div class="flex gap-2">
                <button class="px-3 py-1 text-[10px] font-bold rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">1H</button>
                <button class="px-3 py-1 text-[10px] font-bold rounded hover:bg-white/5 text-slate-400 transition-colors">6H</button>
                <button class="px-3 py-1 text-[10px] font-bold rounded hover:bg-white/5 text-slate-400 transition-colors">24H</button>
             </div>
          </div>
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
            Utilization Trends
          </h3>
          <div class="h-[300px]">
            <app-chart [chartType]="'line'" [chartData]="utilizationTrendData"></app-chart>
          </div>
        </div>
        
        <div class="glass-panel p-6">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
            Load Average
          </h3>
          <div class="flex flex-col justify-center h-[260px] gap-8">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-[10px] font-bold text-slate-500 uppercase mb-1">1 Minute</p>
                <p class="text-3xl font-black text-white">0.85</p>
              </div>
              <div class="w-24 h-12">
                 <app-chart [chartType]="'line'" [chartData]="sparklineData" [height]="'50px'"></app-chart>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-[10px] font-bold text-slate-500 uppercase mb-1">5 Minutes</p>
                <p class="text-3xl font-black text-slate-300">1.12</p>
              </div>
              <div class="w-24 h-12 opacity-50">
                 <app-chart [chartType]="'line'" [chartData]="sparklineData" [height]="'50px'"></app-chart>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-[10px] font-bold text-slate-500 uppercase mb-1">15 Minutes</p>
                <p class="text-3xl font-black text-slate-400">0.98</p>
              </div>
              <div class="w-24 h-12 opacity-30">
                 <app-chart [chartType]="'line'" [chartData]="sparklineData" [height]="'50px'"></app-chart>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="glass-panel overflow-hidden">
        <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
          <h3 class="font-bold">Process Inventory</h3>
          <div class="flex gap-4">
            <input type="text" placeholder="Filter processes..." 
                   class="bg-slate-900/50 border border-white/10 rounded-lg px-3 py-1 text-xs text-white focus:outline-none focus:border-sky-500/50 w-64">
            <button class="text-xs font-bold text-sky-400 hover:text-sky-300 transition-colors uppercase tracking-wider">Kill Process</button>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="text-slate-500 border-b border-white/5 uppercase font-bold bg-white/[0.01]">
                <th class="px-6 py-4">PID</th>
                <th class="px-6 py-4">Process</th>
                <th class="px-6 py-4">User</th>
                <th class="px-6 py-4">CPU %</th>
                <th class="px-6 py-4">Memory %</th>
                <th class="px-6 py-4">Read/Write</th>
                <th class="px-6 py-4">Status</th>
              </tr>
            </thead>
            <tbody class="text-slate-300 divide-y divide-white/5">
              <tr *ngFor="let p of processes" class="hover:bg-white/[0.02] transition-colors group">
                <td class="px-6 py-4 font-mono text-slate-500 group-hover:text-slate-300">{{p.pid}}</td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <span class="w-2 h-2 rounded-full" [ngClass]="p.cpu > 10 ? 'bg-amber-500' : 'bg-sky-500'"></span>
                    <span class="font-bold text-white">{{p.name}}</span>
                  </div>
                </td>
                <td class="px-6 py-4">{{p.user}}</td>
                <td class="px-6 py-4">
                   <div class="flex items-center gap-2">
                     <div class="w-12 h-1 bg-slate-800 rounded-full overflow-hidden">
                        <div class="h-full bg-sky-400" [style.width.%]="p.cpu"></div>
                     </div>
                     <span class="font-mono">{{p.cpu}}%</span>
                   </div>
                </td>
                <td class="px-6 py-4">
                   <div class="flex items-center gap-2">
                     <div class="w-12 h-1 bg-slate-800 rounded-full overflow-hidden">
                        <div class="h-full bg-indigo-400" [style.width.%]="p.mem"></div>
                     </div>
                     <span class="font-mono">{{p.mem}}%</span>
                   </div>
                </td>
                <td class="px-6 py-4 text-slate-500 font-mono">{{p.io}}</td>
                <td class="px-6 py-4">
                  <span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase"
                        [ngClass]="p.status === 'Running' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-slate-500/10 text-slate-400 border border-slate-500/20'">
                    {{p.status}}
                  </span>
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
    .text-vibrant { color: var(--accent-vibrant); }
    th { letter-spacing: 0.05em; }
  `]
})
export class SystemComponent implements OnInit {
  processes = [
    { pid: 1421, name: 'nginx: worker process', user: 'www-data', cpu: 12.4, mem: 4.2, io: '12KB/4KB', status: 'Running' },
    { pid: 3122, name: 'python manage.py runserver', user: 'observer', cpu: 8.1, mem: 15.6, io: '48KB/112KB', status: 'Running' },
    { pid: 981, name: 'postgres: checkpointer', user: 'postgres', cpu: 2.3, mem: 8.7, io: '1MB/2MB', status: 'Running' },
    { pid: 2110, name: 'redis-server *:6379', user: 'redis', cpu: 1.1, mem: 2.4, io: '124KB/56KB', status: 'Running' },
    { pid: 455, name: 'systemd-journald', user: 'root', cpu: 0.8, mem: 1.2, io: '0B/4KB', status: 'Running' },
    { pid: 112, name: 'kworker/u16:1-events', user: 'root', cpu: 0.4, mem: 0.0, io: '0B/0B', status: 'Idle' },
  ];

  utilizationTrendData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [42, 45, 43, 48, 47, 45, 46, 44, 45, 42, 43, 45],
        label: 'CPU Utilization',
        borderColor: '#38bdf8',
        tension: 0.4,
        pointRadius: 0,
        fill: true,
        backgroundColor: 'rgba(56, 189, 248, 0.05)'
      },
      {
        data: [72, 72, 73, 72, 73, 72, 72, 73, 72, 72, 73, 72],
        label: 'Memory Resident',
        borderColor: '#818cf8',
        tension: 0.4,
        pointRadius: 0,
        fill: true,
        backgroundColor: 'rgba(129, 140, 248, 0.05)'
      }
    ],
    labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45', '10:50', '10:55']
  };

  sparklineData: ChartConfiguration['data'] = {
    datasets: [{
      data: [0.8, 0.85, 0.82, 0.88, 0.84, 0.86, 0.85],
      borderColor: '#38bdf8',
      borderWidth: 2,
      tension: 0.4,
      pointRadius: 0,
      fill: false
    }],
    labels: ['', '', '', '', '', '', '']
  };

  ngOnInit(): void { }
}
