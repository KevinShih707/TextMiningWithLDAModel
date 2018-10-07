from DataProcessing.src.corpora import Corpora
from DataProcessing.src.lda import Lda
from CrawlCuration import mlab


class Result():
    def __init__(self, collection="news_test", col="content", numTopics=10, seed=10, topicId=0):
        """
        用來取得LDA分析的結果
        :param collection: 目標DB名稱，預設讀news_test做為測試使用
        :param col: 欲查詢之column，預設為content(即內文)
        :param numTopics: LDA主題數量
        :param seed: ? 預設10
        :param topicId: 指定
        """
        self.collection = collection
        self.numTopics = numTopics
        self.seed = seed
        self.topicId = topicId

        if(collection == "news_test"):
            print("news_test 為測試用之collection，請改用其他collection")

        # 必要之初始化
        self.newsStrList = mlab.getNewsInStringList(collection, col) # 從DB獲得string list
        self.corpora = Corpora(file=self.newsStrList) # 建立Corpora
        self.lda = Lda(self.corpora, numTopics=numTopics, seed=seed)


    def topic_str(self):
        return self.lda.showTopicsStr()


    def topic_list(self):
        return self.lda.showTopicsList()


    def classify_topic(self):
        return self.lda.classifyTopic()


    def authentic_article(self):
        try:
            return self.lda.showAuthenticArticle(self.topicId)
        except Exception as e:
            print(e)


    def article_mathed(self):
        try:
            return self.lda.findArticleMatched()
        except Exception as e:
            print(e)