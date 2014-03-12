import logging

log = logging.getLogger('db_script.ad_media_reporter')

class AdMediaReporter():
    def __init__(self,count):
        self.count = count
    def send_emails(self):
        email = 'There were %d new videos added for your review'%(
                                                            self.count,)
        email += '\nThanks again for all of your help on Ad Hawk!'
        log.info(email)
