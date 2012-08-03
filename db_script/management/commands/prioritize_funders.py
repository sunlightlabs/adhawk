import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from knowledge_base.models import FunderFamily

from db_script.funder_prioritizer import FunderPrioritizer

GDRIVE_URL = "https://docs.google.com/spreadsheet/ccc?key=0Atj5O9EjlK8mdEFMbWJ5TTd0Z1NPSzZneVdkWUc0R2c"

log = logging.getLogger('db_script.funder_prioritizer')

class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        funderfamily_objects = FunderFamily.objects.exclude(
                total_independent_expenditures=0)

        priority_list = []

        for ffo in funderfamily_objects:
            fp = FunderPrioritizer(ffo)
            if fp.is_priority:
                priority_list.append(ffo)

        priority_list = sorted(priority_list,
                reverse=True,key=lambda x: x.total_independent_expenditures)

        
        email = "The following funders have no media profile yet.  To keep the database current, please find youtube user profiles for each and enter them into the reporting spreadsheet at %s.\n\n"%(GDRIVE_URL,)
        email += '\t'.join(
            ["FEC_id","Name","Total Independent Expenditures"])+'\n'

        for p in priority_list:
            email +='\t'.join([str(a) for a in [p.primary_FEC_id,p.name,
                    p.total_independent_expenditures]])+'\n'

        email +="\nThanks!"

        log.info(email)
