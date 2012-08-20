import os
import itertools

from django.core.management import BaseCommand
from django.db import transaction

from db_script.family_finder import FunderLevenshteinComparison, \
                                    FunderJaccardComparison, \
                                    FunderIdentityComparison
from whopaid.settings import SITE_ROOT
from knowledge_base.models import Funder,MediaProfile,FunderFamily

PROC_DIR = os.path.join(SITE_ROOT,'db_script/processing/family_finder')
STATES = [line.strip() for line in 
                open(os.path.join(PROC_DIR,'states.txt')).readlines()]

class Command(BaseCommand):

    def print_funder_info(self,f):
        print f.name
        print f.committee_type
        print f.street_one,f.street_two
        print f.city+',',f.state


    def get_confirmation(self,combo,distance):
        funder_prime,other_funder = combo
        divider = "="*80
        print divider
        print "Method: %s\tDistance:%f"%(self.method,distance)
        print divider
        print "Funder:"
        self.print_funder_info(funder_prime)
        print divider
        print "Other Funder:"
        self.print_funder_info(other_funder)
        print "\n"
        confirm = raw_input("Are these two the same? (y/n)")
        if confirm.lower()[0] == "y":
            other_funder.funder_family = funder_prime.funder_family
            other_funder.save()
            print "added",other_funder,"to",other_funder.funder_family
            return other_funder
        else:
            print "okay, no dice"
            return False

    def compare_funders(self):
        c = self.comparison(self.current_combo)
        if c.distance >= self.threshold:
            print c.distance
            return "ignore"
        else:
            print "compared using %s with threshold %f (score %f)"%(
                self.method,self.threshold,c.distance)
            return self.get_confirmation(self.current_combo,c.distance)

    def new_combo_list(self):
        return itertools.product(
                    self.funders_with_mp,self.other_funders)
    
    def get_funders_with_mp(self,state):
        return [mp.funder for mp in MediaProfile.objects.all() 
                if mp.funder.state == state]

    def initialize_remove_set(self):
        self.remove_set = set()
        rsf = os.path.join(PROC_DIR,'remove_set.txt')
        if os.path.exists(rsf):
            for line in open(rsf):
                f1_id,f2_id = line.strip().split('\t')
                f1 = Funder.objects.get(FEC_id=f1_id)
                f2 = Funder.objects.get(FEC_id=f2_id)
                self.remove_set.add((f1,f2))
        else:
            self.remove_set = set()

    def get_other_funders(self,state):
        funder_set = set()
        for f in Funder.objects.filter(state=state):
            if f.funder_family:
                if len(f.funder_family.funder_set.all()) <= 1:
                    funder_set.add(f)
                else:
                    continue
            else:
                print f,"had no funder family?"
                funder_set.add(f)
        other_funder_set = funder_set - set(self.funders_with_mp)
        return list(other_funder_set)

    @transaction.commit_on_success
    def handle(self, *args, **options):

        if args:
            self.method = args[0]
            self.threshold = float(args[1])
        else:
            self.method = None
            self.threshold = 1

        if self.method == 'levenshtein':
            self.comparison = FunderLevenshteinComparison
        elif self.method == 'jaccard':
            self.comparison = FunderJaccardComparison
        else:
            self.comparison = FunderIdentityComparison
        
        self.initialize_remove_set()

        for state in STATES:
            self.funders_with_mp = self.get_funders_with_mp(state)
            self.other_funders = self.get_other_funders(state)

            self.fc = self.new_combo_list()

            keep_going = True

            while keep_going:
                try:
                    self.current_combo = self.fc.next()
                except StopIteration:
                    print "Finished %s"%(state)
                    keep_going = False
                    continue
                if self.current_combo in self.remove_set:
                    continue
                else:
                    other_funder = self.compare_funders()
                    if other_funder == "ignore":
                        continue
                    elif other_funder:
                        self.other_funders.remove(other_funder)
                        self.fc = self.new_combo_list()
                        continue
                        #kg = raw_input("Keep going? (y/n)")
                        #if kg.lower()[0] == 'y':
                        #    continue
                        #else:
                        #    keep_going = False
                        #    continue
                    else:
                        self.remove_set.add(self.current_combo)
                        continue
            print "populating mediaprofile input fields"
            for fwmp in self.funders_with_mp:
                mp_url = fwmp.mediaprofile_set.all()[0].url
                ff = fwmp.funder_family
                for f in ff.funder_set.all():
                    f.media_profile_url_input = mp_url
                    f.save()

        print "cleaning up..."
        for ff in FunderFamily.objects.all():
            if ff.funder_set.all():
                continue
            else:
                print "deleting orphan:",ff
                ff.delete()

        fout = open(os.path.join(PROC_DIR,'remove_set.txt'),'a')
        for pair in self.remove_set:
            fout.write('\t'.join([f.FEC_id for f in pair])+'\n')
        fout.close()
