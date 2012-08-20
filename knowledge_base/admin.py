from decimal import Decimal


from knowledge_base.models import (Ad, 
AdToCandidate,
Author,
Candidate,
CommitteeType,
Coverage,
CoverageType,
BroadcastType,
Funder,
FunderFamily,
FunderToFunder,
IncumbentChallengerStatus,
InterestGroupCategory,
Issue,
IssueCategory,
Market,
Media,
MediaProfile,
MediaType,
Source,
Stance,
Tag)

from django.contrib import admin
from django.contrib.admin import BooleanFieldListFilter
from django.forms import TextInput, Textarea
from django.db import models
from django.core import urlresolvers

def set_checked(modeladmin, request, queryset):
    queryset.update(checked=True)

set_checked.short_description = "Mark selected as checked"

def set_ignore(modeladmin, request, queryset):
    queryset.update(ignore=True)

set_ignore.short_description = "Ignore selected"

class FunderInline(admin.StackedInline):
    model = Funder
    extra = 0

class MediaInline(admin.StackedInline):
    formfield_overrides = {
            # models.CharField: {'widget': TextInput(attrs={'size':'20'})},
            models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})}
            }
    model = Media
    template = 'admin/stacked-media.html'
    extra = 0

class FunderToFunderInline(admin.StackedInline):
    model = FunderToFunder
    fk_name = "related_funder"
    extra = 3

class MediaProfileInline(admin.StackedInline):
    model = MediaProfile
    raw_id_fields = ('funder',)
    extra = 0

class MediaProfileAdmin(admin.ModelAdmin):
    model = MediaProfile
    raw_id_fields = ('funder',)
    list_display = ('url','funder',)
    list_editable = ('funder',)
    search_fields = ['url','funder__name']

class FunderAdmin(admin.ModelAdmin):
    raw_id_fields = ('funder_family',)
    fieldsets = (
            (None, {
                'fields':(('name','FEC_id','party','funder_family'))
                }),
            ('Address', {
                'classes': ('collapse',),
                'fields':(('street_one','street_two'),('city','state','zip_code'))
                }),
            ('Regulatory Details', {
                'classes': ('collapse',),
                'fields': (('filing_frequency',
                    'interest_group_category',
                    'committee_type',
                    'committee_designation'),
                    'treasurer_name',
                    'connected_organization')
                })
            )
    inlines = [
            MediaProfileInline,
            ]
    list_display = ('__unicode__',
            'media_profile_assigned',
            'ignore',
            'total_contributions',
            'party',
            'media_profile_url_input',
            )
    list_editable = ('ignore','party','media_profile_url_input')
    list_per_page = 25
    actions = [set_ignore]
    ordering = ('-total_contributions',)
    list_filter = ('ignore','media_profile_assigned','committee_type','party',)
    search_fields = ['FEC_id','name']

class FunderFamilyAdmin(admin.ModelAdmin):
    model = FunderFamily
    inlines = [ FunderInline ]
    search_fields = ['primary_FEC_id','name','funder__name']

class AdToCandidateInline(admin.StackedInline):
    model = AdToCandidate
    extra = 0

class AdAdmin(admin.ModelAdmin):
    inlines = [
            MediaInline,
            AdToCandidateInline
            ]
    filter_horizontal = [
            'markets',
            'tags',
            'stances'
            ]
    search_fields = ['title','profile_url']

class CoverageAdmin(admin.ModelAdmin):
    fields = ('url',
            'headline',
            'date',
#            'source',
            'coverage_type',
            'authors',
            'ads',
            'funders',
            'candidates',
            'tags',
            'issues',
            'stances')
    filter_horizontal = [
            'tags',
            'ads',
            'issues',
            'candidates',
            'funders',
            'authors',
            'stances'
            ]

class CommitteeTypeAdmin(admin.ModelAdmin):
    model = CommitteeType

class CandidateAdmin(admin.ModelAdmin):
    inlines = [
            AdToCandidateInline
            ]

class MediaAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',
            'funder_name',
            'checked',
            'valid',
            'duration',
            'thumbstrip',
            'thumbvid',)
    list_editable = ('checked','valid',)
    list_per_page = 10
    ordering = ('rmse',)
    actions = [set_checked]
    list_filter = ('checked','valid',)
    search_fields = ['ad__title','url','media_profile__funder__funder_family__name']

admin.site.disable_action('delete_selected')
admin.site.register(Ad,AdAdmin)
admin.site.register(AdToCandidate)
admin.site.register(Author)
admin.site.register(BroadcastType)
admin.site.register(Candidate,CandidateAdmin)
admin.site.register(CommitteeType,CommitteeTypeAdmin)
admin.site.register(Coverage,CoverageAdmin)
admin.site.register(CoverageType)
admin.site.register(Funder,FunderAdmin)
admin.site.register(FunderFamily,FunderFamilyAdmin)
admin.site.register(FunderToFunder)
admin.site.register(Issue)
admin.site.register(IssueCategory)
admin.site.register(Market)
admin.site.register(Media,MediaAdmin)
admin.site.register(MediaProfile,MediaProfileAdmin)
admin.site.register(MediaType)
admin.site.register(Source)
admin.site.register(Stance)
admin.site.register(Tag)
