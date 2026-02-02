import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-alerts',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="page-container">
      <header class="page-header">
        <h1>🔔 Alerts Management</h1>
        <p>Configure and manage alerts</p>
      </header>
      <div class="alerts-panel">
        <p>No active alerts</p>
      </div>
    </div>
  `,
    styles: [`
    .page-container { padding: 2rem; max-width: 1400px; margin: 0 auto; }
    .page-header { margin-bottom: 2rem; }
    .page-header h1 { font-size: 2rem; color: #1a1a2e; }
    .alerts-panel { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }
  `]
})
export class AlertsComponent { }
