import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface CloudResource {
    name: string;
    provider: string;
    region: string;
    type: string;
    utilization: number;
    status: string;
}

@Component({
    selector: 'app-cloud-resource-inventory',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="glass-panel overflow-hidden">
      <div class="p-6 border-b border-white/5 bg-white/[0.02] flex justify-between items-center">
        <h3 class="font-bold text-white">Managed Cloud Inventory</h3>
        <div class="flex gap-2">
           <span class="px-2 py-1 bg-white/5 border border-white/10 rounded text-[10px] font-bold text-slate-400">Total Resources: {{ resources.length }}</span>
        </div>
      </div>
      <div class="divide-y divide-white/5">
        <div *ngFor="let res of resources" class="flex items-center justify-between p-6 hover:bg-white/[0.02] transition-all group">
          <div class="flex items-center gap-5">
            <div class="w-10 h-10 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-lg shadow-inner">
              {{res.provider === 'AWS' ? '🟠' : (res.provider === 'Azure' ? '🔵' : '🔴')}}
            </div>
            <div>
              <div class="font-bold text-slate-200 text-base leading-tight">{{res.name}}</div>
              <div class="text-[10px] font-mono text-slate-500 mt-1 flex items-center gap-2">
                 {{res.provider}} <span class="text-[8px]">•</span> {{res.region}} <span class="text-[8px]">•</span> {{res.type}}
              </div>
            </div>
          </div>
          <div class="text-right flex items-center gap-8">
            <div class="hidden md:block">
               <p class="text-[10px] font-bold text-slate-500 uppercase mb-0.5">CPU Avg</p>
               <div class="w-24 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div class="h-full bg-sky-400" [style.width.%]="res.utilization"></div>
               </div>
            </div>
            <div class="w-24">
               <p class="text-[10px] font-bold text-slate-500 uppercase mb-0.5">Status</p>
               <span class="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-[10px] font-black rounded uppercase border border-emerald-500/20">
                  {{res.status}}
               </span>
            </div>
            <button class="w-8 h-8 rounded-lg hover:bg-white/5 flex items-center justify-center text-slate-500 hover:text-sky-400 transition-all opacity-0 group-hover:opacity-100">
              <span class="text-lg">→</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  `
})
export class CloudResourceInventoryComponent {
    @Input() resources: CloudResource[] = [];
}
