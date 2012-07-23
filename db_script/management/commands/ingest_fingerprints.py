import os

from django.core.management.base import BaseCommand
from django.db import transaction

from db_script.fingerprinter import Fingerprinter
from db_script.log import set_up_logger
from whopaid.settings import MEDIA_ROOT
from knowledge_base.models import Media

VIDEO_DIR = os.path.join(MEDIA_ROOT,'videos')

class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        log = set_up_logger('fingerprinter','db_script/processing')

        w = os.walk(VIDEO_DIR)
        medias = Media.objects.filter(ingested=False)
        pks = [m.pk for m in medias]
        dirpath, dirnames, fnames = w.next()
        loc_dic = {}
        for fn in fnames:
            pk = int(fn.split('_')[1])
            if pk in pks:
                loc_dic[pk] = os.path.join(dirpath,fn)
        if loc_dic:
            for media_pk,loc in loc_dic.items():
                print "fingerprinting %s"%loc
                f = Fingerprinter(loc)
                log.info(f.get_codegen())
        else:
            print "Nothing to ingest"
