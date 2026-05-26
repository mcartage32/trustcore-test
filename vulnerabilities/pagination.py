from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from vulnerabilities.constants import NVD_DEFAULT_LIMIT


class VulnerabilityPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = NVD_DEFAULT_LIMIT

    def get_paginated_response(self, data):
        return Response({
            "total": self.page.paginator.count,
            "page": self.page.number,
            "page_size": self.get_page_size(self.request),
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })