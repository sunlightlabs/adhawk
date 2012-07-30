import urlparse

from django.template import Context,RequestContext
from django.shortcuts import render_to_response

from knowledge_base.models import Ad, \
                                  Media, \
                                  Funder, \
                                  FunderFamily, \
                                  CommitteeType

def set_client(request):
    user_agent = request.META['HTTP_USER_AGENT']
    if user_agent == 'com.sunlightfoundation.com.adhawk.android':
        return 'android'
    elif user_agent == 'com.sunlightfoundation.com.adhawk.ios':
        return 'ios'
    else:
        return user_agent

def ad_profile(request, path):
    client = set_client(request)
    user_agent = request.META['HTTP_USER_AGENT']

    print 'user agent is %s'%(user_agent,)
    media = Media.objects.get(pk=path)
    #pk_pad = str(media.pk).zfill(5)
    c = RequestContext(request, {
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

def top_ads(request):
    client = set_client(request)
    ads = Ad.objects.filter(top_ad=True)
    medias = [a.media_set.get() for a in ads]
    c = RequestContext(request,{
            'client' : client,
            'medias' : medias,
            })
    return render_to_response('knowledge_base/top_ads.html',c)
    
