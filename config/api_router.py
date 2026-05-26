from django.urls import path, include

urlpatterns = [
    path("auth/", include("common.urls")),
    # path("appointments/", include("appointments.presentation.urls")),
]