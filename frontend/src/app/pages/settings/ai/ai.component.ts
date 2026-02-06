import { Component, OnInit, inject, ChangeDetectionStrategy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
   FormSliderComponent,
   FormToggleComponent,
   FormSelectComponent,
   SelectOption
} from '../../../components';
import { SettingsService } from '../../../services/settings.service';

@Component({
   selector: 'app-settings-ai',
   standalone: true,
   imports: [
      CommonModule,
      FormsModule,
      FormSliderComponent,
      FormToggleComponent,
      FormSelectComponent
   ],
   changeDetection: ChangeDetectionStrategy.OnPush,
   template: `
    <div class="space-y-6 page-transition">
      <header class="flex justify-between items-end mb-8">
        <div>
          <h2 class="text-2xl font-black text-white mb-1 uppercase tracking-tighter">AI Intelligence Core</h2>
          <p class="text-xs text-slate-500">Configure machine learning models for deep anomaly detection</p>
        </div>
        <div class="flex gap-2">
           <span class="px-3 py-1 bg-sky-500/10 text-sky-400 text-[10px] font-black rounded uppercase border border-sky-500/20 shadow-[0_0_10px_rgba(14,165,233,0.1)]">
             ML Engine: v2.4-stable
           </span>
        </div>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Core ML Settings -->
        <div class="glass-panel p-8 border border-white/5 shadow-xl relative overflow-hidden">
           <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 to-purple-500"></div>
           <h3 class="text-lg font-bold text-white mb-8 flex items-center gap-2">
             <span class="w-2 h-2 rounded-full bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.5)]"></span>
             Anomaly Detection Engine
           </h3>
           
           <div class="space-y-8">
               <app-form-slider
                 label="Sensitivity Threshold"
                 [ngModel]="sensitivity()"
                 [min]="0"
                 [max]="1"
                 [step]="0.01"
                 minLabel="Conservative"
                 maxLabel="Aggressive"
                 (ngModelChange)="updateSensitivity($event)">
               </app-form-slider>

               <div class="p-4 bg-white/[0.02] rounded-2xl border border-white/5 space-y-6">
                  <app-form-toggle
                    label="Adaptive Baselines"
                    description="Automatically adjust thresholds based on seasonal patterns."
                    [ngModel]="settingsService.aiEnabled()"
                    (ngModelChange)="updateAiEnabled($event)">
                  </app-form-toggle>

                  <app-form-toggle
                    label="Forecasting (Predictive)"
                    description="Predict resource exhaustion 24h in advance."
                    [ngModel]="forecastingEnabled()"
                    (ngModelChange)="toggleForecasting($event)">
                  </app-form-toggle>
               </div>

               <app-form-select
                 label="Model Retraining Interval"
                 [options]="intervalOptions"
                 [ngModel]="selectedInterval()"
                 (ngModelChange)="updateInterval($event)">
               </app-form-select>
           </div>
        </div>

        <!-- Model Selection & Resource Usage -->
        <div class="space-y-6">
           <div class="glass-panel p-6 border border-white/5 shadow-xl">
              <h3 class="text-sm font-bold text-slate-200 mb-6 flex items-center gap-2">
                 <span class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></span>
                 Active Models (Production)
              </h3>
              <div class="space-y-4">
                 <div *ngFor="let model of models" class="flex items-center justify-between p-4 bg-white/[0.02] border border-white/5 rounded-xl hover:bg-white/[0.04] transition-all group">
                    <div class="flex items-center gap-3">
                       <span class="text-xl group-hover:scale-110 transition-transform">{{model.icon}}</span>
                       <div>
                          <div class="font-bold text-slate-300 text-sm tracking-tight">{{model.name}}</div>
                          <div class="text-[9px] text-slate-600 font-mono tracking-tighter">{{model.latency}}ms latency</div>
                       </div>
                    </div>
                    <div class="flex items-center gap-3">
                       <span class="w-2 h-2 rounded-full" [ngClass]="model.status === 'Active' ? 'bg-emerald-500 animate-pulse' : 'bg-slate-600'"></span>
                       <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest">{{model.status}}</span>
                    </div>
                 </div>
              </div>
           </div>

           <div class="glass-panel p-6 border border-indigo-500/10 bg-gradient-to-br from-indigo-500/5 to-transparent relative overflow-hidden">
              <div class="absolute -right-10 -bottom-10 w-32 h-32 bg-indigo-500/10 blur-3xl rounded-full"></div>
              <h3 class="text-sm font-bold text-slate-200 mb-2">AI Resource Impact</h3>
              <p class="text-xs text-slate-500 mb-6">Current compute allocation for ML workloads</p>
              
              <div class="space-y-6">
                 <div>
                    <div class="flex justify-between text-[10px] font-bold uppercase mb-2 tracking-widest">
                       <span class="text-slate-400">Worker CPU Affinity</span>
                       <span class="text-indigo-400 font-black">12.4%</span>
                    </div>
                    <div class="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                       <div class="h-full bg-gradient-to-r from-indigo-500 to-purple-500 shadow-[0_0_10px_rgba(99,102,241,0.5)]" style="width: 12.4%"></div>
                    </div>
                 </div>
                 <div>
                    <div class="flex justify-between text-[10px] font-bold uppercase mb-2 tracking-widest">
                       <span class="text-slate-400">Neural Cache (Redis)</span>
                       <span class="text-sky-400 font-black">842.5 MB</span>
                    </div>
                    <div class="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                       <div class="h-full bg-gradient-to-r from-sky-500 to-indigo-500 shadow-[0_0_10px_rgba(14,165,233,0.5)]" style="width: 45%"></div>
                    </div>
                 </div>
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
export class SettingsAIComponent implements OnInit {
   protected readonly settingsService = inject(SettingsService);

   // Local feature signals
   readonly sensitivity = signal<number>(0.85);
   readonly forecastingEnabled = signal<boolean>(false);
   readonly selectedInterval = signal<string>('6h');

   workspaceSlug = 'default';

   models = [
      { name: 'Prophet (Long-term Correlation)', icon: '📈', status: 'Active', latency: 450 },
      { name: 'LSTM Neural Forecaster', icon: '🧠', status: 'Active', latency: 120 },
      { name: 'DBSCAN Temporal Clustering', icon: '⛓️', status: 'Idle', latency: 85 }
   ];

   intervalOptions: SelectOption[] = [
      { label: 'Every Hour', value: '1h' },
      { label: 'Every 6 Hours', value: '6h' },
      { label: 'Every 24 Hours', value: '24h' }
   ];

   ngOnInit(): void {
      this.loadSettings();
   }

   loadSettings(): void {
      this.settingsService.getWorkspaceSettings(this.workspaceSlug).subscribe();

      this.settingsService.getSettingsByCategory('ai').subscribe({
         next: (settings: any[]) => {
            const sens = settings.find(s => s.key === 'ai_sensitivity');
            if (sens) this.sensitivity.set(Number.parseFloat(sens.value));

            const forecast = settings.find(s => s.key === 'ai_forecasting');
            if (forecast) this.forecastingEnabled.set(forecast.value === 'true' || forecast.value === true);

            const interval = settings.find(s => s.key === 'ai_training_interval');
            if (interval) this.selectedInterval.set(interval.value);
         }
      });
   }

   updateAiEnabled(val: boolean) {
      this.settingsService.updateWorkspaceSettings(this.workspaceSlug, { ai_enabled: val }).subscribe();
   }

   updateSensitivity(val: number) {
      this.sensitivity.set(val);
   }

   toggleForecasting(val: boolean) {
      this.forecastingEnabled.set(val);
   }

   updateInterval(val: string) {
      this.selectedInterval.set(val);
   }

   saveSettings(): void {
      console.log('AI configuration synchronized');
   }
}
