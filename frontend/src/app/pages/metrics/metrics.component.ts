import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-metrics',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="page-container">
      <header class="page-header">
        <h1>📊 Metrics Explorer</h1>
        <p>Real-time metric visualization and analysis</p>
      </header>
      
      <div class="metrics-grid">
        <div class="metric-panel">
          <h3>Application Metrics</h3>
          <p>Request latency, throughput, error rates</p>
        </div>
        <div class="metric-panel">
          <h3>System Metrics</h3>
          <p>CPU, Memory, Disk, Network</p>
        </div>
        <div class="metric-panel">
          <h3>Network Metrics</h3>
          <p>Bandwidth, latency, packet loss</p>
        </div>
        <div class="metric-panel">
          <h3>Security Metrics</h3>
          <p>Auth attempts, threats, compliance</p>
        </div>
      </div>
    </div>
  `,
    styles: [`
    .page-container { padding: 2rem; max-width: 1400px; margin: 0 auto; }
    .page-header { margin-bottom: 2rem; }
    .page-header h1 { font-size: 2rem; color: #1a1a2e; }
    .page-header p { color: #666; }
    .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
    .metric-panel { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }
    .metric-panel h3 { color: #667eea; margin-bottom: 0.5rem; }
  `]
})
export class MetricsComponent { }
