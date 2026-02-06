import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-logs',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-end bg-gradient-to-r from-sky-500/10 to-transparent p-6 rounded-2xl border border-white/5">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Log Explorer</h1>
          <p class="text-slate-400">Centralized log aggregation and semantic search</p>
        </div>
        <div class="flex gap-4 mb-1">
          <div class="glass-panel px-4 py-2 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="text-xs font-bold text-slate-300">Live Stream</span>
          </div>
          <button (click)="loadLogs()" class="btn-premium py-2 px-6 text-sm flex items-center gap-2">
            <span>🔄</span> Refresh
          </button>
        </div>
      </header>

      <div class="glass-panel overflow-hidden border border-white/5 shadow-2xl">
        <div class="bg-slate-900/50 p-4 border-b border-white/5 flex gap-4">
          <input type="text" #searchInput placeholder="Search logs (e.g. service:auth level:error)..." 
                 class="bg-slate-900 border border-white/10 rounded-lg px-4 py-2 text-sm w-full focus:outline-none focus:border-sky-500/50 transition-colors text-white"
                 (keyup.enter)="loadLogs(searchInput.value)">
          <button class="py-2 px-8 rounded-xl bg-sky-500 hover:bg-sky-400 text-sm font-bold text-white transition-all shadow-lg shadow-sky-500/20"
                  (click)="loadLogs(searchInput.value)">
            Search
          </button>
        </div>
        
        <div class="p-0 font-mono text-xs leading-relaxed min-h-[400px] max-h-[600px] overflow-y-auto custom-scrollbar bg-[#020617]/80">
          <div *ngFor="let log of logs" class="group flex border-b border-white/5 hover:bg-white/[0.02] transition-colors">
            <div class="py-2 px-4 border-r border-white/5 text-slate-500 whitespace-nowrap w-48">{{log.timestamp | date:'yyyy-MM-dd HH:mm:ss'}}</div>
            <div class="py-2 px-4 border-r border-white/5 w-24 font-bold uppercase" 
                 [ngClass]="getLevelClass(log.level)">
              {{log.level}}
            </div>
            <div class="py-2 px-4 flex-1 text-slate-300 group-hover:text-white transition-colors">
              <span class="text-sky-400/80 mr-2">[{{log.source || log.logger_name || 'system'}}]</span>
              {{log.message}}
            </div>
          </div>

          <div *ngIf="logs.length === 0" class="p-20 text-center">
            <div class="text-4xl opacity-20 mb-4">📜</div>
            <p class="text-slate-500">No logs matching your criteria were found.</p>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
    .custom-scrollbar::-webkit-scrollbar { width: 6px; }
    .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
  `]
})
export class LogsComponent implements OnInit {
  private apiService = inject(ApiService);
  logs: any[] = [];

  ngOnInit(): void {
    this.loadLogs();
  }

  loadLogs(query?: string): void {
    // For now, we use a simple level filter if query is provided, or just fetch all
    const level = query?.toUpperCase().includes('ERROR') ? 'ERROR' :
      query?.toUpperCase().includes('WARN') ? 'WARNING' : undefined;

    this.apiService.getLogs(level).subscribe({
      next: (data) => {
        this.logs = data;
      },
      error: () => {
        this.logs = [];
      }
    });
  }

  getLevelClass(level: string): string {
    level = level?.toUpperCase();
    if (level === 'ERROR' || level === 'CRITICAL') return 'text-rose-400';
    if (level === 'WARNING' || level === 'WARN') return 'text-amber-400';
    if (level === 'INFO') return 'text-sky-400';
    if (level === 'DEBUG') return 'text-slate-500';
    return 'text-white';
  }
}
