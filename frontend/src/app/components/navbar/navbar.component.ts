import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
    selector: 'app-navbar',
    standalone: true,
    imports: [CommonModule, RouterModule],
    template: `
    <nav class="navbar">
      <div class="navbar-brand">
        <a routerLink="/dashboard" class="logo">
          <span class="logo-icon">👁️</span>
          <span class="logo-text">Observer-Eye</span>
        </a>
      </div>
      
      <div class="navbar-menu">
        <a routerLink="/metrics" routerLinkActive="active" class="nav-link">Metrics</a>
        <a routerLink="/events" routerLinkActive="active" class="nav-link">Events</a>
        <a routerLink="/logs" routerLinkActive="active" class="nav-link">Logs</a>
        <a routerLink="/traces" routerLinkActive="active" class="nav-link">Traces</a>
        <a routerLink="/apm" routerLinkActive="active" class="nav-link">APM</a>
        <a routerLink="/alerts" routerLinkActive="active" class="nav-link">
          Alerts
          <span *ngIf="alertCount > 0" class="badge">{{ alertCount }}</span>
        </a>
      </div>
      
      <div class="navbar-actions">
        <button class="btn-icon" title="Settings">⚙️</button>
        <button class="btn-icon" title="User">👤</button>
      </div>
    </nav>
  `,
    styles: [`
    .navbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      height: 60px;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      border-bottom: 1px solid rgba(255,255,255,0.1);
      position: sticky;
      top: 0;
      z-index: 100;
    }
    
    .navbar-brand .logo {
      display: flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      color: white;
    }
    
    .logo-icon { font-size: 24px; }
    .logo-text { 
      font-size: 18px;
      font-weight: 600;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    .navbar-menu {
      display: flex;
      gap: 4px;
    }
    
    .nav-link {
      padding: 8px 16px;
      color: rgba(255,255,255,0.7);
      text-decoration: none;
      border-radius: 8px;
      transition: all 0.2s;
      position: relative;
    }
    
    .nav-link:hover {
      color: white;
      background: rgba(255,255,255,0.1);
    }
    
    .nav-link.active {
      color: white;
      background: rgba(102, 126, 234, 0.3);
    }
    
    .badge {
      position: absolute;
      top: 2px;
      right: 2px;
      background: #ef4444;
      color: white;
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 10px;
    }
    
    .navbar-actions {
      display: flex;
      gap: 8px;
    }
    
    .btn-icon {
      width: 36px;
      height: 36px;
      border: none;
      background: rgba(255,255,255,0.1);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
    }
    
    .btn-icon:hover {
      background: rgba(255,255,255,0.2);
    }
  `]
})
export class NavbarComponent {
    @Input() alertCount = 0;
}
