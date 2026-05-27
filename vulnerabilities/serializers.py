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



class SyncRequestSerializer(serializers.Serializer):
    cve_id = serializers.CharField(
        required=False
    )

    pub_start_date = serializers.DateTimeField(
        required=False
    )

    pub_end_date = serializers.DateTimeField(
        required=False
    )

    page = serializers.IntegerField(
        required=False,
        default=0
    )

    limit = serializers.IntegerField(
        required=False,
        default=20
    )


class FixedVulnerabilityRequestSerializer(serializers.Serializer):
    cve_ids = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )
    notes = serializers.CharField(required=False, allow_blank=True)