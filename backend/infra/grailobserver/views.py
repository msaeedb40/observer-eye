"""Grail Observer views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import GrailEntity, GrailRelationship
from .serializers import GrailEntitySerializer, GrailEntityListSerializer, GrailRelationshipSerializer


class GrailEntityViewSet(viewsets.ModelViewSet):
    queryset = GrailEntity.objects.filter(is_active=True).prefetch_related('outgoing_relationships', 'incoming_relationships')
    serializer_class = GrailEntitySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entity_type', 'health_status']
    search_fields = ['display_name', 'entity_id']
    ordering = ['-last_seen']

    def get_serializer_class(self):
        if self.action == 'list':
            return GrailEntityListSerializer
        return GrailEntitySerializer

    @action(detail=False, methods=['get'])
    def topology(self, request):
        """Get topology graph."""
        entities = list(self.get_queryset().values('id', 'entity_id', 'display_name', 'entity_type', 'health_status'))
        relationships = list(GrailRelationship.objects.values('source_id', 'target_id', 'relationship_type'))
        return Response({'nodes': entities, 'edges': relationships})


class GrailRelationshipViewSet(viewsets.ModelViewSet):
    queryset = GrailRelationship.objects.filter(is_active=True)
    serializer_class = GrailRelationshipSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['source', 'target', 'relationship_type']
