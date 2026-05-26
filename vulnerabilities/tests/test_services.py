import pytest
from vulnerabilities.models import Vulnerability, FixedVulnerability
from vulnerabilities.services.vulnerability_service import unfix_vulnerability


@pytest.mark.django_db
def test_unfix_vulnerability_success(django_user_model):
    user = django_user_model.objects.create_user(
        username="test",
        password="123"
    )

    v = Vulnerability.objects.create(
        cve_id="CVE-TEST-002",
        description="test",
        severity="HIGH"
    )

    FixedVulnerability.objects.create(
        vulnerability=v,
        fixed_by=user
    )

    result = unfix_vulnerability(user, "CVE-TEST-002")

    assert result["unfixed"] is True
    assert FixedVulnerability.objects.count() == 0