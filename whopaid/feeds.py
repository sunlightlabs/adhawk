from knowledge_base.models import Media
from django.utils.feedgenerator import Atom1Feed


class LatestValidAdsFeed(Atom1Feed):
    title = "Ad Hawk latest ads"
    link = "/latest/"
    description = "Latest Campaign Ads Discovered by Ad Hawk"
    author_name = "Ad Hawk, by Sunlight Foundation"
    author_link = "http://adhawk.sunlightfoundation.com"
    author_email = "adhawk@sunlightfoundation.com"

    def items(self):
        for obj in Media.objects.filter(checked=True, valid=True) \
                                .order_by('-pub_date')[:50]:
            item = {}
            item['title'] = obj.ad.title
            item['description'] = obj.thumbstrip
            item['unique_id'] = obj.pk
            item['pubdate'] = obj.pub_date
            item['link'] = obj.get_absolute_url()
            yield item


class LatestUncheckedAdsFeed(Atom1Feed):
    title = "Ad Hawk latest unchecked"
    link = "/unchecked/"
    description = "Latest Campaign Ads to be Validated"
    author_name = "Ad Hawk, by Sunlight Foundation"
    author_link = "http://adhawk.sunlightfoundation.com"
    author_email = "adhawk@sunlightfoundation.com"

    def items(self):
        for obj in Media.objects.filter(checked=False, downloaded=True) \
                                .order_by('-pub_date')[:50]:
            item = {}
            item['title'] = obj.ad.title
            item['description'] = obj.thumbstrip
            item['unique_id'] = obj.pk
            item['pubdate'] = obj.pub_date
            item['link'] = obj.get_absolute_url()
            yield item
