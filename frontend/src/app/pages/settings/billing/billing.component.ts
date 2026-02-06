import { Component, OnInit, inject, ChangeDetectionStrategy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SettingsService } from '../../../services/settings.service';

@Component({
   selector: 'app-settings-billing',
   standalone: true,
   imports: [CommonModule],
   changeDetection: ChangeDetectionStrategy.OnPush,
   template: `
    <div class="space-y-6 page-transition">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
         <!-- Subscription Plan -->
         <div class="glass-panel p-8 bg-gradient-to-br from-sky-500/10 to-transparent border border-sky-500/10 shadow-2xl relative overflow-hidden group">
            <div class="absolute -right-16 -top-16 w-48 h-48 bg-sky-500/5 blur-3xl rounded-full group-hover:bg-sky-500/10 transition-colors"></div>
            
            <header class="relative z-10">
               <h3 class="text-[10px] font-black text-sky-400 uppercase tracking-[0.2em] mb-4">Current Subscription</h3>
               <div class="text-4xl font-black text-white mb-2 tracking-tighter">Enterprise Plus</div>
               <p class="text-xs text-slate-500 mb-10 max-w-[200px]">Unmetered ingestion with 90-day retention and VIP support</p>
            </header>
            
            <button class="w-full btn-premium py-3 text-[10px] relative z-10">Manage Billing Portal</button>
         </div>

         <!-- Usage Overview -->
         <div class="glass-panel p-8 border border-white/5 relative overflow-hidden">
            <h3 class="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-8">Resource Consumption (Feb)</h3>
            <div class="space-y-8">
               <div *ngFor="let stat of usageStats()">
                  <div class="flex justify-between text-[10px] font-bold uppercase mb-3 tracking-widest">
                     <span class="text-slate-400">{{stat.label}}</span>
                     <span class="text-white">{{stat.current}} / {{stat.limit}}</span>
                  </div>
                  <div class="w-full h-1.5 bg-white/5 rounded-full overflow-hidden shadow-inner">
                     <div class="h-full transition-all duration-1000 ease-out shadow-[0_0_10px_rgba(14,165,233,0.3)]" 
                          [ngClass]="stat.color"
                          [style.width.%]="stat.percent"></div>
                  </div>
               </div>
            </div>
         </div>
      </div>

      <div class="glass-panel p-8 border border-white/5 shadow-2xl">
         <div class="flex justify-between items-center mb-10">
            <div>
               <h3 class="font-black text-white uppercase tracking-tight">Recent Invoices</h3>
               <p class="text-[10px] text-slate-500 mt-1">Downloadable history of financial transactions</p>
            </div>
            <button class="text-sky-400 text-[10px] font-black uppercase tracking-widest hover:text-white transition-colors">View All Invoices</button>
         </div>
         
         <div class="overflow-x-auto">
            <table class="w-full text-left">
               <thead class="text-[10px] font-black text-slate-600 uppercase tracking-[0.2em] border-b border-white/5">
                  <tr>
                     <th class="pb-6">Reference ID</th>
                     <th class="pb-6">Billing Period</th>
                     <th class="pb-6">Status</th>
                     <th class="pb-6 text-right">Total Amount</th>
                  </tr>
               </thead>
               <tbody class="text-sm divide-y divide-white/5">
                  <tr *ngFor="let inv of invoices()" class="group hover:bg-white/[0.02] transition-colors">
                     <td class="py-5 text-slate-300 font-mono tracking-tighter text-xs">{{inv.id}}</td>
                     <td class="py-5 text-slate-500 text-xs">{{inv.date}}</td>
                     <td class="py-5">
                        <span class="px-2 py-0.5 bg-sky-500/10 text-sky-400 text-[9px] font-black rounded uppercase border border-sky-500/20">Paid</span>
                     </td>
                     <td class="py-5 text-right text-white font-black tabular-nums">{{inv.amount}}</td>
                  </tr>
               </tbody>
            </table>
         </div>
      </div>
    </div>
  `,
   styles: [`
    :host { display: block; }
  `]
})
export class SettingsBillingComponent implements OnInit {
   private readonly settingsService = inject(SettingsService);

   // Reactive signals for state
   readonly invoices = signal<any[]>([
      { id: 'INV-2024-0012-P', date: 'Jan 1, 2024 - Jan 31, 2024', amount: '$4,250.00' },
      { id: 'INV-2023-0145-P', date: 'Dec 1, 2023 - Dec 31, 2023', amount: '$3,890.40' },
      { id: 'INV-2023-0098-P', date: 'Nov 1, 2023 - Nov 30, 2023', amount: '$3,920.10' }
   ]);

   readonly usageStats = signal<any[]>([
      { label: 'Metrics Ingested', current: '12.4 GB', limit: '50 GB', percent: 24.8, color: 'bg-sky-500' },
      { label: 'Logs Ingested', current: '482 GB', limit: '1 TB', percent: 48.2, color: 'bg-indigo-500' },
      { label: 'Trace Spans', current: '8.2M', limit: '10M', percent: 82, color: 'bg-amber-500' }
   ]);

   ngOnInit(): void {
      this.loadBillingInfo();
   }

   loadBillingInfo(): void {
      // Fetch from backend...
   }
}
