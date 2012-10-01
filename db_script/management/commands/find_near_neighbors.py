from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction

from superfastmatch import client

from knowledge_base.models import Media,MediaNearNeighbor


sfm_client = client.Client(url='http://127.0.0.1:9000/')

#out = open('sfm_results.csv','w')
true = True
false = False

class Command(BaseCommand):

    def handle(self, *args, **options):
        for mmn in MediaNearNeighbor.objects.all():
            mmn.delete()

        for m in Media.objects.filter(ingested=True):
            doc = eval(sfm_client.get(1,m.id))
            comp_list = []
            for other_doc in doc['documents']['rows']:
                shared = 0
                for frag in other_doc['fragments']:
                    shared += frag[2]
                comp_list.append((other_doc['docid'],shared))
                #out.write('\t'.join([str(a) for a in [m.id,other_doc['docid'],shared]]))
                #out.write('\n')
            comp_list = sorted(comp_list,key=lambda x: x[1],reverse=True)[0:10]
            l = min([len(comp_list),10])
            for i in range(l):
                od,s = comp_list[i]
                m2 = Media.objects.get(id=od)
                mnn = MediaNearNeighbor(media=m,neighbor=m2,rank=i+1)
                mnn.save()

        #out.close()
