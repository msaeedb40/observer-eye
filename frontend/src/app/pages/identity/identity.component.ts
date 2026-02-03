import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from '../../components';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-identity',
  standalone: true,
  imports: [CommonModule, ChartComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-end">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Identity Monitoring</h1>
          <p class="text-slate-400">Authentication telemetry and session lifecycle tracking</p>
        </div>
        <div class="flex gap-4">
           <button class="btn-premium py-2 text-xs">Security Audit</button>
        </div>
      </header>

      <div class="dashboard-grid mb-8">
        <div *ngFor="let stat of identityStats" class="glass-panel p-6 card-hover-effect">
          <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">{{stat.label}}</h3>
          <div class="text-3xl font-bold" [ngClass]="stat.color">{{stat.value}}</div>
          <div class="mt-4 flex items-center justify-between">
            <span class="text-[10px] font-bold" [ngClass]="stat.trend.startsWith('↑') ? 'text-emerald-400' : 'text-slate-500'">
              {{stat.trend}}
            </span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div class="lg:col-span-2 glass-panel p-6">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            Authentication Lifecycle (Success vs Failure)
          </h3>
          <div class="h-[300px]">
             <app-chart [chartType]="'line'" [chartData]="authLifecycleData"></app-chart>
          </div>
        </div>
        <div class="glass-panel p-6">
          <h3 class="font-bold mb-6 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
            Session Risk Distribution
          </h3>
          <div class="h-[240px] flex items-center justify-center">
             <app-chart [chartType]="'doughnut'" [chartData]="riskScoreData"></app-chart>
          </div>
          <div class="mt-6 pt-6 border-t border-white/5 space-y-3">
             <div class="flex justify-between items-center text-[10px] font-bold uppercase tracking-widest">
                <span class="text-slate-500">Critical Threats</span>
                <span class="text-rose-400">0 Active</span>
             </div>
             <div class="flex justify-between items-center text-[10px] font-bold uppercase tracking-widest">
                <span class="text-slate-500">MFA Policy bypass</span>
                <span class="text-amber-400">2 flagged</span>
             </div>
          </div>
        </div>
      </div>

      <div class="glass-panel overflow-hidden">
        <div class="p-6 border-b border-white/5 bg-white/[0.02] flex justify-between items-center">
          <h3 class="font-bold">Active Secure Sessions</h3>
          <span class="text-[10px] font-black text-sky-400 bg-sky-500/10 px-2 py-1 rounded border border-sky-500/20">LIVE STREAM</span>
        </div>
        <div class="divide-y divide-white/5">
          <div *ngFor="let s of sessions" class="flex items-center justify-between p-6 hover:bg-white/[0.02] transition-all group">
            <div class="flex items-center gap-5">
              <div class="relative">
                <div class="w-12 h-12 rounded-full bg-sky-500/5 border border-white/10 flex items-center justify-center text-sky-400 font-black text-lg">
                  {{s.user.charAt(0).toUpperCase()}}
                </div>
                <div class="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-emerald-500 border-2 border-[#020617]"></div>
              </div>
              <div>
                <div class="font-bold text-slate-200 text-base leading-tight">{{s.user}} <span class="text-[10px] font-normal text-slate-500 ml-2">({{s.id}})</span></div>
                <div class="text-xs font-mono text-slate-500 mt-1 flex items-center gap-2">
                   {{s.ip}} <span class="text-[8px]">•</span> {{s.os}} <span class="text-[8px]">•</span> {{s.location}}
                </div>
              </div>
            </div>
            <div class="text-right flex items-center gap-8">
              <div class="hidden md:block">
                 <p class="text-[10px] font-bold text-slate-500 uppercase mb-0.5">Session Age</p>
                 <p class="text-xs text-slate-300 font-mono">{{s.duration}}</p>
              </div>
              <div class="w-24 text-center">
                 <p class="text-[10px] font-bold text-slate-500 uppercase mb-0.5">Risk Level</p>
                 <span class="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-[10px] font-black rounded uppercase border border-emerald-500/20">
                    {{s.risk}}
                 </span>
              </div>
              <button class="w-8 h-8 rounded-lg hover:bg-white/5 flex items-center justify-center text-slate-500 hover:text-rose-400 transition-all">✕</button>
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
export class IdentityComponent implements OnInit {
  identityStats = [
    { label: 'Avg Login Time', value: '124ms', color: 'text-white', trend: '↓ 5% latency' },
    { label: 'Auth Success Rate', value: '99.2%', color: 'text-emerald-400', trend: 'Stable' },
    { label: 'Active Sessions', value: '1,458', color: 'text-sky-400', trend: '↑ 12% growth' },
    { label: 'MFA Adoption', value: '68%', color: 'text-indigo-400', trend: '↑ 2% adoption' }
  ];

  sessions = [
    { id: 'sess_4x912', user: 'admin', ip: '10.0.0.1', os: 'macOS 14.2', location: 'San Francisco, US', duration: '2h 15m', risk: 'low' },
    { id: 'sess_1z882', user: 'j-doe', ip: '192.168.1.5', os: 'Linux (Ubuntu)', location: 'London, UK', duration: '45m', risk: 'low' },
    { id: 'sess_9v003', user: 'm-smith', ip: '172.16.0.4', os: 'Windows 11', location: 'Berlin, DE', duration: '12m', risk: 'medium' }
  ];

  authLifecycleData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [120, 145, 110, 160, 130, 155, 125, 140, 135, 145, 115, 150],
        label: 'Successful Logins',
        borderColor: '#38bdf8',
        tension: 0.4,
        pointRadius: 0,
        fill: true,
        backgroundColor: 'rgba(56, 189, 248, 0.05)'
      },
      {
        data: [2, 5, 3, 12, 1, 4, 8, 2, 5, 3, 1, 6],
        label: 'Failed Attempts',
        borderColor: '#fb7185',
        tension: 0.4,
        pointRadius: 2,
        fill: false
      }
    ],
    labels: ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
  };

  riskScoreData: ChartConfiguration['data'] = {
    datasets: [{
      data: [85, 12, 3],
      backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
      hoverOffset: 4,
      borderWidth: 0
    }],
    labels: ['Low Risk', 'Medium Risk', 'High Risk']
  };

  ngOnInit(): void { }
}
