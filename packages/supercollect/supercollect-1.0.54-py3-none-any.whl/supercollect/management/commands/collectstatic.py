from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.contrib.staticfiles.management.commands import collectstatic
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage,
    StaticFilesStorage,
    staticfiles_storage,
)

from supercollect.utils import get_all_files
import json


class Command(collectstatic.Command):
    """
    Uses FileSystemStorage to collect and post-process files.
    Then, files are uploaded.
    This significantly speeds up the process for remote locations.
    """

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--turbo",
            action="store_true",
            help="Use turbo mode.",
        )

    def set_options(self, **options):
        super().set_options(**options)
        self.turbo = options["turbo"]

    def collect(self):
        manifest_deployment, temp_storage = False, None

        if self.turbo:
            if hasattr(staticfiles_storage, "manifest_version"):
                manifest_deployment = True

            self.storage = temp_storage = (
                ManifestStaticFilesStorage(location=settings.STATIC_ROOT)
                if manifest_deployment
                else StaticFilesStorage(location=settings.STATIC_ROOT)
            )

        is_dry_run = self.dry_run

        if is_dry_run and self.turbo:
            self.dry_run = False
        
        report = super().collect()

        if not self.turbo:
            return report

        if is_dry_run:
            self.dry_run = True
        
        self.storage = staticfiles_storage

        report = {"modified": 0, "unmodified": 0}
        
        files_to_upload = get_all_files(temp_storage)

        if manifest_deployment:
            # Read old manifest
            try:
                with temp_storage.open("staticfiles.json") as manifest:
                    old_manifest = manifest.read().decode()
            except FileNotFoundError:
                old_manifest = None

            if old_manifest:
                # Read new manifest
                try:
                    with self.storage.open("staticfiles.json") as manifest:
                        new_manifest = manifest.read().decode()
                except FileNotFoundError:
                    new_manifest = None

                if new_manifest:
                    # Do diffing to determine which files to update
                    new_manifest = json.loads(new_manifest)["paths"]
                    old_manifest = json.loads(old_manifest)["paths"]

                    def get_files_to_upload(report):
                        for file_path in new_manifest:
                            if file_path not in old_manifest or old_manifest[file_path] != new_manifest[file_path]:
                                yield new_manifest[file_path]
                            else:
                                report["unmodified"] += 1
                        
                        yield "staticfiles.json"

                    files_to_upload = get_files_to_upload(report)

        with ThreadPoolExecutor(max_workers=32) as executor:
            for file in files_to_upload:
                if not self.dry_run:
                    executor.submit(self.upload, file, temp_storage)
                report["modified"] += 1

        return report

    def handle(self, **options):
        report = super().handle(**options)

        if not self.turbo:
            # Vanilla Django Report
            return report
        
        if self.dry_run:
            return f"super().would_have_collected(modified={str(report['modified'])}, unmodified={str(report['unmodified'])})"
        
        return f"super().collected(modified={str(report['modified'])}, unmodified={str(report['unmodified'])})"

    def upload(self, path, source_storage):
        with source_storage.open(path) as source_file:
            self.storage.save(path, source_file)
