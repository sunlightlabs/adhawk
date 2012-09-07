from whopaid_api.models import FpQuery
from knowledge_base.models import Media,FunderFamily
from echoprint_server_api import fp

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

try: 
    import json
except ImportError:
    import simplejson as json

# Create your views here.

BASE_URL = 'http://adhawk.sunlightfoundation.com/ad/%s/'
SHARE_TEXT = 'I just used Ad Hawk from @sunfoundation to discover the sponsor behind this ad: %s'

def lookup(fingerprint):
    if len(fingerprint):
        decoded = fp.decode_code_string(fingerprint)
        result = fp.best_match_for_query(decoded)
        if result.match():
            return result.TRID
        else:
            return False
    else:
        return False

def make_media_response_dict(media):
    response_data = {}
    #result_url = BASE_URL %(str(media.pk),)
    result_url = media.gigya_url
    response_data['result_url'] = result_url
    response_data['share_text'] = SHARE_TEXT%(result_url,)
    return response_data


@csrf_exempt
def fp_search(request):
    json_request = json.loads(request.body)
    fingerprint = json_request['fingerprint']
    lat = json_request['lat']
    lon = json_request['lon']

    response_data = {}

    result = lookup(fingerprint)

    if result:
        fpquery = FpQuery(fingerprint=fingerprint, \
                lat=lat, \
                lon=lon, \
                result=result)
        fpquery.save()
        media = Media.objects.get(pk=result)
        response_data = make_media_response_dict(media)
        return HttpResponse(json.dumps(response_data),
                mimetype="application/json")
    else:
        response_data['result_url'] = None
        response_data['share_text'] = None
        return HttpResponse(json.dumps(response_data),
                mimetype="application/json")

@csrf_exempt
def site_mapping(request):
    base_ah_url = '/sponsor/%s/'
    base_ie_url = '/organization/%s/%s/'
    funder_families = FunderFamily.objects.exclude(ftum_url=None)
    response_data = {'committees': [] }
    for ff in funder_families:
        ff_data = { 'primary_fec_id': ff.primary_FEC_id,
                    'fec_ids': [], 
                    'name': ff.name,
                    'ftum_url': ff.ftum_url,
                    'adhawk_url': base_ah_url%(ff.slug,) }
        for f in ff.funder_set.all():
            ff_data['fec_ids'].append(f.FEC_id)
        if ff.IE_id:
            ff_data['ie_url'] = base_ie_url%(ff.slug,ff.IE_id)
        response_data['committees'].append(ff_data)
    return HttpResponse(json.dumps(response_data,sort_keys=True,indent=4),
                        mimetype="application/json")
