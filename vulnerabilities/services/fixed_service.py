from django.db import transaction
from vulnerabilities.models import (
    Vulnerability,
    FixedVulnerability,
    AuditLog,
)

@transaction.atomic
def mark_vulnerabilities_fixed(user, cve_ids, notes=None):
    vulnerabilities = Vulnerability.objects.filter(
        cve_id__in=cve_ids
    )

    fixed_records = []

    for vuln in vulnerabilities:
        vuln.status = Vulnerability.StatusChoices.FIXED
        vuln.save(update_fields=["status"])

        fixed, created = FixedVulnerability.objects.get_or_create(
            vulnerability=vuln,
            fixed_by=user,
            defaults={"notes": notes},
        )

        fixed_records.append(fixed)

        AuditLog.objects.create(
            user=user,
            action=AuditLog.ActionChoices.FIX,
            cve_id=vuln.cve_id,
            metadata={
                "notes": notes,
                "source": "api_fixed_endpoint"
            },
        )

    return {
        "updated": len(fixed_records),
        "cve_ids": cve_ids,
    }