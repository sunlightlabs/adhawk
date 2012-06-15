from django.db import models

# Create your models here.

class CommitteeDesignation(models.Model):
    COMMITTEE_DESIGNATION_CHOICES = (('A','AUTHORIZED BY A CANDIDATE'),
            ('B','LOBBYIST/REGISTRANT PAC'),
            ('D','LEADERSHIP PAC'),
            ('J','JOINT FUND RAISER'),
            ('P','PRINCIPAL CAMPAIGN COMMITTEE OF A CANDIDATE'),
            ('U','UNAUTHORIZED'),)
    committee_designation_type = models.CharField(max_length=1, 
            choices=COMMITTEE_DESIGNATION_CHOICES)


class CoverageType(models.Model):
    name = models.CharField(max_length=50)

class BroadcastType(models.Model):
    name = models.CharField(max_length=50)

class Market(models.Model):
    MARKET_TYPE_CHOICES = (('A','Area'),
            ('C','County'),
            ('S','State'),
            ('N','Nationwide'),
            )
    market_type = models.CharField(max_length=1,choices=MARKET_TYPE_CHOICES)
    name = models.CharField(max_length=50)

class MediaType(models.Model):
    main_url = models.URLField(max_length=50)
    scraper_added = models.BooleanField(default=False)

class Source(models.Model):
    main_url = models.URLField(max_length=50)
    scraper_added = models.BooleanField(default=False)
