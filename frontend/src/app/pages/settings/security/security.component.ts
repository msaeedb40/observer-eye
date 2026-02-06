import { Component, OnInit, inject, ChangeDetectionStrategy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FormToggleComponent } from '../../../components';
import { SettingsService } from '../../../services/settings.service';

@Component({
  selector: 'app-settings-security',
  standalone: true,
  imports: [CommonModule, FormsModule, FormToggleComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="space-y-6 page-transition">
      <div class="glass-panel p-8 border border-white/5 shadow-xl relative overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-rose-500 to-orange-500"></div>
        
        <header class="mb-8">
          <h3 class="text-xl font-black text-white uppercase tracking-tighter">Security & Access Control</h3>
          <p class="text-xs text-slate-500 mt-1">Manage API keys, SSO providers, and security hardening policies</p>
        </header>
        
        <div class="space-y-8">
          <div class="p-4 bg-white/[0.02] rounded-2xl border border-white/5">
            <app-form-toggle
              label="Enforce Security Hardening"
              description="Automatically rotate API keys and enforce stricter RBAC policies."
              [ngModel]="hardeningEnabled()"
              (ngModelChange)="saveHardening($event)">
            </app-form-toggle>
          </div>

          <div>
            <div class="flex justify-between items-center mb-6">
              <label class="block text-[10px] font-black text-slate-500 uppercase tracking-widest">API Access Keys</label>
              <span class="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 text-[10px] font-bold rounded border border-emerald-500/20">
                {{apiKeys().length}} Active
              </span>
            </div>

            <div class="space-y-3">
              <div *ngFor="let key of apiKeys()" class="flex items-center justify-between p-4 bg-white/[0.02] border border-white/5 rounded-xl group hover:bg-white/[0.04] transition-all">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-xl bg-orange-500/10 flex items-center justify-center text-orange-400 border border-orange-500/20 group-hover:scale-110 transition-transform">
                    🔑
                  </div>
                  <div>
                    <div class="text-sm font-bold text-slate-200">{{key.name}}</div>
                    <code class="text-[10px] text-slate-600 font-mono tracking-tighter">{{key.truncated_secret || 'obs_eye_****'}}</code>
                  </div>
                </div>
                <div class="flex items-center gap-3">
                  <button (click)="revokeKey(key)" class="px-4 py-2 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-400/10 text-[10px] font-black uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-all">
                    Revoke
                  </button>
                </div>
              </div>

              <button class="w-full py-4 border-2 border-dashed border-white/5 rounded-2xl text-slate-500 hover:text-white hover:border-white/20 hover:bg-white/[0.01] transition-all font-black text-[10px] uppercase tracking-[0.2em] group">
                <span class="inline-block group-hover:rotate-90 transition-transform mr-2">+</span>
                Create New API Key
              </button>
            </div>
          </div>

          <div class="pt-8 border-t border-white/5">
             <h4 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6">SSO & SAML Configuration</h4>
             <div class="glass-panel p-6 bg-gradient-to-br from-blue-500/5 to-transparent border-blue-500/10 flex items-center justify-between group overflow-hidden relative">
                <div class="absolute -right-10 -top-10 w-24 h-24 bg-blue-500/5 blur-2xl rounded-full group-hover:bg-blue-500/10 transition-colors"></div>
                <div class="flex items-center gap-4 relative z-10">
                   <div class="w-12 h-12 rounded-2xl bg-blue-500/10 flex items-center justify-center text-2xl border border-blue-500/20 group-hover:scale-110 transition-transform">🏢</div>
                   <div>
                      <div class="text-[10px] text-slate-500 font-black uppercase tracking-widest mb-1">Identity Provider</div>
                      <div class="text-sm font-bold text-slate-200">{{ssoProvider() || 'Not Connected'}}</div>
                   </div>
                </div>
                <button class="btn-premium px-6 py-2.5 text-[10px] relative z-10">
                  {{ssoProvider() ? 'Manage Gateway' : 'Setup SSO'}}
                </button>
             </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; }
  `]
})
export class SettingsSecurityComponent implements OnInit {
  protected readonly settingsService = inject(SettingsService);

  // Reactive signals for state
  readonly hardeningEnabled = signal<boolean>(false);
  readonly apiKeys = signal<any[]>([]);
  readonly ssoProvider = signal<string | null>(null);

  workspaceSlug = 'default';

  ngOnInit(): void {
    this.loadSecurityData();
  }

  loadSecurityData(): void {
    // Mock data for API keys - in real app fetch from dedicated security service
    this.apiKeys.set([
      { id: 1, name: 'Production Telemetry Key', truncated_secret: 'obs_eye_live_****************abc123' },
      { id: 2, name: 'CI/CD Scanner Key', truncated_secret: 'obs_eye_test_****************xyz789' }
    ]);

    this.settingsService.getSettingsByCategory('security').subscribe({
      next: (settings) => {
        const hard = settings.find((s: any) => s.key === 'security_hardening');
        if (hard) this.hardeningEnabled.set(hard.value === 'true' || hard.value === true);

        const sso = settings.find((s: any) => s.key === 'sso_provider');
        if (sso) this.ssoProvider.set(sso.value);
      }
    });
  }

  saveHardening(val: boolean): void {
    this.hardeningEnabled.set(val);
    console.log('Updating security hardening:', val);
    // Persist via service...
  }

  revokeKey(key: any): void {
    console.log('Revoking key:', key.name);
    this.apiKeys.update(keys => keys.filter(k => k.id !== key.id));
    // DELETE request to backend...
  }
}
