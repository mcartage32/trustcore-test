from django.core.management.base import BaseCommand
from vulnerabilities.services.nvd_sync_service import run_nvd_sync


class Command(BaseCommand):
    help = "Sync vulnerabilities from NVD API"

    def add_arguments(self, parser):
        parser.add_argument("--page", type=int, default=0)
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        self.stdout.write("Starting NVD sync...")

        page = options["page"]
        limit = options["limit"]

        result = run_nvd_sync(
            page=page,
            limit=limit
        )

        self.stdout.write(self.style.SUCCESS(
            f"Sync completed: {result}"
        ))