from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import VulnerabilitySerializer
from .services.vulnerability_service import (
    get_all_vulnerabilities,
)

@extend_schema(
    summary="List vulnerabilities",
    description="Get vulnerabilities from local database",
    responses=VulnerabilitySerializer(many=True),
)
class VulnerabilityListView(ListAPIView):
    serializer_class = VulnerabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        severity = self.request.query_params.get(
            "severity"
        )
        status = self.request.query_params.get(
            "status"
        )
        search = self.request.query_params.get(
            "search"
        )

        return get_all_vulnerabilities(
            severity=severity,
            status=status,
            search=search,
        )