import sys
import os
import collections
import string
import csv
import logging

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
        FunderToCandidate
#from db_script.log import set_up_logger
from django.db import connections

CONN = connections['default']

PROCESSING_DIR = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        'processing/reporting_youtube')
PROCESSING_FILENAME = os.path.join(PROCESSING_DIR,'reporting_youtube.csv')

log = logging.getLogger('db_script.reporting_importer')

rchars = string.whitespace + string.punctuation

TABLE = string.maketrans(rchars,"_"*len(rchars))

class ReportingYouTubeImporter():
    def __init__(self):
        log.info('BEGINNING YOUTUBE IMPORT')
        self.dialect = csv.Sniffer().sniff(open(PROCESSING_FILENAME).read())
        self.fname = self.sqlify(os.path.splitext(
            os.path.basename(PROCESSING_FILENAME))[0])
        self.csvfile = open(PROCESSING_FILENAME)
        self.reader = self.get_csv_reader()
        self.max_col_lens =self.get_max_col_lens(self.reader)
    def sqlify(self,s):
        return s.translate(TABLE).lower()
    def get_csv_reader(self):
        log.info('reading csv')
        reader = csv.DictReader(self.csvfile,
                dialect=self.dialect)
        for k in reader.fieldnames:
            nk = self.sqlify(k)
            reader.fieldnames[reader.fieldnames.index(k)] = nk
        log.info('...read')
        return reader
    def get_max_col_lens(self,reader):
        maxes = dict.fromkeys(reader.fieldnames)
        for row in reader:
            for k,v in row.items():
                if len(v) > maxes[k]:
                    maxes[k] = len(v)
                else:
                    continue
        return maxes
    def check_sql_table_exists(self):
        log.info('checking to see if sql table exists')
        c = CONN.cursor()
        tables = CONN.introspection.get_table_list(c)
        if self.fname in tables:
            log.info('...it does!')
            return True
        else:
            log.info("...it doesn't")
            return False
    def make_sql_table(self):
        log.info("making sql table")
        c = CONN.cursor()
        if self.check_sql_table_exists():
            drop_str = "DROP TABLE %s ;"%(self.fname,)
            c.execute(drop_str)
        create_str = "CREATE TABLE %s ( "%(self.fname,)
        cols = []
        for fn in self.reader.fieldnames:
             cols.append(" %s varchar(%d) "%(fn,self.max_col_lens[fn]+1))
        create_str += ','.join(cols)
        create_str += ");"
        c.execute(create_str)
        log.info("...made")
    def upload(self):
        log.info('uploading csv')
        c = CONN.cursor()
        self.csvfile.seek(0)
        self.csvfile.readline()
        c.copy_expert("COPY %s FROM STDIN CSV DELIMITER '%s'"%(
            self.fname, self.dialect.delimiter),self.csvfile)
        log.info('...uploaded')
