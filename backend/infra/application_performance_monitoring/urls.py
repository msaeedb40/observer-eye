"""APM URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'apm'

router = DefaultRouter()
router.register(r'transactions', views.APMTransactionViewSet, basename='apm-transaction')
router.register(r'spans', views.APMSpanViewSet, basename='apm-span')
router.register(r'errors', views.APMErrorViewSet, basename='apm-error')

urlpatterns = [
    path('', include(router.urls)),
]
