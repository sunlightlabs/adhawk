import urlparse,httplib

from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)
    profile_page_url = models.URLField(max_length=100)
            
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
    issues = models.ManyToManyField(Issue,null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.relevant == False and self.scraped == False:
            raise Exception('A manually entered tag must be relevant')
        else:
            super(Tag, self).save(*args, **kwargs)

class Candidate(models.Model):
    FEC_id = models.CharField(max_length=9)
    name = models.CharField(max_length=38)
    party = models.CharField(max_length=3)
    year_of_election = models.IntegerField(max_length=4,null=True,blank=True)
    street_one = models.CharField(max_length=34)
    street_two = models.CharField(max_length=34)
    city = models.CharField(max_length=18)
    state = models.CharField(max_length=2)
    zip_code = models.IntegerField(max_length=5)


    incumbent_challenger_status = models.ForeignKey(IncumbentChallengerStatus)
    candidate_status = models.ForeignKey(CandidateStatus)

    stances = models.ManyToManyField(Stance)

class Funder(models.Model):
    FEC_id = models.CharField(max_length=9)
    name = models.CharField(max_length=90)
    treasurer_name = models.CharField(max_length=38)
    street_one = models.CharField(max_length=34)
    street_two = models.CharField(max_length=34)
    city = models.CharField(max_length=18)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    filing_frequency = models.CharField(max_length=1)
    party = models.CharField(max_length=3)

    #FK fields
    interest_group_category = models.ForeignKey(InterestGroupCategory, 
            on_delete=models.PROTECT)
    committee_type = models.ForeignKey(CommitteeType, 
            on_delete=models.PROTECT)
    committee_designation = models.ForeignKey(CommitteeDesignation,
            on_delete=models.PROTECT)
    connected_organization = models.ForeignKey(ConnectedOrganization,
            null=True, 
            blank=True,
            on_delete=models.SET_NULL)

    #MTM fields
    stances = models.ManyToManyField(Stance,null=True,blank=True)
    candidates = models.ManyToManyField(Candidate,
            through="FunderToCandidate",
            blank=True,
            null=True)

class FunderToCandidate(models.Model):
    funder = models.ForeignKey(Funder)
    candidate = models.ForeignKey(Candidate)
    relationship = models.CharField(max_length=50)

class MediaProfile(models.Model):
    url = models.URLField()

    # FK relations
    funder = models.ForeignKey(Funder,
            null=True,
            blank=True,
            on_delete=models.SET_NULL)
    media_type = models.ForeignKey(MediaType,
            on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        sr = urlparse.urlsplit(self.url)
        conn = httplib.HTTPConnection(sr.netloc)
        conn.request("HEAD",sr.path)
        status = conn.getresponse().status
        if status == 200:
            super(MediaProfile, self).save(*args, **kwargs)
        else:
            raise Exception('not a working url')

class Media(models.Model):
    url = models.URLField()
    creator_description = models.CharField(max_length=500,default="No description available.")
    curator_description = models.CharField(max_length=500,blank=True,null=True)
    link_broken = models.BooleanField(default=False)

    # FK relations
    media_profile = models.ForeignKey(MediaProfile,
            on_delete=models.PROTECT)

    # MTM relations
    tags = models.ManyToManyField(Tag)

class Ad(models.Model):
    title = models.CharField(max_length=200)
    ingested = models.BooleanField(default=False)
    
    # OTO relation
    media = models.OneToOneField(Media,on_delete=models.PROTECT)

    # MTM relations
    markets = models.ManyToManyField(Market,
            blank=True,
            null=True)
    broadcast_types = models.ManyToManyField(BroadcastType,
            blank=True,
            null=True)
    stances = models.ManyToManyField(Stance,
            blank=True,
            null=True)

    # MTM through relation
    candidates = models.ManyToManyField(Candidate,
            through='AdToCandidate')

class AdToCandidate(models.Model):
    CHOICES = (
            ('POS','Positive'),
            ('NEG','Negative'),
            ('NEU','Neutral'),
            )
    ad = models.ForeignKey(Ad)
    candidate = models.ForeignKey(Candidate)
    portrayal = models.CharField(max_length=3,choices=CHOICES)

class Coverage(models.Model):
    url = models.URLField()
    headline = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateField()

    # FK relations
    source = models.ForeignKey(Source,on_delete=models.PROTECT)
    coverage_type = models.ForeignKey(CoverageType,null=True,blank=True,on_delete=models.SET_NULL)
    
    # MTM relations
    tags = models.ManyToManyField(Tag,null=True,blank=True)
    ads = models.ManyToManyField(Ad,null=True,blank=True)
    issues = models.ManyToManyField(Issue,null=True,blank=True)
    candidates = models.ManyToManyField(Candidate,null=True,blank=True)
    funders = models.ManyToManyField(Funder,null=True,blank=True)
    authors = models.ManyToManyField(Author,null=True,blank=True)
    stances = models.ManyToManyField(Stance,null=True,blank=True)






