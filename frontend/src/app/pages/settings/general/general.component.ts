import { Component, OnInit, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FormToggleComponent, FormSliderComponent } from '../../../components';
import { SettingsService } from '../../../services/settings.service';

@Component({
  selector: 'app-settings-general',
  standalone: true,
  imports: [CommonModule, FormsModule, FormToggleComponent, FormSliderComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="glass-panel p-8 page-transition border border-white/5 shadow-xl relative overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-sky-500/50 to-indigo-500/50"></div>
      
      <header class="mb-8">
        <h3 class="text-xl font-bold text-white tracking-tight">General Configuration</h3>
        <p class="text-xs text-slate-500 mt-1">Global workspace settings and data retention policies</p>
      </header>
      
      <div class="space-y-8 max-w-2xl">
        <div class="p-4 bg-white/[0.02] rounded-2xl border border-white/5 space-y-6">
          <app-form-toggle
            label="Real-time Telemetry"
            description="Streaming data updates every 5 seconds via WebSockets."
            [ngModel]="realtimeEnabled()"
            (ngModelChange)="toggleRealtime()">
          </app-form-toggle>

          <app-form-toggle
            label="Anomalies Detection (AI)"
            description="Enable automated pattern recognition and forecasting."
            [ngModel]="settingsService.aiEnabled()"
            (ngModelChange)="updateAiEnabled($event)">
          </app-form-toggle>
        </div>

        <div class="p-6 bg-white/[0.02] rounded-2xl border border-white/5">
          <app-form-slider
            label="Data Retention Policy"
            [min]="1" [max]="365" unit=" Days"
            minLabel="1 Day" maxLabel="1 Year"
            [ngModel]="settingsService.retentionDays()"
            (ngModelChange)="updateRetention($event)">
          </app-form-slider>
          <p class="text-[10px] text-slate-500 mt-3 px-1 italic">
            * Older telemetry data will be automatically purged or archived based on your current storage plan.
          </p>
        </div>

        <div class="pt-6 flex justify-end gap-3 border-t border-white/5">
          <button (click)="loadSettings()" class="px-6 py-2.5 rounded-xl text-xs font-bold text-slate-500 hover:text-white transition-colors uppercase tracking-widest">Discard</button>
          <button (click)="saveChanges()" class="btn-premium px-10 py-2.5 text-xs">Sync Settings</button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; }
  `]
})
export class SettingsGeneralComponent implements OnInit {
  protected readonly settingsService = inject(SettingsService);
  workspaceSlug = 'default';

  ngOnInit(): void {
    this.loadSettings();
  }

  loadSettings(): void {
    this.settingsService.getWorkspaceSettings(this.workspaceSlug).subscribe();
    this.settingsService.getFeatureFlags().subscribe();
  }

  realtimeEnabled() {
    return this.settingsService.featureFlags().find(f => f.name === 'realtime_telemetry')?.enabled ?? true;
  }

  toggleRealtime() {
    const flag = this.settingsService.featureFlags().find(f => f.name === 'realtime_telemetry');
    if (flag) {
      this.settingsService.toggleFeatureFlag(flag.id).subscribe();
    }
  }

  updateAiEnabled(val: boolean) {
    // Local signal update via service tap in PATCH, but we can also optimistically update if we had writable signals exposed
    // For now we'll just call the service which updates the signal on success
    this.settingsService.updateWorkspaceSettings(this.workspaceSlug, { ai_enabled: val }).subscribe();
  }

  updateRetention(val: number) {
    this.settingsService.updateWorkspaceSettings(this.workspaceSlug, { retention_days: val }).subscribe();
  }

  saveChanges(): void {
    // Settings are updated reactively on change, this acts as a final sync check
    this.loadSettings();
    console.log('Settings synchronized with backend');
  }
}
