import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface TableColumn {
    key: string;
    label: string;
    sortable?: boolean;
    width?: string;
}

export interface TableRow {
    [key: string]: any;
}

@Component({
    selector: 'app-data-table',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="data-table-container">
      <div class="table-header" *ngIf="title || searchable">
        <h3 *ngIf="title">{{ title }}</h3>
        <input *ngIf="searchable" 
               type="text" 
               placeholder="Search..." 
               class="search-input"
               (input)="onSearch($event)">
      </div>
      
      <table class="data-table">
        <thead>
          <tr>
            <th *ngFor="let col of columns" 
                [style.width]="col.width"
                [class.sortable]="col.sortable"
                (click)="col.sortable && onSort(col.key)">
              {{ col.label }}
              <span *ngIf="col.sortable && sortKey === col.key" class="sort-indicator">
                {{ sortDirection === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let row of data; let i = index" 
              (click)="rowClick.emit(row)"
              class="clickable">
            <td *ngFor="let col of columns">
              <ng-container *ngIf="col.key === 'status'; else defaultCell">
                <span class="status-badge" [class]="'status-' + row[col.key]">
                  {{ row[col.key] }}
                </span>
              </ng-container>
              <ng-template #defaultCell>
                {{ row[col.key] }}
              </ng-template>
            </td>
          </tr>
          <tr *ngIf="data.length === 0">
            <td [attr.colspan]="columns.length" class="empty-state">
              {{ emptyMessage }}
            </td>
          </tr>
        </tbody>
      </table>
      
      <div class="table-footer" *ngIf="pagination">
        <span>Showing {{ data.length }} items</span>
        <div class="pagination">
          <button (click)="prevPage.emit()" [disabled]="currentPage <= 1">←</button>
          <span>Page {{ currentPage }}</span>
          <button (click)="nextPage.emit()">→</button>
        </div>
      </div>
    </div>
  `,
    styles: [`
    .data-table-container {
      background: rgba(255,255,255,0.05);
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid rgba(255,255,255,0.1);
    }
    
    .table-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 20px;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .table-header h3 {
      margin: 0;
      color: white;
      font-size: 16px;
    }
    
    .search-input {
      padding: 8px 16px;
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 8px;
      background: rgba(255,255,255,0.05);
      color: white;
      width: 250px;
    }
    
    .search-input::placeholder { color: rgba(255,255,255,0.4); }
    
    .data-table {
      width: 100%;
      border-collapse: collapse;
    }
    
    .data-table th {
      text-align: left;
      padding: 12px 16px;
      color: rgba(255,255,255,0.7);
      font-weight: 500;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      background: rgba(0,0,0,0.2);
    }
    
    .data-table th.sortable { cursor: pointer; }
    .data-table th.sortable:hover { color: white; }
    
    .sort-indicator { margin-left: 4px; }
    
    .data-table td {
      padding: 14px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      color: rgba(255,255,255,0.9);
      font-size: 14px;
    }
    
    .data-table tr.clickable { cursor: pointer; }
    .data-table tr.clickable:hover { background: rgba(255,255,255,0.05); }
    
    .status-badge {
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 500;
    }
    
    .status-success, .status-healthy { background: rgba(34,197,94,0.2); color: #22c55e; }
    .status-warning, .status-degraded { background: rgba(245,158,11,0.2); color: #f59e0b; }
    .status-error, .status-critical, .status-unhealthy { background: rgba(239,68,68,0.2); color: #ef4444; }
    .status-info, .status-pending { background: rgba(59,130,246,0.2); color: #3b82f6; }
    
    .empty-state {
      text-align: center;
      padding: 40px !important;
      color: rgba(255,255,255,0.5);
    }
    
    .table-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 20px;
      border-top: 1px solid rgba(255,255,255,0.1);
      color: rgba(255,255,255,0.6);
      font-size: 13px;
    }
    
    .pagination {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .pagination button {
      padding: 6px 12px;
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 6px;
      background: transparent;
      color: white;
      cursor: pointer;
    }
    
    .pagination button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  `]
})
export class DataTableComponent {
    @Input() columns: TableColumn[] = [];
    @Input() data: TableRow[] = [];
    @Input() title = '';
    @Input() searchable = false;
    @Input() pagination = false;
    @Input() currentPage = 1;
    @Input() emptyMessage = 'No data available';

    @Output() rowClick = new EventEmitter<TableRow>();
    @Output() search = new EventEmitter<string>();
    @Output() sort = new EventEmitter<{ key: string; direction: 'asc' | 'desc' }>();
    @Output() prevPage = new EventEmitter<void>();
    @Output() nextPage = new EventEmitter<void>();

    sortKey = '';
    sortDirection: 'asc' | 'desc' = 'asc';

    onSearch(event: Event) {
        const value = (event.target as HTMLInputElement).value;
        this.search.emit(value);
    }

    onSort(key: string) {
        if (this.sortKey === key) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortKey = key;
            this.sortDirection = 'asc';
        }
        this.sort.emit({ key: this.sortKey, direction: this.sortDirection });
    }
}
