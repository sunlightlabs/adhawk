import urlparse

from django.template import Context
from django.shortcuts import render_to_response

from knowledge_base.models import Ad, \
                                  Media, \
                                  Funder, \
                                  FunderFamily, \
                                  CommitteeType

def ad_profile(request, path):
    if path[-1] == 'c':
        template = 'knowledge_base/client_ad_profile.html'
        media_pk = path[:-1]
    else:
        template = 'knowledge_base/ad_profile.html'
        media_pk = path
    media = Media.objects.get(pk=media_pk)
    pk_pad = str(media.pk).zfill(5)
    c = Context({
            'media' : media,
            'ad' : media.ad,
            'funder_family' : media.media_profile.funder.funder_family,
            'pk_pad' : pk_pad
            })
    return render_to_response(template,c)

def not_found(request):
    return render_to_response('knowledge_base/not_found.html')
