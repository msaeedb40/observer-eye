from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogPipelineViewSet, SanitizationRuleViewSet

app_name = 'logstach'

router = DefaultRouter()
router.register(r'pipelines', LogPipelineViewSet)
router.register(r'sanitization', SanitizationRuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
