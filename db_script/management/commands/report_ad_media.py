from django.core.management.base import BaseCommand

from db_script.ad_media_reporter import AdMediaReporter
from knowledge_base.models import Media

class Command(BaseCommand):

    def handle(self, *args, **options):
        count = Media.objects.filter(checked=False)
        amr = AdMediaReporter(count)
