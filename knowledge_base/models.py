from django.db import models

# Create your models here.

class CandidateStatus(models.Model):
    code = models.CharField(max_length=1)
    value = models.CharField(max_length=40)
    description = models.CharField(max_length=500)

class CommitteeDesignation(models.Model):
    code = models.CharField(max_length=1)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

class CommitteeType(models.Model):
    code = models.CharField(max_length=1)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

class ConnectedOrganization(models.Model):
    name = models.CharField(max_length=38)
    description = models.CharField(max_length=500)

class CoverageType(models.Model):
    name = models.CharField(max_length=50)

class BroadcastType(models.Model):
    name = models.CharField(max_length=50)

class IncumbentChallengerStatus(models.Model):
    code = models.CharField(max_length=1)
    value = models.CharField(max_length=11)
    description = models.CharField(max_length=500)

class InterestGroupCategory(models.Model):
    code = models.CharField(max_length=1)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500)

class IssueCategory(models.Model):
    name = models.CharField(max_length=100)
    parent =  models.ForeignKey("self", 
            null=True, 
            blank=True,
            related_name='children',
            on_delete=models.SET_NULL
            )

    def __unicode__(self):
        return '%s' % self.name

class Issue(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    issue_categories = models.ManyToManyField(IssueCategory,null=True,blank=True)

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

class Stance(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    issue = models.ForeignKey(Issue)

class Tag(models.Model):
    name = models.CharField(max_length=100)
    relevant = models.BooleanField(default=True)
    scraped = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.relevant == False and self.scraped == False:
            raise Exception('A manually entered tag must be relevant')
        else:
            super(Tag, self).save(*args, **kwargs)

