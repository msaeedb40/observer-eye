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
        """Execute a query."""
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
        
        # In real implementation, execute the query asynchronously
        execution.status = 'success'
        execution.duration_ms = 0
        execution.row_count = 0
        execution.save()
        
        return Response(self.get_serializer(execution).data)
