import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private readonly middlewareUrl = 'http://localhost:8400/api/v1';

    constructor(private http: HttpClient) { }

    private getHeaders(): HttpHeaders {
        return new HttpHeaders({
            'Content-Type': 'application/json'
        });
    }

    // ========================
    // TELEMETRY (4 Pillars)
    // ========================

    // METRICS
    getMetrics(name?: string): Observable<any> {
        const params = name ? `?name=${name}` : '';
        return this.http.get(`${this.middlewareUrl}/telemetry/metrics${params}`);
    }

    recordMetrics(metrics: any[]): Observable<any> {
        return this.http.post(`${this.middlewareUrl}/telemetry/metrics`, metrics);
    }

    // EVENTS
    getEvents(source?: string): Observable<any> {
        const params = source ? `?source=${source}` : '';
        return this.http.get(`${this.middlewareUrl}/telemetry/events${params}`);
    }

    recordEvents(events: any[]): Observable<any> {
        return this.http.post(`${this.middlewareUrl}/telemetry/events`, events);
    }

    // LOGS
    getLogs(level?: string, source?: string): Observable<any> {
        const params = new URLSearchParams();
        if (level) params.append('level', level);
        if (source) params.append('source', source);
        const queryString = params.toString() ? `?${params.toString()}` : '';
        return this.http.get(`${this.middlewareUrl}/telemetry/logs${queryString}`);
    }

    recordLogs(logs: any[]): Observable<any> {
        return this.http.post(`${this.middlewareUrl}/telemetry/logs`, logs);
    }

    // TRACES
    getTraces(limit: number = 100): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/telemetry/traces?limit=${limit}`);
    }

    getTrace(traceId: string): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/telemetry/traces/${traceId}`);
    }

    recordTraces(spans: any[]): Observable<any> {
        return this.http.post(`${this.middlewareUrl}/telemetry/traces`, spans);
    }

    // ========================
    // PERFORMANCE
    // ========================

    getPerformanceMetrics(source?: string, limit: number = 100): Observable<any> {
        const params = new URLSearchParams();
        if (source) params.append('source', source);
        params.append('limit', limit.toString());
        return this.http.get(`${this.middlewareUrl}/performance/metrics?${params.toString()}`);
    }

    getPerformanceSummary(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/performance/summary`);
    }

    // ========================
    // ERRORS
    // ========================

    getErrorLogs(severity?: string, source?: string, limit: number = 100): Observable<any> {
        const params = new URLSearchParams();
        if (severity) params.append('severity', severity);
        if (source) params.append('source', source);
        params.append('limit', limit.toString());
        return this.http.get(`${this.middlewareUrl}/errors/logs?${params.toString()}`);
    }

    getErrorStats(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/errors/stats`);
    }

    // ========================
    // CACHE
    // ========================

    getCacheStats(): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/cache/stats`);
    }

    // ========================
    // HEALTH
    // ========================

    healthCheck(): Observable<any> {
        return this.http.get('http://localhost:8400/health');
    }

    readinessCheck(): Observable<any> {
        return this.http.get('http://localhost:8400/ready');
    }
}
