from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkInterfaceViewSet, TrafficFlowViewSet, FirewallRuleViewSet, VPNConnectionViewSet

app_name = 'network'

router = DefaultRouter()
router.register(r'interfaces', NetworkInterfaceViewSet)
router.register(r'traffic-flows', TrafficFlowViewSet)
router.register(r'firewall-rules', FirewallRuleViewSet)
router.register(r'vpn-connections', VPNConnectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
