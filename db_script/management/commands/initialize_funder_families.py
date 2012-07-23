from django.core.management.base import BaseCommand
from django.db import transaction

from db_script.funder_family_initializer import FunderFamilyInitializer
from knowledge_base.models import Funder

from db_script.log import set_up_logger

class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        log = set_up_logger("funder_family_initialize","db_script/processing")

        funder_objects = Funder.objects.filter(funder_family=None)

        if funder_objects:
            print "%d funder_family values to initialize"%(len(funder_objects),)
            for funder_object in funder_objects:
                print "initializing funder_family for pk=%d"%(funder_object.pk,)
                ffi = FunderFamilyInitializer(funder_object)
                log.info(ffi.assign_new_funder_family())
