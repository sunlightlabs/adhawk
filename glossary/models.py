from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify

from sectors.models import Sector


class Item(models.Model):
    term        = models.CharField(max_length=255, unique=True, db_index=True)
    acronym     = models.CharField(max_length=32, db_index=True, blank=True)
    slug        = models.SlugField(db_index=True, unique=True)
    synonym     = models.CharField(max_length=255, db_index=True, blank=True)
    definition  = models.TextField()
    term_length = models.IntegerField(db_index=True)
    
    sectors = models.ManyToManyField(Sector, blank=True)
    
    def __unicode__(self):  
        return u"%s" % self.term

    def save(self):
        self.update_term_length()
        self.autogenerate_slug_if_blank()
        super(Item, self).save()

    def update_term_length(self):
        self.term_length = len(self.term) if self.term else 0

    def autogenerate_slug_if_blank(self):
        if self.term and not self.slug:
            self.slug = slugify(self.term)
