from django.utils.dateparse import parse_datetime
from django.utils.dateparse import parse_datetime
from django.utils import timezone

def extract_severity(cve: dict):
    metrics = cve.get("metrics", {})

    if "cvssMetricV31" in metrics:
        return metrics["cvssMetricV31"][0]["cvssData"]["baseSeverity"]

    if "cvssMetricV30" in metrics:
        return metrics["cvssMetricV30"][0]["cvssData"]["baseSeverity"]

    if "cvssMetricV2" in metrics:
        return metrics["cvssMetricV2"][0]["baseSeverity"]

    return "UNKNOWN"


def extract_score(cve: dict):
    metrics = cve.get("metrics", {})

    if "cvssMetricV31" in metrics:
        return metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]

    if "cvssMetricV30" in metrics:
        return metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]

    if "cvssMetricV2" in metrics:
        return metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]

    return None


def extract_description(cve: dict):
    for desc in cve.get("descriptions", []):
        if desc.get("lang") == "en":
            return desc.get("value")
    return ""


def parse_date(value):
    if not value:
        return None

    dt = parse_datetime(value)

    if dt is None:
        return None

    # convertir a timezone aware
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())

    return dt