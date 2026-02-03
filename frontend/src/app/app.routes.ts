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
        path: 'metrics/network',
        loadComponent: () => import('./pages/network/network.component').then(m => m.NetworkComponent)
    },
    {
        path: 'metrics/system',
        loadComponent: () => import('./pages/system/system.component').then(m => m.SystemComponent)
    },
    {
        path: 'metrics/security',
        loadComponent: () => import('./pages/security/security.component').then(m => m.SecurityComponent)
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
    {
        path: 'topology',
        loadComponent: () => import('./pages/topology/topology.component').then(m => m.TopologyComponent)
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
    {
        path: 'alerts/manage',
        loadComponent: () => import('./pages/alerts-manage/alerts-manage.component').then(m => m.AlertsManageComponent)
    },
    {
        path: 'integrations',
        loadComponent: () => import('./pages/integrations/integrations.component').then(m => m.IntegrationsComponent)
    },
    {
        path: 'identity',
        loadComponent: () => import('./pages/identity/identity.component').then(m => m.IdentityComponent)
    },
    {
        path: 'traffic',
        loadComponent: () => import('./pages/traffic/traffic.component').then(m => m.TrafficComponent)
    },

    // Settings
    {
        path: 'settings',
        loadComponent: () => import('./pages/settings/settings.component').then(m => m.SettingsComponent)
    },
    {
        path: 'insights',
        loadComponent: () => import('./pages/insights/insights.component').then(m => m.InsightsComponent)
    },

    // 404
    {
        path: '**',
        loadComponent: () => import('./pages/not-found/not-found.component').then(m => m.NotFoundComponent)
    }
];
