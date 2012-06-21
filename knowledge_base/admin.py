from knowledge_base.models import (Ad, 
AdToCandidate,
Author,
Candidate,
Coverage,
CoverageType,
BroadcastType,
Funder,
IncumbentChallengerStatus,
InterestGroupCategory,
Issue,
IssueCategory,
Market,
Media,
MediaType,
Source,
Stance,
Tag)

from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

class MediaInline(admin.StackedInline):
    formfield_overrides = {
            # models.CharField: {'widget': TextInput(attrs={'size':'20'})},
            models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})}
            }
    model = Media
    template = 'admin/stacked-media.html'
    extra = 0

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
            'source',
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

admin.site.register(Ad,AdAdmin)
admin.site.register(AdToCandidate)
admin.site.register(Author)
admin.site.register(BroadcastType)
admin.site.register(Candidate,CandidateAdmin)
admin.site.register(Coverage,CoverageAdmin)
admin.site.register(CoverageType)
admin.site.register(Funder)
admin.site.register(Issue)
admin.site.register(IssueCategory)
admin.site.register(Market)
admin.site.register(Media)
admin.site.register(MediaType)
admin.site.register(Source)
admin.site.register(Stance)
admin.site.register(Tag)
