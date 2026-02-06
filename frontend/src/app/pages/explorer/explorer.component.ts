import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
   selector: 'app-explorer',
   standalone: true,
   imports: [CommonModule, FormsModule],
   template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Data Explorer</h1>
        <p class="text-slate-400">Ad-hoc query builder for metrics, logs, and traces</p>
      </header>

      <div class="glass-panel p-0 overflow-hidden mb-8">
         <div class="p-4 bg-slate-900 border-b border-white/5 flex gap-4">
            <select class="form-select bg-slate-800 border-white/10 rounded text-sm text-slate-300 focus:ring-indigo-500" [(ngModel)]="selectedSource">
               <option value="metrics">Metrics (PromQL)</option>
               <option value="logs">Logs (LogQL)</option>
               <option value="traces">Traces (TraceQL)</option>
               <option value="sql">SQL Analytics</option>
            </select>
            <div class="flex-1 relative">
               <input type="text" 
                      class="w-full bg-slate-950 border border-white/10 rounded px-4 py-2 text-sm text-white font-mono focus:outline-none focus:border-indigo-500 transition-colors"
                      placeholder="Enter your query here... (e.g. rate(http_requests_total[5m]))"
                      [(ngModel)]="query">
               <div class="absolute right-2 top-1.5 text-xs text-slate-600 font-mono">CMD+ENTER</div>
            </div>
            <button class="btn-primary" (click)="executeQuery()">Run Query</button>
         </div>
      </div>

      <div *ngIf="results.length > 0" class="glass-panel overflow-hidden">
        <div class="p-4 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
           <div class="flex gap-4">
              <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">{{results.length}} results found</span>
              <span class="text-xs font-bold text-emerald-400 uppercase tracking-widest">0.124s execution time</span>
           </div>
           <div class="flex gap-2">
              <button class="text-xs font-bold text-slate-500 hover:text-white transition-colors uppercase">CSV</button>
              <button class="text-xs font-bold text-slate-500 hover:text-white transition-colors uppercase">JSON</button>
           </div>
        </div>
        <div class="overflow-x-auto">
           <table class="w-full text-left text-sm text-slate-400">
              <thead class="text-xs text-slate-500 uppercase bg-slate-900/50">
                 <tr>
                    <th *ngFor="let col of columns" class="px-6 py-3 font-bold tracking-wider">{{col}}</th>
                 </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                 <tr *ngFor="let row of results" class="hover:bg-white/[0.02] transition-colors">
                    <td *ngFor="let col of columns" class="px-6 py-3 font-mono text-slate-300 whitespace-nowrap">
                       {{row[col]}}
                    </td>
                 </tr>
              </tbody>
           </table>
        </div>
      </div>

      <div *ngIf="results.length === 0" class="flex flex-col items-center justify-center py-20 opacity-50">
         <div class="text-6xl mb-4">🔍</div>
         <h3 class="font-bold text-xl text-slate-400">No data requested</h3>
         <p class="text-slate-600">Enter a query above to explore your telemetry data.</p>
      </div>
    </div>
  `,
   styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class ExplorerComponent implements OnInit {
   selectedSource = 'metrics';
   query = '';
   columns: string[] = [];
   results: any[] = [];

   constructor(private apiService: ApiService) { }

   ngOnInit(): void { }

   executeQuery() {
      if (!this.query) return;

      if (this.selectedSource === 'metrics') {
         this.apiService.getMetrics(this.query).subscribe(data => {
            this.results = data;
            if (data.length > 0) {
               this.columns = Object.keys(data[0]);
            }
         });
      } else if (this.selectedSource === 'logs') {
         this.apiService.getLogs(undefined, this.query).subscribe(data => {
            this.results = data;
            if (data.length > 0) {
               this.columns = Object.keys(data[0]);
            }
         });
      }
   }
}
