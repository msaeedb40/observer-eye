import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { TopologyNode, TopologyLink } from '../components/topology-graph/topology-graph.component';

export interface TopologyData {
    nodes: TopologyNode[];
    links: TopologyLink[];
}

@Injectable({
    providedIn: 'root'
})
export class TopologyService {
    private readonly baseUrl = 'http://localhost:8400/api/v1';

    constructor(private http: HttpClient) { }

    getTopology(): Observable<TopologyData> {
        return this.http.get<TopologyData>(`${this.baseUrl}/grail/topology`);
    }

    getEntityDetails(id: string): Observable<any> {
        return this.http.get<any>(`${this.baseUrl}/backend/grailobserver/entities/${id}/`);
    }
}
