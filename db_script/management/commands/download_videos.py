from django.core.management.base import BaseCommand
from django.db import transaction

from db_script.video_downloader import VideoDownloader
from knowledge_base.models import Media

#from db_script.log import set_up_logger

class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        #log = set_up_logger("video_download.log","db_script/processing")

        media_objects = Media.objects.filter(downloaded=False,
                                             valid=True,
                                             checked=True)
        
        if media_objects:
            print "%d videos to download"%len(media_objects)
            for media_object in media_objects:
                print "downloading videos for pk=%d"%media_object.pk
                vd = VideoDownloader(media_object)
                vd.download_file()
                #log.info(vd.download_file())
        else:
            print "Nothing to download"
