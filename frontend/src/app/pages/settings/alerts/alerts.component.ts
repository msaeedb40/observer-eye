import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  FormToggleComponent,
  FormInputComponent,
  FormSelectComponent,
  FormSliderComponent,
  SelectOption
} from '../../../components';
import { AlertsService } from '../../../services/alerts.service';

@Component({
  selector: 'app-settings-alerts',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    FormToggleComponent,
    FormInputComponent,
    FormSelectComponent,
    FormSliderComponent
  ],
  template: `
    <div class="space-y-6 page-transition">
      <header class="flex justify-between items-end mb-8">
        <div>
          <h2 class="text-2xl font-bold text-white mb-1">Alerting & Notifications</h2>
          <p class="text-xs text-slate-500">Configure alert rules and delivery channels</p>
        </div>
        <div class="flex gap-4">
           <button (click)="openChannelModal()" class="px-4 py-2 text-xs font-bold text-slate-400 hover:text-white transition-colors">
            + Add Channel
           </button>
           <button (click)="openRuleModal()" class="btn-premium px-6 py-2 text-xs">+ Create Alert Rule</button>
        </div>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Notification Channels -->
        <div class="glass-panel p-6 border border-white/5 shadow-xl">
          <h3 class="text-sm font-bold text-slate-200 mb-6 flex items-center gap-2">
             <span class="w-2 h-2 rounded-full bg-sky-400 shadow-[0_0_10px_rgba(56,189,248,0.5)]"></span>
             Delivery Channels
          </h3>
          <div class="space-y-4">
            <div *ngFor="let channel of channels" class="flex items-center justify-between p-4 bg-white/[0.02] rounded-xl border border-white/5 group hover:border-sky-500/30 transition-all hover:bg-white/[0.04]">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center text-lg border border-white/5">
                   {{getChannelIcon(channel.type)}}
                </div>
                <div>
                   <div class="font-bold text-slate-200 text-sm">{{channel.name}}</div>
                   <div class="text-[10px] text-slate-500 uppercase tracking-widest">{{channel.type}}</div>
                </div>
              </div>
              <div class="flex items-center gap-4">
                <app-form-toggle
                  [(ngModel)]="channel.is_active"
                  (ngModelChange)="updateChannel(channel)">
                </app-form-toggle>
                <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all">
                   <button (click)="editChannel(channel)" class="w-8 h-8 rounded-lg hover:bg-white/10 flex items-center justify-center text-slate-500 hover:text-sky-400">
                      ⚙️
                   </button>
                   <button (click)="deleteChannel(channel)" class="w-8 h-8 rounded-lg hover:bg-rose-500/10 flex items-center justify-center text-slate-500 hover:text-rose-400">
                      🗑️
                   </button>
                </div>
              </div>
            </div>
            
            <div *ngIf="channels.length === 0" class="p-8 text-center border-2 border-dashed border-white/5 rounded-xl">
               <p class="text-xs text-slate-600">No channels configured</p>
            </div>
          </div>
        </div>

        <!-- Alert Rules -->
        <div class="glass-panel p-6 border border-white/5 shadow-xl">
          <h3 class="text-sm font-bold text-slate-200 mb-6 flex items-center gap-2">
             <span class="w-2 h-2 rounded-full bg-amber-400 shadow-[0_0_10px_rgba(251,191,36,0.5)]"></span>
             Alert Rules
          </h3>
          <div class="space-y-3">
             <div *ngFor="let rule of alertRules" class="p-4 bg-white/[0.02] border border-white/5 rounded-xl group hover:border-amber-500/30 transition-all">
                <div class="flex justify-between items-start mb-2">
                   <div>
                      <div class="font-bold text-slate-200 text-sm">{{rule.name}}</div>
                      <div class="text-[10px] text-slate-500 mt-1">{{rule.description}}</div>
                   </div>
                   <div class="flex items-center gap-2">
                     <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase" 
                           [ngClass]="getSeverityClass(rule.severity)">
                       {{rule.severity}}
                     </span>
                     <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all">
                        <button (click)="editRule(rule)" class="w-6 h-6 rounded-md hover:bg-white/10 flex items-center justify-center text-[10px]">
                           ✏️
                        </button>
                        <button (click)="deleteRule(rule)" class="w-6 h-6 rounded-md hover:bg-rose-500/10 flex items-center justify-center text-[10px]">
                           🗑️
                        </button>
                     </div>
                   </div>
                </div>
                 <div class="flex justify-between items-center mt-4">
                    <div class="flex items-center gap-4">
                       <div class="text-[10px] text-slate-500 flex items-center gap-1">
                          <span class="opacity-50">Type:</span> {{rule.condition_type}}
                       </div>
                       <div class="text-[10px] text-slate-500 flex items-center gap-1">
                          <span class="opacity-50">Threshold:</span> <span class="text-sky-400 font-bold">{{rule.threshold}}</span>
                       </div>
                    </div>
                    <app-form-toggle
                      [(ngModel)]="rule.is_active"
                      (ngModelChange)="updateRuleStatus(rule)">
                    </app-form-toggle>
                 </div>
             </div>
             
             <div *ngIf="alertRules.length === 0" class="p-8 text-center border-2 border-dashed border-white/5 rounded-xl">
                <p class="text-xs text-slate-600">No alert rules defined</p>
             </div>
          </div>
        </div>
      </div>

      <!-- MODAL OVERLAY (Rule Form) -->
      <div *ngIf="showRuleModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-[#020617]/90 backdrop-blur-sm animate-in fade-in zoom-in duration-200">
         <div class="glass-panel w-full max-w-xl p-8 border border-white/10 shadow-2xl relative overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-amber-500 to-amber-300"></div>
            <header class="mb-8">
               <h3 class="text-xl font-bold text-white">{{ editingRule ? 'Edit' : 'Create' }} Alert Rule</h3>
               <p class="text-xs text-slate-500">Define conditions for triggering system alerts</p>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2">
               <app-form-input label="Rule Name" placeholder="e.g. High CPU Usage" [(ngModel)]="currentRule.name"></app-form-input>
               <app-form-select label="Severity" [options]="severityOptions" [(ngModel)]="currentRule.severity"></app-form-select>
               <div class="md:col-span-2">
                  <app-form-input label="Description" placeholder="What happens when this rule triggers?" [(ngModel)]="currentRule.description"></app-form-input>
               </div>
               <app-form-select label="Condition Type" [options]="conditionTypeOptions" [(ngModel)]="currentRule.condition_type"></app-form-select>
               <app-form-slider label="Threshold" [min]="0" [max]="1000" unit="" [(ngModel)]="currentRule.threshold"></app-form-slider>
            </div>

            <div class="mt-10 flex justify-end gap-4">
               <button (click)="closeRuleModal()" class="px-6 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:text-white transition-all">Cancel</button>
               <button (click)="saveRule()" class="btn-premium px-8 py-2.5 text-xs">Save Changes</button>
            </div>
         </div>
      </div>

      <!-- MODAL OVERLAY (Channel Form) -->
      <div *ngIf="showChannelModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-[#020617]/90 backdrop-blur-sm animate-in fade-in zoom-in duration-200">
         <div class="glass-panel w-full max-w-md p-8 border border-white/10 shadow-2xl relative overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-sky-500 to-indigo-500"></div>
            <header class="mb-8">
               <h3 class="text-xl font-bold text-white">{{ editingChannel ? 'Edit' : 'Add' }} Delivery Channel</h3>
               <p class="text-xs text-slate-500">Connect a new destination for notifications</p>
            </header>

            <div class="space-y-4">
               <app-form-input label="Channel Name" placeholder="e.g. SRE Slack" [(ngModel)]="currentChannel.name"></app-form-input>
               <app-form-select label="Channel Type" [options]="channelTypeOptions" [(ngModel)]="currentChannel.type"></app-form-select>
               <app-form-input label="Target URI / Webhook" placeholder="https://..." [(ngModel)]="currentChannel.destination"></app-form-input>
               <div class="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/5 mt-6">
                  <span class="text-xs font-bold text-slate-200">Enable Channel</span>
                  <app-form-toggle [(ngModel)]="currentChannel.is_active"></app-form-toggle>
               </div>
            </div>

            <div class="mt-10 flex justify-end gap-4">
               <button (click)="closeChannelModal()" class="px-6 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:text-white transition-all">Cancel</button>
               <button (click)="saveChannel()" class="btn-premium px-8 py-2.5 text-xs">Confirm</button>
            </div>
         </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; }
    .animate-in { animation: fadeIn 0.2s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: scale(0.98); } to { opacity: 1; transform: scale(1); } }
  `]
})
export class SettingsAlertsComponent implements OnInit {
  private alertsService = inject(AlertsService);

  channels: any[] = [];
  alertRules: any[] = [];

  // Modal State
  showRuleModal = false;
  editingRule = false;
  currentRule: any = {};

  showChannelModal = false;
  editingChannel = false;
  currentChannel: any = {};

  // Options
  severityOptions: SelectOption[] = [
    { label: 'Critical', value: 'critical' },
    { label: 'Warning', value: 'warning' },
    { label: 'Info', value: 'info' }
  ];

  conditionTypeOptions: SelectOption[] = [
    { label: 'Threshold', value: 'threshold' },
    { label: 'Outlier', value: 'outlier' },
    { label: 'Missing Data', value: 'missing' }
  ];

  channelTypeOptions: SelectOption[] = [
    { label: 'Slack', value: 'slack' },
    { label: 'Email', value: 'email' },
    { label: 'Webhook', value: 'webhook' },
    { label: 'PagerDuty', value: 'pagerduty' }
  ];

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.alertsService.getChannels().subscribe(data => this.channels = data);
    this.alertsService.getRules().subscribe(data => this.alertRules = data);
  }

  // ========================
  // CHANNEL METHODS
  // ========================

  openChannelModal() {
    this.editingChannel = false;
    this.currentChannel = { name: '', type: 'slack', is_active: true, destination: '' };
    this.showChannelModal = true;
  }

  editChannel(channel: any) {
    this.editingChannel = true;
    this.currentChannel = { ...channel };
    this.showChannelModal = true;
  }

  closeChannelModal() {
    this.showChannelModal = false;
  }

  saveChannel() {
    if (this.editingChannel) {
      this.alertsService.updateChannel(this.currentChannel.id, this.currentChannel).subscribe(() => {
        this.loadData();
        this.closeChannelModal();
      });
    } else {
      this.alertsService.createChannel(this.currentChannel).subscribe(() => {
        this.loadData();
        this.closeChannelModal();
      });
    }
  }

  updateChannel(channel: any) {
    this.alertsService.updateChannel(channel.id, channel).subscribe();
  }

  deleteChannel(channel: any) {
    if (confirm(`Are you sure you want to delete channel "${channel.name}"?`)) {
      this.alertsService.deleteChannel(channel.id).subscribe(() => this.loadData());
    }
  }

  // ========================
  // RULE METHODS
  // ========================

  openRuleModal() {
    this.editingRule = false;
    this.currentRule = { name: '', severity: 'warning', condition_type: 'threshold', threshold: 80, is_active: true, description: '' };
    this.showRuleModal = true;
  }

  editRule(rule: any) {
    this.editingRule = true;
    this.currentRule = { ...rule };
    this.showRuleModal = true;
  }

  closeRuleModal() {
    this.showRuleModal = false;
  }

  saveRule() {
    if (this.editingRule) {
      this.alertsService.updateRule(this.currentRule.id, this.currentRule).subscribe(() => {
        this.loadData();
        this.closeRuleModal();
      });
    } else {
      this.alertsService.createRule(this.currentRule).subscribe(() => {
        this.loadData();
        this.closeRuleModal();
      });
    }
  }

  updateRuleStatus(rule: any) {
    this.alertsService.updateRule(rule.id, rule).subscribe();
  }

  deleteRule(rule: any) {
    if (confirm(`Are you sure you want to delete rule "${rule.name}"?`)) {
      this.alertsService.deleteRule(rule.id).subscribe(() => this.loadData());
    }
  }

  // ========================
  // UI HELPERS
  // ========================

  getChannelIcon(type: string): string {
    switch (type?.toLowerCase()) {
      case 'slack': return '💬';
      case 'email': return '📧';
      case 'webhook': return '🔗';
      case 'pagerduty': return '📟';
      default: return '📣';
    }
  }

  getSeverityClass(severity: string): string {
    switch (severity?.toLowerCase()) {
      case 'critical': return 'bg-rose-500/10 text-rose-400 border border-rose-500/20';
      case 'warning': return 'bg-amber-500/10 text-amber-500 border border-amber-500/20';
      default: return 'bg-sky-500/10 text-sky-400 border border-sky-500/20';
    }
  }
}
