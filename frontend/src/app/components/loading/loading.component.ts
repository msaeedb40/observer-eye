import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-loading',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="loading-container" [class.overlay]="overlay" [class.inline]="!overlay">
      <div class="spinner" [style.width.px]="size" [style.height.px]="size"></div>
      <span *ngIf="message" class="loading-message">{{ message }}</span>
    </div>
  `,
    styles: [`
    .loading-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 16px;
    }
    
    .loading-container.overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0,0,0,0.7);
      z-index: 1000;
    }
    
    .loading-container.inline {
      padding: 40px;
    }
    
    .spinner {
      border: 3px solid rgba(255,255,255,0.1);
      border-top-color: #667eea;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    
    .loading-message {
      color: rgba(255,255,255,0.8);
      font-size: 14px;
    }
  `]
})
export class LoadingComponent {
    @Input() size = 40;
    @Input() message = '';
    @Input() overlay = false;
}
