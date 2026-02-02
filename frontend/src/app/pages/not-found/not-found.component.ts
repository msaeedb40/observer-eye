import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
    selector: 'app-not-found',
    standalone: true,
    imports: [CommonModule, RouterModule],
    template: `
    <div class="not-found">
      <h1>404</h1>
      <p>Page not found</p>
      <a routerLink="/dashboard">Go to Dashboard</a>
    </div>
  `,
    styles: [`
    .not-found { text-align: center; padding: 4rem; }
    .not-found h1 { font-size: 6rem; color: #667eea; margin-bottom: 1rem; }
    .not-found p { font-size: 1.5rem; color: #666; margin-bottom: 2rem; }
    .not-found a { color: #667eea; font-weight: 600; }
  `]
})
export class NotFoundComponent { }
