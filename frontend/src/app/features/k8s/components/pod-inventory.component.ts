import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface PodInfo {
    name: string;
    namespace: string;
    status: 'Running' | 'Pending' | 'Failed' | 'Succeeded';
    cpu: string;
    memory: string;
    age: string;
}

@Component({
    selector: 'app-pod-inventory',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="glass-panel overflow-hidden">
      <div class="p-4 bg-white/[0.02] border-b border-white/5 flex justify-between items-center">
        <h3 class="text-sm font-bold text-white">Pod Inventory</h3>
        <span class="text-[10px] text-slate-500">{{ pods.length }} active pods</span>
      </div>
      <table class="w-full text-left">
        <thead class="text-[10px] font-black uppercase tracking-widest text-slate-500">
          <tr>
            <th class="p-4">Name</th>
            <th class="p-4">Namespace</th>
            <th class="p-4">Status</th>
            <th class="p-4">CPU</th>
            <th class="p-4">Mem</th>
            <th class="p-4">Age</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/5">
          <tr *ngFor="let pod of pods" class="hover:bg-white/[0.02] transition-colors group">
            <td class="p-4 text-xs font-bold text-slate-200">{{ pod.name }}</td>
            <td class="p-4 text-xs text-slate-400">{{ pod.namespace }}</td>
            <td class="p-4">
              <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase"
                    [ngClass]="{
                      'bg-emerald-500/10 text-emerald-400': pod.status === 'Running',
                      'bg-amber-500/10 text-amber-400': pod.status === 'Pending',
                      'bg-rose-500/10 text-rose-400': pod.status === 'Failed'
                    }">
                {{ pod.status }}
              </span>
            </td>
            <td class="p-4 text-xs font-mono text-sky-400">{{ pod.cpu }}</td>
            <td class="p-4 text-xs font-mono text-indigo-400">{{ pod.memory }}</td>
            <td class="p-4 text-xs text-slate-500">{{ pod.age }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  `
})
export class PodInventoryComponent {
    @Input() pods: PodInfo[] = [];
}
