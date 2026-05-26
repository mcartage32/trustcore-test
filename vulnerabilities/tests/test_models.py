import pytest
from vulnerabilities.models import Vulnerability

@pytest.mark.django_db
def test_create_vulnerability():
    v = Vulnerability.objects.create(
        cve_id="CVE-TEST-001",
        description="Test vulnerability",
        severity="HIGH"
    )

    assert v.cve_id == "CVE-TEST-001"
    assert v.status == "ACTIVE"