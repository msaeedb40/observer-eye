import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { ReliabilityMetrics } from '../components/reliability-metrics.component';

@Injectable({
    providedIn: 'root'
})
export class ReliabilityService {
    private readonly API_URL = `${environment.apiUrl}/notification/alerts/reliability/`;

    constructor(private http: HttpClient) { }

    getMetrics(): Observable<ReliabilityMetrics> {
        return this.http.get<ReliabilityMetrics>(this.API_URL);
    }

    getIncidents(): Observable<any[]> {
        return this.http.get<any[]>(`${environment.apiUrl}/notification/alerts/history/`);
    }
}
