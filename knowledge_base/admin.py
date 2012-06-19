from knowledge_base.models import Ad,AdToCandidate,Market,BroadcastType,Candidate,Funder,Coverage,Media
from django.contrib import admin

class MediaInline(admin.StackedInline):
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
            'markets'
            ]

class CandidateAdmin(admin.ModelAdmin):
    inlines = [
            AdToCandidateInline
            ]




admin.site.register(Ad,AdAdmin)
admin.site.register(Candidate,CandidateAdmin)
admin.site.register(AdToCandidate)
admin.site.register(Funder)
admin.site.register(Coverage)
admin.site.register(Market)
admin.site.register(BroadcastType)
