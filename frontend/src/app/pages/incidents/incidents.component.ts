import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ReliabilityMetricsComponent, ReliabilityMetrics } from '../../features/reliability';
import { ReliabilityService } from '../../features/reliability/services/reliability.service';

export interface Incident {
  id: string;
  incidentId: string;
  title: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  status: 'open' | 'investigating' | 'contained' | 'resolved';
  detectedAt: Date;
  assignee: string;
  component: string;
}

@Component({
  selector: 'app-incidents',
  standalone: true,
  imports: [CommonModule, RouterModule, ReliabilityMetricsComponent, DatePipe],
  template: `
    <div class="page-container page-transition">
      <header class="mb-8 flex justify-between items-end">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Incident Management</h1>
          <p class="text-slate-400">Track, investigate, and resolve critical system disruptions</p>
        </div>
        <button class="btn-premium px-8 py-3">Report Incident</button>
      </header>

      <!-- Reliability Metrics (Feature Component) -->
      <app-reliability-metrics [metrics]="reliabilityMetrics"></app-reliability-metrics>

      <div class="filters mb-6 flex justify-between items-center gap-4">
        <div class="relative flex-1 max-w-md">
          <input type="text" placeholder="Search incidents..." class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-300 focus:outline-none focus:border-sky-500/50">
        </div>
        <div class="flex gap-2">
          <button *ngFor="let tab of ['All', 'Open', 'Resolved']" 
                  class="px-4 py-2 rounded-lg text-xs font-bold transition-all"
                  [ngClass]="tab === 'All' ? 'bg-sky-500 text-white' : 'bg-white/5 text-slate-400 hover:text-white'">
            {{tab}}
          </button>
        </div>
      </div>

      <div class="glass-panel overflow-hidden">
        <table class="w-full text-left">
          <thead class="bg-white/[0.01] text-[10px] font-black uppercase tracking-widest text-slate-500">
            <tr>
              <th class="p-4">ID</th>
              <th class="p-4">Incident</th>
              <th class="p-4">Severity</th>
              <th class="p-4">Status</th>
              <th class="p-4">Detected</th>
              <th class="p-4">Assignee</th>
              <th class="p-4"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5">
            <tr *ngFor="let incident of incidents" class="hover:bg-white/[0.02] transition-colors group">
              <td class="p-4 font-mono text-xs text-sky-400 font-bold">{{ incident.incidentId }}</td>
              <td class="p-4">
                <div class="flex flex-column">
                  <div class="font-bold text-slate-200 text-sm">{{ incident.title }}</div>
                  <div class="text-[9px] text-slate-600 mt-0.5">{{ incident.component }}</div>
                </div>
              </td>
              <td class="p-4">
                <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase border"
                      [ngClass]="{
                        'bg-rose-500/10 text-rose-400 border-rose-500/20': incident.severity === 'critical',
                        'bg-orange-500/10 text-orange-400 border-orange-500/20': incident.severity === 'high',
                        'bg-amber-500/10 text-amber-400 border-amber-500/20': incident.severity === 'medium',
                        'bg-sky-500/10 text-sky-400 border-sky-500/20': incident.severity === 'low'
                      }">
                  {{ incident.severity }}
                </span>
              </td>
              <td class="p-4">
                <span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase transition-all"
                      [ngClass]="{
                        'bg-rose-500 text-white': incident.status === 'open',
                        'bg-sky-500 text-white': incident.status === 'investigating',
                        'bg-emerald-500 text-white': incident.status === 'contained',
                        'bg-emerald-900/50 text-emerald-400 border border-emerald-500/30': incident.status === 'resolved'
                      }">
                  {{ incident.status }}
                </span>
              </td>
              <td class="p-4 text-xs text-slate-400">{{ incident.detectedAt | date:'medium' }}</td>
              <td class="p-4 text-xs font-bold text-slate-300">{{ incident.assignee }}</td>
              <td class="p-4 text-right">
                 <button class="text-xs font-bold text-slate-500 hover:text-white transition-all opacity-0 group-hover:opacity-100">VIEW DETAILS →</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class IncidentsComponent implements OnInit {
  reliabilityMetrics: ReliabilityMetrics = { mttd: 0, mttr: 0, mtts: 0, incident_count: 0 };
  incidents: Incident[] = [];

  constructor(private reliabilityService: ReliabilityService) { }

  ngOnInit(): void {
    this.fetchReliability();
    this.fetchIncidents();
  }

  fetchReliability(): void {
    this.reliabilityService.getMetrics().subscribe({
      next: (m) => this.reliabilityMetrics = m,
      error: (e) => console.error('Failed to fetch reliability metrics', e)
    });
  }

  fetchIncidents(): void {
    this.reliabilityService.getIncidents().subscribe({
      next: (data) => this.incidents = data,
      error: (e) => console.error('Failed to fetch incidents', e)
    });
  }
}
