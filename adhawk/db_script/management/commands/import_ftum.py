from django.core.management.base import BaseCommand
from django.db import transaction

from db_script.ftum_importer import FTUMImporter


class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        i = FTUMImporter()
        i.upload_data()
        i.update_families()
