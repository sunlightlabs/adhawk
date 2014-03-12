from collections import defaultdict, Counter
import datetime

from whopaid_api.models import FpQuery,TopAdsSnapshot
from knowledge_base.models import Media

class TopAdsRanker():
    def __init__(self):
        self.today = datetime.datetime.combine(datetime.date.today(),
                                                datetime.time(0,0,0))
        #self.week_ago = self.today - datetime.timedelta(days=7)
        #self.month_ago = self.today - datetime.timedelta(weeks=4)
        #self.queries = FpQuery.objects.all()
    def get_top(self,num):
        month_ago = self.today() - datetime.timedelta(days=30)
        sorted_list = Counter([fpq.result for fpq in FpQuery.objects.filter(
                              time__gt=month_ago)])

        rank = 0
        for entry, score in sorted_list.iteritems():
            rank += 1
            tas = TopAdsSnapshot(media_id=entry.result.id,
                                 score=score,
                                 rank=rank)
            tas.save()
        return sorted_list[0:num]

        # this week's top ten
#        result_count = defaultdict(int)
#        for q in self.queries.filter(time__gte=self.week_ago):
#            result_count[q.result] += 1
#        self.top_tens['last_week'] = sorted(
#                            [(k,v) for k,v in result_count.items()],
#                            key=lambda x: x[1],reverse=True)[0:10]
#        for q in self.queries.filter(time__gte=self.week_ago):
#            result_count[q.result] += 1
#        return  sorted([(k,v) for k,v in result_count.items()],
#                            key=lambda x: x[1],reverse=True)[0:10]
#        # today's top ten
#        result_count = defaultdict(int)
#        for q in self.queries.filter(time__gt=self.today):
#            result_count[q.result] += 1
#        self.top_tens['today'] = sorted(
#                            [(k,v) for k,v in result_count.items()],
#                            key=lambda x: x[1],reverse=True)[0:10]
