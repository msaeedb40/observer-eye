"""APM views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, F
from .models import APMTransaction, APMSpan, APMError
from .serializers import APMTransactionSerializer, APMTransactionListSerializer, APMSpanSerializer, APMErrorSerializer


class APMTransactionViewSet(viewsets.ModelViewSet):
    queryset = APMTransaction.objects.filter(is_active=True).prefetch_related('spans')
    serializer_class = APMTransactionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['app_name', 'transaction_name', 'result', 'http_status_code']
    search_fields = ['transaction_name', 'http_url']
    ordering = ['-timestamp']

    def get_serializer_class(self):
        if self.action == 'list':
            return APMTransactionListSerializer
        return APMTransactionSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get APM summary statistics."""
        qs = self.get_queryset()
        summary = qs.aggregate(
            total_transactions=Count('id'),
            avg_duration=Avg('duration_ms'),
            error_count=Count('id', filter=F('result')!='success')
        )
        return Response(summary)

    @action(detail=False, methods=['get'])
    def slow_transactions(self, request):
        """Get slowest transactions."""
        limit = int(request.query_params.get('limit', 10))
        slow = self.get_queryset().order_by('-duration_ms')[:limit]
        serializer = APMTransactionListSerializer(slow, many=True)
        return Response(serializer.data)


class APMSpanViewSet(viewsets.ModelViewSet):
    queryset = APMSpan.objects.all()
    serializer_class = APMSpanSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['transaction', 'span_type']
    ordering = ['start_offset_ms']


class APMErrorViewSet(viewsets.ModelViewSet):
    queryset = APMError.objects.filter(is_active=True)
    serializer_class = APMErrorSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['app_name', 'error_type', 'handled']
    search_fields = ['message', 'error_type']
    ordering = ['-timestamp']
