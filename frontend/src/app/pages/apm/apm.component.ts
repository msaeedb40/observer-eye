import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-apm',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="page-container">
      <header class="page-header">
        <h1>⚡ Application Performance Monitoring</h1>
        <p>Real-time application performance insights</p>
      </header>
      <div class="apm-grid">
        <div class="apm-panel"><h3>Response Time</h3><p>Avg: 0 ms</p></div>
        <div class="apm-panel"><h3>Throughput</h3><p>0 req/s</p></div>
        <div class="apm-panel"><h3>Error Rate</h3><p>0%</p></div>
        <div class="apm-panel"><h3>Apdex</h3><p>1.00</p></div>
      </div>
    </div>
  `,
    styles: [`
    .page-container { padding: 2rem; max-width: 1400px; margin: 0 auto; }
    .page-header { margin-bottom: 2rem; }
    .page-header h1 { font-size: 2rem; color: #1a1a2e; }
    .apm-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; }
    .apm-panel { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); text-align: center; }
    .apm-panel h3 { color: #667eea; margin-bottom: 0.5rem; }
    .apm-panel p { font-size: 1.5rem; font-weight: bold; color: #1a1a2e; }
  `]
})
export class ApmComponent { }
