from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from vulnerabilities.serializers import SyncResponseSerializer, SyncRequestSerializer
from vulnerabilities.services.nvd_sync_service import run_nvd_sync
from vulnerabilities.constants import (
    NVD_DEFAULT_PAGE,
    NVD_DEFAULT_LIMIT,
)
from vulnerabilities.throttles import SyncRateThrottle

@extend_schema(
    request=SyncRequestSerializer,
    responses=SyncResponseSerializer,
    summary="Sync vulnerabilities from NVD",
    description="Fetch vulnerabilities from NVD API and store/update them in local database",
)
class SyncVulnerabilitiesView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [SyncRateThrottle]

    def post(self, request):
        result = run_nvd_sync(
            cve_id=request.data.get("cve_id"),
            pub_start_date=request.data.get("pub_start_date"),
            pub_end_date=request.data.get("pub_end_date"),
            page=request.data.get("page", NVD_DEFAULT_PAGE),
            limit=request.data.get("limit", NVD_DEFAULT_LIMIT),
        )

        return Response(result)