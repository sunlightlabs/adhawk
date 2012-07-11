from django.core.management.base import BaseCommand
from django.db import transaction,connections

from db_script.reporting_kb_updater import *

class Command(BaseCommand):

    def check_youtube_entries(self):
        conn = connections['default']
        c = conn.cursor()
        c.execute("select distinct youtube_channel_url from reporting_youtube where youtube_channel_url is not null")
        yt_urls = [a[0] for a in c.fetchall()]
        l = [MediaProfileFilter(i) for i in yt_urls]
        bad = [j for j in l if not j.ok_url]
        if bad:
            return bad
        else:
            return False

    @transaction.commit_on_success
    def handle(self, *args, **options):

        bad = self.check_youtube_entries()

        if bad:
            badlist = ['\n'.join(bad)]
            raise Exception("Clean up these entries: %s"%(badlist,))
        else:
            i = MediaProfileImporter()
            i.upload()
