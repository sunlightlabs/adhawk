from django.core.management.base import BaseCommand

from db_script.ad_media_reporter import AdMediaReporter

class Command(BaseCommand):
    def handle(self, *args, **options):
        amr = AdMediaReporter()
