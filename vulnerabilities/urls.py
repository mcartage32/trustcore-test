from django.urls import path
from vulnerabilities.api.nvd_sync_views import SyncVulnerabilitiesView
from .views import VulnerabilityListView

urlpatterns = [
    path(
        "",
        VulnerabilityListView.as_view(),
        name="vulnerability-list",
    ),
    path("sync/", SyncVulnerabilitiesView.as_view()),
]