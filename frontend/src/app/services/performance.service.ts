import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class PerformanceService {
    private readonly middlewareUrl = 'http://localhost:8400/api/v1';

    constructor(private http: HttpClient) { }

    // Network Performance
    getNetworkSummary(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/network/summary`);
    }

    getNetworkConnections(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/network/connections`);
    }

    // Traffic Performance
    getTrafficMetrics(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/traffic/metrics`);
    }

    getTrafficAnalysis(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/traffic/analysis`);
    }

    // Security Performance
    getSecurityStats(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/security/stats`);
    }

    getSecurityThreats(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/security/threats`);
    }

    // Identity Performance
    getIdentityMetrics(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/identity/metrics`);
    }

    getIdentitySessions(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/identity/sessions`);
    }

    // Analytics (Insights)
    getHealthScore(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/analytics/health-score`);
    }

    getAnomalies(metricName: string): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/analytics/anomalies?name=${metricName}`);
    }

    // Cloud Performance
    getCloudMetrics(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/cloud/metrics`);
    }

    getCloudCosts(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/cloud/costs`);
    }
}
