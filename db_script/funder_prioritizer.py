from knowledge_base.models import Funder,FunderFamily


class FunderPrioritizer():
    def __init__(self,funderfamily_object):
        self.funder_family = funderfamily_object
        self.is_priority = self.prioritize()
    def prioritize(self):
        funders = self.funder_family.funder_set.all()
        for funder in funders:
            if funder.mediaprofile_set.all():
                return False
            else:
                return True
