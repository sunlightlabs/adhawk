import os
import sys

from knowledge_base.models import Funder,FunderFamily

class FunderFamilyInitializer():
    def __init__(self,funder_object):
        self.funder_object = funder_object
        self.get_new_funder_family_object()
    def get_new_funder_family_object(self):
        self.new_funder_family_object = FunderFamily(
                primary_FEC_id=self.funder_object.FEC_id,
                name=self.funder_object.name)
        self.new_funder_family_object.save()
        self.new_funder_family_object.committee_types.add(
                self.funder_object.committee_type)
        self.new_funder_family_object.save()
    def assign_new_funder_family(self):
        self.funder_object.funder_family = self.new_funder_family_object
        self.funder_object.save()
        return "Funder(pk=%d) added to FunderFamily(pk=%d)"%(
                    self.funder_object.pk,self.new_funder_family_object.pk)
