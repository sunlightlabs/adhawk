import os
import subprocess
import urllib
import logging

from collections import namedtuple
from django.db import connection

F = namedtuple('F', ['url', 'filename', 'sql_table'])

# note: tables will be created/destroyed in this order. So must do dependant tables first to avoid constraint errors.
FEC_CONFIG = [
    F('ftp://ftp.fec.gov/FEC/2012/indiv12.zip', 'itcont.txt', 'fec_indiv_import'),
    F('ftp://ftp.fec.gov/FEC/2012/pas212.zip', 'itpas2.txt', 'fec_pac2cand_import'),
    F('ftp://ftp.fec.gov/FEC/2012/oth12.zip', 'itoth.txt', 'fec_pac2pac_import'),
    F('ftp://ftp.fec.gov/FEC/2012/cm12.zip', 'cm.txt', 'fec_committees'),
    F('ftp://ftp.fec.gov/FEC/2012/cn12.zip', 'cn.txt', 'fec_candidates_import'),
    F('ftp://ftp.fec.gov/FEC/2012/weball12.zip', 'weball12.txt', 'fec_candidate_summaries'),
    F('ftp://ftp.fec.gov/FEC/2012/webk12.zip', 'webk12.txt', 'fec_committee_summaries')
]

SQL_PRELOAD_FILE = os.path.join(os.path.dirname(__file__), 'create_fec.sql')
SQL_POSTLOAD_FILE = os.path.join(os.path.dirname(__file__), 'postload.sql')

log = logging.getLogger('db_script.fec_importer')

class FECImporter():
    def __init__(self, processing_dir, config=FEC_CONFIG):
        self.processing_dir = os.path.expanduser(processing_dir)
        self.FEC_CONFIG = config

    def update_csv(self):
        try:
            log.info("Downloading files to %s..." % self.processing_dir)
            self.download()

            log.info("Extracting files...")
            self.extract()

            log.info("Converting to unicode...")
            self.fix_unicode()

        except Exception as e:
            log.error(e)
            raise


    def update_db(self):
        try:
            c = connection.cursor()

            self.execute_file(c, SQL_PRELOAD_FILE)

            log.info("Uploading data...")
            self.upload(c)

            log.info("Processing uploaded data...")
            self.execute_file(c, SQL_POSTLOAD_FILE)

            log.info("Done.")
        except Exception as e:
            log.error(e)
            raise

    def _download_file(self, conf):
        filename = conf.url.split("/")[-1]
        dirname = filename.split(".")[0]
        return os.path.join(self.processing_dir, dirname, filename)
        
    def _working_dir(self, conf):
        filename = conf.url.split("/")[-1]
        dirname = filename.split(".")[0]
        return os.path.join(self.processing_dir, dirname)

    def download(self):
        for conf in self.FEC_CONFIG:
            if not os.path.isdir(self._working_dir(conf)):
                os.makedirs(self._working_dir(conf))

            log.info("downloading %s to %s..." % (conf.url, self._download_file(conf)))
            urllib.urlretrieve(conf.url, self._download_file(conf))


    def extract(self):
        for conf in self.FEC_CONFIG:
            subprocess.check_call(['unzip', '-oqu', self._download_file(conf), "-d" + self._working_dir(conf)])


    def fix_unicode(self):
        for conf in self.FEC_CONFIG:
            infile = open(os.path.join(self._working_dir(conf), conf.filename), 'r')
            outfile = open(os.path.join(self._working_dir(conf), conf.filename + ".utf8"), 'w')

            for line in infile:
                fixed_line = line.decode('utf8', 'replace').encode('utf8', 'replace')
                outfile.write(fixed_line)


    def execute_file(self, cursor, filename):
        contents = " ".join([line for line in open(filename, 'r') if line[0:2] != '--'])
        statements = contents.split(';')[:-1] # split on semi-colon. Last element will be trailing whitespace

        for statement in statements:
            log.info("Executing %s" % statement)
            cursor.execute(statement)


    def upload(self, c):

        for conf in self.FEC_CONFIG:
            infile = open(os.path.join(self._working_dir(conf), conf.filename + '.utf8'), 'r')
            c.execute("DELETE FROM %s" % conf.sql_table)
            # note: quote character is an arbitrary ASCII code that is unlikely to appear in data.
            # FEC uses single and double quotes and most other printable characters in the data,
            # so we have to be sure not to misinterpret any of them as semantically meaningful.
            c.copy_expert("COPY %s FROM STDIN CSV HEADER DELIMITER '|' QUOTE E'\\x1F'" % conf.sql_table, infile)

