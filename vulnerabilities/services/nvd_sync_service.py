import requests
from vulnerabilities.models import Vulnerability
from vulnerabilities.utils.nvd_parser import (
    extract_severity,
    extract_score,
    extract_description,
    parse_date,
)
from vulnerabilities.constants import (
    NVD_DEFAULT_PAGE,
    NVD_DEFAULT_LIMIT,
)


NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"



def fetch_nvd_vulnerabilities(params: dict):
    response = requests.get(NVD_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def build_params(
    cve_id=None,
    pub_start_date=None,
    pub_end_date=None,
    page=NVD_DEFAULT_PAGE,
    limit=NVD_DEFAULT_LIMIT,
):
    params = {
        "startIndex": page,
        "resultsPerPage": limit,
    }

    if cve_id:
        params["cveId"] = cve_id

    if pub_start_date:
        params["pubStartDate"] = pub_start_date

    if pub_end_date:
        params["pubEndDate"] = pub_end_date

    return params


def sync_vulnerabilities(payload: dict):
    items = payload.get("vulnerabilities", [])

    created, updated = 0, 0

    for item in items:
        cve = item.get("cve")
        if not cve:
            continue

        obj, created_flag = Vulnerability.objects.update_or_create(
            cve_id=cve.get("id"),
            defaults={
                "description": extract_description(cve),
                "severity": extract_severity(cve),
                "score": extract_score(cve),
                "published_at": parse_date(cve.get("published")),
                "last_modified_at": parse_date(cve.get("lastModified")),
                "raw_payload": cve,
                "source": "NVD",
            },
        )

        if created_flag:
            created += 1
        else:
            updated += 1

    return {
        "created": created,
        "updated": updated,
        "total": len(items),
    }


def run_nvd_sync(
    cve_id=None,
    pub_start_date=None,
    pub_end_date=None,
    page=NVD_DEFAULT_PAGE,
    limit=NVD_DEFAULT_LIMIT,
):
    params = build_params(
        cve_id=cve_id,
        pub_start_date=pub_start_date,
        pub_end_date=pub_end_date,
        page=page,
        limit=limit,
    )

    raw = fetch_nvd_vulnerabilities(params)
    return sync_vulnerabilities(raw)