from django.core.management.base import BaseCommand
from django.db import transaction

from db_script.stats_uploader import RMSEUploader
from knowledge_base.models import Media

#from db_script.log import set_up_logger

class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        if args:
            data_dir = sys.argv[1]
        else:
            data_dir = 'db_script/processing'

        #log = set_up_logger("","db_script/processing")

        rmse = RMSEUploader()
        rmse.upload()
