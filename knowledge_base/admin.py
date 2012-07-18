from knowledge_base.models import (Ad, 
AdToCandidate,
Author,
Candidate,
Coverage,
CoverageType,
BroadcastType,
Funder,
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
from django.forms import TextInput, Textarea
from django.db import models

def set_checked(modeladmin, request, queryset):
    queryset.update(checked=True)

set_checked.short_description = "Mark selected as checked"

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
    extra = 0

class FunderAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {
                'fields':(('name','FEC_id','party'))
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
            FunderToFunderInline
            ]

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


class CandidateAdmin(admin.ModelAdmin):
    inlines = [
            AdToCandidateInline
            ]

class MediaAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','thumbstrip','checked','valid',)
    list_editable = ('checked','valid',)
    list_per_page = 10
    ordering = ('rmse',)
    actions = [set_checked]
    list_filter = ('checked','valid',)


admin.site.register(Ad,AdAdmin)
admin.site.register(AdToCandidate)
admin.site.register(Author)
admin.site.register(BroadcastType)
admin.site.register(Candidate,CandidateAdmin)
admin.site.register(Coverage,CoverageAdmin)
admin.site.register(CoverageType)
admin.site.register(Funder,FunderAdmin)
admin.site.register(FunderToFunder)
admin.site.register(Issue)
admin.site.register(IssueCategory)
admin.site.register(Market)
admin.site.register(Media,MediaAdmin)
admin.site.register(MediaProfile)
admin.site.register(MediaType)
admin.site.register(Source)
admin.site.register(Stance)
admin.site.register(Tag)
