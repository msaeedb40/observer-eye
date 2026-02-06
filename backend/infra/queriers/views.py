"""Queriers views."""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import QueryTemplate, QueryExecution
from .serializers import QueryTemplateSerializer, QueryExecutionSerializer


class QueryTemplateViewSet(viewsets.ModelViewSet):
    queryset = QueryTemplate.objects.filter(is_active=True)
    serializer_class = QueryTemplateSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['data_type', 'query_language']
    search_fields = ['name', 'description']


class QueryExecutionViewSet(viewsets.ModelViewSet):
    queryset = QueryExecution.objects.filter(is_active=True)
    serializer_class = QueryExecutionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user_id', 'data_type', 'status']
    ordering = ['-executed_at']
    http_method_names = ['get', 'post', 'head']

    @action(detail=False, methods=['post'])
    def execute(self, request):
        """Execute a query against real data tables using JSON filters."""
        query = request.data.get('query')
        data_type = request.data.get('data_type', 'metrics')
        user_id = request.data.get('user_id', 'anonymous')
        
        execution = QueryExecution.objects.create(
            query=query,
            data_type=data_type,
            user_id=user_id,
            parameters=request.data.get('parameters', {}),
            status='running'
        )
        
        results = []
        try:
            start_time = timezone.now()
            
            # Simplified Logic: Map basic "query" to Django filters
            # Real implementation would use a proper grammar parser or raw SQL if safe
            # Here we support simple JSON based filtering for 'metrics', 'logs', 'traces'
            
            if data_type == 'metrics':
                # Query: {"name": "cpu_usage", "source": "app-01"}
                from core.models import Metric
                filters = request.data.get('parameters', {})
                qs = Metric.objects.filter(**filters).order_by('-timestamp')[:100]
                results = [
                    {"time": m.timestamp, "metric": m.name, "value": m.value, "source": m.source}
                    for m in qs
                ]
                
            elif data_type == 'logs':
                from core.models import LogEntry
                filters = request.data.get('parameters', {})
                qs = LogEntry.objects.filter(**filters).order_by('-timestamp')[:50]
                results = [
                    {"timestamp": l.timestamp, "level": l.level, "message": l.message, "source": l.source}
                    for l in qs
                ]

            elif data_type == 'traces':
                from core.models import Trace
                qs = Trace.objects.all().order_by('-start_time')[:20]
                results = [
                     {"trace_id": t.trace_id, "service": t.service_name, "duration": t.duration_ms, "status": t.status}
                     for t in qs
                ]
            
            execution.status = 'success'
            execution.row_count = len(results)
            
        except Exception as e:
            execution.status = 'failed'
            execution.error_message = str(e)
            
        finally:
            execution.duration_ms = (timezone.now() - start_time).total_seconds() * 1000
            execution.save()
        
        if execution.status == 'failed':
            return Response({"status": "error", "message": execution.error_message}, status=400)

        return Response({
            "execution_id": execution.id,
            "status": "success",
            "columns": list(results[0].keys()) if results else [],
            "results": results
        })

    @action(detail=False, methods=['post'], url_path='promql')
    def execute_promql(self, request):
        """
        Execute a PromQL-like query.
        
        Supports syntax like:
          - metrics{name="cpu_usage", source="app-01"}
          - logs{level="error", source=~"web-.*"}
          - avg(metrics{name="memory_usage"})[5m]
          - rate(metrics{name="requests_total"})[1m]
        """
        query_string = request.data.get('query', '')
        user_id = request.data.get('user_id', 'anonymous')
        limit = request.data.get('limit', 100)
        
        if not query_string:
            return Response({"status": "error", "message": "Query is required"}, status=400)
        
        # Create execution record
        execution = QueryExecution.objects.create(
            query=query_string,
            data_type='promql',
            user_id=user_id,
            parameters={'limit': limit},
            status='running'
        )
        
        try:
            start_time = timezone.now()
            
            # Use PromQL parser
            from .services.promql_parser import execute_query
            result = execute_query(query_string, limit=limit)
            
            execution.duration_ms = (timezone.now() - start_time).total_seconds() * 1000
            
            if result.get('status') == 'success':
                execution.status = 'success'
                execution.row_count = result.get('count', 0)
                execution.save()
                # Return Prometheus-compatible response format
                return Response({
                    "status": "success",
                    "data": {
                        "resultType": "vector",
                        "result": result.get('results', [])
                    },
                    "execution_id": str(execution.id)
                })
            else:
                execution.status = 'failed'
                execution.error_message = result.get('error', 'Unknown error')
                execution.save()
                return Response({
                    "status": "error",
                    "error": result.get('error', 'Unknown error'),
                    "execution_id": str(execution.id)
                }, status=400)
                
        except Exception as e:
            execution.status = 'failed'
            execution.error_message = str(e)
            execution.duration_ms = (timezone.now() - start_time).total_seconds() * 1000
            execution.save()
            return Response({
                "execution_id": str(execution.id),
                "status": "error",
                "error": str(e)
            }, status=500)

