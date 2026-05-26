from django.conf import settings
from django.db import models


class Vulnerability(models.Model):
    class SeverityChoices(models.TextChoices):
        CRITICAL = "CRITICAL", "Critical"
        HIGH = "HIGH", "High"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"
        UNKNOWN = "UNKNOWN", "Unknown"

    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        FIXED = "FIXED", "Fixed"
        DEPRECATED = "DEPRECATED", "Deprecated"

    cve_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )
    description = models.TextField()
    severity = models.CharField(
        max_length=20,
        choices=SeverityChoices.choices,
        default=SeverityChoices.UNKNOWN
    )
    score = models.FloatField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True
    )
    last_modified_at = models.DateTimeField(
        null=True,
        blank=True
    )
    source = models.CharField(
        max_length=20,
        default="NVD"
    )

    # payload originally NIST
    raw_payload = models.JSONField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "vulnerabilities"
        ordering = ["-published_at"]

    def __str__(self):
        return self.cve_id


class FixedVulnerability(models.Model):
    vulnerability = models.ForeignKey(
        Vulnerability,
        on_delete=models.CASCADE,
        related_name="fixed_records"
    )
    fixed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    notes = models.TextField(
        null=True,
        blank=True
    )
    fixed_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "fixed_vulnerabilities"
        unique_together = ("vulnerability", "fixed_by")

    def __str__(self):
        return f"{self.vulnerability.cve_id} fixed by {self.fixed_by}"


class AuditLog(models.Model):
    class ActionChoices(models.TextChoices):
        FIX = "FIX", "Fix"
        UNFIX = "UNFIX", "Unfix"
        SYNC = "SYNC", "Sync"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(
        max_length=20,
        choices=ActionChoices.choices
    )
    cve_id = models.CharField(
        max_length=50,
        db_index=True
    )
    metadata = models.JSONField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "audit_logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.cve_id}"