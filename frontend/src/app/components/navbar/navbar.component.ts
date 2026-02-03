import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <nav class="glass-panel mx-4 mt-4 px-6 h-16 flex items-center justify-between sticky top-4 z-[100] backdrop-blur-xl border-white/5">
      <div class="flex items-center gap-8">
        <a routerLink="/dashboard" class="flex items-center gap-2 no-underline group">
          <span class="text-2xl group-hover:scale-110 transition-transform">👁️</span>
          <span class="text-xl font-bold gradient-text">Observer-Eye</span>
        </a>

        <div class="hidden lg:flex items-center gap-1">
          <a routerLink="/metrics" routerLinkActive="active" class="nav-item">Metrics</a>
          <a routerLink="/logs" routerLinkActive="active" class="nav-item">Logs</a>
          <a routerLink="/traces" routerLinkActive="active" class="nav-item">Traces</a>
          <a routerLink="/topology" routerLinkActive="active" class="nav-item">Topology</a>
          <a routerLink="/insights" routerLinkActive="active" class="nav-item font-semibold text-sky-400">AI-Insights</a>
        </div>
      </div>
      
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2 mr-4 border-r border-white/10 pr-4">
          <a routerLink="/metrics/network" title="Network" class="nav-icon no-underline">🌐</a>
          <a routerLink="/metrics/security" title="Security" class="nav-icon no-underline">🛡️</a>
          <a routerLink="/metrics/system" title="System" class="nav-icon no-underline">🖥️</a>
        </div>
        
        <button class="w-10 h-10 rounded-xl bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors border border-white/5">
          <span class="text-xs font-bold">JD</span>
        </button>
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
}
