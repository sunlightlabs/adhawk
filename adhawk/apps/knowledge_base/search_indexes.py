import datetime

from haystack import indexes

from knowledge_base.models import Media

class MediaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    funder_name = indexes.CharField(faceted=True)
    funder_party = indexes.CharField(faceted=True)
    funder_committee_type = indexes.CharField(faceted=True)
    #ad_markets = indexes.MultiValueField()
    #ad_broadcast_types = indexes.MultiValueField()
    #ad_candidates = indexes.MultiValueField()

    def get_model(self):
        return Media

    def index_queryset(self):
        return self.get_model().objects.filter(valid=True,ingested=True)

    def prepare_funder_name(self, obj):
        return unicode(obj.media_profile.funder)

    def prepare_funder_party(self, obj):
        return obj.media_profile.funder.party

    def prepare_funder_committee_type(self, obj):
        return obj.media_profile.funder.committee_type.name

    #def prepare_ad_markets(self, obj):
    #    return [m.name for m in obj.ad.markets.all()]

    #def prepare_broadcast_types(self, obj):
    #    return [b.name for b in obj.ad.broadcast_types.all()]

    #def prepare_candidates(self, obj):
    #    return [c.name for c in obj.ad.candidates.all()]
