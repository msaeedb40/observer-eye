import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-events',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Event Timeline</h1>
        <p class="text-slate-400">Chronological history of system-wide significant occurrences</p>
      </header>

      <div class="relative">
        <!-- Vertical Timeline Line -->
        <div class="absolute left-8 top-0 bottom-0 w-px bg-white/10 hidden md:block"></div>

        <div class="space-y-8">
          <div *ngFor="let event of eventGroups" class="relative">
            <div class="md:sticky md:top-24 md:left-0 mb-4 md:mb-0">
              <span class="bg-slate-900 border border-white/10 rounded-full px-4 py-1 text-[10px] font-bold text-slate-400 uppercase tracking-widest relative z-10 md:-ml-[12px]">
                {{event.date}}
              </span>
            </div>

            <div class="space-y-4 pt-4">
              <div *ngFor="let item of event.items" class="md:ml-16 glass-panel p-5 card-hover-effect relative">
                <!-- Timeline Dot -->
                <div class="absolute -left-[53px] top-6 w-3 h-3 rounded-full border-2 border-slate-900 z-10 hidden md:block"
                     [ngClass]="getDotClass(item.type)"></div>
                
                <div class="flex justify-between items-start">
                  <div class="flex gap-4">
                    <div class="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-xl shrink-0">
                      {{item.icon}}
                    </div>
                    <div>
                      <h4 class="font-bold text-white mb-1">{{item.title}}</h4>
                      <p class="text-sm text-slate-400">{{item.description}}</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <span class="text-xs font-mono text-slate-500">{{item.time}}</span>
                    <div class="mt-2 text-[10px] font-bold px-2 py-0.5 rounded border inline-block uppercase tracking-wider"
                         [ngClass]="getBadgeClass(item.type)">{{item.type}}</div>
                  </div>
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
export class EventsComponent implements OnInit {
  eventGroups = [
    {
      date: 'Today, Feb 03',
      items: [
        { title: 'Deployment Success', description: 'v2.4.1 successful healthy rollout to 12 production nodes.', type: 'DEPLOY', icon: '🚀', time: '06:30 AM' },
        { title: 'High Memory Usage', description: 'worker-node-04 memory exceeded 85% threshold.', type: 'ALERT', icon: '⚠️', time: '05:45 AM' },
        { title: 'New Peer Joined', description: 'Node cluster-east-02 (10.0.4.12) joined the mesh.', type: 'SYSTEM', icon: '🌐', time: '04:12 AM' }
      ]
    },
    {
      date: 'Yesterday, Feb 02',
      items: [
        { title: 'Backup Completed', description: 'Weekly database snapshot stored to S3 (bucket: obs-eye-backup).', type: 'SYSTEM', icon: '💾', time: '11:00 PM' },
        { title: 'Security Threat Blocked', description: 'Multiple failed brute-force attempts from 185.x.x.x.', type: 'SECURITY', icon: '🛡️', time: '08:15 PM' }
      ]
    }
  ];

  ngOnInit(): void { }

  getDotClass(type: string) {
    switch (type) {
      case 'ALERT': return 'bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.5)]';
      case 'DEPLOY': return 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]';
      case 'SECURITY': return 'bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.5)]';
      default: return 'bg-sky-500 shadow-[0_0_8px_rgba(56,189,248,0.5)]';
    }
  }

  getBadgeClass(type: string) {
    switch (type) {
      case 'ALERT': return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
      case 'DEPLOY': return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
      case 'SECURITY': return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
      default: return 'bg-sky-500/10 text-sky-400 border-sky-500/20';
    }
  }
}
