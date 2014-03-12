import os
import datetime

from django.contrib.sitemaps import Sitemap

from whopaid import settings
from knowledge_base.models import Media,FunderFamily,Funder


class AdProfileSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return Media.objects.filter(valid=True,checked=True)

    def location(self,obj):
        return '/ad/%s/'%(obj.slug,)

class FunderFamilyProfileSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.80

    def items(self):
        funders = Funder.objects.filter(media_profile_assigned=True)
        funder_families = set([])
        for funder in funders:
            funder_families.add(funder.funder_family)
        return list(funder_families)

    def location(self,obj):
        return '/sponsor/%s/'%(obj.slug,)

class StaticSitemap(Sitemap):
    priority = 0.5

    def __init__(self,my_staticsites):
        self._items = my_staticsites

    def items(self):
        return self._items

    def location(self,obj):
        return obj[0]

    def changefreq(self,obj):
        return obj[1]

    def lastmod(self,obj):
        return self._get_modification_date(obj[2])

    def _get_modification_date(self,template):
        template_path = self._get_template_path(template)
        mtime = os.stat(template_path).st_mtime
        return datetime.datetime.fromtimestamp(mtime)

    def _get_template_path(self,template):
        for template_dir in settings.TEMPLATE_DIRS:
            path = os.path.join(template_dir,template)
            if os.path.exists(path):
                return path
