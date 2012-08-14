from django.core.management.base import BaseCommand
from django.db import transaction

from knowledge_base.models import Funder
from db_script.ie_importer import IEDescriptionImporter,IEIDImporter,API

class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        funders = Funder.objects.filter(IE_id=None)[:10]

        count = len(funders)

        print "%d funders to update"%(count,)

        for f in funders:
            i = IEIDImporter(f,ie_api=API)
            if i.ie_id:
                i.save_to_funder()
            count -= 1
            print "... %d more to go"%(count,)

        funders = Funder.objects.exclude(
                    IE_id=None
                ).filter(
                    description=None)

        for f in funders:
            d = IEDescriptionImporter(f,ie_api=API)
            if d.ie_description:
                d.save_to_funder()
