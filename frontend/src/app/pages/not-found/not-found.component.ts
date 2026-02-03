import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-not-found',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="observer-container flex items-center justify-center min-h-[80vh] page-transition">
      <div class="glass-panel p-16 text-center max-w-lg relative overflow-hidden">
        <div class="absolute -top-24 -right-24 w-64 h-64 bg-sky-500/10 rounded-full blur-3xl"></div>
        <div class="absolute -bottom-24 -left-24 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl"></div>
        
        <h1 class="text-9xl font-black gradient-text mb-4 opacity-20">404</h1>
        <div class="relative z-10">
          <h2 class="text-3xl font-bold text-white mb-4">Space-Time Anomaly</h2>
          <p class="text-slate-400 mb-8 leading-relaxed">
            The entity you are looking for has either been garbage-collected or never existed in this observability mesh.
          </p>
          <a routerLink="/dashboard" class="btn-premium no-underline inline-block">
            Return to Command Center
          </a>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class NotFoundComponent { }
