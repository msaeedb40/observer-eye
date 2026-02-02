import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
    selector: 'app-dashboard',
    standalone: true,
    imports: [CommonModule, RouterModule],
    template: `
    <div class="dashboard">
      <header class="dashboard-header">
        <h1>Observer-Eye Dashboard</h1>
        <p>4 Pillars of Observability: Metrics | Events | Logs | Traces</p>
      </header>
      
      <nav class="dashboard-nav">
        <a routerLink="/metrics" class="nav-card">
          <div class="icon">📊</div>
          <h3>Metrics</h3>
          <p>Real-time metric visualization</p>
        </a>
        <a routerLink="/events" class="nav-card">
          <div class="icon">📅</div>
          <h3>Events</h3>
          <p>Event timeline analysis</p>
        </a>
        <a routerLink="/logs" class="nav-card">
          <div class="icon">📝</div>
          <h3>Logs</h3>
          <p>Log aggregation & search</p>
        </a>
        <a routerLink="/traces" class="nav-card">
          <div class="icon">🔗</div>
          <h3>Traces</h3>
          <p>Distributed tracing</p>
        </a>
      </nav>
      
      <section class="dashboard-stats">
        <div class="stat-card">
          <h4>System Health</h4>
          <div class="stat-value healthy">100%</div>
        </div>
        <div class="stat-card">
          <h4>Active Alerts</h4>
          <div class="stat-value">0</div>
        </div>
        <div class="stat-card">
          <h4>Requests/min</h4>
          <div class="stat-value">0</div>
        </div>
        <div class="stat-card">
          <h4>Error Rate</h4>
          <div class="stat-value healthy">0%</div>
        </div>
      </section>
    </div>
  `,
    styles: [`
    .dashboard {
      padding: 2rem;
      max-width: 1400px;
      margin: 0 auto;
    }
    .dashboard-header {
      text-align: center;
      margin-bottom: 3rem;
    }
    .dashboard-header h1 {
      font-size: 2.5rem;
      color: #1a1a2e;
      margin-bottom: 0.5rem;
    }
    .dashboard-header p {
      color: #666;
      font-size: 1.1rem;
    }
    .dashboard-nav {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
      margin-bottom: 3rem;
    }
    .nav-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2rem;
      border-radius: 16px;
      color: white;
      text-decoration: none;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .nav-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
    }
    .nav-card .icon {
      font-size: 2.5rem;
      margin-bottom: 1rem;
    }
    .nav-card h3 {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
    }
    .nav-card p {
      opacity: 0.9;
      font-size: 0.95rem;
    }
    .dashboard-stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1.5rem;
    }
    .stat-card {
      background: white;
      padding: 1.5rem;
      border-radius: 12px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
      text-align: center;
    }
    .stat-card h4 {
      color: #666;
      font-size: 0.9rem;
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .stat-value {
      font-size: 2rem;
      font-weight: bold;
      color: #1a1a2e;
    }
    .stat-value.healthy {
      color: #10b981;
    }
  `]
})
export class DashboardComponent { }
