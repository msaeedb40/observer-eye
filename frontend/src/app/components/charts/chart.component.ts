import { Component, Input, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective, NgChartsModule } from 'ng2-charts';
import { ChartConfiguration, ChartOptions, ChartType } from 'chart.js';

@Component({
  selector: 'app-chart',
  standalone: true,
  imports: [CommonModule, NgChartsModule],
  template: `
    <div class="chart-container" [style.height]="formatHeight(height)">
      <canvas
        baseChart
        [data]="chartData"
        [options]="finalOptions"
        [type]="chartType"
      >
      </canvas>
    </div>
  `,
  styles: [`
    .chart-container {
      position: relative;
      width: 100%;
    }
  `]
})
export class ChartComponent implements OnInit, OnDestroy {
  @Input() height: number | string = 250;
  @Input() chartType: ChartType = 'line';

  @Input() chartData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [35, 45, 30, 55, 45, 60, 50],
        label: 'System Load',
        borderColor: '#38bdf8',
        backgroundColor: 'rgba(56, 189, 248, 0.1)',
        fill: true,
        tension: 0.4
      }
    ],
    labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30']
  };

  @Input() chartOptions: ChartOptions = {};

  finalOptions: ChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          color: '#94a3b8',
          font: { family: 'Inter', size: 10, weight: 'bold' },
          usePointStyle: true,
          padding: 20
        }
      },
      tooltip: {
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        titleFont: { family: 'Inter', size: 12 },
        bodyFont: { family: 'Inter', size: 12 },
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
        displayColors: true
      }
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 } }
      },
      y: {
        grid: { color: 'rgba(255, 255, 255, 0.03)' },
        ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 } }
      }
    }
  };

  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;

  ngOnInit(): void {
    // Merge provided options with defaults
    this.finalOptions = { ...this.finalOptions, ...this.chartOptions };
  }

  ngOnDestroy(): void { }

  formatHeight(h: number | string): string {
    return typeof h === 'number' ? `${h}px` : h;
  }

  public update(): void {
    this.chart?.update();
  }
}
