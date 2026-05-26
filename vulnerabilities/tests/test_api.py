import pytest
from rest_framework.test import APIClient
from vulnerabilities.models import Vulnerability
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_list_vulnerabilities_api():
    user = User.objects.create_user(username="test", password="123")
    client = APIClient()
    client.force_authenticate(user=user)

    Vulnerability.objects.create(
        cve_id="CVE-API-001",
        description="test",
        severity="HIGH"
    )

    response = client.get("/api/v1/vulnerabilities/")

    assert response.status_code == 200

@pytest.mark.django_db
def test_protected_endpoint_requires_auth():
    client = APIClient()

    response = client.get("/api/v1/vulnerabilities/")

    assert response.status_code == 401