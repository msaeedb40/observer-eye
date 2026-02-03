import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-metrics',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Metrics Explorer</h1>
        <p class="text-slate-400">Deep-dive into multi-domain performance metrics</p>
      </header>
      
      <div class="dashboard-grid">
        <div class="glass-panel p-8 card-hover-effect cursor-pointer group" routerLink="/apm">
          <div class="text-3xl mb-4 group-hover:scale-110 transition-transform">🚀</div>
          <h3 class="text-xl font-bold mb-2 text-white">Application Performance</h3>
          <p class="text-slate-400 text-sm leading-relaxed">Request latency, throughput, and error rates for distributed services.</p>
          <div class="mt-4 flex items-center text-sky-400 text-xs font-bold uppercase tracking-widest">
            Explore APM <span class="ml-2 group-hover:translate-x-2 transition-transform">→</span>
          </div>
        </div>

        <div class="glass-panel p-8 card-hover-effect cursor-pointer group" routerLink="/metrics/system">
          <div class="text-3xl mb-4 group-hover:scale-110 transition-transform">🖥️</div>
          <h3 class="text-xl font-bold mb-2 text-white">System Resources</h3>
          <p class="text-slate-400 text-sm leading-relaxed">Host CPU, memory utilization, disk I/O, and process inventory.</p>
          <div class="mt-4 flex items-center text-sky-400 text-xs font-bold uppercase tracking-widest">
            Explore System <span class="ml-2 group-hover:translate-x-2 transition-transform">→</span>
          </div>
        </div>

        <div class="glass-panel p-8 card-hover-effect cursor-pointer group" routerLink="/metrics/network">
          <div class="text-3xl mb-4 group-hover:scale-110 transition-transform">🌐</div>
          <h3 class="text-xl font-bold mb-2 text-white">Network Traffic</h3>
          <p class="text-slate-400 text-sm leading-relaxed">Bandwidth analysis, connection mapping, and protocol distribution.</p>
          <div class="mt-4 flex items-center text-sky-400 text-xs font-bold uppercase tracking-widest">
            Explore Network <span class="ml-2 group-hover:translate-x-2 transition-transform">→</span>
          </div>
        </div>

        <div class="glass-panel p-8 card-hover-effect cursor-pointer group" routerLink="/metrics/security">
          <div class="text-3xl mb-4 group-hover:scale-110 transition-transform">🛡️</div>
          <h3 class="text-xl font-bold mb-2 text-white">Security Audits</h3>
          <p class="text-slate-400 text-sm leading-relaxed">Authentication telemetry, threat indicators, and compliance signals.</p>
          <div class="mt-4 flex items-center text-sky-400 text-xs font-bold uppercase tracking-widest">
            Explore Security <span class="ml-2 group-hover:translate-x-2 transition-transform">→</span>
          </div>
        </div>

        <div class="glass-panel p-8 card-hover-effect cursor-pointer group" routerLink="/identity">
          <div class="text-3xl mb-4 group-hover:scale-110 transition-transform">👤</div>
          <h3 class="text-xl font-bold mb-2 text-white">Identity Signals</h3>
          <p class="text-slate-400 text-sm leading-relaxed">User session monitoring and identity provider performance.</p>
          <div class="mt-4 flex items-center text-sky-400 text-xs font-bold uppercase tracking-widest">
            Explore Identity <span class="ml-2 group-hover:translate-x-2 transition-transform">→</span>
          </div>
        </div>

        <div class="glass-panel p-8 card-hover-effect cursor-pointer group" routerLink="/traffic">
          <div class="text-3xl mb-4 group-hover:scale-110 transition-transform">🏎️</div>
          <h3 class="text-xl font-bold mb-2 text-white">Advanced Traffic</h3>
          <p class="text-slate-400 text-sm leading-relaxed">L7 analysis, endpoint bottlenecks, and payload size tracking.</p>
          <div class="mt-4 flex items-center text-sky-400 text-xs font-bold uppercase tracking-widest">
            Explore Traffic <span class="ml-2 group-hover:translate-x-2 transition-transform">→</span>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class MetricsComponent { }
