import requests
import json

from knowlege_base.models import Media

API_KEY = '3_BLRB_2LlQJZDUW1wb9_ZOps-sOnnzA_e6xxNSwJBBGoB-SavmPAKHkaVVZPE5Kx8' 
SECRET = 'ZXW+RovYBpK3NxA9ZcN//yoMcbZ4A8dCel/ju+YNDQQ='
GIGYA_ENDPOINT = "https://socialize-api.gigya.com/socialize.shortenURL"

class GigyaURLImporter():
    def __init__(self,media_object):
        self.media = media_object
    def get_gigya_url(self):
        payload = { 'apiKey' : API_KEY,
                    'secret': SECRET,
                    'url':'http://adhawk.sunlightfoundation.com/ad/%d'%media.pk,
                    'cid':'[Ad Hawk] ad-profile_%d_%d'%(media.pk,media.media_profile.funder.pk),
                    'format':'json', 
                    'httpStatusCodes':'false' }

        r = requests.get(GIGYA_ENDPOINT, params=payload)
        response = json.loads(r.text)
        if response['statusCode'] == 200:
            media.gigya_url = response['shortURL']
        else:
            print 'error on media',media.pk,'status',response['statusCode'],'reason:',response['statusReason']
