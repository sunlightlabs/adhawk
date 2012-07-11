import sys
import os
import collections
import string
import csv
import re

from knowledge_base.models import Candidate, \
        CandidateStatus, \
        CommitteeDesignation, \
        CommitteeType, \
        ConnectedOrganization, \
        IncumbentChallengerStatus, \
        InterestGroupCategory, \
        Candidate, \
        Funder, \
        FunderToFunder, \
        FunderToCandidate, \
        MediaType, \
        MediaProfile
from db_script.log import set_up_logger
from django.db import connections

CONN = connections['default']

PROCESSING_DIR = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        'processing/reporting_youtube')
PROCESSING_FILENAME = os.path.join(PROCESSING_DIR,'reporting_youtube.csv')

URLTYPE_DICT = { 
    'youtube':'^(http:\\/\\/www\\.youtube\\.com\\/user\\/)',
    'vimeo':'^(http:\\/\\/vimeo.com\\/)'
    }


rchars = string.whitespace + string.punctuation

def make_result_object(executed_cursor):
    return collections.namedtuple('Result', 
            ', '.join([col.name for col in executed_cursor.description]))

def make_media_profile_object(mpr,log):
    #hard coded, just doing youtubez for now
    media_type = MediaType.objects.get(main_url='http://www.youtube.com')
    media_profile = MediaProfile()
    media_profile.url=mpr.youtube_channel_url
    media_profile.media_type=media_type
    try:
        funder = Funder.objects.get(FEC_id=mpr.fec_id)
        media_profile.funder=funder
    except Funder.DoesNotExist:
        log.info(
                "%s: Media Profile for a nonexistent funder!"%
                (mpr.youtube_channel_url,))        
    return media_profile

class MediaProfileQuery():
    def __init__(self,conn,url_set):
        self.url_list_string = self.make_url_list_string(url_set)
        self.cursor = conn.cursor()
    def get_result_cursor(self):
        quy = "select * from reporting_youtube WHERE youtube_channel_url in "
        quy += self.url_list_string
        self.cursor.execute(quy)
        return self.cursor
    def make_url_list_string(self,url_set):
        return ' ('+','.join(["'"+str(a)+"'" for a in url_set])+') '

class MediaProfileFilter():
    def __init__(self,url,urltype=None):
        self.url = url
        if urltype:
            self.rx = self.compile_re(urltype)
        else:
            for k in URLTYPE_DICT.keys():
                if k in self.url:
                    self.urltype = k
                    self.rx = self.compile_re()
        if self.test_url():
            self.ok_url = True
        else:
            self.ok_url = False
    def compile_re(self):
        re1= URLTYPE_DICT[self.urltype] # http://www.youtube.com/user/
        re2='((?:[a-z0-9][a-z0-9]+))$' # username
        rx = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
        return rx
    def test_url(self):
        m = self.rx.search(self.url)
        if m:
            self.username = m.group(2)
            return True
        else:
            return False


class MediaProfileImporter():
    def __init__(self,processing_dir=PROCESSING_DIR,conn=CONN):
        self.processing_dir = os.path.expanduser(processing_dir)
        self.log = set_up_logger("media_profile_importer",self.processing_dir)
        self.conn = conn
        self.imported_url_set = self.get_imported_urls()
        self.model_url_set = self.get_model_urls()
        self.new_urls = self.get_new_urls()
    def get_imported_urls(self):
        c = self.conn.cursor()
        c.execute("select youtube_channel_url from reporting_youtube")
        return set([i[0] for i in c])
    def get_model_urls(self):
        return set([obj.url for obj in MediaProfile.objects.all()])
    def get_new_urls(self):
        return self.imported_url_set - self.model_url_set
    def upload(self):
        if self.new_urls:
            self.add_new_media_profiles()
    def add_new_media_profiles(self):
        added_entries = 0
        mpq = MediaProfileQuery(self.conn,self.new_urls)
        ec = mpq.get_result_cursor()
        MediaProfileResult = make_result_object(ec)
        for r in ec:
            mpr = MediaProfileResult(*r)
            media_profile = make_media_profile_object(mpr,self.log)
            media_profile.save()
            self.log.info(",,,added\tMediaProfile\t%s"%(unicode(media_profile),))
            added_entries += 1
        self.log.info("Added %d new entries"%(added_entries,))

