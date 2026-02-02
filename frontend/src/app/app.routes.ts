import { Routes } from '@angular/router';

/**
 * Observer-Eye Frontend Routes
 * Presentation Layer - Port 80
 */
export const routes: Routes = [
    // Default redirect
    {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
    },

    // Authentication routes
    {
        path: 'auth',
        children: [
            {
                path: 'login',
                loadComponent: () => import('./pages/auth/login/login.component').then(m => m.LoginComponent)
            },
            {
                path: 'register',
                loadComponent: () => import('./pages/auth/register/register.component').then(m => m.RegisterComponent)
            },
            {
                path: 'oauth/:provider',
                loadComponent: () => import('./pages/auth/oauth-callback/oauth-callback.component').then(m => m.OAuthCallbackComponent)
            }
        ]
    },

    // Main application routes (protected)
    {
        path: 'dashboard',
        loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent)
    },

    // Observability pillars
    {
        path: 'metrics',
        loadComponent: () => import('./pages/metrics/metrics.component').then(m => m.MetricsComponent)
    },
    {
        path: 'events',
        loadComponent: () => import('./pages/events/events.component').then(m => m.EventsComponent)
    },
    {
        path: 'logs',
        loadComponent: () => import('./pages/logs/logs.component').then(m => m.LogsComponent)
    },
    {
        path: 'traces',
        loadComponent: () => import('./pages/traces/traces.component').then(m => m.TracesComponent)
    },

    // Performance Monitoring
    {
        path: 'apm',
        loadComponent: () => import('./pages/apm/apm.component').then(m => m.ApmComponent)
    },

    // Alerts & Notifications
    {
        path: 'alerts',
        loadComponent: () => import('./pages/alerts/alerts.component').then(m => m.AlertsComponent)
    },

    // Settings
    {
        path: 'settings',
        loadComponent: () => import('./pages/settings/settings.component').then(m => m.SettingsComponent)
    },

    // 404
    {
        path: '**',
        loadComponent: () => import('./pages/not-found/not-found.component').then(m => m.NotFoundComponent)
    }
];
