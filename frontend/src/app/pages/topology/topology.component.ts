import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TopologyGraphComponent, TopologyNode, TopologyLink } from '../../components/topology-graph/topology-graph.component';
import { TopologyService } from '../../services/topology.service';

@Component({
  selector: 'app-topology',
  standalone: true,
  imports: [CommonModule, TopologyGraphComponent],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Topology Explorer</h1>
        <p class="text-slate-400">Interactive dependency mapping and entity relationships</p>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div class="lg:col-span-3">
          <div class="glass-panel p-6 min-h-[650px] relative overflow-hidden flex flex-col">
            <div class="absolute inset-0 opacity-10 pointer-events-none" 
                 style="background-image: radial-gradient(circle at 2px 2px, var(--accent-primary) 1px, transparent 0); background-size: 24px 24px;">
            </div>
            
            <div class="relative z-10 flex flex-col flex-1">
              <div class="flex justify-between items-center mb-6">
                <div class="flex gap-4">
                  <span class="flex items-center gap-2 text-xs font-bold text-slate-400">
                    <span class="w-3 h-3 rounded-full bg-sky-400 shadow-[0_0_8px_rgba(56,189,248,0.5)]"></span> Service
                  </span>
                  <span class="flex items-center gap-2 text-xs font-bold text-slate-400">
                    <span class="w-3 h-3 rounded-full bg-indigo-400 shadow-[0_0_8px_rgba(129,140,248,0.5)]"></span> Database
                  </span>
                  <span class="flex items-center gap-2 text-xs font-bold text-slate-400">
                    <span class="w-3 h-3 rounded-full bg-pink-400 shadow-[0_0_8px_rgba(244,114,182,0.5)]"></span> External
                  </span>
                </div>
                <button (click)="loadTopology()" class="btn-premium py-2 text-sm">Refresh View</button>
              </div>

              <div class="flex-1 min-h-[500px] bg-slate-900/40 rounded-2xl border border-slate-800/50 relative backdrop-blur-sm overflow-hidden">
                <app-topology-graph 
                  [nodes]="nodes" 
                  [links]="links"
                  (nodeSelected)="onNodeSelected($event)">
                </app-topology-graph>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar Details -->
        <div class="space-y-6">
          <div class="glass-panel p-6 min-h-[400px]">
            <h3 class="text-lg font-bold text-white mb-6 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-sky-400"></span>
              Entity Details
            </h3>

            <div *ngIf="selectedNode; else noSelection" class="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
              <div class="p-4 bg-white/5 rounded-xl border border-white/5">
                <div class="text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-1">{{selectedNode.type}}</div>
                <div class="text-xl font-bold text-white">{{selectedNode.name}}</div>
                <div class="flex items-center gap-2 mt-2">
                  <span class="w-2 h-2 rounded-full" [ngClass]="getStatusClass(selectedNode.status || 'unknown')"></span>
                  <span class="text-xs font-bold uppercase" [ngClass]="getStatusTextClass(selectedNode.status || 'unknown')">{{selectedNode.status}}</span>
                </div>
              </div>

              <div class="space-y-4">
                <div *ngIf="entityDetails?.properties" class="space-y-2">
                  <div class="text-[10px] text-slate-500 font-bold uppercase">Properties</div>
                  <div class="grid grid-cols-2 gap-2">
                    <div *ngFor="let prop of entityDetails.properties | keyvalue" class="p-2 bg-slate-900/50 rounded-lg border border-white/[0.02]">
                      <div class="text-[8px] text-slate-600 font-bold uppercase">{{prop.key}}</div>
                      <div class="text-xs text-slate-300">{{prop.value}}</div>
                    </div>
                  </div>
                </div>

                <div *ngIf="entityDetails?.tags?.length" class="space-y-2">
                  <div class="text-[10px] text-slate-500 font-bold uppercase">Tags</div>
                  <div class="flex flex-wrap gap-2">
                    <span *ngFor="let tag of entityDetails.tags" class="px-2 py-0.5 bg-sky-500/10 text-sky-400 text-[10px] font-bold rounded-lg border border-sky-500/20">
                      {{tag}}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <ng-template #noSelection>
              <div class="flex flex-col items-center justify-center h-[300px] text-center">
                <div class="text-4xl mb-4 opacity-20">🖱️</div>
                <p class="text-slate-500 text-sm">Select an entity to view detailed relationships and metrics.</p>
              </div>
            </ng-template>
          </div>

          <div class="glass-panel p-6 bg-gradient-to-br from-indigo-500/5 to-transparent border-indigo-500/10">
             <h4 class="text-xs font-bold text-indigo-400 uppercase tracking-widest mb-2">Grail Engine</h4>
             <p class="text-[10px] text-slate-500 leading-relaxed">
               Dynamic graph mapping automatically discovers service dependencies across your distributed architecture.
             </p>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
    .animate-in { animation: animateIn 0.3s ease-out; }
    @keyframes animateIn {
      from { opacity: 0; transform: translateX(20px); }
      to { opacity: 1; transform: translateX(0); }
    }
  `]
})
export class TopologyComponent implements OnInit {
  nodes: TopologyNode[] = [];
  links: TopologyLink[] = [];
  selectedNode: TopologyNode | null = null;
  entityDetails: any = null;

  constructor(private topologyService: TopologyService) { }

  ngOnInit(): void {
    this.loadTopology();
  }

  loadTopology(): void {
    this.topologyService.getTopology().subscribe({
      next: (data) => {
        this.nodes = data.nodes;
        this.links = data.links;
      },
      error: (err) => console.error('Failed to load topology:', err)
    });
  }

  onNodeSelected(node: TopologyNode): void {
    this.selectedNode = node;
    this.topologyService.getEntityDetails(node.id).subscribe({
      next: (details) => this.entityDetails = details,
      error: (err) => console.error('Failed to load entity details:', err)
    });
  }

  getStatusClass(status: string): string {
    switch (status) {
      case 'healthy': return 'bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.5)]';
      case 'warning': return 'bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.5)]';
      case 'critical': return 'bg-rose-400 shadow-[0_0_8px_rgba(251,113,133,0.5)]';
      default: return 'bg-slate-400';
    }
  }

  getStatusTextClass(status: string): string {
    switch (status) {
      case 'healthy': return 'text-emerald-400';
      case 'warning': return 'text-amber-400';
      case 'critical': return 'text-rose-400';
      default: return 'text-slate-400';
    }
  }
}
