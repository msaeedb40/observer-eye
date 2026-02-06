import { Component, Input } from '@angular/core';
import { CommonModule, DecimalPipe } from '@angular/common';

export interface ReliabilityMetrics {
    mttd: number;
    mttr: number;
    mtts: number;
    incident_count: number;
}

@Component({
    selector: 'app-reliability-metrics',
    standalone: true,
    imports: [CommonModule, DecimalPipe],
    template: `
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="glass-panel p-4 border-l-4 border-sky-500">
        <div class="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-1">MTTD</div>
        <div class="flex items-baseline gap-2">
          <div class="text-2xl font-bold">{{ metrics.mttd | number:'1.1-1' }}</div>
          <div class="text-[10px] text-slate-500 font-medium">min to detect</div>
        </div>
      </div>

      <div class="glass-panel p-4 border-l-4 border-emerald-500">
        <div class="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-1">MTTR</div>
        <div class="flex items-baseline gap-2">
          <div class="text-2xl font-bold">{{ metrics.mttr | number:'1.1-1' }}</div>
          <div class="text-[10px] text-slate-500 font-medium">min to resolve</div>
        </div>
      </div>

      <div class="glass-panel p-4 border-l-4 border-amber-500">
        <div class="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-1">MTTS</div>
        <div class="flex items-baseline gap-2">
          <div class="text-2xl font-bold">{{ metrics.mtts | number:'1.1-1' }}</div>
          <div class="text-[10px] text-slate-500 font-medium">min to silence</div>
        </div>
      </div>

      <div class="glass-panel p-4 border-l-4 border-indigo-500">
        <div class="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-1">Total Incidents</div>
        <div class="flex items-baseline gap-2">
          <div class="text-2xl font-bold">{{ metrics.incident_count }}</div>
          <div class="text-[10px] text-slate-500 font-medium">evaluated alerts</div>
        </div>
      </div>
    </div>
  `
})
export class ReliabilityMetricsComponent {
    @Input() metrics: ReliabilityMetrics = {
        mttd: 0,
        mttr: 0,
        mtts: 0,
        incident_count: 0
    };
}
