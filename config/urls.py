from django.urls import path, include

urlpatterns = [
    # path("api/schema/", OpenAPIView.as_view(), name="schema"),
    # path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
    path("api/v1/", include("config.api_router")),
]
