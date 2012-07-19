import urlparse
from django.shortcuts import render_to_response

from knowledge_base.models import Ad,Media,Funder,CommitteeType

def ad_profile(request, path):
    pass
#    if path[-1] == 'c':
#        template = 'ad/client_ad_profile.html'
#        ad_pk = path[:-1]
#    else:
#        ad_pk = path
#    ad = Ad.objects.get(pk=ad_pk)
#    c = Context({
#            'ad' : ad,
#            'funder' : ad.
