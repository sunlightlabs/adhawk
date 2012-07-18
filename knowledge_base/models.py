import urlparse,httplib

from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)
    profile_page_url = models.URLField(max_length=100, 
            verbose_name='Profile page URL',
            null=True)

    def __unicode__(self):
        return self.name
            
class CandidateStatus(models.Model):
    code = models.CharField(max_length=1)
    value = models.CharField(max_length=40,null=True)
    description = models.CharField(max_length=500,null=True)

    def __unicode__(self):
        return "%s - %s"%(self.code,self.value)

class CommitteeDesignation(models.Model):
    code = models.CharField(max_length=1)
    name = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=500,null=True)

    def __unicode__(self):
        return "%s - %s"%(self.code,self.name)

class CommitteeType(models.Model):
    code = models.CharField(max_length=1)
    name = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=500,null=True)

    def __unicode__(self):
        return "%s - %s"%(self.code,self.name)

class ConnectedOrganization(models.Model):
    name = models.CharField(max_length=38)
    description = models.CharField(max_length=500,null=True,blank=True)

    def __unicode__(self):
        return self.name.title()

class CoverageType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class BroadcastType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class IncumbentChallengerStatus(models.Model):
    code = models.CharField(max_length=1)
    value = models.CharField(max_length=11,null=True)
    description = models.CharField(max_length=500,null=True)

    def __unicode__(self):
        return '%s - %s'%(self.code,self.value)

class InterestGroupCategory(models.Model):
    code = models.CharField(max_length=1)
    name = models.CharField(max_length=40,null=True)
    description = models.CharField(max_length=500,null=True)

    def __unicode__(self):
        return '%s - %s'%(self.code,self.name)

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

    def __unicode__(self):
        return self.name

class Market(models.Model):
    MARKET_TYPE_CHOICES = (('A','Area'),
            ('C','County'),
            ('S','State'),
            ('N','Nationwide'),
            )
    MARKET_TYPE_DICT = {'A':'Area',
            'C':'County',
            'S':'State',
            'N':'Nationwide'
            }
    market_type = models.CharField(max_length=1,choices=MARKET_TYPE_CHOICES)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        try:
            mt = self.MARKET_TYPE_DICT[self.market_type]
            return "%s (%s)"%(self.name,mt)
        except KeyError:
            return "%s (%s)"%(self.name,self.market_type)

class MediaType(models.Model):
    main_url = models.URLField(max_length=50)
    scraper_added = models.BooleanField(default=False)

    def __unicode__(self):
        return self.main_url

class Source(models.Model):
    main_url = models.URLField(max_length=50)
    scraper_added = models.BooleanField(default=False)

    def __unicode__(self):
        return self.main_url

class Stance(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    issue = models.ForeignKey(Issue)

    def __unicode__(self):
        return "[%s] %s"%(self.name,self.issue.name)

class Tag(models.Model):
    name = models.CharField(max_length=100)
    relevant = models.BooleanField(default=True)
    scraped = models.BooleanField(default=True)
    issues = models.ManyToManyField(Issue,null=True,blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.relevant == False and self.scraped == False:
            raise Exception('A manually entered tag must be relevant')
        else:
            super(Tag, self).save(*args, **kwargs)

class Candidate(models.Model):
    FEC_id = models.CharField(max_length=9)
    name = models.CharField(max_length=38)
    party = models.CharField(max_length=3,null=True,blank=True)
    year_of_election = models.IntegerField(max_length=4,null=True,blank=True)
    street_one = models.CharField(max_length=34,null=True,blank=True)
    street_two = models.CharField(max_length=34,null=True,blank=True)
    city = models.CharField(max_length=18,null=True,blank=True)
    state = models.CharField(max_length=2,null=True,blank=True)
    zip_code = models.IntegerField(max_length=5,null=True,blank=True)


    incumbent_challenger_status = models.ForeignKey(
            IncumbentChallengerStatus,
            blank=True,
            null=True)
    candidate_status = models.ForeignKey(
            CandidateStatus,
            blank=True,
            null=True)

    stances = models.ManyToManyField(Stance)

    def __unicode__(self):
        try:
            if self.party:
                return '%s (%s)'%(self.name.title(),self.party[0])
            else:
                return '%s (UNK)'%(self.name.title(),)
        except IndexError:
            return '%s (UNK)'%(self.name.title(),)

class Funder(models.Model):
    FEC_id = models.CharField(max_length=9)
    name = models.CharField(max_length=90)
    treasurer_name = models.CharField(max_length=38,null=True,blank=True)
    street_one = models.CharField(max_length=34,null=True,blank=True)
    street_two = models.CharField(max_length=34,null=True,blank=True)
    city = models.CharField(max_length=18,null=True,blank=True)
    state = models.CharField(max_length=2,null=True,blank=True)
    zip_code = models.CharField(max_length=5,null=True,blank=True)
    filing_frequency = models.CharField(max_length=1,null=True,blank=True)
    party = models.CharField(max_length=3,null=True,blank=True)

    #FK fields
    interest_group_category = models.ForeignKey(InterestGroupCategory, 
            on_delete=models.PROTECT,null=True,blank=True)
    committee_type = models.ForeignKey(CommitteeType, 
            on_delete=models.PROTECT,null=True,blank=True)
    committee_designation = models.ForeignKey(CommitteeDesignation,
            on_delete=models.PROTECT,null=True,blank=True)
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
    related_funders = models.ManyToManyField("self",
            through="FunderToFunder",
            blank=True,
            null=True,
            symmetrical=False)

    def __unicode__(self):
        return self.name.title()

class MediaProfile(models.Model):
    url = models.URLField()

    # FK relations
    media_type = models.ForeignKey(MediaType,
            on_delete=models.PROTECT)
    funder = models.ForeignKey(Funder,
            null=True, 
            blank=True,
            on_delete=models.SET_NULL)

    def __unicode__(self):
        funder = self.funder
        if funder:
            return '%s (%s)'%(unicode(funder),self.url)
        else:
            return 'NO FUNDER ASSIGNED (%s)'%(self.url,)

    def save(self, *args, **kwargs):
        sr = urlparse.urlsplit(self.url)
        conn = httplib.HTTPConnection(sr.netloc)
        conn.request("HEAD",sr.path)
        status = conn.getresponse().status
        if status == 200:
            super(MediaProfile, self).save(*args, **kwargs)
        else:
            raise Exception('not a working url')

class FunderToFunder(models.Model):
    funder = models.ForeignKey(Funder,related_name="funder_has_relative")
    related_funder = models.ForeignKey(Funder,related_name="related_funder")
    relationship = models.CharField(max_length=50)

    def __unicode__(self):
        return ('%s -> %s (%s)'%(funder_a,funder_b,relationship))

class FunderToCandidate(models.Model):
    funder = models.ForeignKey(Funder)
    candidate = models.ForeignKey(Candidate)
    relationship = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s -> %s (%s)"%(unicode(self.funder),
                self.candidate.name.title(),
                self.relationship)

class Ad(models.Model):
    title = models.CharField(max_length=200)
    ingested = models.BooleanField(default=False)
    profile_url = models.URLField(null=True)
    
    # OTO relation
    #media = models.OneToOneField(Media,on_delete=models.PROTECT)

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
    tags = models.ManyToManyField(Tag,
            blank=True,
            null=True)

    # MTM through relation
    candidates = models.ManyToManyField(Candidate,
            through='AdToCandidate')

    def __unicode__(self):
        return self.title

class Media(models.Model):
    url = models.URLField()
    embed_code = models.CharField(max_length=200,blank=True,null=True)
    creator_description = models.TextField(default="No description available.")
    curator_description = models.TextField(blank=True,null=True)
    duration = models.IntegerField()
    pub_date = models.DateTimeField()
    link_broken = models.BooleanField(default=False)
    downloaded = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)
    rmse = models.FloatField(default=0.0)

    # FK relations
    media_profile = models.ForeignKey(MediaProfile,
            on_delete=models.PROTECT)
    ad = models.ForeignKey(Ad,
            on_delete=models.PROTECT)

    def thumbstrip(self):
        pad = str(self.pk).zfill(5)
        loc = u'http://localhost:8000/media/'
        loc += u'images/media_thumbnails/strips/'
        loc += u'Media_%s_strip.jpg'%(pad,)
        img_tag = u'<img src="%s" />'%(loc,)
        popup = u'<a href="%s" target="_blank" onclick="link_popup(this); return false">%s</a>'%(self.url,img_tag)
        return popup

    thumbstrip.short_description = "thumbstrip"
    thumbstrip.allow_tags = True

    # MTM relations (moved to Ad)
    # tags = models.ManyToManyField(Tag)
    def __unicode__(self):
        return "%s (%s)"%(self.ad.title,self.url)
    
    def save(self, *args, **kwargs):
        sr = urlparse.urlsplit(self.url)
        if sr.netloc=='www.youtube.com':
            self.embed_code = '<iframe width="560" height="315" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>'%sr.query.replace('v=','')
            super(Media, self).save(*args, **kwargs)
        else:
            super(Media, self).save(*args, **kwargs)

class AdToCandidate(models.Model):
    CHOICES = (
            ('POS','Positive'),
            ('NEG','Negative'),
            ('NEU','Neutral'),
            )
    CHOICES_DICT = {'POS':'Positive',
            'NEG':'Negative',
            'NEU':'Neutral'
            }
    ad = models.ForeignKey(Ad)
    candidate = models.ForeignKey(Candidate)
    portrayal = models.CharField(max_length=3,choices=CHOICES)

    def __unicode__(self):
        return "%s -> %s (%s)"%(self.ad.title,
                self.candidate.name.title(),
                self.CHOICES_DICT[self.portrayal])

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

    def __unicode__(self):
        return "%s (%s)"%(self.headline,self.source.main_url)

