from rest_framework import serializers
from .models import Vulnerability


class VulnerabilityFilterSerializer(serializers.Serializer):
    cve_id = serializers.CharField(required=False)
    published_from = serializers.DateField(required=False)
    published_to = serializers.DateField(required=False)
    severity = serializers.ChoiceField(
        choices=Vulnerability.SeverityChoices.choices,
        required=False
    )
    status = serializers.ChoiceField(
        choices=Vulnerability.StatusChoices.choices,
        required=False
    )


class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = [
            "id",
            "cve_id",
            "description",
            "severity",
            "score",
            "status",
            "published_at",
            "last_modified_at",
            "source",
        ]

class SyncResponseSerializer(serializers.Serializer):
    created = serializers.IntegerField()
    updated = serializers.IntegerField()
    total = serializers.IntegerField()