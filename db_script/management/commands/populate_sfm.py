from collections import defaultdict
import urlparse
import json
import os

from django.core.management.base import BaseCommand

from superfastmatch import client

from whopaid import settings
from echoprint_server_api import fp
from knowledge_base.models import Media

CODEGEN_DIR = os.path.join(settings.MEDIA_ROOT,'codegens')
#CODEGEN_DIR = '/home/blannon/test_set/codegens'

sfm_client = client.Client(url='http://127.0.0.1:9000/')

class Command(BaseCommand):
    def handle(self, *args, **options):
        w = os.walk(CODEGEN_DIR)
        d,dns,fns = w.next()
        for fn in fns:
            media_id = int(fn.split('_')[1])
            try:
                media_object = Media.objects.get(id=media_id)
            except Media.DoesNotExist:
                print '%s has no media object!'%(fn,)
                continue
            dd = eval(open(os.path.join(d,fn)).read())
            try:
                code_string = ' '.join(fp.decode_code_string(dd['code']).split()[::2])
            except KeyError:
                print '%s has no code!'%(fn,)
            res = sfm_client.add(1,media_id,code_string,title=media_object.ad.title)
            if res['success']:
                continue
            else:
                print "problem ingesting Media object %d"%(media_id,)
