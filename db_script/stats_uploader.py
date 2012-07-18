from collections import defaultdict
from knowledge_base.models import Media
from whopaid.settings import MEDIA_ROOT

RMSE_FILE = MEDIA_ROOT+'images/media_thumbnails/stats/rmse.csv'

class RMSEUploader():
    def __init__(self):
        self.stats_file = open(RMSE_FILE)
        self.set_d()
    def clean_line(self,line):
        return line.replace('(','').replace(')','').strip()
    def parse_line(self,line):
        l = line.split()
        pk = int(l[0])
        min_rmse = min([float(i) for i in [l[2],l[4],l[6]]])
        return pk,min_rmse
    def set_d(self):
        self.d = defaultdict(float)
        for line in self.stats_file:
            pk,min_rmse = self.parse_line(self.clean_line(line))
            self.d[pk] = min_rmse
    def upload(self):
        for pk,min_rmse in self.d.items():
            m = Media.objects.get(pk=pk)
            m.rmse = min_rmse
            m.save()

