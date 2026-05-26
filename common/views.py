from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField()
    service = serializers.CharField()
    version = serializers.CharField()


@extend_schema(
    auth=[],
    summary="Healthcheck",
    description="Check if API is alive",
    responses=HealthCheckSerializer,
)
class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "status": "ok",
            "service": "trustcore-api",
            "version": "1.0.0",
        })

@extend_schema(auth=[])
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


@extend_schema(auth=[])
class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]