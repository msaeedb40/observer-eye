import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-alert-badge',
    standalone: true,
    imports: [CommonModule],
    template: `
    <span class="alert-badge" [class]="'severity-' + severity">
      <span class="pulse" *ngIf="pulse"></span>
      {{ count }}
    </span>
  `,
    styles: [`
    .alert-badge {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 24px;
      height: 24px;
      padding: 0 8px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
    }
    
    .severity-info { background: rgba(59,130,246,0.2); color: #3b82f6; }
    .severity-warning { background: rgba(245,158,11,0.2); color: #f59e0b; }
    .severity-error { background: rgba(239,68,68,0.2); color: #ef4444; }
    .severity-critical { background: #ef4444; color: white; }
    
    .pulse {
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: inherit;
      background: inherit;
      animation: pulse 2s infinite;
      opacity: 0.5;
    }
    
    @keyframes pulse {
      0% { transform: scale(1); opacity: 0.5; }
      50% { transform: scale(1.3); opacity: 0; }
      100% { transform: scale(1); opacity: 0; }
    }
  `]
})
export class AlertBadgeComponent {
    @Input() count = 0;
    @Input() severity: 'info' | 'warning' | 'error' | 'critical' = 'info';
    @Input() pulse = false;
}
