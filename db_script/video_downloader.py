import os
import subprocess

from knowledge_base.models import Media
from whopaid.settings import MEDIA_ROOT


TEMPLATE = 'videos/Media_%s_%%(id)s_%%(uploader)s.%%(ext)s'

class VideoDownloader():
    def __init__(self,media_object):
        self.media_object = media_object
        self.pk = str(media_object.pk).zfill(5)
        self.url = media_object.url
        self.output_file = os.path.join(MEDIA_ROOT,TEMPLATE%self.pk)
    def download_file(self):
        process = subprocess.Popen(
                ['youtube-dl.py','-o',self.output_file,self.url],
                stderr=subprocess.PIPE)
        self.error = process.communicate()[1]
        exit_code = process.wait()
        if int(exit_code) == 0:
            self.media_object.downloaded = True
            self.media_object.save()
            return "Media Object\t%s\tdownloaded to\t%s"%(self.pk,self.output_file)
        else:
            return "Media Object\t%s\terror\t%s"%(self.pk,self.error.replace('\n',' '))

