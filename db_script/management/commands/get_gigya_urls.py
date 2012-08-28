from django.core.management.base import BaseCommand
from django.db import transaction

from knowledge_base.models import Media
from db_script.gigya_url_importer import GigyaURLImporter

class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        media_objects = Media.objects.filter(gigya_url=None)

        for media_object in media_objects:
            i = GigyaURLImporter(media_object)
            i.get_gigya_url()
