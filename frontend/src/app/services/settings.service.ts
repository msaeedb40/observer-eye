import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class SettingsService {
    private readonly middlewareUrl = 'http://localhost:8400/api/v1/backend';

    // Signals for Global State
    private readonly aiEnabledSignal = signal<boolean>(true);
    private readonly retentionDaysSignal = signal<number>(30);
    private readonly featureFlagsSignal = signal<any[]>([]);

    // Public Signals
    readonly aiEnabled = this.aiEnabledSignal.asReadonly();
    readonly retentionDays = this.retentionDaysSignal.asReadonly();
    readonly featureFlags = this.featureFlagsSignal.asReadonly();

    constructor(private http: HttpClient) { }

    /**
     * Fetch all settings for a specific category.
     */
    getSettingsByCategory(category: string): Observable<any[]> {
        return this.http.get<any>(`${this.middlewareUrl}/settings/setting/by_category/`).pipe(
            map(response => response[category] || [])
        );
    }

    /**
     * Update a specific setting by key.
     */
    updateSetting(id: number, value: any): Observable<any> {
        return this.http.patch(`${this.middlewareUrl}/settings/setting/${id}/`, { value });
    }

    /**
     * Get workspace settings (retention, ai_enabled, etc).
     */
    getWorkspaceSettings(slug: string = 'default'): Observable<any> {
        return this.http.get(`${this.middlewareUrl}/settings/workspace-settings/${slug}/`).pipe(
            tap((settings: any) => {
                this.aiEnabledSignal.set(settings.ai_enabled);
                this.retentionDaysSignal.set(settings.retention_days);
            })
        );
    }

    /**
     * Update workspace settings.
     */
    updateWorkspaceSettings(slug: string, data: any): Observable<any> {
        return this.http.patch(`${this.middlewareUrl}/settings/workspace-settings/${slug}/`, data).pipe(
            tap((settings: any) => {
                if (settings.ai_enabled !== undefined) this.aiEnabledSignal.set(settings.ai_enabled);
                if (settings.retention_days !== undefined) this.retentionDaysSignal.set(settings.retention_days);
            })
        );
    }

    /**
     * Get feature flags.
     */
    getFeatureFlags(): Observable<any[]> {
        return this.http.get<any[]>(`${this.middlewareUrl}/settings/feature-flag/`).pipe(
            tap(flags => this.featureFlagsSignal.set(flags))
        );
    }

    /**
     * Toggle feature flag.
     */
    toggleFeatureFlag(id: number): Observable<any> {
        return this.http.post(`${this.middlewareUrl}/settings/feature-flag/${id}/toggle/`, {}).pipe(
            tap(() => {
                // Refresh flags after toggle
                this.getFeatureFlags().subscribe();
            })
        );
    }
}
