from whopaid_api.models import FpQuery
from knowledge_base.models import Media
from echoprint_server_api import fp

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

try: 
    import json
except ImportError:
    import simplejson as json

# Create your views here.

BASE_URL = 'http://adhawk.sunlightfoundation.com/ad/%s'

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
        path = str(media.pk)+'c'
        response_data['result_url'] = BASE_URL%(path,)
        return HttpResponse(json.dumps(response_data),
                mimetype="application/json")
    else:
        response_data['result_url'] = None
        return HttpResponse(json.dumps(response_data),
                mimetype="application/json")
