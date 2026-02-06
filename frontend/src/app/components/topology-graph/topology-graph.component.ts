import { Component, OnInit, OnChanges, Input, Output, EventEmitter, ElementRef, ViewChild, SimpleChanges, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import * as d3 from 'd3';

export interface TopologyNode extends d3.SimulationNodeDatum {
    id: string;
    name: string;
    type: string;
    status?: 'healthy' | 'warning' | 'critical' | 'unknown';
    icon?: string;
}

export interface TopologyLink extends d3.SimulationLinkDatum<TopologyNode> {
    source: string | TopologyNode;
    target: string | TopologyNode;
    type?: string;
    value?: number;
    status?: 'healthy' | 'warning' | 'critical';
}

@Component({
    selector: 'app-topology-graph',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="topology-container" #container>
      <svg #svg></svg>
      <div class="controls">
        <button (click)="zoomIn()" title="Zoom In">+</button>
        <button (click)="zoomOut()" title="Zoom Out">-</button>
        <button (click)="resetZoom()" title="Reset Zoom">⟲</button>
      </div>
      <div class="legend">
        <div class="legend-item"><span class="dot healthy"></span> Healthy</div>
        <div class="legend-item"><span class="dot warning"></span> Warning</div>
        <div class="legend-item"><span class="dot critical"></span> Critical</div>
      </div>
    </div>
  `,
    styles: [`
    .topology-container {
      width: 100%;
      height: 100%;
      position: relative;
      background: #0f172a;
      border-radius: 12px;
      overflow: hidden;
    }
    svg {
      width: 100%;
      height: 100%;
    }
    .node circle {
      stroke: #1e293b;
      stroke-width: 2px;
      transition: all 0.3s ease;
    }
    .node text {
      font-family: 'Inter', sans-serif;
      font-size: 12px;
      fill: #e2e8f0;
      pointer-events: none;
      text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }
    .link {
      stroke-opacity: 0.6;
      stroke-width: 1.5px;
      fill: none;
      transition: all 0.3s ease;
    }
    .link.healthy { stroke: #10b981; }
    .link.warning { stroke: #f59e0b; }
    .link.critical { stroke: #ef4444; }
    
    .controls {
      position: absolute;
      top: 10px;
      right: 10px;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .controls button {
      width: 32px;
      height: 32px;
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid #334155;
      color: #f8fafc;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }
    .controls button:hover {
      background: #334155;
    }
    
    .legend {
      position: absolute;
      bottom: 10px;
      left: 10px;
      background: rgba(15, 23, 42, 0.8);
      padding: 8px 12px;
      border-radius: 8px;
      border: 1px solid #1e293b;
      display: flex;
      gap: 15px;
      font-size: 11px;
      color: #94a3b8;
    }
    .legend-item { display: flex; align-items: center; gap: 5px; }
    .dot { width: 8px; height: 8px; border-radius: 50%; }
    .dot.healthy { background: #10b981; box-shadow: 0 0 8px #10b981; }
    .dot.warning { background: #f59e0b; box-shadow: 0 0 8px #f59e0b; }
    .dot.critical { background: #ef4444; box-shadow: 0 0 8px #ef4444; }
  `]
})
export class TopologyGraphComponent implements OnInit, OnChanges {
    @Input() nodes: TopologyNode[] = [];
    @Input() links: TopologyLink[] = [];
    @Output() nodeSelected = new EventEmitter<TopologyNode>();

    @ViewChild('svg', { static: true }) svgElement!: ElementRef<SVGSVGElement>;
    @ViewChild('container', { static: true }) containerElement!: ElementRef<HTMLDivElement>;

    private svg!: d3.Selection<SVGSVGElement, unknown, null, undefined>;
    private g!: d3.Selection<SVGGElement, unknown, null, undefined>;
    private zoom!: d3.ZoomBehavior<SVGSVGElement, unknown>;
    private simulation!: d3.Simulation<TopologyNode, TopologyLink>;

    constructor() { }

    ngOnInit(): void {
        this.initGraph();
    }

    ngOnChanges(changes: SimpleChanges): void {
        if (this.simulation && (changes['nodes'] || changes['links'])) {
            this.updateGraph();
        }
    }

    @HostListener('window:resize')
    onResize(): void {
        if (this.svg) {
            const width = this.containerElement.nativeElement.clientWidth;
            const height = this.containerElement.nativeElement.clientHeight;
            this.simulation.force('center', d3.forceCenter(width / 2, height / 2));
            this.simulation.alpha(0.3).restart();
        }
    }

    private initGraph(): void {
        const width = this.containerElement.nativeElement.clientWidth;
        const height = this.containerElement.nativeElement.clientHeight;

        this.svg = d3.select(this.svgElement.nativeElement);
        this.g = this.svg.append('g');

        this.zoom = d3.zoom<SVGSVGElement, unknown>()
            .scaleExtent([0.1, 8])
            .on('zoom', (event: d3.D3ZoomEvent<SVGSVGElement, unknown>) => {
                this.g.attr('transform', event.transform.toString());
            });

        this.svg.call(this.zoom);

        this.simulation = d3.forceSimulation<TopologyNode>(this.nodes)
            .force('link', d3.forceLink<TopologyNode, TopologyLink>(this.links).id((d: any) => d.id).distance(150))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(50));

        this.updateGraph();
    }

    private updateGraph(): void {
        // Clear old elements
        this.g.selectAll('*').remove();

        // Define arrow markers
        this.g.append('defs').append('marker')
            .attr('id', 'arrowhead')
            .attr('viewBox', '-0 -5 10 10')
            .attr('refX', 20)
            .attr('refY', 0)
            .attr('orient', 'auto')
            .attr('markerWidth', 6)
            .attr('markerHeight', 6)
            .attr('xoverflow', 'visible')
            .append('svg:path')
            .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
            .attr('fill', '#475569')
            .style('stroke', 'none');

        // Draw links
        const link = this.g.append('g')
            .attr('class', 'links')
            .selectAll('line')
            .data(this.links)
            .enter().append('line')
            .attr('class', (d: TopologyLink) => `link ${d.status || 'healthy'}`)
            .attr('marker-end', 'url(#arrowhead)');

        // Draw nodes
        const node = this.g.append('g')
            .attr('class', 'nodes')
            .selectAll('g')
            .data(this.nodes)
            .enter().append('g')
            .attr('class', 'node')
            .call(d3.drag<SVGGElement, TopologyNode>()
                .on('start', this.dragstarted.bind(this))
                .on('drag', this.dragged.bind(this))
                .on('end', this.dragended.bind(this)))
            .on('click', (event: MouseEvent, d: TopologyNode) => this.nodeSelected.emit(d));

        // Node circles
        node.append('circle')
            .attr('r', 16)
            .attr('fill', (d: TopologyNode) => this.getStatusColor(d.status || 'healthy'))
            .style('filter', (d: TopologyNode) => `drop-shadow(0 0 5px ${this.getStatusColor(d.status || 'healthy')})`);

        // Node icons (simplified text for now)
        node.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', '.35em')
            .style('font-size', '10px')
            .style('fill', '#fff')
            .text((d: TopologyNode) => d.type.charAt(0).toUpperCase());

        // Node labels
        node.append('text')
            .attr('dx', 22)
            .attr('dy', '.35em')
            .text((d: TopologyNode) => d.name);

        this.simulation.nodes(this.nodes);
        this.simulation.force<d3.ForceLink<TopologyNode, TopologyLink>>('link')!.links(this.links);

        this.simulation.on('tick', () => {
            link
                .attr('x1', (d: any) => d.source.x)
                .attr('y1', (d: any) => d.source.y)
                .attr('x2', (d: any) => d.target.x)
                .attr('y2', (d: any) => d.target.y);

            node.attr('transform', (d: any) => `translate(${d.x},${d.y})`);
        });

        this.simulation.alpha(1).restart();
    }

    private dragstarted(event: any, d: any): void {
        if (!event.active) this.simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    private dragged(event: any, d: any): void {
        d.fx = event.x;
        d.fy = event.y;
    }

    private dragended(event: any, d: any): void {
        if (!event.active) this.simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    private getStatusColor(status: string): string {
        switch (status) {
            case 'healthy': return '#10b981';
            case 'warning': return '#f59e0b';
            case 'critical': return '#ef4444';
            default: return '#94a3b8';
        }
    }

    // Public control methods
    zoomIn(): void {
        this.svg.transition().call(this.zoom.scaleBy, 1.5);
    }

    zoomOut(): void {
        this.svg.transition().call(this.zoom.scaleBy, 0.6);
    }

    resetZoom(): void {
        this.svg.transition().call(this.zoom.transform, d3.zoomIdentity);
    }
}
