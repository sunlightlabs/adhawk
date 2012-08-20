import os
from itertools import combinations

from nltk import wordpunct_tokenize
from nltk.metrics.distance import jaccard_distance,edit_distance

from whopaid.settings import SITE_ROOT
PROC_DIR = os.path.join(SITE_ROOT,'db_script/processing/family_finder')

from knowledge_base.models import Funder

STOPS = [line.strip() for line in 
            open(os.path.join(PROC_DIR,'stopwords.txt')).readlines()]

class FunderLevenshteinComparison():
    def __init__(self,combo):
        self.f1,self.f2 = combo
        self.distance = edit_distance(
                self.clean_name(self.f1.name),
                self.clean_name(self.f2.name))
        #self.distance = edit_distance(
        #        self.clean_street(self.f1),
        #        self.clean_street(self.f2))
    def clean_name(self,name):
        tokens = wordpunct_tokenize(name)
        return ' '.join(
                [t for t in tokens])
    def clean_street(self,f):
        st = ''
        if f.street_one:
            st += f.street_one
        if f.street_two:
            st += f.street_two
        return st
        
class FunderJaccardComparison():
    def __init__(self,combo):
        self.f1,self.f2 = combo
        self.f1_set = set(self.clean_name(f1.name))
        self.f2_set = set(self.clean_name(f2.name))
        self.distance = jaccard_distance(self.f1_set,self.f2_set)
    def clean_name (self,name):
        tokens = wordpunct_tokenize(name)
        return [t for t in tokens if t.isalnum() and t not in STOPS]

class FunderIdentityComparison():
    def __init__(self,combo):
        self.f1,self.f2 = combo
        self.distance = self.identity()
    def identity(self):
        if self.f1.name == self.f2.name:
            return 0
        else:
            return 1
