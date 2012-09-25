import os
import subprocess
import json
import logging

from knowledge_base.models import Media
from whopaid.settings import MEDIA_ROOT
from echoprint_server_api import fp

log = logging.getLogger('db_script.fingerprint_ingester')

VIDEO_DIR = os.path.join(os.path.abspath(MEDIA_ROOT),'videos')
CODEGEN_DIR = os.path.join(os.path.abspath(MEDIA_ROOT),'codegens')

class FingerprintIngester():
    def __init__(self,loc,sfm_client):
        self.loc = loc
        self.sfm_client = sfm_client
        self.video_fname = self.get_video_fname()
        self.codegen_fname = self.get_codegen_fname()
        self.pk = self.get_pk()
        self.media = self.get_media()
    def get_codegen_fname(self):
        return '.'.join([os.path.splitext(self.video_fname)[0],'cgn'])
    def get_media(self):
        return Media.objects.get(pk=self.pk)
    def get_pk(self):
        return int(self.video_fname.split('_')[1])
    def get_video_fname(self):
        return os.path.basename(self.loc)
    def write_codegen_file(self,j):
        fout = open(os.path.join(CODEGEN_DIR,self.codegen_fname),'w')
        fout.write(json.dumps(j))
        fout.close()
        self.sfm_client.add(1,
                            self.media.id,
                            fp.decode_code_string(j['code']),
                            title=self.media.ad.title)
    def build_ingest_dict(self,j):
        i = {   "track_id"  : self.pk,
                "fp"        : fp.decode_code_string(j['code']),
                "codever"   : j['metadata']['version'],
                "length"    : self.media.duration }
        return i
    def ingest_fingerprint(self,j):
        i = self.build_ingest_dict(j)
        #print "ingesting %s"%(str(i))
        fp.ingest(i)
    def get_codegen(self):
        process = subprocess.Popen(
            ['echoprint-codegen',self.loc],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        exit_code = process.wait()
        out,err = process.communicate()
        if exit_code == 0:
            j = json.loads(out)[0]
            self.write_codegen_file(j)
            self.ingest_fingerprint(j)
            self.media.ingested = True
            self.media.save()
            log.info('Media %s ingested as %s'%(str(self.pk).zfill(5),
                                                self.codegen_fname))
        else:
            log.info('Media %s ERROR %s'%(str(self.pk).zfill(5),
                                            err))
