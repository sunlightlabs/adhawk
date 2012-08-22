import requests
import json

from knowlege_base.models import Media

API = 
secret = 

payload = { 'apiKey' : API,
            'secret':secret,
            'url':'http://adhawk.sunlightfoundation.com/ad/%d'%media.pk,
            'cid':'[Ad Hawk] ad-profile_%d_%d'%(media.pk,media.media_profile.funder.pk)
            'format':'json', 'httpStatusCodes':'false' }

r = requests.get("https://socialize-api.gigya.com/socialize.shortenURL", params=payload)
response = json.loads(r.text)
if response['statusCode'] == 200:
    media.gigya_url = response['shortURL']
else:
    print 'error on media',media.pk,'status',response['statusCode'],'reason:',response['statusReason']
