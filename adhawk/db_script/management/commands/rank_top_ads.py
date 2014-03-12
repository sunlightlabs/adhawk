from django.core.management.base import BaseCommand
from django.db import transaction

from db_script.top_ads_ranker import TopAdsRanker
from knowledge_base.models import Ad,Media

class Command(BaseCommand):
    
    @transaction.commit_on_success
    def handle(self, *args, **options):
        for a in Ad.objects.filter(top_ad=True):
            a.top_ad = False
            a.save()

        tar = TopAdsRanker()
        top_ten = tar.get_top(10)
        for k,v in top_ten:
            media_object = Media.objects.get(pk=k)
            ad_object = media_object.ad
            ad_object.top_ad = True
            ad_object.save()
