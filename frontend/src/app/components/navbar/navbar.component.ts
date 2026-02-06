import { Component, Input, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <nav class="glass-panel mx-4 mt-4 px-6 h-16 flex items-center justify-between sticky top-4 z-[100] backdrop-blur-xl border-white/5">
      <div class="flex items-center gap-8">
        <a routerLink="/dashboard" class="flex items-center gap-2 no-underline group shrink-0">
          <span class="text-2xl group-hover:scale-110 transition-transform">👁️</span>
          <span class="text-xl font-bold gradient-text">Observer-Eye</span>
        </a>

        <div class="hidden xl:flex items-center gap-1">
          <a routerLink="/dashboard" routerLinkActive="active" class="nav-item">Overview</a>
          
          <!-- Modules Dropdown -->
          <div class="relative group/menu">
            <button class="nav-item flex items-center gap-1 group-hover/menu:text-white transition-colors">
              Modules
              <span class="text-[10px] opacity-50 group-hover/menu:rotate-180 transition-transform">▼</span>
            </button>
            <div class="absolute top-[calc(100%+8px)] left-0 w-[480px] glass-panel p-4 opacity-0 invisible group-hover/menu:opacity-100 group-hover/menu:visible transition-all duration-200 grid grid-cols-2 gap-4 border-white/10 shadow-2xl">
              <div>
                <h4 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-3 px-2">Observability Pillars</h4>
                <a routerLink="/metrics" class="menu-item">
                  <span class="menu-icon">📊</span>
                  <div>
                    <div class="menu-title">Metrics</div>
                    <div class="menu-desc">Time-series performance data</div>
                  </div>
                </a>
                <a routerLink="/logs" class="menu-item">
                  <span class="menu-icon">📄</span>
                  <div>
                    <div class="menu-title">Logs</div>
                    <div class="menu-desc">Distributed log processing</div>
                  </div>
                </a>
                <a routerLink="/traces" class="menu-item">
                  <span class="menu-icon">⛓️</span>
                  <div>
                    <div class="menu-title">Traces</div>
                    <div class="menu-desc">End-to-end request tracking</div>
                  </div>
                </a>
                <a routerLink="/topology" class="menu-item">
                  <span class="menu-icon">🕸️</span>
                  <div>
                    <div class="menu-title">Topology</div>
                    <div class="menu-desc">Service mesh & dependencies</div>
                  </div>
                </a>
                <a routerLink="/kubernetes" class="menu-item">
                  <span class="menu-icon">☸️</span>
                  <div>
                    <div class="menu-title">Kubernetes</div>
                    <div class="menu-desc">Cluster & Pod orchestration</div>
                  </div>
                </a>
              </div>
              <div>
                <h4 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-3 px-2">Performance & Ops</h4>
                <a routerLink="/apm" class="menu-item">
                  <span class="menu-icon">🚀</span>
                  <div>
                    <div class="menu-title">APM</div>
                    <div class="menu-desc">App performance monitoring</div>
                  </div>
                </a>
                <a routerLink="/traffic" class="menu-item">
                  <span class="menu-icon">🚥</span>
                  <div>
                    <div class="menu-title">Traffic</div>
                    <div class="menu-desc">L7 Analysis & User Sessions</div>
                  </div>
                </a>
                <a routerLink="/cloud" class="menu-item">
                  <span class="menu-icon">☁️</span>
                  <div>
                    <div class="menu-title">Cloud</div>
                    <div class="menu-desc">Multi-cloud orchestration</div>
                  </div>
                </a>
                <a routerLink="/identity" class="menu-item">
                  <span class="menu-icon">👤</span>
                  <div>
                    <div class="menu-title">Identity</div>
                    <div class="menu-desc">Auth & Session telemetry</div>
                  </div>
                </a>
              </div>
            </div>
          </div>

          <a routerLink="/incidents" routerLinkActive="active" class="nav-item">Incidents</a>
          <a routerLink="/slo" routerLinkActive="active" class="nav-item">SLOs</a>
          <a routerLink="/explorer" routerLinkActive="active" class="nav-item">Explorer</a>
          <a routerLink="/insights" routerLinkActive="active" class="nav-item font-semibold text-sky-400">AI-Insights</a>
        </div>
      </div>
      
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2 mr-4 border-r border-white/10 pr-4">
          <a routerLink="/alerts" title="Alerts" class="nav-icon no-underline relative">
            🔔
            <span *ngIf="alertCount > 0" class="absolute -top-1 -right-1 w-2 h-2 bg-rose-500 rounded-full"></span>
          </a>
          <a routerLink="/integrations" title="Integrations" class="nav-icon no-underline">🔌</a>
          <a routerLink="/settings" title="Settings" class="nav-icon no-underline">⚙️</a>
        </div>
        
        <div class="relative group/user">
          <button class="w-10 h-10 rounded-xl bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors border border-white/5 group-hover/user:border-sky-500/50">
            <span class="text-xs font-bold">{{ userInitials() }}</span>
          </button>
          
          <div class="absolute top-[calc(100%+8px)] right-0 w-48 glass-panel p-2 opacity-0 invisible group-hover/user:opacity-100 group-hover/user:visible transition-all duration-200 border-white/10 shadow-2xl">
            <div class="px-3 py-2 border-b border-white/5 mb-1">
              <div class="text-[10px] font-bold text-slate-500 uppercase tracking-widest truncate">{{ authService.currentUser()?.full_name }}</div>
              <div class="text-[8px] text-slate-600 truncate">{{ authService.currentUser()?.email }}</div>
            </div>
            <a routerLink="/settings/profile" class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/5 text-xs transition-colors">
              <span>👤</span> Profile
            </a>
            <button (click)="authService.logout()" class="w-full flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-rose-500/10 text-rose-400 text-xs transition-colors">
              <span>🚪</span> Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  `,
  styles: [`
    .nav-item {
      padding: 0.5rem 1rem;
      font-size: 0.875rem;
      font-weight: 500;
      color: var(--text-secondary);
      border-radius: 12px;
      transition: all 0.2s ease;
    }
    .nav-item:hover {
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.05);
    }
    .nav-item.active {
      color: var(--accent-primary);
      background: rgba(56, 189, 248, 0.1);
    }
    .menu-item {
      display: flex;
      gap: 1rem;
      padding: 0.75rem;
      border-radius: 12px;
      transition: all 0.2s;
      text-decoration: none;
    }
    .menu-item:hover {
      background: rgba(255, 255, 255, 0.05);
    }
    .menu-icon {
      font-size: 1.25rem;
      margin-top: 0.125rem;
    }
    .menu-title {
      font-weight: 700;
      font-size: 0.875rem;
      color: var(--text-primary);
      margin-bottom: 0.125rem;
    }
    .menu-desc {
      font-size: 0.75rem;
      color: var(--text-secondary);
    }
    .nav-icon {
      font-size: 1.25rem;
      opacity: 0.6;
      transition: all 0.2s;
    }
    .nav-icon:hover {
      opacity: 1;
      transform: translateY(-2px);
    }
  `]
})
export class NavbarComponent {
  @Input() alertCount = 0;

  constructor(public authService: AuthService) { }

  userInitials = computed(() => {
    const user = this.authService.currentUser();
    if (!user) return '??';
    const names = user.full_name.split(' ');
    if (names.length >= 2) return (names[0][0] + names[1][0]).toUpperCase();
    return names[0].substring(0, 2).toUpperCase();
  });
}
