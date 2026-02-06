from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserIdentity, AccessLog, UserGroup, MFAStatus
from .serializers import UserIdentitySerializer, AccessLogSerializer, UserGroupSerializer, MFAStatusSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import UserIdentity

class SocialLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        full_name = data.get('full_name', email)
        provider = data.get('provider')
        provider_id = data.get('provider_id', email) # Fallback to email as ID if not provided

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_VALUE)

        # Get or create Django user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': email, 'first_name': full_name}
        )

        # Ensure UserIdentity exists
        identity, _ = UserIdentity.objects.get_or_create(
            user_id=provider_id,
            defaults={
                'email': email,
                'full_name': full_name,
                'role': 'viewer', # Default role
                'is_active': True
            }
        )

        # Generate JWT
        refresh = RefreshToken.for_user(user)
        # Add custom claims to access token
        refresh['role'] = identity.role
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserIdentitySerializer(identity).data
        })

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = getattr(user, 'useridentity', None).role if hasattr(user, 'useridentity') else 'viewer'
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        identity = getattr(request.user, 'useridentity', None)
        if not identity:
            return Response({"error": "User identity not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserIdentitySerializer(identity)
        return Response(serializer.data)

class UserIdentityViewSet(viewsets.ModelViewSet):
    queryset = UserIdentity.objects.filter(is_active=True)
    serializer_class = UserIdentitySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role', 'department']
    search_fields = ['email', 'full_name']

class AccessLogViewSet(viewsets.ModelViewSet):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'action', 'status']
    search_fields = ['user__email', 'ip_address']

class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']

class MFAStatusViewSet(viewsets.ModelViewSet):
    queryset = MFAStatus.objects.all()
    serializer_class = MFAStatusSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_enabled', 'method']
    search_fields = ['user__email']
