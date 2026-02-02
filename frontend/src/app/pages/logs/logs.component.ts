import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-logs',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="page-container">
      <header class="page-header">
        <h1>📝 Log Viewer</h1>
        <p>Centralized log aggregation and search</p>
      </header>
      <div class="logs-panel">
        <p>Log entries will be displayed here</p>
      </div>
    </div>
  `,
    styles: [`
    .page-container { padding: 2rem; max-width: 1400px; margin: 0 auto; }
    .page-header { margin-bottom: 2rem; }
    .page-header h1 { font-size: 2rem; color: #1a1a2e; }
    .logs-panel { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); font-family: monospace; }
  `]
})
export class LogsComponent { }
