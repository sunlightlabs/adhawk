import hashlib

from django.db import models


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    subscribed = models.BooleanField(default=True)
    hashcode = models.CharField(max_length=128, blank=True)

    def save(self):
        if not self.id:
            if self.email:
                self.hashcode = hashlib.md5('stuff').hexdigest()
        super(Recipient, self).save()

    def __unicode__(self):
        return "%s %s" % (self.email, self.zipcode)
