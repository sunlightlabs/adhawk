import logging
import urllib
import urlparse
import time

from knowledge_base.models import *
import whopaid.settings as settings

YTIMG = "http://img.youtube.com/vi/%s/"
thumbs_dir = settings.MEDIA_ROOT+"/images/media_thumbnails/"

log = logging.getLogger('db_script.thumb_getter')

class ThumbDownloader():
    def __init__(self,media):
        self.pk = media.pk
        self.vid = self.get_vid(media.url)
        self.fout_base = "Media_%s_"%(str(self.pk).zfill(5),)
        self.ytimg_base = YTIMG%(self.vid,)
        #self.log = set_up_logger("thumb_downloader",'db_script/processing')
    def get_vid(self,url):
        up = urlparse.urlparse(url)
        qs = up.query
        return urlparse.parse_qs(qs)['v'][0]
    def get_thumbs(self):
        log.info("getting thumbs for Media(%s)"%(self.ytimg_base,))
        for n in ['1','2','3']:
            #self.log.info(".")
            not_successful_yet = True
            fname = "%s.jpg"%n
            f = self.fout_base+fname
            ytimg = self.ytimg_base+fname
            while not_successful_yet:
                try:
                    urllib.urlretrieve(ytimg,thumbs_dir+f)
                    not_successful_yet = False
                except IOError:
                    log.warning("Warning: IOError, waiting 5 seconds")
                    time.sleep(5)
                    not_successful_yet = True
        log.info("...gotten")


