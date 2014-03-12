from django.core.management.base import BaseCommand
from django.db import transaction

from db_script.fec_importer import FECImporter


class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        if args:
            data_dir = sys.argv[1]
        else:
            data_dir = 'db_script/processing'

        i = FECImporter(data_dir)
        i.update_csv()
        i.update_db()
