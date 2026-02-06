import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

export interface SLO {
  id: string;
  name: string;
  target: number;
  currentValue: number;
  period: string;
  status: 'met' | 'at_risk' | 'breached';
  errorBudget: number;
  burnRate: number;
}

@Component({
  selector: 'app-slo',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="page-container">
      <div class="header">
        <h1>Service Level Objectives (SLOs)</h1>
        <button class="btn-primary">+ Create SLO</button>
      </div>

      <div class="summary-cards">
        <div class="card">
          <h3>Total SLOs</h3>
          <p class="value">{{ slos.length }}</p>
        </div>
        <div class="card success">
          <h3>Met</h3>
          <p class="value">{{ getCount('met') }}</p>
        </div>
        <div class="card warning">
          <h3>At Risk</h3>
          <p class="value">{{ getCount('at_risk') }}</p>
        </div>
        <div class="card danger">
          <h3>Breached</h3>
          <p class="value">{{ getCount('breached') }}</p>
        </div>
      </div>

      <div class="slo-grid">
        <div class="slo-card" *ngFor="let slo of slos">
          <div class="slo-header">
            <h4>{{ slo.name }}</h4>
            <span class="badge" [class]="slo.status">{{ slo.status | uppercase }}</span>
          </div>
          <div class="slo-content">
            <div class="metric-row">
              <span class="label">Target:</span>
              <span class="value">{{ slo.target }}%</span>
            </div>
            <div class="metric-row">
              <span class="label">Current:</span>
              <span class="value" [class.text-danger]="slo.currentValue < slo.target">{{ slo.currentValue }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress" [style.width.%]="slo.currentValue" [class]="slo.status"></div>
            </div>
            <div class="footer-metrics">
              <div class="m-item">
                <span class="m-label">Error Budget</span>
                <span class="m-value" [class.text-danger]="slo.errorBudget < 0">{{ slo.errorBudget }}%</span>
              </div>
              <div class="m-item">
                <span class="m-label">Burn Rate</span>
                <span class="m-value">{{ slo.burnRate }}x</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .page-container { padding: 24px; color: #f8fafc; }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
    h1 { font-size: 24px; font-weight: 600; margin: 0; }
    .btn-primary { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 500; }
    
    .summary-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 32px; }
    .card { background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }
    .card h3 { font-size: 14px; color: #94a3b8; margin: 0 0 10px 0; }
    .card .value { font-size: 28px; font-weight: 700; margin: 0; }
    .card.success .value { color: #10b981; }
    .card.warning .value { color: #f59e0b; }
    .card.danger .value { color: #ef4444; }
    
    .slo-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 24px; }
    .slo-card { background: #1e293b; border-radius: 12px; border: 1px solid #334155; overflow: hidden; }
    .slo-header { padding: 16px 20px; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
    .slo-header h4 { margin: 0; font-size: 16px; }
    .badge { padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: 600; }
    .badge.met { background: rgba(16, 185, 129, 0.1); color: #10b981; }
    .badge.at_risk { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }
    .badge.breached { background: rgba(239, 68, 68, 0.1); color: #ef4444; }
    
    .slo-content { padding: 20px; }
    .metric-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 14px; }
    .metric-row .label { color: #94a3b8; }
    .metric-row .value { font-weight: 600; }
    
    .progress-bar { height: 8px; background: #0f172a; border-radius: 4px; overflow: hidden; margin-bottom: 20px; }
    .progress { height: 100%; transition: width 0.3s ease; }
    .progress.met { background: #10b981; }
    .progress.at_risk { background: #f59e0b; }
    .progress.breached { background: #ef4444; }
    
    .footer-metrics { display: flex; gap: 24px; padding-top: 16px; border-top: 1px solid #334155; }
    .m-item { display: flex; flex-direction: column; gap: 4px; }
    .m-label { font-size: 11px; color: #94a3b8; }
    .m-value { font-size: 14px; font-weight: 600; }
    .text-danger { color: #ef4444; }
  `]
})
export class SloComponent {
  slos: SLO[] = [
    { id: '1', name: 'API Latency (p95)', target: 99.9, currentValue: 99.95, period: '30d', status: 'met', errorBudget: 0.05, burnRate: 0.8 },
    { id: '2', name: 'Successful Requests', target: 99.99, currentValue: 99.98, period: '30d', status: 'at_risk', errorBudget: -0.01, burnRate: 1.2 },
    { id: '3', name: 'Database Availability', target: 99.9, currentValue: 99.7, period: '30d', status: 'breached', errorBudget: -0.2, burnRate: 2.5 },
    { id: '4', name: 'Web Dashboard Uptime', target: 99.5, currentValue: 99.8, period: '30d', status: 'met', errorBudget: 0.3, burnRate: 0.5 },
  ];

  constructor() { }

  getCount(status: string): number {
    return this.slos.filter(s => s.status === status).length;
  }
}
