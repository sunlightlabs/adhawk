from django.db import models

# Create your models here.
class FpQuery(models.Model):
    fingerprint = models.TextField()
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    result = models.IntegerField(null=True)
