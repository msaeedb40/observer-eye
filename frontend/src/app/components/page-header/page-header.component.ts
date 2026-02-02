import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Breadcrumb {
    label: string;
    link?: string;
}

@Component({
    selector: 'app-page-header',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="page-header">
      <div class="header-content">
        <div class="breadcrumbs" *ngIf="breadcrumbs.length">
          <span *ngFor="let crumb of breadcrumbs; let last = last">
            <a *ngIf="crumb.link; else textCrumb" [href]="crumb.link">{{ crumb.label }}</a>
            <ng-template #textCrumb>{{ crumb.label }}</ng-template>
            <span *ngIf="!last" class="separator">/</span>
          </span>
        </div>
        <h1>{{ title }}</h1>
        <p *ngIf="subtitle">{{ subtitle }}</p>
      </div>
      
      <div class="header-actions">
        <ng-content></ng-content>
      </div>
    </div>
  `,
    styles: [`
    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 24px;
      padding-bottom: 20px;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .breadcrumbs {
      font-size: 13px;
      color: rgba(255,255,255,0.5);
      margin-bottom: 8px;
    }
    
    .breadcrumbs a {
      color: #667eea;
      text-decoration: none;
    }
    
    .breadcrumbs a:hover {
      text-decoration: underline;
    }
    
    .separator {
      margin: 0 8px;
      color: rgba(255,255,255,0.3);
    }
    
    h1 {
      margin: 0;
      font-size: 28px;
      font-weight: 700;
      color: white;
    }
    
    p {
      margin: 8px 0 0;
      color: rgba(255,255,255,0.6);
      font-size: 14px;
    }
    
    .header-actions {
      display: flex;
      gap: 12px;
    }
  `]
})
export class PageHeaderComponent {
    @Input() title = '';
    @Input() subtitle = '';
    @Input() breadcrumbs: Breadcrumb[] = [];
}
