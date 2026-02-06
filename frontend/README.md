# Frontend - Observer-Eye

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 21.0.4.

## Design System

The platform utilizes a **Bento-box** design system for high-density information display.

### Bento Grid Architecture
- **12-Column Grid**: Flexible grid system defined in `styles.css`.
- **Responsive Layouts**: Grids automatically adjust based on screen size using `col-span-*` and `row-span-*` utilities.
- **Glassmorphism**: Premium frosted-glass panels (`.glass-panel`) with subtle gradients and borders.
- **Premium Aesthetics**: Curated color palettes (Indigo, Sky, Pink, Orange) for distinct monitoring domains.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Performance Monitoring Integration

The frontend utilizes a centralized `PerformanceService` to aggregate data from:
- **Network**: Layer 3/4 metrics
- **Traffic**: Layer 7 protocol analysis
- **Security**: Threat surface and events
- **Identity**: Session risk and auth life-cycles
- **Insights**: Anomaly probability and health scores
- **Cloud/K8s**: Multi-cloud and cluster resource tracking

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```
