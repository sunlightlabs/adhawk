import urlparse
import json
from collections import defaultdict

from influenceexplorer import InfluenceExplorer

from django.template import Context,RequestContext
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from knowledge_base.models import Ad, \
                                  Media, \
                                  Funder, \
                                  FunderFamily, \
                                  CommitteeType

from whopaid_api.views import make_media_response_dict,BASE_URL,SHARE_TEXT

API = InfluenceExplorer('***REMOVED***')

class Contributor():
    def __init__(self,name,amount):
        self.name = name
        self.amount = amount

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
    
def get_top_contribs(funder_family):
    contrib_data = defaultdict(float)
    for f in funder_family.funder_set.all():
        if f.IE_id:
            for e in API.org.fec_top_contribs(f.IE_id):
                contrib_data[e['contributor_name']] += float(e['amount'])
        else:
            continue
    if contrib_data:
        return sorted([Contributor(name,amount) for name,amount in
            contrib_data.items()],key=lambda x: x.amount, reverse=True)
    else:
        return None

def funder_family_profile(request, path):
    client = set_client(request)
    funder_family = FunderFamily.objects.get(slug=path)
    funders = funder_family.funder_set.all()
    media_profiles = []
    for funder in funders:
        if funder.media_profile_assigned:
            for media_profile in funder.mediaprofile_set.all():
                media_profiles.append(media_profile)
    media_list = []
    for media_profile in media_profiles:
        for media in media_profile.media_set.filter(valid=True,checked=True):
            media_list.append(media)
    paginator = Paginator(media_list,15)
    page = request.GET.get('page')
    try:
        medias = paginator.page(page)
    except PageNotAnInteger:
        medias = paginator.page(1)
    except EmptyPage:
        medias = paginator.page(paginator.num_pages)
    c = RequestContext(request, {
            'client'        : client,
            'medias'        : medias,
            'funder_family' : funder_family,
            })
    return render_to_response('knowledge_base/funder_family_profile.html',c)
    
def ad_profile(request, path):
    client = set_client(request)
    try:
        user_agent = request.META['HTTP_X_CLIENT_APP']
    except KeyError:
        user_agent = request.META['HTTP_USER_AGENT']
    print 'user agent is %s'%(user_agent,)
    #print request.META.keys()
    media = Media.objects.get(slug=path)
    funder_family = media.media_profile.funder.funder_family
    try:
        top_contribs = get_top_contribs(funder_family)
    except:
        top_contribs = None
    #pk_pad = str(media.pk).zfill(5)
    c = RequestContext(request, {
            'client' : client,
            'media' : media,
            'ad' : media.ad,
            'funder_family' : funder_family,
            'top_contribs' : top_contribs,
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
