from django.db import models

# Create your models here.
class FpQuery(models.Model):
    fingerprint = models.TextField()
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    result = models.IntegerField(null=True)
    time = models.DateTimeField(auto_now=True,auto_now_add=True,blank=True,null=True)

class TopAdsSnapshot(models.Model):
    media_id = models.IntegerField()
    rank = models.IntegerField()
    score = models.IntegerField()
    time = models.DateTimeField(auto_now=True,auto_now_add=True)
