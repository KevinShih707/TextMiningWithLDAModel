from CrawlCuration.visual import barchart, bubblechart
from CrawlCuration.visual.word_cloud import WC

# TODO: 更新註解
class Reco():
    def __init__(self, result, user_id=None, RUNNING_DEVSERVER=False):
        self.result = result
        self.user_id = user_id
        self.RUNNING_DEVSERVER = RUNNING_DEVSERVER
        self.topics_list = result.topics_list
        self.topic_article_count = result.topic_article_count
        self.newsStrList = result.newsStrList
        self.article_buckets = result.article_matched

    def barchart(self):
        result = barchart.provide_bar_chart_data(self.topic_article_count)
        return result

    def bubblechart(self):
        result = bubblechart.provide_bubble_chart_data(self.topics_list)
        return result

    def wc(self):
        if self.user_id is None:
            raise ValueError('By calling Reco.wc(), user_id must be given!')
        url_list = []
        for i in range(self.result.numTopics):
            wc = WC(self.result, self.topics_list, self.user_id, i, self.RUNNING_DEVSERVER)
            url_list.append(wc.draw_wordcloud())
        return url_list

    def article_matched(self):
        content_buckets = []
        for bucket in self.article_buckets:
            contents = []
            if bucket is not []:
                contents = [self.newsStrList[article_no] for article_no in bucket]
            content_buckets.append(contents)
        return content_buckets
