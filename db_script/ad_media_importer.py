import sys
import os
import urlparse
from collections import defaultdict
from datetime import datetime

import gdata.youtube
import gdata.youtube.service
from gdata.service import RequestError

#from db_script.log import set_up_logger
import logging

from knowledge_base.models import Ad,Media,MediaProfile,MediaType,Tag

log = logging.getLogger('db_script.ad_media_importer')

URI = 'http://gdata.youtube.com/feeds/api/users/%s/uploads'
WATCH = 'http://www.youtube.com/watch?v=%s'
EARLIEST = datetime.strptime('2011-09-01','%Y-%m-%d')

def init_yt_service():
    yt_service = gdata.youtube.service.YouTubeService()
    yt_service.developer_key = '***REMOVED***'
    yt_service.email = 'blannon@gmail.com'
    yt_service.password = '***REMOVED***'
    yt_service.ProgrammaticLogin()
    return yt_service

YTS = init_yt_service()

class YouTubeMedia():
    def __init__(self,test_result):
        pub_date,duration,video_feed_entry = test_result
        self.video_feed_entry = video_feed_entry
        self.video_id = self.get_video_id()
        self.url = self.get_url()
        self.title = self.get_title()
        self.description = self.get_description()
        self.keywords = self.get_keywords()
        self.duration = duration
        self.pub_date = pub_date
    def get_video_id(self):
        qs = urlparse.urlsplit(self.video_feed_entry.media.player.url).query
        return urlparse.parse_qs(qs)['v'][0]
    def get_url(self):
        return WATCH%self.video_id
    def get_title(self):
        return self.video_feed_entry.media.title.text
    def get_description(self):
        return self.video_feed_entry.media.description.text
    def get_keywords(self):
        if self.video_feed_entry.media.keywords.text:
            return self.video_feed_entry.media.keywords.text.split(", ")
        else:
            return None

class YouTubeMediaCollector():
    def __init__(self,username):
        self.username = username
        self.yts = YTS
        self.collect_youtube_medias()
    def collect_youtube_medias(self):
        entries_len = 50
        start_index = 1
        uri = URI%self.username
        uri = uri+'?start-index=%d&max-results=%d'
        self.youtube_medias = []
        while entries_len == 50:
            video_feed = self.yts.GetYouTubeVideoFeed(uri%(start_index,50))
            for entry in video_feed.entry:
                test_result = self.test_entry(entry)
                if test_result:
                    self.youtube_medias.append(YouTubeMedia(test_result))
                else:
                    continue
            entries_len = len(video_feed.entry)
            start_index += 50
    def test_entry(self,entry):
        pub_date = datetime.strptime(entry.published.text[:-5],'%Y-%m-%dT%H:%M:%S')
        duration = int(entry.media.duration.seconds)
        if pub_date >= EARLIEST and duration <= 120:
            return (pub_date,duration,entry)
        else:
            return False

class YouTubeMediaImporter():
    def __init__(self,media_type,media_profile):
        self.processing_dir = os.path.expanduser('db_script/processing')
        #self.log = set_up_logger("ad_media_importer",self.processing_dir)
        log.info("Beginning import for %s"%(media_profile.url,))
        self.media_type = media_type
        self.media_profile = media_profile
        log.info("collecting youtube media for %s"%(media_profile.url,))
        self.collector = YouTubeMediaCollector(
                self.extract_username(media_profile))
        log.info("filtering out old ads for %s"%(media_profile.url,))
        self.filter_for_new_ads()
    def extract_username(self,media_profile):
        path = urlparse.urlparse(media_profile.url).path
        return path.replace('/user/','')
    def upload(self):
        log.info("uploading %d ads for %s"%
                (len(self.collector.youtube_medias),self.media_profile.url))
        if self.collector.youtube_medias:
            for youtube_media in self.collector.youtube_medias:
                ad = Ad(title=youtube_media.title, \
                        ingested=False, \
                        profile_url=self.media_profile.url)
                ad.save()
                try:
                    if youtube_media.keywords:
                        for keyword in youtube_media.keywords:
                            tag,created_tag = Tag.objects.get_or_create(name=keyword)
                            if created_tag:
                                tag.save()
                            ad.tags.add(tag)
                except AttributeError:
                    print youtube_media
                ad.save()
                media = Media(url=youtube_media.url, \
                              media_profile=self.media_profile, \
                              duration=youtube_media.duration, \
                              pub_date=youtube_media.pub_date, \
                              ad=ad)
                if youtube_media.description:
                    media.creator_description = youtube_media.description
                media.save()
        else:
            log.info("No ads to upload for %s"%(self.media_profile.url,))
            pass
    def filter_for_new_ads(self):
        imported = set([m.url for m in self.media_profile.media_set.all()])
        found = set([ym.url for ym in self.collector.youtube_medias])
        new = found - imported
        log.info("%d of %d ads have already been imported"%
            (len(found) - len(new),len(found)))
        log.info("imported\n%s"%'\n'.join(list(imported)))
        log.info("found\n%s"%'\n'.join(list(found)))
        log.info("new\n%s"%'\n'.join(list(new)))
        new_youtube_medias = [ym for ym in self.collector.youtube_medias 
                if ym.url in new]
        log.info("%d ads in new_youtube_medias"%(len(new_youtube_medias),))
        self.collector.youtube_medias = new_youtube_medias


