from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from vulnerabilities.pagination import VulnerabilityPagination
from vulnerabilities.serializers import (
    VulnerabilitySerializer,
    VulnerabilityFilterSerializer,
)
from vulnerabilities.services.vulnerability_service import (
    get_all_vulnerabilities,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    summary="List vulnerabilities",
    parameters=[
        OpenApiParameter(
            name="severity",
            type=OpenApiTypes.STR,
            required=False,
            enum=["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"],
        ),
        OpenApiParameter(
            name="status",
            type=OpenApiTypes.STR,
            required=False,
            enum=["ACTIVE", "FIXED", "DEPRECATED"],
        ),
        OpenApiParameter("cve_id", OpenApiTypes.STR, required=False),
        OpenApiParameter("published_from", OpenApiTypes.DATE, required=False),
        OpenApiParameter("published_to", OpenApiTypes.DATE, required=False),
    ],
    responses=VulnerabilitySerializer(many=True),
)
class VulnerabilityListView(ListAPIView):
    serializer_class = VulnerabilitySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = VulnerabilityPagination

    def get_queryset(self):
        serializer = VulnerabilityFilterSerializer(
            data=self.request.query_params
        )
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data
        return get_all_vulnerabilities(**filters)