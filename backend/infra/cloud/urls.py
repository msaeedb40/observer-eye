from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CloudProviderViewSet, CloudRegionViewSet

app_name = 'cloud'

router = DefaultRouter()
router.register(r'providers', CloudProviderViewSet)
router.register(r'regions', CloudRegionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
