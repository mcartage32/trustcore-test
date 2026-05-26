from django.contrib import admin
from .models import Vulnerability, FixedVulnerability, AuditLog

admin.site.register(Vulnerability)
admin.site.register(FixedVulnerability)
admin.site.register(AuditLog)