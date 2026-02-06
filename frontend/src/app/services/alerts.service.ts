import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

export interface Alert {
    id: string;
    title: string;
    description: string;
    severity: string;
    triggeredAt: string;
    service: string;
    icon: string;
    status: string;
}

@Injectable({
    providedIn: 'root'
})
export class AlertsService {
    private readonly middlewareUrl = 'http://localhost:8400/api/v1/notifications';

    // Signals for State Management
    private readonly activeAlertsSignal = signal<Alert[]>([]);
    private readonly alertHistorySignal = signal<Alert[]>([]);

    // Public Signals (Read-only)
    readonly activeAlerts = this.activeAlertsSignal.asReadonly();
    readonly alertHistory = this.alertHistorySignal.asReadonly();
    readonly activeAlertCount = computed(() => this.activeAlerts().length);

    constructor(private http: HttpClient) { }

    // ========================
    // ALERTS & HISTORY
    // ========================

    refreshActiveAlerts(): void {
        this.http.get<Alert[]>(`${this.middlewareUrl}/active`).subscribe({
            next: (alerts) => this.activeAlertsSignal.set(alerts),
            error: () => this.activeAlertsSignal.set([])
        });
    }

    refreshAlertHistory(): void {
        this.http.get<Alert[]>(`${this.middlewareUrl}/history`).subscribe({
            next: (history) => this.alertHistorySignal.set(history),
            error: () => this.alertHistorySignal.set([])
        });
    }

    getActiveAlerts(): Observable<Alert[]> {
        return this.http.get<Alert[]>(`${this.middlewareUrl}/active`).pipe(
            tap(alerts => this.activeAlertsSignal.set(alerts))
        );
    }

    getAlertHistory(): Observable<Alert[]> {
        return this.http.get<Alert[]>(`${this.middlewareUrl}/history`).pipe(
            tap(history => this.alertHistorySignal.set(history))
        );
    }

    // ========================
    // ALERT RULES CRUD
    // ========================

    getRules(): Observable<any[]> {
        return this.http.get<any[]>(`${this.middlewareUrl}/rules`);
    }

    createRule(rule: any): Observable<any> {
        return this.http.post(`${this.middlewareUrl}/rules`, rule);
    }

    updateRule(id: number | string, rule: any): Observable<any> {
        return this.http.put(`${this.middlewareUrl}/rules/${id}`, rule);
    }

    deleteRule(id: number | string): Observable<any> {
        return this.http.delete(`${this.middlewareUrl}/rules/${id}`);
    }

    // ========================
    // CHANNELS CRUD
    // ========================

    getChannels(): Observable<any[]> {
        return this.http.get<any[]>(`${this.middlewareUrl}/channels`);
    }

    createChannel(channel: any): Observable<any> {
        return this.http.post(`${this.middlewareUrl}/channels`, channel);
    }

    updateChannel(id: number | string, channel: any): Observable<any> {
        return this.http.put(`${this.middlewareUrl}/channels/${id}`, channel);
    }

    deleteChannel(id: number | string): Observable<any> {
        return this.http.delete(`${this.middlewareUrl}/channels/${id}`);
    }
}
