from django.core.management.base import BaseCommand
from django.db import transaction

from knowledge_base.models import FunderFamily

from db_script.funder_prioritizer import FunderPrioritizer

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

        for p in priority_list:
            print '\t'.join([str(a) for a in [p.primary_FEC_id,p.name,
                    p.total_independent_expenditures]])
