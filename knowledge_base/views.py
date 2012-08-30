import urlparse
import json

from django.template import Context,RequestContext
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from knowledge_base.models import Ad, \
                                  Media, \
                                  Funder, \
                                  FunderFamily, \
                                  CommitteeType

from whopaid_api.views import make_media_response_dict,BASE_URL,SHARE_TEXT


def set_client(request):
    try:
        user_agent = request.META['HTTP_X_CLIENT_APP']
    except KeyError:
        return request.META['HTTP_USER_AGENT']
    if 'com.sunlightfoundation.adhawk.android' in user_agent:
        return 'android'
    elif 'com.sunlightfoundation.adhawk.ios' in user_agent:
        return 'ios'
    else:
        return user_agent

def ad_profile(request, path):
    client = set_client(request)
    try:
        user_agent = request.META['HTTP_X_CLIENT_APP']
    except KeyError:
        user_agent = request.META['HTTP_USER_AGENT']
    print 'user agent is %s'%(user_agent,)
    #print request.META.keys()
    media = Media.objects.get(slug=path)
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

#@csrf_exempt
def top_ad_select(request,path):
    client = set_client(request)
    if client in ['android','ios']:
        media = Media.objects.get(pk=path)
        response_data = make_media_response_dict(media)
        return HttpResponse(json.dumps(response_data),
                mimetype="application/json")
    else:
        return redirect('/ad/%s/'%(path))
