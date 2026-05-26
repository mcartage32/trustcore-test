from django.urls import path
from vulnerabilities.api.nvd_sync_views import SyncVulnerabilitiesView
from .views import FixedVulnerabilitiesView, UnfixVulnerabilitiesView, VulnerabilityListView, ActiveVulnerabilitiesView, VulnerabilitySummaryView

urlpatterns = [
    path("", VulnerabilityListView.as_view(),),
    path("sync/", SyncVulnerabilitiesView.as_view()),
    path("fixed/", FixedVulnerabilitiesView.as_view()),
    path("active/", ActiveVulnerabilitiesView.as_view()),
    path("summary/", VulnerabilitySummaryView.as_view()),
     path("unfixed/", UnfixVulnerabilitiesView.as_view())
]