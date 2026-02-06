import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Platform Settings</h1>
        <p class="text-slate-400">Manage global observability configurations and data retention</p>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Sidebar Navigation -->
        <div class="lg:col-span-1 space-y-2">
          <div *ngFor="let group of settingGroups" 
               [routerLink]="['/settings', group.id]"
               routerLinkActive="border-sky-500 bg-white/5"
               class="glass-panel p-4 cursor-pointer hover:bg-white/5 transition-colors border-l-2 border-transparent">
            <h3 class="font-bold text-white text-sm flex items-center gap-3">
              <span>{{group.icon}}</span>
              {{group.label}}
            </h3>
            <p class="text-[10px] text-slate-500 mt-1 pl-7">{{group.description}}</p>
          </div>
        </div>

        <!-- Main Content (Sub-routes) -->
        <div class="lg:col-span-3">
           <router-outlet></router-outlet>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class SettingsComponent implements OnInit {
  settingGroups = [
    { id: 'general', label: 'General', icon: '⚙️', description: 'Appearance and core behavior.' },
    { id: 'alerts', label: 'Alerting', icon: '🔔', description: 'Rules and notification channels.' },
    { id: 'integrations', label: 'Integrations', icon: '🔌', description: 'Third-party data sources.' },
    { id: 'ai', label: 'AI & ML', icon: '🧠', description: 'Anomaly detection settings.' },
    { id: 'security', label: 'Security', icon: '🛡️', description: 'RBAC and API keys.' },
    { id: 'billing', label: 'Billing', icon: '💳', description: 'Subscription and limits.' }
  ];

  constructor(private router: Router) { }

  ngOnInit(): void {
    if (this.router.url === '/settings') {
      this.router.navigate(['/settings/general']);
    }
  }
}
