import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-topology',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container page-transition">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold gradient-text mb-2">Topology Explorer</h1>
        <p class="text-slate-400">Interactive dependency mapping and entity relationships</p>
      </header>

      <div class="glass-panel p-8 min-h-[600px] relative overflow-hidden">
        <div class="absolute inset-0 opacity-10 pointer-events-none" 
             style="background-image: radial-gradient(circle at 2px 2px, var(--accent-primary) 1px, transparent 0); background-size: 24px 24px;">
        </div>
        
        <div class="relative z-10">
          <div class="flex justify-between items-center mb-6">
            <div class="flex gap-4">
              <span class="flex items-center gap-2 text-xs font-bold text-slate-400">
                <span class="w-3 h-3 rounded-full bg-sky-400 shadow-[0_0_8px_rgba(56,189,248,0.5)]"></span> Service
              </span>
              <span class="flex items-center gap-2 text-xs font-bold text-slate-400">
                <span class="w-3 h-3 rounded-full bg-indigo-400 shadow-[0_0_8px_rgba(129,140,248,0.5)]"></span> Database
              </span>
              <span class="flex items-center gap-2 text-xs font-bold text-slate-400">
                <span class="w-3 h-3 rounded-full bg-pink-400 shadow-[0_0_8px_rgba(244,114,182,0.5)]"></span> External API
              </span>
            </div>
            <button class="btn-premium py-2 text-sm">Refresh View</button>
          </div>

          <div class="h-[500px] bg-slate-900/40 rounded-2xl border border-slate-800/50 flex items-center justify-center backdrop-blur-sm">
            <!-- Topology visualization placeholder -->
            <div class="text-center">
              <div class="text-6xl mb-4 animate-pulse">🕸️</div>
              <p class="text-slate-500 font-medium">Grail Graph Engine Active</p>
              <p class="text-xs text-slate-600 mt-1">Found 42 entities and 156 relationships</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class TopologyComponent implements OnInit {
  ngOnInit(): void { }
}
