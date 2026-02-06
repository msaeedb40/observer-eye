import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-traces',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8 flex justify-between items-end bg-gradient-to-r from-indigo-500/10 to-transparent p-6 rounded-2xl border border-white/5">
        <div>
          <h1 class="text-4xl font-extrabold gradient-text mb-2">Distributed Tracing</h1>
          <p class="text-slate-400">End-to-end request visibility across the service mesh</p>
        </div>
        <button (click)="loadTraces()" class="btn-premium py-2 px-6 text-sm flex items-center gap-2">
          <span>🔄</span> Refresh
        </button>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-4">
          <div *ngFor="let trace of traces" class="glass-panel p-5 card-hover-effect group cursor-pointer border-l-4" 
               [ngClass]="trace.status === 'error' ? 'border-l-rose-500' : 'border-l-sky-500'">
            <div class="flex justify-between items-start mb-4">
              <div>
                <div class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">{{trace.trace_id}}</div>
                <h3 class="text-lg font-bold text-white group-hover:text-sky-400 transition-colors">{{trace.name}}</h3>
              </div>
              <div class="text-right">
                <div class="text-xl font-bold text-white">{{trace.duration_ms | number:'1.0-2'}}ms</div>
                <div class="text-[10px] text-slate-500 font-mono">{{trace.start_time | date:'HH:mm:ss'}}</div>
              </div>
            </div>
            
            <div class="space-y-2">
              <div *ngFor="let span of trace.spans" class="flex items-center gap-3">
                <div class="text-[10px] font-bold text-slate-400 w-24 truncate">{{span.name}}</div>
                <div class="flex-1 h-1.5 bg-white/5 rounded-full overflow-hidden relative">
                  <div class="absolute h-full bg-sky-400/60 rounded-full" 
                       [style.left.%]="getSpanOffset(trace, span)" 
                       [style.width.%]="getSpanWidth(trace, span)"></div>
                </div>
                <div class="text-[10px] text-slate-500 w-12 text-right">{{span.duration_ms | number:'1.0-1'}}ms</div>
              </div>
            </div>
          </div>

          <div *ngIf="traces.length === 0" class="glass-panel p-20 text-center">
            <div class="text-4xl opacity-20 mb-4">🔗</div>
            <p class="text-slate-500">No distributed traces recorded in this window.</p>
          </div>
        </div>

        <div class="space-y-6">
          <div class="glass-panel p-6">
            <h3 class="font-bold mb-4 text-sm uppercase tracking-widest text-slate-400">Trace Stats</h3>
            <div class="space-y-4">
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-slate-500">P99 Latency</span>
                  <span class="text-white font-bold">{{p99Latency}}ms</span>
                </div>
                <div class="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                  <div class="h-full bg-rose-400" [style.width.%]="75"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-slate-500">Error Rate</span>
                  <span class="text-white font-bold">{{errorRate}}%</span>
                </div>
                <div class="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                  <div class="h-full bg-emerald-400" [style.width.%]="errorRate"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="glass-panel p-12 text-center bg-gradient-to-br from-sky-500/5 to-transparent">
             <div class="text-3xl mb-4">🕸️</div>
             <h4 class="text-sm font-bold text-white mb-2">Service Mesh Discoverer</h4>
             <p class="text-[10px] text-slate-500 leading-relaxed">
               Traces are automatically associated with the Grail Discovery Engine for deep causal analysis.
             </p>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class TracesComponent implements OnInit {
  private apiService = inject(ApiService);
  traces: any[] = [];
  p99Latency = 0;
  errorRate = 0;

  ngOnInit(): void {
    this.loadTraces();
  }

  loadTraces(): void {
    this.apiService.getTraces(50).subscribe({
      next: (data) => {
        this.traces = data;
        this.calculateStats();
      },
      error: () => {
        this.traces = [];
      }
    });
  }

  calculateStats(): void {
    if (this.traces.length === 0) return;

    const durations = this.traces.map(t => t.duration_ms).sort((a, b) => a - b);
    this.p99Latency = Math.round(durations[Math.floor(durations.length * 0.99)] || durations[durations.length - 1]);

    const errors = this.traces.filter(t => t.status === 'error').length;
    this.errorRate = parseFloat(((errors / this.traces.length) * 100).toFixed(1));
  }

  getSpanOffset(trace: any, span: any): number {
    if (!trace.duration_ms) return 0;
    const startOffset = new Date(span.start_time).getTime() - new Date(trace.start_time).getTime();
    return (startOffset / trace.duration_ms) * 100;
  }

  getSpanWidth(trace: any, span: any): number {
    if (!trace.duration_ms || !span.duration_ms) return 1;
    return (span.duration_ms / trace.duration_ms) * 100;
  }
}
