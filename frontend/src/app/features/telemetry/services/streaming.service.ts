import { Injectable, OnDestroy } from '@angular/core';
import { Observable, Subject, BehaviorSubject, timer, EMPTY } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { retry, catchError, switchMap, takeUntil } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';

/**
 * Streaming message types for Observer-Eye real-time data.
 */
export interface StreamMessage<T = any> {
  type: 'metric' | 'log' | 'trace' | 'event' | 'alert' | 'system';
  data: T;
  timestamp: string;
}

export interface MetricStreamData {
  name: string;
  value: number;
  unit: string;
  source: string;
  labels: Record<string, string>;
}

export interface LogStreamData {
  level: string;
  message: string;
  source: string;
  trace_id?: string;
  span_id?: string;
}

export interface AlertStreamData {
  id: string;
  name: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  message: string;
  source: string;
  triggered_at: string;
}

export interface StreamConfig {
  filters?: Record<string, any>;
  limit?: number;
  since?: string;
}

/**
 * StreamingService provides real-time WebSocket connections to Observer-Eye middleware.
 * Supports metrics, logs, traces, events, and alerts streaming.
 */
@Injectable({
  providedIn: 'root'
})
export class StreamingService implements OnDestroy {
  private readonly WS_BASE_URL = environment.wsUrl || 'ws://localhost:8400/api/v1/stream';

  private metricsSocket$: WebSocketSubject<StreamMessage<MetricStreamData>> | null = null;
  private logsSocket$: WebSocketSubject<StreamMessage<LogStreamData>> | null = null;
  private alertsSocket$: WebSocketSubject<StreamMessage<AlertStreamData>> | null = null;

  private destroy$ = new Subject<void>();

  // Connection status
  private metricsConnected$ = new BehaviorSubject<boolean>(false);
  private logsConnected$ = new BehaviorSubject<boolean>(false);
  private alertsConnected$ = new BehaviorSubject<boolean>(false);

  constructor() { }

  ngOnDestroy(): void {
    this.disconnectAll();
    this.destroy$.next();
    this.destroy$.complete();
  }

  /**
   * Connect to metrics stream with optional filters.
   */
  connectToMetrics(config?: StreamConfig): Observable<StreamMessage<MetricStreamData>> {
    if (this.metricsSocket$) {
      return this.metricsSocket$.asObservable();
    }

    this.metricsSocket$ = webSocket<StreamMessage<MetricStreamData>>({
      url: `${this.WS_BASE_URL}/metrics`,
      openObserver: {
        next: () => {
          console.log('[StreamingService] Metrics WebSocket connected');
          this.metricsConnected$.next(true);
          if (config) {
            this.metricsSocket$?.next({ type: 'system', data: { action: 'subscribe', ...config } } as any);
          }
        }
      },
      closeObserver: {
        next: () => {
          console.log('[StreamingService] Metrics WebSocket disconnected');
          this.metricsConnected$.next(false);
        }
      }
    });

    return this.metricsSocket$.pipe(
      retry({ count: 5, delay: (error, retryCount) => timer(Math.min(1000 * Math.pow(2, retryCount), 30000)) }),
      catchError(err => {
        console.error('[StreamingService] Metrics stream error:', err);
        return EMPTY;
      }),
      takeUntil(this.destroy$)
    );
  }

  /**
   * Connect to logs stream with optional query filter.
   */
  connectToLogs(query?: string, config?: StreamConfig): Observable<StreamMessage<LogStreamData>> {
    if (this.logsSocket$) {
      return this.logsSocket$.asObservable();
    }

    this.logsSocket$ = webSocket<StreamMessage<LogStreamData>>({
      url: `${this.WS_BASE_URL}/logs`,
      openObserver: {
        next: () => {
          console.log('[StreamingService] Logs WebSocket connected');
          this.logsConnected$.next(true);
          if (query || config) {
            this.logsSocket$?.next({ type: 'system', data: { action: 'subscribe', query, ...config } } as any);
          }
        }
      },
      closeObserver: {
        next: () => {
          console.log('[StreamingService] Logs WebSocket disconnected');
          this.logsConnected$.next(false);
        }
      }
    });

    return this.logsSocket$.pipe(
      retry({ count: 5, delay: (error, retryCount) => timer(Math.min(1000 * Math.pow(2, retryCount), 30000)) }),
      catchError(err => {
        console.error('[StreamingService] Logs stream error:', err);
        return EMPTY;
      }),
      takeUntil(this.destroy$)
    );
  }

  /**
   * Connect to alerts stream for real-time notifications.
   */
  connectToAlerts(): Observable<StreamMessage<AlertStreamData>> {
    if (this.alertsSocket$) {
      return this.alertsSocket$.asObservable();
    }

    this.alertsSocket$ = webSocket<StreamMessage<AlertStreamData>>({
      url: `${this.WS_BASE_URL}/alerts`,
      openObserver: {
        next: () => {
          console.log('[StreamingService] Alerts WebSocket connected');
          this.alertsConnected$.next(true);
        }
      },
      closeObserver: {
        next: () => {
          console.log('[StreamingService] Alerts WebSocket disconnected');
          this.alertsConnected$.next(false);
        }
      }
    });

    return this.alertsSocket$.pipe(
      retry({ count: 5, delay: (error, retryCount) => timer(Math.min(1000 * Math.pow(2, retryCount), 30000)) }),
      catchError(err => {
        console.error('[StreamingService] Alerts stream error:', err);
        return EMPTY;
      }),
      takeUntil(this.destroy$)
    );
  }

  /**
   * Update subscription filters for metrics stream.
   */
  updateMetricsFilters(filters: Record<string, any>): void {
    if (this.metricsSocket$ && this.metricsConnected$.value) {
      this.metricsSocket$.next({ type: 'system', data: { action: 'filter', filters } } as any);
    }
  }

  /**
   * Update query for logs stream.
   */
  updateLogsQuery(query: string): void {
    if (this.logsSocket$ && this.logsConnected$.value) {
      this.logsSocket$.next({ type: 'system', data: { action: 'filter', query } } as any);
    }
  }

  /**
   * Disconnect metrics stream.
   */
  disconnectMetrics(): void {
    if (this.metricsSocket$) {
      this.metricsSocket$.complete();
      this.metricsSocket$ = null;
      this.metricsConnected$.next(false);
    }
  }

  /**
   * Disconnect logs stream.
   */
  disconnectLogs(): void {
    if (this.logsSocket$) {
      this.logsSocket$.complete();
      this.logsSocket$ = null;
      this.logsConnected$.next(false);
    }
  }

  /**
   * Disconnect alerts stream.
   */
  disconnectAlerts(): void {
    if (this.alertsSocket$) {
      this.alertsSocket$.complete();
      this.alertsSocket$ = null;
      this.alertsConnected$.next(false);
    }
  }

  /**
   * Disconnect all streams.
   */
  disconnectAll(): void {
    this.disconnectMetrics();
    this.disconnectLogs();
    this.disconnectAlerts();
  }

  /**
   * Get connection status observables.
   */
  get metricsConnectionStatus$(): Observable<boolean> {
    return this.metricsConnected$.asObservable();
  }

  get logsConnectionStatus$(): Observable<boolean> {
    return this.logsConnected$.asObservable();
  }

  get alertsConnectionStatus$(): Observable<boolean> {
    return this.alertsConnected$.asObservable();
  }

  /**
   * Check if any stream is currently connected.
   */
  get isConnected(): boolean {
    return this.metricsConnected$.value || this.logsConnected$.value || this.alertsConnected$.value;
  }
}
