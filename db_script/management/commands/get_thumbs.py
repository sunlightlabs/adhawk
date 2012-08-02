from django.core.management.base import BaseCommand

from db_script.thumb_getter import ThumbDownloader
from knowledge_base.models import Media

#from db_script.log import set_up_logger

class Command(BaseCommand):

    def handle(self, *args, **options):

        if args:
            data_dir = sys.argv[1]
        else:
            data_dir = 'db_script/processing'

        #log = set_up_logger("thumb_download","db_script/processing")

        for media in Media.objects.filter(checked=False):
            #log.info("downloading thumbs for pk=%s"%media.pk)
            i = ThumbDownloader(media)
            i.get_thumbs()
