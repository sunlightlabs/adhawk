from django.core.management.base import BaseCommand
from django.db import transaction

from db_script.fec_kb_updater import CandidateImporter,CommitteeImporter


class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        if args:
            data_dir = args[0]
        else:
            data_dir = 'db_script/processing'

        cni = CandidateImporter(data_dir)
        cni.update()
        
        cmi = CommitteeImporter(data_dir)
        cmi.update()

