"""
Report Generator Service for Observer-Eye Platform.

Generates analytics reports in multiple formats:
- PDF (using WeasyPrint or ReportLab)
- CSV
- JSON
- HTML

Supports scheduled and on-demand report generation.
"""
import csv
import io
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from django.utils import timezone
from django.template import Template, Context

logger = logging.getLogger(__name__)


class ReportFormat(str, Enum):
    """Supported report formats."""
    PDF = "pdf"
    CSV = "csv"
    JSON = "json"
    HTML = "html"


@dataclass
class ReportData:
    """Container for report data and metadata."""
    title: str
    description: str
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    data: List[Dict[str, Any]]
    columns: List[str]
    summary: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'description': self.description,
            'generated_at': self.generated_at.isoformat(),
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'data': self.data,
            'columns': self.columns,
            'summary': self.summary,
            'row_count': len(self.data),
        }


class ReportExporter(ABC):
    """Abstract base class for report exporters."""
    
    @abstractmethod
    def export(self, report_data: ReportData) -> bytes:
        """Export report data to bytes."""
        raise NotImplementedError("Subclasses must implement export()")
    
    @property
    @abstractmethod
    def content_type(self) -> str:
        """MIME type for the exported format."""
        raise NotImplementedError("Subclasses must implement content_type")
    
    @property
    @abstractmethod
    def file_extension(self) -> str:
        """File extension for the exported format."""
        raise NotImplementedError("Subclasses must implement file_extension")


class CSVExporter(ReportExporter):
    """Export reports to CSV format."""
    
    @property
    def content_type(self) -> str:
        return "text/csv"
    
    @property
    def file_extension(self) -> str:
        return "csv"
    
    def export(self, report_data: ReportData) -> bytes:
        output = io.StringIO()
        
        # Write header comment
        output.write(f"# {report_data.title}\n")
        output.write(f"# Generated: {report_data.generated_at.isoformat()}\n")
        output.write(f"# Period: {report_data.period_start.date()} to {report_data.period_end.date()}\n")
        output.write("#\n")
        
        if not report_data.data:
            output.write("# No data available\n")
            return output.getvalue().encode('utf-8')
        
        # Write data
        writer = csv.DictWriter(output, fieldnames=report_data.columns)
        writer.writeheader()
        for row in report_data.data:
            writer.writerow({k: row.get(k, '') for k in report_data.columns})
        
        return output.getvalue().encode('utf-8')


class JSONExporter(ReportExporter):
    """Export reports to JSON format."""
    
    @property
    def content_type(self) -> str:
        return "application/json"
    
    @property
    def file_extension(self) -> str:
        return "json"
    
    def export(self, report_data: ReportData) -> bytes:
        return json.dumps(report_data.to_dict(), indent=2, default=str).encode('utf-8')


class HTMLExporter(ReportExporter):
    """Export reports to HTML format."""
    
    TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #1a1a2e; margin-bottom: 8px; }
        .meta { color: #666; margin-bottom: 24px; font-size: 14px; }
        .summary { background: #f8f9fa; padding: 16px; border-radius: 4px; margin-bottom: 24px; }
        .summary h3 { margin-top: 0; color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 16px; }
        th { background: #1a1a2e; color: white; padding: 12px 8px; text-align: left; font-weight: 500; }
        td { padding: 10px 8px; border-bottom: 1px solid #e5e5e5; }
        tr:hover { background: #f8f9fa; }
        .footer { margin-top: 24px; padding-top: 16px; border-top: 1px solid #e5e5e5; color: #888; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <div class="meta">
            <p>{{ description }}</p>
            <p><strong>Period:</strong> {{ period_start }} to {{ period_end }}</p>
            <p><strong>Generated:</strong> {{ generated_at }}</p>
            <p><strong>Total Records:</strong> {{ row_count }}</p>
        </div>
        
        {% if summary %}
        <div class="summary">
            <h3>Summary</h3>
            {% for key, value in summary.items %}
            <p><strong>{{ key }}:</strong> {{ value }}</p>
            {% endfor %}
        </div>
        {% endif %}
        
        <table>
            <thead>
                <tr>
                    {% for col in columns %}<th>{{ col }}</th>{% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for row in data %}
                <tr>
                    {% for col in columns %}<td>{{ row|get_item:col }}</td>{% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <div class="footer">
            Observer-Eye Observability Platform - Report generated automatically
        </div>
    </div>
</body>
</html>
"""
    
    @property
    def content_type(self) -> str:
        return "text/html"
    
    @property
    def file_extension(self) -> str:
        return "html"
    
    def export(self, report_data: ReportData) -> bytes:
        from django import template
        
        # Register custom filter
        register = template.Library()
        
        @register.filter
        def get_item(dictionary, key):
            return dictionary.get(key, '')
        
        # Simple template rendering without Django template engine complexities
        html = self._render_html(report_data)
        return html.encode('utf-8')
    
    def _render_html(self, report_data: ReportData) -> str:
        """Render HTML without Django template engine."""
        rows_html = ""
        for row in report_data.data:
            cells = "".join(f"<td>{row.get(col, '')}</td>" for col in report_data.columns)
            rows_html += f"<tr>{cells}</tr>\n"
        
        headers_html = "".join(f"<th>{col}</th>" for col in report_data.columns)
        
        summary_html = ""
        if report_data.summary:
            items = "".join(f"<p><strong>{k}:</strong> {v}</p>" for k, v in report_data.summary.items())
            summary_html = f'<div class="summary"><h3>Summary</h3>{items}</div>'
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{report_data.title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a1a2e; margin-bottom: 8px; }}
        .meta {{ color: #666; margin-bottom: 24px; font-size: 14px; }}
        .summary {{ background: #f8f9fa; padding: 16px; border-radius: 4px; margin-bottom: 24px; }}
        .summary h3 {{ margin-top: 0; color: #333; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
        th {{ background: #1a1a2e; color: white; padding: 12px 8px; text-align: left; font-weight: 500; }}
        td {{ padding: 10px 8px; border-bottom: 1px solid #e5e5e5; }}
        tr:hover {{ background: #f8f9fa; }}
        .footer {{ margin-top: 24px; padding-top: 16px; border-top: 1px solid #e5e5e5; color: #888; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{report_data.title}</h1>
        <div class="meta">
            <p>{report_data.description}</p>
            <p><strong>Period:</strong> {report_data.period_start.date()} to {report_data.period_end.date()}</p>
            <p><strong>Generated:</strong> {report_data.generated_at}</p>
            <p><strong>Total Records:</strong> {len(report_data.data)}</p>
        </div>
        {summary_html}
        <table>
            <thead><tr>{headers_html}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        <div class="footer">Observer-Eye Observability Platform - Report generated automatically</div>
    </div>
</body>
</html>
"""
        return html


class PDFExporter(ReportExporter):
    """Export reports to PDF format using HTML to PDF conversion."""
    
    @property
    def content_type(self) -> str:
        return "application/pdf"
    
    @property
    def file_extension(self) -> str:
        return "pdf"
    
    def export(self, report_data: ReportData) -> bytes:
        # Generate HTML first
        html_exporter = HTMLExporter()
        html_content = html_exporter.export(report_data).decode('utf-8')
        
        # Try to convert to PDF using weasyprint or fallback
        try:
            from weasyprint import HTML
            pdf = HTML(string=html_content).write_pdf()
            return pdf
        except ImportError:
            logger.warning("WeasyPrint not installed, falling back to HTML")
            # Return HTML as fallback (user can print to PDF)
            return html_content.encode('utf-8')


# Exporter registry
EXPORTERS = {
    ReportFormat.CSV: CSVExporter(),
    ReportFormat.JSON: JSONExporter(),
    ReportFormat.HTML: HTMLExporter(),
    ReportFormat.PDF: PDFExporter(),
}


class ReportGenerator:
    """
    Main report generator service.
    
    Usage:
        generator = ReportGenerator()
        
        # Generate metrics report
        report = generator.generate_metrics_report(
            period_days=7,
            metric_names=['cpu_usage', 'memory_usage'],
            format=ReportFormat.PDF
        )
    """
    
    def __init__(self):
        self.exporters = EXPORTERS
    
    def generate_metrics_report(
        self,
        period_days: int = 7,
        metric_names: List[str] = None,
        sources: List[str] = None,
        format: ReportFormat = ReportFormat.PDF,
    ) -> Dict[str, Any]:
        """Generate a metrics report."""
        from core.models import Metric
        from django.db.models import Avg, Max, Min, Count
        
        end_time = timezone.now()
        start_time = end_time - timedelta(days=period_days)
        
        # Build query
        queryset = Metric.objects.filter(timestamp__range=(start_time, end_time))
        if metric_names:
            queryset = queryset.filter(name__in=metric_names)
        if sources:
            queryset = queryset.filter(source__in=sources)
        
        # Aggregate data
        aggregated = queryset.values('name', 'source').annotate(
            avg_value=Avg('value'),
            max_value=Max('value'),
            min_value=Min('value'),
            count=Count('id'),
        ).order_by('name', 'source')
        
        data = list(aggregated)
        columns = ['name', 'source', 'avg_value', 'max_value', 'min_value', 'count']
        
        # Calculate summary
        total_count = queryset.count()
        unique_metrics = queryset.values('name').distinct().count()
        unique_sources = queryset.values('source').distinct().count()
        
        report_data = ReportData(
            title='Metrics Summary Report',
            description=f'Aggregated metrics for the past {period_days} days',
            generated_at=timezone.now(),
            period_start=start_time,
            period_end=end_time,
            data=data,
            columns=columns,
            summary={
                'Total Data Points': total_count,
                'Unique Metrics': unique_metrics,
                'Unique Sources': unique_sources,
            }
        )
        
        return self._export(report_data, format)
    
    def generate_logs_report(
        self,
        period_days: int = 7,
        levels: List[str] = None,
        sources: List[str] = None,
        format: ReportFormat = ReportFormat.PDF,
    ) -> Dict[str, Any]:
        """Generate a logs report."""
        from core.models import LogEntry
        from django.db.models import Count
        
        end_time = timezone.now()
        start_time = end_time - timedelta(days=period_days)
        
        queryset = LogEntry.objects.filter(timestamp__range=(start_time, end_time))
        if levels:
            queryset = queryset.filter(level__in=levels)
        if sources:
            queryset = queryset.filter(source__in=sources)
        
        # Aggregate by level and source
        aggregated = queryset.values('level', 'source').annotate(
            count=Count('id'),
        ).order_by('-count')
        
        data = list(aggregated)
        columns = ['level', 'source', 'count']
        
        # Summary
        level_counts = queryset.values('level').annotate(count=Count('id'))
        summary = {f"{item['level'].title()} Logs": item['count'] for item in level_counts}
        summary['Total Logs'] = queryset.count()
        
        report_data = ReportData(
            title='Logs Summary Report',
            description=f'Log entries summary for the past {period_days} days',
            generated_at=timezone.now(),
            period_start=start_time,
            period_end=end_time,
            data=data,
            columns=columns,
            summary=summary,
        )
        
        return self._export(report_data, format)
    
    def generate_alerts_report(
        self,
        period_days: int = 7,
        severities: List[str] = None,
        format: ReportFormat = ReportFormat.PDF,
    ) -> Dict[str, Any]:
        """Generate an alerts report."""
        from notification.models import Alert
        
        end_time = timezone.now()
        start_time = end_time - timedelta(days=period_days)
        
        queryset = Alert.objects.filter(started_at__range=(start_time, end_time))
        if severities:
            queryset = queryset.filter(severity__in=severities)
        
        # Get alert details
        alerts = queryset.values('name', 'severity', 'state', 'started_at', 'resolved_at')
        data = list(alerts)
        columns = ['name', 'severity', 'state', 'started_at', 'resolved_at']
        
        # Summary
        total = queryset.count()
        firing = queryset.filter(state='firing').count()
        resolved = queryset.filter(state='resolved').count()
        
        report_data = ReportData(
            title='Alerts Report',
            description=f'Alert activity for the past {period_days} days',
            generated_at=timezone.now(),
            period_start=start_time,
            period_end=end_time,
            data=data,
            columns=columns,
            summary={
                'Total Alerts': total,
                'Currently Firing': firing,
                'Resolved': resolved,
            }
        )
        
        return self._export(report_data, format)
    
    def generate_custom_report(
        self,
        title: str,
        description: str,
        data: List[Dict[str, Any]],
        columns: List[str],
        period_start: datetime,
        period_end: datetime,
        summary: Dict[str, Any] = None,
        format: ReportFormat = ReportFormat.PDF,
    ) -> Dict[str, Any]:
        """Generate a custom report from provided data."""
        report_data = ReportData(
            title=title,
            description=description,
            generated_at=timezone.now(),
            period_start=period_start,
            period_end=period_end,
            data=data,
            columns=columns,
            summary=summary or {},
        )
        
        return self._export(report_data, format)
    
    def _export(self, report_data: ReportData, format: ReportFormat) -> Dict[str, Any]:
        """Export report data to specified format."""
        exporter = self.exporters.get(format)
        if not exporter:
            raise ValueError(f"Unsupported format: {format}")
        
        content = exporter.export(report_data)
        filename = f"{report_data.title.lower().replace(' ', '_')}_{report_data.generated_at.strftime('%Y%m%d_%H%M%S')}.{exporter.file_extension}"
        
        return {
            'filename': filename,
            'content': content,
            'content_type': exporter.content_type,
            'size_bytes': len(content),
            'format': format.value,
            'row_count': len(report_data.data),
        }


# Convenience function
def generate_report(
    report_type: str,
    format: str = 'pdf',
    period_days: int = 7,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate a report.
    
    Args:
        report_type: 'metrics', 'logs', or 'alerts'
        format: 'pdf', 'csv', 'json', or 'html'
        period_days: Number of days to include
        **kwargs: Additional filters
        
    Returns:
        Dict with filename, content (bytes), and metadata
    """
    generator = ReportGenerator()
    report_format = ReportFormat(format)
    
    if report_type == 'metrics':
        return generator.generate_metrics_report(period_days, format=report_format, **kwargs)
    elif report_type == 'logs':
        return generator.generate_logs_report(period_days, format=report_format, **kwargs)
    elif report_type == 'alerts':
        return generator.generate_alerts_report(period_days, format=report_format, **kwargs)
    else:
        raise ValueError(f"Unknown report type: {report_type}")
