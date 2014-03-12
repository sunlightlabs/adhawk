from knowledge_base.models import Media
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed


class LatestValidAdsFeed(Feed):
    feed_type = Atom1Feed
    title = "Ad Hawk latest ads"
    link = "/latest/"
    description = "Latest Campaign Ads Discovered by Ad Hawk"
    author_name = "Ad Hawk, by Sunlight Foundation"
    author_link = "http://adhawk.sunlightfoundation.com"
    author_email = "adhawk@sunlightfoundation.com"
    
    def items(self):
        for obj in Media.objects.filter(checked=True, valid=True) \
                                .order_by('-pub_date')[:50]:
            yield obj

    def item_title(self, obj): 
        return obj.ad.title
    
    def item_description(self, obj):
        return obj.thumbstrip()

    def item_pubdate(self, obj):
        return obj.pub_date
    
    def item_link(self, obj):
        return obj.get_absolute_url()


class LatestUncheckedAdsFeed(Feed):
    feed_type = Atom1Feed
    title = "Ad Hawk latest unchecked"
    link = "/unchecked/"
    description = "Latest Campaign Ads to be Validated"
    author_name = "Ad Hawk, by Sunlight Foundation"
    author_link = "http://adhawk.sunlightfoundation.com"
    author_email = "adhawk@sunlightfoundation.com"
 
    def items(self):
        for obj in Media.objects.filter(checked=True, valid=True) \
                                .order_by('-pub_date')[:50]:
            yield obj

    def item_title(self, obj): 
        return obj.ad.title

    def item_description(self, obj):
        return obj.thumbstrip()

    def item_pubdate(self, obj):
        return obj.pub_date

    def item_link(self, obj):
        return obj.get_absolute_url()
