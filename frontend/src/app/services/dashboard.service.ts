import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DashboardStats {
    health_score: number;
    active_users: number;
    request_rate: number;
    error_rate: number;
    critical_anomalies: CriticalAnomaly[];
}

export interface CriticalAnomaly {
    title: string;
    timestamp: string;
    source: string;
}

@Injectable({
    providedIn: 'root'
})
export class DashboardService {
    // Access Backend via Middleware Proxy
    private readonly apiUrl = 'http://localhost:8400/api/v1/backend/analytics/stats';

    constructor(private http: HttpClient) { }

    getDashboardStats(): Observable<DashboardStats> {
        return this.http.get<DashboardStats>(this.apiUrl);
    }
}
