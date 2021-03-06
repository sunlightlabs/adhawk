import urlparse,httplib
from decimal import Decimal
import requests
import json

from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import slugify

from adhawk.settings import EXTERNAL_URL,MEDIA_URL
from adhawk.local_settings import GIGYA_ENDPOINT,GIGYA_API_KEY,GIGYA_SECRET

def slugify_uniquely(value, model, slugfield="slug"):
    suffix = 0
    potential = base = slugify(value)
    while True:
       if suffix:
           potential = "-".join([base, str(suffix)])
                
       if not model.objects.filter(**{slugfield: potential}).count():
           return potential
       # we hit a conflicting slug, so bump the suffix & try again
       suffix += 1

def gigya_url_request(media_object):
    base_url = 'http://adhawk.sunlightfoundation.com/ad/'
    url = base_url+media_object.slug
    cid = '[Ad Hawk] /ad adprofile %d_%d'%(media_object.media_profile_id,media_object.pk)
    payload = { 'apiKey'            :  GIGYA_API_KEY,
                'secret'            :  GIGYA_SECRET,
                'url'               :  url,
                'cid'               :  cid,
                'format'            : 'json',
                'httpStatusCodes'   : 'false'}
    d = requests.get(GIGYA_ENDPOINT,params=payload).json
    if d['statusCode'] == 200:
        return d['shortURL']
    else:
        return None

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
    name = models.CharField(max_length=200)
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
    name = models.CharField(max_length=200)
    party = models.CharField(max_length=3,null=True,blank=True)
    year_of_election = models.IntegerField(max_length=4,null=True,blank=True)
    street_one = models.CharField(max_length=34,null=True,blank=True)
    street_two = models.CharField(max_length=34,null=True,blank=True)
    city = models.CharField(max_length=18,null=True,blank=True)
    state = models.CharField(max_length=2,null=True,blank=True)
    zip_code = models.IntegerField(max_length=5,null=True,blank=True)
    office_state = models.CharField(max_length=2,null=True,blank=True)
    office = models.CharField(max_length=1,null=True,blank=True)
    office_district = models.CharField(max_length=2,null=True,blank=True)


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

class FunderFamily(models.Model):
    primary_FEC_id = models.CharField(max_length=9)
    candidate_id = models.CharField(max_length=9,null=True,blank=True)
    IE_id_type = models.CharField(max_length=12,null=True,blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True,null=True)
    ftum_url = models.URLField(blank=True,null=True)
    IE_id = models.CharField(max_length=32,null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    total_contributions = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    cash_on_hand = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    total_independent_expenditures = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    total_disbursements = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    ie_negative_percent = models.FloatField(default=0.0)
    ie_positive_percent = models.FloatField(default=0.0)
    ie_opposes_dems = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    ie_opposes_dems_percent = models.FloatField(default=0.0)
    ie_opposes_reps = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    ie_opposes_reps_percent = models.FloatField(default=0.0)
    ie_supports_dems = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    ie_supports_dems_percent = models.FloatField(default=0.0)
    ie_supports_reps = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    ie_supports_reps_percent = models.FloatField(default=0.0)
    is_superpac = models.BooleanField(default=False)
    
    #MTM relations
    committee_types = models.ManyToManyField(CommitteeType,null=True,blank=True)

    def __unicode__(self):
        display = self.name.title()
        display += '['+self.primary_FEC_id+']'
        display += ' ('
        display += ','.join([ct.code for ct in self.committee_types.all()])
        display += ')'
        return display

    class Meta:
        verbose_name_plural = 'funder families'

    def update_values(self):
        if self.funder_set:
            for funder in self.funder_set.all():
                if funder.FEC_id == self.primary_FEC_id:
                    self.candidate_id = funder.candidate_id
                    self.description = funder.description
                    self.ftum_url = funder.ftum_url
                    self.IE_id = funder.IE_id
                    self.IE_id_type = funder.IE_id_type
                if funder.committee_type:
                    self.committee_types.add(funder.committee_type)
                    if funder.committee_type.code == "O":
                        self.is_superpac = True
                else:
                    continue
            self.total_contributions = self.funder_set.aggregate(
                    Sum('total_contributions'))['total_contributions__sum']
            self.cash_on_hand = self.funder_set.aggregate(
                    Sum('cash_on_hand'))['cash_on_hand__sum']
            self.total_disbursements = self.funder_set.aggregate(
                    Sum('total_disbursements'))['total_disbursements__sum']
            self.total_independent_expenditures = self.funder_set.aggregate(
                    Sum('total_independent_expenditures'))['total_independent_expenditures__sum']
            self.ie_opposes_dems = self.funder_set.aggregate(
                    Sum('ie_opposes_dems'))['ie_opposes_dems__sum']
            self.ie_opposes_reps = self.funder_set.aggregate(
                    Sum('ie_opposes_reps'))['ie_opposes_reps__sum']
            self.ie_supports_dems = self.funder_set.aggregate(
                    Sum('ie_supports_dems'))['ie_supports_dems__sum']
            self.ie_supports_reps = self.funder_set.aggregate(
                    Sum('ie_supports_reps'))['ie_supports_reps__sum']
        total_pos = float(self.ie_supports_dems + self.ie_supports_reps)
        total_neg = float(self.ie_opposes_dems + self.ie_opposes_reps)
        grand_total = total_pos + total_neg
        denom = total_pos + total_neg
        if denom:
            self.ie_negative_percent = total_neg / denom
            self.ie_positive_percent = total_pos / denom
            self.ie_supports_dems_percent = (float(str(
                    self.ie_supports_dems)) / denom)
            self.ie_supports_reps_percent = (float(str(
                    self.ie_supports_reps)) / denom)
            self.ie_opposes_dems_percent = (float(str(
                    self.ie_opposes_dems)) / denom)
            self.ie_opposes_reps_percent = (float(str(
                    self.ie_opposes_reps)) / denom)
        self.save()
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name,self.__class__)
        super(FunderFamily, self).save(*args,**kwargs)


class Funder(models.Model):
    FEC_id = models.CharField(max_length=9)
    candidate_id = models.CharField(max_length=9,null=True,blank=True)
    IE_id = models.CharField(max_length=32,null=True,blank=True)
    IE_id_type = models.CharField(max_length=12,null=True,blank=True)
    media_profile_assigned = models.BooleanField(default=False)
    media_profile_assigned_elsewhere = models.BooleanField(default=False)
    media_profile_url_input = models.URLField(blank=True,null=True)
    ignore = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    ftum_url = models.URLField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    treasurer_name = models.CharField(max_length=90,null=True,blank=True)
    street_one = models.CharField(max_length=34,null=True,blank=True)
    street_two = models.CharField(max_length=34,null=True,blank=True)
    city = models.CharField(max_length=30,null=True,blank=True)
    state = models.CharField(max_length=2,null=True,blank=True)
    zip_code = models.CharField(max_length=9,null=True,blank=True)
    filing_frequency = models.CharField(max_length=1,null=True,blank=True)
    party = models.CharField(max_length=3,null=True,blank=True)
    total_contributions = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    cash_on_hand = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    total_independent_expenditures = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    total_disbursements = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    ie_negative_percent = models.FloatField(default=0.0)
    ie_positive_percent = models.FloatField(default=0.0)
    ie_opposes_dems = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    ie_opposes_reps = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    ie_supports_dems = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))
    ie_supports_reps = models.DecimalField(
            max_digits=21,
            decimal_places=2,
            default=Decimal("0.00"))

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
    funder_family = models.ForeignKey(FunderFamily,
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
        return '%s (%s)'%(self.name.title(),self.committee_type.code)

    def media_profile_is_not_null(self):
        if self.mediaprofile_set.all() or self.media_profile_assigned_elsewhere:
            return True
        else:
            return False

    def clean_media_profile_url_input(self):
        if 'https' in self.media_profile_url_input:
            self.media_profile_url_input = \
                    self.media_profile_url_input.replace('https','http')
        if self.media_profile_url_input[-1] == '/':
            self.media_profile_url_input = \
                    self.media_profile_url_input[:-1]

    def save(self, *args, **kwargs): 
        self.media_profile_assigned = self.media_profile_is_not_null()
        if self.media_profile_url_input and not self.media_profile_assigned:
            self.clean_media_profile_url_input()
            try:
                mp = MediaProfile.objects.get(url=self.media_profile_url_input)
                if mp:
                    self.media_profile_assigned_elsewhere = True
            except MediaProfile.DoesNotExist:
                mt = MediaType.objects.get(main_url='http://www.youtube.com')
                mp = MediaProfile(url=self.media_profile_url_input,
                                    media_type=mt,
                                    funder=self)
                mp.save()
        super(Funder, self).save(*args,**kwargs)
        self.media_profile_assigned = self.media_profile_is_not_null()
        if self.media_profile_assigned:
            try:
                input_url = self.mediaprofile_set.all()[0].url
            except IndexError:
                try:
                    input_url = mp.url
                except UnboundLocalError:
                    input_url = ''
            if not self.media_profile_url_input:
                self.media_profile_url_input = input_url
        total_pos = float(self.ie_supports_dems + self.ie_supports_reps)
        total_neg = float(self.ie_opposes_dems + self.ie_opposes_reps)
        denom = total_pos + total_neg
        if denom:
            self.ie_negative_percent = total_neg / denom
            self.ie_positive_percent = total_pos / denom
        super(Funder, self).save(*args,**kwargs)
        if self.funder_family:
            self.funder_family.update_values()

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

    def clean_url(self):
        if 'https' in self.url:
            self.url = self.url.replace('https','http')
        if self.url[-1] == '/':
            self.url = self.url[:-1]

    def save(self, *args, **kwargs):
        self.clean_url()
        #sr = urlparse.urlsplit(self.url)
        #conn = httplib.HTTPConnection(sr.netloc)
        #conn.request("HEAD",sr.path)
        #status = conn.getresponse().status
        #if status == 200:
        super(MediaProfile, self).save(*args, **kwargs)
        #else:
        #    raise Exception('not a working url')

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
    profile_url = models.URLField(null=True)
    top_ad = models.BooleanField(default=False)
    
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
    gigya_url = models.URLField(blank=True,null=True)
    slug = models.SlugField(max_length=200,default="slug")
    embed_code = models.CharField(max_length=200,blank=True,null=True)
    creator_description = models.TextField(default="No description available.")
    curator_description = models.TextField(blank=True,null=True)
    duration = models.IntegerField()
    funder_name = models.CharField(max_length=200,blank=True,null=True)
    pub_date = models.DateTimeField()
    link_broken = models.BooleanField(default=False)
    downloaded = models.BooleanField(default=False)
    ingested = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)
    rmse = models.FloatField(default=0.0)
    # FK relations
    media_profile = models.ForeignKey(MediaProfile,
            on_delete=models.PROTECT)
    ad = models.ForeignKey(Ad,
            on_delete=models.PROTECT)
    # MTM relations
    near_neighbors = models.ManyToManyField("self",
            through="MediaNearNeighbor",
            blank=True,
            null=True,
            symmetrical=False)

    def thumbstrip(self):
        pad = str(self.pk).zfill(5)
        loc = MEDIA_URL
        loc += u'images/media_thumbnails/strips/'
        loc += u'Media_%s_strip.jpg'%(pad,)
        img_tag = u'<img class="strip" src="%s" />'%(loc,)
        popup = u'<a href="%s" target="_blank" onclick="link_popup(this); return false">%s</a>'%(self.url,img_tag)
        return popup

    def get_absolute_url(self):
        return '/'+'/'.join([str(a) for a in ['ad',self.slug]])+'/'

    def thumbvid(self):
        vid = urlparse.parse_qs(urlparse.urlsplit(self.url).query)['v'][0]
        embed = '<iframe width="120" height="90"'
        embed += 'src="http://www.youtube.com/embed/%s"'%(vid,)
        embed += 'frameborder="0" allowfullscreen></iframe>'
        return embed

    thumbstrip.short_description = "thumbstrip"
    thumbstrip.allow_tags = True

    thumbvid.short_description = "video"
    thumbvid.allow_tags = True

    class Meta:
        verbose_name_plural = "media"

    # MTM relations (moved to Ad)
    # tags = models.ManyToManyField(Tag)
    def __unicode__(self):
        return "%s (%s)"%(self.ad.title,self.url)

    def request_gigya_url(self):
        self.gigya_url = gigya_url_request(self)
        #print self.gigya_url
        self.save()
    
    def save(self, *args, **kwargs):
        self.funder_name = self.media_profile.funder.name
        if self.slug == "slug" or self.slug == None:
            self.slug = slugify_uniquely(self.ad.title, self.__class__)
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

class MediaNearNeighbor(models.Model):
    media = models.ForeignKey(Media,related_name="media_has_neighbor")
    neighbor = models.ForeignKey(Media,related_name="media_neighbor")
    rank = models.IntegerField()
    cookie_cutter = models.BooleanField(default=False)

    def __unicode__(self):
        return ('%s -> %s (%s)'%(self.media,self.neighbor,self.rank))

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


