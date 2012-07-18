from knowledge_base.models import *
import urllib
import urlparse


YTIMG = "http://img.youtube.com/vi/%s/"
thumbs_dir = "static/images/media_thumbnails/"

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
        #self.log.info("getting thumbs for Media(%s)"%(self.ytimg_base,))
        for n in ['1','2','3']:
            #self.log.info(".")
            fname = "%s.jpg"%n
            f = self.fout_base+fname
            ytimg = self.ytimg_base+fname
            urllib.urlretrieve(ytimg,thumbs_dir+f)


#pk_vid = []
#ms = Media.objects.all()
#for m in ms:
#    up = urlparse.urlparse(m.url)
#    qs = up.query
#    vid = urlparse.parse_qs(qs)['v'][0]
#    pk_vid.append((m.pk,vid))
#for pk,vid in pk_vid:
#    foutname = "Media_%s_"%(str(pk).zfill(5),)
#    for n in ['1','2','3']:
#        f = foutname+"%s.jpg"%n
#        ytimg = "http://img.youtube.com/vi/%s/%s.jpg"%(vid,n)
#        urllib.urlretrieve(ytimg,'static/images/media_thumbnails/'+f)
