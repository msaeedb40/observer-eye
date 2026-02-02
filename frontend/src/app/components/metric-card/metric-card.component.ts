import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface MetricData {
    label: string;
    value: number | string;
    unit?: string;
    change?: number;
    changeLabel?: string;
    icon?: string;
    color?: 'default' | 'success' | 'warning' | 'danger' | 'info';
}

@Component({
    selector: 'app-metric-card',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="metric-card" [class]="'color-' + (metric.color || 'default')">
      <div class="metric-header">
        <span class="metric-icon" *ngIf="metric.icon">{{ metric.icon }}</span>
        <span class="metric-label">{{ metric.label }}</span>
      </div>
      
      <div class="metric-value">
        {{ metric.value }}
        <span class="metric-unit" *ngIf="metric.unit">{{ metric.unit }}</span>
      </div>
      
      <div class="metric-change" *ngIf="metric.change !== undefined">
        <span [class]="metric.change >= 0 ? 'positive' : 'negative'">
          {{ metric.change >= 0 ? '↑' : '↓' }} {{ Math.abs(metric.change) }}%
        </span>
        <span class="change-label">{{ metric.changeLabel || 'vs last period' }}</span>
      </div>
    </div>
  `,
    styles: [`
    .metric-card {
      background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
      border-radius: 16px;
      padding: 20px;
      border: 1px solid rgba(255,255,255,0.1);
      transition: all 0.3s;
    }
    
    .metric-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .metric-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
    }
    
    .metric-icon { font-size: 20px; }
    
    .metric-label {
      color: rgba(255,255,255,0.7);
      font-size: 14px;
      font-weight: 500;
    }
    
    .metric-value {
      font-size: 32px;
      font-weight: 700;
      color: white;
      margin-bottom: 8px;
    }
    
    .metric-unit {
      font-size: 16px;
      color: rgba(255,255,255,0.5);
      font-weight: 400;
    }
    
    .metric-change {
      font-size: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .positive { color: #22c55e; }
    .negative { color: #ef4444; }
    
    .change-label { color: rgba(255,255,255,0.5); }
    
    .color-success { border-left: 4px solid #22c55e; }
    .color-warning { border-left: 4px solid #f59e0b; }
    .color-danger { border-left: 4px solid #ef4444; }
    .color-info { border-left: 4px solid #3b82f6; }
  `]
})
export class MetricCardComponent {
    @Input() metric!: MetricData;
    Math = Math;
}
