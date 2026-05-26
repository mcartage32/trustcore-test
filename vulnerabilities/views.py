from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from vulnerabilities.pagination import VulnerabilityPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from vulnerabilities.services.fixed_service import mark_vulnerabilities_fixed
from vulnerabilities.serializers import (
    FixedVulnerabilityRequestSerializer,
    VulnerabilitySerializer,
    VulnerabilityFilterSerializer,
)
from vulnerabilities.services.vulnerability_service import (
    get_all_vulnerabilities,
)


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
    

@extend_schema(
    summary="Mark vulnerabilities as fixed",
    request=FixedVulnerabilityRequestSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "updated": {"type": "integer"},
                "cve_ids": {"type": "array", "items": {"type": "string"}},
            }
        }
    }
)
class FixedVulnerabilitiesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FixedVulnerabilityRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = mark_vulnerabilities_fixed(
            user=request.user,
            cve_ids=serializer.validated_data["cve_ids"],
            notes=serializer.validated_data.get("notes"),
        )

        return Response(result)