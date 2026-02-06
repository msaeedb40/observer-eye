from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CloudMetricViewSet, CloudCostViewSet

app_name = 'cloud_performance_monitoring'

router = DefaultRouter()
router.register(r'metrics', CloudMetricViewSet)
router.register(r'costs', CloudCostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
