from DataProcessing.src.corpora import Corpora
from DataProcessing.src.lda import Lda
from CrawlCuration import mlab


class Result():
    def __init__(self, collection, office, classification, col="content", numTopics=10, seed=10, topicId=0):
        """
        用來取得LDA分析的結果
        :param collection: string 目標DB名稱，預設讀news_test做為測試使用
        :param office: string 要爬哪一家網站
        :param classification: string 指定新聞分類
        :param col: string 欲查詢之column，預設為content(即內文)
        :param numTopics: number LDA主題數量
        :param seed: number 預設10
        :param topicId: number 指定主題
        """
        self.collection = collection
        self.office = office
        self.classification = classification
        self.numTopics = numTopics
        self.seed = seed
        self.topicId = topicId

        # 必要之初始化
        self.newsStrList = mlab.getNewsInStringList(collection, office, classification, col) # 從DB獲得string list
        self.corpora = Corpora(file=self.newsStrList) # 建立Corpora
        self.lda = Lda(self.corpora,numTopics=numTopics, seed=seed)

        self.topics_list = self.lda.showTopicsList()
        self.article_matched = self.lda.findArticleMatched()
        self.topic_article_count = self.lda.getTopicArticleCount()
        print(self.topic_article_count)
        print(len(self.corpora))

    def authentic_article(self):
        list = self.lda.showAuthenticArticle()
        strlst = []
        for index in list:
            article = self.newsStrList[index].encode(encoding='UTF-8',errors='strict')
            strlst.append(article)
        return strlst