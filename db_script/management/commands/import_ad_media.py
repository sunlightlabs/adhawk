import sys

from django.core.management.base import BaseCommand
from django.db import transaction

from db_script.ad_media_importer import YouTubeMediaImporter
from db_script.ad_media_reporter import AdMediaReporter
from knowledge_base.models import MediaType,MediaProfile

if sys.argv[1] == 'test':
    TEST = True
else:
    TEST = False

class Command(BaseCommand):

    def get_youtube_profiles(self):
        mt = MediaType.objects.get(main_url='http://www.youtube.com')
        if TEST:
            return mt,[mt.mediaprofile_set.all()[0]]
        else:
            return mt,mt.mediaprofile_set.iterator()


    @transaction.commit_on_success
    def handle(self, *args, **options):

        media_type,media_profile_iterator = self.get_youtube_profiles()

        count = 0

        for media_profile in media_profile_iterator:
            ytmi = YouTubeMediaImporter(media_type=media_type, \
                                        media_profile=media_profile)
            count += ytmi.upload()


