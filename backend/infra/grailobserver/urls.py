"""Grail Observer URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'grailobserver'

router = DefaultRouter()
router.register(r'entities', views.GrailEntityViewSet, basename='grail-entity')
router.register(r'relationships', views.GrailRelationshipViewSet, basename='grail-relationship')

urlpatterns = [
    path('', include(router.urls)),
]
