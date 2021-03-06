from CrawlCuration.visual import barchart, bubblechart
from CrawlCuration.visual.word_cloud import WC

# TODO: 更新註解
class Reco():
    def __init__(self, result, user_id=None, RUNNING_DEVSERVER=False, isWC=False):
        if not isWC:
            self.result = result
            self.user_id = user_id
            self.RUNNING_DEVSERVER = RUNNING_DEVSERVER
            self.topic_article_count = result.topic_article_count
            self.newsStrList = result.newsStrList
            self.titleList = result.titleList
            self.article_buckets = result.article_matched
            self.topicList = result.topicList
            self.newsList = result.newsList

        self.topics_list = result.topics_list

    def barchart(self):
        result = barchart.provide_bar_chart_data(self.topic_article_count)
        return result

    def bubblechart(self):
        result = bubblechart.provide_bubble_chart_data(self.topics_list)
        return result

    # def wc(self):
    #     if self.user_id is None:
    #         raise ValueError('By calling Reco.wc(), user_id must be given!')
    #     url_list = []
    #     for i in range(self.result.numTopics):
    #         wc = WC(self.topics_list, self.user_id, i, self.RUNNING_DEVSERVER)
    #         url_list.append(wc.draw_wordcloud())
    #     return url_list

    def wc(self):
        wc = WC(self.topics_list, self.user_id, 0, self.RUNNING_DEVSERVER)
        return wc.draw_wordcloud()

    def newsDistri(self):
        content_buckets = []
        for bucket in self.article_buckets:
            contents = []
            if bucket is not []:
                contents = [self.newsList[article_no] for article_no in bucket]
            content_buckets.append(contents)
        print("content buckets", len(content_buckets))
        return content_buckets