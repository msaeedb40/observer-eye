import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-traces',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Distributed Tracing</h1>
        <p class="text-slate-400">End-to-end request visibility across the service mesh</p>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-4">
          <div *ngFor="let trace of traces" class="glass-panel p-5 card-hover-effect group cursor-pointer border-l-4" 
               [ngClass]="trace.status === 'ERROR' ? 'border-l-rose-500' : 'border-l-sky-500'">
            <div class="flex justify-between items-start mb-4">
              <div>
                <div class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">{{trace.id}}</div>
                <h3 class="text-lg font-bold text-white group-hover:text-sky-400 transition-colors">{{trace.operation}}</h3>
              </div>
              <div class="text-right">
                <div class="text-xl font-bold text-white">{{trace.duration}}ms</div>
                <div class="text-[10px] text-slate-500 font-mono">{{trace.timestamp}}</div>
              </div>
            </div>
            
            <div class="space-y-2">
              <div *ngFor="let span of trace.spans" class="flex items-center gap-3">
                <div class="text-[10px] font-bold text-slate-400 w-24 truncate">{{span.service}}</div>
                <div class="flex-1 h-1.5 bg-white/5 rounded-full overflow-hidden relative">
                  <div class="absolute h-full bg-sky-400/60 rounded-full" 
                       [style.left.%]="span.offset" [style.width.%]="span.width"></div>
                </div>
                <div class="text-[10px] text-slate-500 w-8 text-right">{{span.duration}}ms</div>
              </div>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="glass-panel p-6">
            <h3 class="font-bold mb-4 text-sm uppercase tracking-widest text-slate-400">Trace Stats</h3>
            <div class="space-y-4">
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-slate-500">P99 Latency</span>
                  <span class="text-white font-bold">452ms</span>
                </div>
                <div class="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                  <div class="h-full bg-rose-400" style="width: 75%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-slate-500">Error Rate</span>
                  <span class="text-white font-bold">1.2%</span>
                </div>
                <div class="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                  <div class="h-full bg-emerald-400" style="width: 12%"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="glass-panel p-6">
            <h3 class="font-bold mb-4 text-sm uppercase tracking-widest text-slate-400">Dependency Map</h3>
            <div class="h-40 bg-slate-900/50 rounded-xl border border-white/5 flex items-center justify-center">
              <span class="text-4xl">🔗</span>
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
export class TracesComponent implements OnInit {
  traces = [
    {
      id: 'trace-f842-990a',
      operation: 'POST /api/v1/checkout',
      duration: 852,
      timestamp: '06:45:01',
      status: 'OK',
      spans: [
        { service: 'ingress', duration: 852, offset: 0, width: 100 },
        { service: 'auth-srv', duration: 120, offset: 5, width: 15 },
        { service: 'cart-srv', duration: 250, offset: 25, width: 30 },
        { service: 'payment-srv', duration: 400, offset: 55, width: 40 },
        { service: 'db-main', duration: 80, offset: 80, width: 10 }
      ]
    },
    {
      id: 'trace-c211-45ea',
      operation: 'GET /api/v1/products',
      duration: 125,
      timestamp: '06:45:12',
      status: 'OK',
      spans: [
        { service: 'ingress', duration: 125, offset: 0, width: 100 },
        { service: 'product-srv', duration: 90, offset: 10, width: 70 },
        { service: 'redis-cache', duration: 15, offset: 85, width: 12 }
      ]
    },
    {
      id: 'trace-e552-bf83',
      operation: 'PUT /api/v1/user/profile',
      duration: 1450,
      timestamp: '06:45:25',
      status: 'ERROR',
      spans: [
        { service: 'ingress', duration: 1450, offset: 0, width: 100 },
        { service: 'auth-srv', duration: 1200, offset: 15, width: 80 },
        { service: 'db-user', duration: 50, offset: 95, width: 5 }
      ]
    }
  ];

  ngOnInit(): void { }
}
