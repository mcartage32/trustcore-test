from django.urls import path, include

urlpatterns = [
    path("health/", include("common.urls")),
    path("auth/", include("common.auth_urls")),
]