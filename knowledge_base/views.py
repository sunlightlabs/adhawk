import urlparse

from django.template import Context
from django.shortcuts import render_to_response

from knowledge_base.models import Ad, \
                                  Media, \
                                  Funder, \
                                  FunderFamily, \
                                  CommitteeType

def ad_profile(request, path):
    client = request.GET.get('client','normal')
    media = Media.objects.get(pk=path)
    #pk_pad = str(media.pk).zfill(5)
    c = Context({
            'client' : client,
            'media' : media,
            'ad' : media.ad,
            'funder_family' : media.media_profile.funder.funder_family,
            #'pk_pad' : pk_pad
            })
    return render_to_response('knowledge_base/ad_profile.html',c)

# NO LONGER NEEDED, MOVED TO NATIVE VIEW
#def not_found(request):
#    return render_to_response('knowledge_base/not_found.html')

def top_ads(request,path):
    client = request.GET.get('client','normal')
    ads = Ad.objects.filter(top_ad=True)
    medias = [a.media_set.get() for a in ads]
    c = Context({
            'client' : client,
            'medias' : medias,
            })
    return render_to_response('knowledge_base/top_ads.html',c)
    
