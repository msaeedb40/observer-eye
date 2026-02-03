import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-security',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-end">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Security Command Center</h1>
          <p class="text-slate-400">Threat monitoring, surface analysis, and real-time security events</p>
        </div>
        <div class="flex gap-4">
           <button class="px-4 py-2 rounded-lg bg-rose-500/10 text-rose-400 border border-rose-500/20 text-xs font-black uppercase tracking-widest animate-pulse">Emergency Lockdown</button>
        </div>
      </header>

      <div class="dashboard-grid mb-8">
        <div class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Risk Exposure</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold text-amber-400">Low</div>
            <div class="text-[10px] font-bold text-slate-500 uppercase">Score: 24/100</div>
          </div>
          <div class="mt-4 h-2 w-full bg-slate-800 rounded-full overflow-hidden">
             <div class="h-full bg-amber-500" style="width: 24%"></div>
          </div>
        </div>
        <div class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Blocked Threats</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold text-rose-500">142</div>
            <div class="text-[10px] font-bold text-slate-500 uppercase">Last 24h</div>
          </div>
          <p class="mt-4 text-[10px] text-emerald-400 font-bold uppercase tracking-widest">↑ 12% blocked rate</p>
        </div>
        <div class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Identity Security</h3>
          <div class="flex items-baseline gap-2">
            <div class="text-3xl font-bold text-sky-400">99.8%</div>
            <div class="text-[10px] font-bold text-slate-500 uppercase">Auth Score</div>
          </div>
           <p class="mt-4 text-[10px] text-sky-400 font-bold uppercase tracking-widest">3 active MFA bypass attempts</p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div class="lg:col-span-2 glass-panel p-6">
          <div class="flex justify-between items-center mb-6">
            <h3 class="font-bold flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-rose-500"></span>
              Threat Surface Analysis
            </h3>
            <div class="flex gap-2">
               <span class="px-2 py-0.5 rounded text-[10px] bg-slate-900 border border-white/5 text-slate-400 uppercase font-black">Scanning v1.4.2</span>
            </div>
          </div>
          <div class="h-[300px]">
             <app-chart [chartType]="'line'" [chartData]="threatSurfaceData"></app-chart>
          </div>
        </div>
        
        <div class="glass-panel p-6">
           <h3 class="font-bold mb-6 flex items-center gap-2">
             <span class="w-2 h-2 rounded-full bg-amber-400"></span>
             Top Attack Vectors
          </h3>
          <div class="h-[240px] flex items-center justify-center">
             <app-chart [chartType]="'bar'" [chartData]="attackVectorData"></app-chart>
          </div>
          <div class="mt-6 pt-6 border-t border-white/5 space-y-4">
             <div *ngFor="let v of vulnerabilities" class="flex justify-between items-center text-xs">
                 <span class="text-slate-400 font-bold uppercase">{{v.name}}</span>
                 <span class="px-2 py-0.5 rounded font-black text-[10px] uppercase" 
                       [ngClass]="v.severity === 'High' ? 'bg-rose-500/10 text-rose-400' : 'bg-amber-500/10 text-amber-400'">
                   {{v.severity}}
                 </span>
             </div>
          </div>
        </div>
      </div>

      <div class="glass-panel overflow-hidden">
        <div class="p-6 border-b border-white/5 bg-white/[0.02] flex justify-between items-center">
           <h3 class="font-bold">Active Security Event Stream</h3>
           <div class="flex gap-3">
              <button class="text-[10px] font-bold text-slate-500 uppercase hover:text-white transition-colors">Clear Stream</button>
              <button class="text-[10px] font-bold text-sky-400 uppercase hover:text-sky-300 transition-colors">Download Report</button>
           </div>
        </div>
        <div class="divide-y divide-white/5">
           <div *ngFor="let e of events" class="p-6 hover:bg-white/[0.02] transition-all group flex items-start gap-6">
              <div class="w-12 h-12 shrink-0 rounded-2xl flex items-center justify-center border transition-all"
                   [ngClass]="e.type === 'Alert' ? 'bg-rose-500/5 border-rose-500/20 text-rose-500' : 'bg-sky-500/5 border-sky-500/20 text-sky-500'">
                 <span class="text-xl">{{e.type === 'Alert' ? '⚠️' : '🛡️'}}</span>
              </div>
              <div class="flex-1">
                 <div class="flex justify-between mb-1">
                    <h4 class="font-bold text-white text-base">{{e.title}}</h4>
                    <span class="text-xs font-mono text-slate-500">{{e.time}}</span>
                 </div>
                 <p class="text-sm text-slate-400 leading-relaxed mb-3">{{e.description}}</p>
                 <div class="flex items-center gap-4">
                    <div class="flex items-center gap-2">
                       <span class="text-[10px] font-bold text-slate-500 uppercase">Target:</span>
                       <code class="text-[10px] font-mono text-sky-400 bg-slate-900 px-2 py-0.5 rounded border border-white/5">{{e.target}}</code>
                    </div>
                    <div class="flex items-center gap-2">
                       <span class="text-[10px] font-bold text-slate-500 uppercase">Source:</span>
                       <code class="text-[10px] font-mono text-slate-300">{{e.source}}</code>
                    </div>
                 </div>
              </div>
              <div class="text-right flex flex-col items-end gap-3">
                 <span class="px-3 py-1 bg-white/5 border border-white/10 rounded-lg text-[10px] font-black uppercase tracking-widest text-slate-400">
                    {{e.status}}
                 </span>
                 <button class="text-[10px] font-black uppercase tracking-widest text-sky-400 hover:text-vibrant transition-colors">Investigate</button>
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
export class SecurityComponent implements OnInit {
  vulnerabilities = [
    { name: 'CVE-2024-1182 (SSH)', severity: 'High' },
    { name: 'XSS on Checkout Page', severity: 'Medium' },
    { name: 'Insecure S3 Policy', severity: 'Medium' },
    { name: 'JWT Secret weak entropy', severity: 'High' }
  ];

  events = [
    {
      type: 'Alert',
      title: 'Potential SQL Injection Detected',
      time: '14:22:01',
      description: 'Heuristic analysis detected malicious SQL patterns in URL parameters from multiple sources.',
      target: 'api-gateway',
      source: '182.42.11.9, 14.122.91.4',
      status: 'Blocked'
    },
    {
      type: 'Info',
      title: 'WAF Rule Update Successful',
      time: '13:58:12',
      description: 'Distributed security policies updated across all edge bastions to include new zero-day definitions.',
      target: 'Global-WAF',
      source: 'Security-Orchestrator',
      status: 'Active'
    },
    {
      type: 'Alert',
      title: 'MFA Bypass Attempt',
      time: '13:21:44',
      description: 'Multiple authentication attempts detected targeting administrative accounts with bypassed local MFA.',
      target: 'auth-srv-v3',
      source: 'unknown-proxy-de',
      status: 'Mitigated'
    }
  ];

  threatSurfaceData: ChartConfiguration['data'] = {
    datasets: [{
      data: [12, 11, 15, 12, 14, 13, 15, 12, 11, 12, 14, 12],
      label: 'Open Threat Surface',
      borderColor: '#f43f5e',
      backgroundColor: 'rgba(244, 63, 94, 0.05)',
      fill: true,
      tension: 0.4,
      pointRadius: 0
    }],
    labels: ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
  };

  attackVectorData: ChartConfiguration['data'] = {
    datasets: [{
      data: [300, 150, 50, 20],
      backgroundColor: ['#f6c23e', '#e74a3b', '#4e73df', '#1cc88a'],
    }],
    labels: ['SQLi', 'BruteForce', 'DDoS', 'PortScan']
  };

  ngOnInit(): void { }
}
