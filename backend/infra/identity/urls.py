from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserIdentityViewSet, AccessLogViewSet, UserGroupViewSet, MFAStatusViewSet,
    MyTokenObtainPairView, ProfileView, SocialLoginView
)

app_name = 'identity'

router = DefaultRouter()
router.register(r'users', UserIdentityViewSet)
router.register(r'access-logs', AccessLogViewSet)
router.register(r'groups', UserGroupViewSet)
router.register(r'mfa', MFAStatusViewSet)

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('social-login/', SocialLoginView.as_view(), name='social_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]
