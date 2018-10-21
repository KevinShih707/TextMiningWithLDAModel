from DataProcessing.src.corpora import Corpora
from DataProcessing.src.lda import Lda
from CrawlCuration import mlab


class Result():
    def __init__(self, collection, office, classification, numTopics=10, seed=10, topicId=0, isWC = False):
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

        MODEL = "DataProcessing/model/model20181018853"
        # 必要之初始化
        if not isWC:
            if office == 'all' or office=='all':
                self.newsList = mlab.getAllNews(collection)
            else:
                self.newsList = mlab.getNews(collection, office, classification) # 從DB獲得string list

            self.allNews = mlab.getAllNews(collection)

            self.newsStrList = list()
            self.titleList = list()
            self.topicList = list()
            for n in self.newsList:
                self.newsStrList.append(n['content'])

            self.corpora = Corpora(file=self.newsStrList) # 建立Corpora
            self.lda = Lda(self.corpora,savedModel=MODEL,numTopics=numTopics, seed=seed)
            # self.__topics_list = self.lda.showTopicsList()
            self.__article_matched = None
            self.__topic_article_count = None
        else:
            self.lda = None

        self.__topics_list = [(0,  [('中國', 0.00047639062),
        ('美國', 0.00037435137),
        ('公司', 0.00029225092),
        ('指數', 0.0002566627),
        ('張俊彥', 0.00022969527),
        ('勇士', 0.00021694035),
        ('高雄', 0.00021350497),
        ('蘇貞昌', 0.00021222568),
        ('我們', 0.00021186536),
        ('以來', 0.0001997602)]),
        (1,
        [('小玉', 0.00027346183),
        ('影片', 0.00025995134),
        ('網友', 0.00025635093),
        ('美國', 0.00024250784),
        ('Google', 0.00022178936),
        ('活動', 0.00019575178),
        ('崔永元', 0.00019312654),
        ('LINE', 0.00019151834),
        ('川普', 0.00019090022),
        ('用戶', 0.00018937563)]),
        (2,
        [('韓國瑜', 0.00036978678),
        ('美國', 0.00030094176),
        ('中國', 0.00029430917),
        ('直播', 0.0002806509),
        ('川普', 0.00024176562),
        ('高雄', 0.00023355831),
        ('以色列', 0.00022885053),
        ('工作', 0.00021130609),
        ('市長', 0.00020245614),
        ('敘利亞', 0.00019777469)]),
        (3,
        [('美國', 0.00046023855),
        ('中國', 0.00040899497),
        ('珍珠', 0.00033986394),
        ('盈餘', 0.0003134913),
        ('指數', 0.00030400278),
        ('成長', 0.000278213),
        ('營收', 0.00027212195),
        ('台灣', 0.00027164244),
        ('投資', 0.00025646214),
        ('美股', 0.0002553117)]),
        (4,
        [('中國', 0.00049620384),
        ('指數', 0.0003966621),
        ('美國', 0.00038175387),
        ('LINE', 0.0003690428),
        ('直播', 0.00033433284),
        ('川普', 0.00027259253),
        ('日本', 0.00026921192),
        ('高雄', 0.00026903325),
        ('台股', 0.00026437643),
        ('大跌', 0.0002498227)]),
        (5,
        [('直播', 0.00042494907),
        ('美國', 0.00038126222),
        ('營收', 0.0003430544),
        ('雲端', 0.0003261396),
        ('Google', 0.00031676222),
        ('盈餘', 0.00029556805),
        ('指數', 0.00027676107),
        ('半導體', 0.00026872774),
        ('台積電', 0.00026708128),
        ('friDay', 0.000266988)]),
        (6,
        [('中國', 0.00062330905),
        ('美國', 0.00045605327),
        ('經濟', 0.0003190892),
        ('企業', 0.00031888098),
        ('川普', 0.0002911905),
        ('新創', 0.00029117696),
        ('關稅', 0.0002837851),
        ('公司', 0.00027078294),
        ('台灣', 0.0002545215),
        ('直播', 0.00024436583)]),
        (7,
        [('美國', 0.0006012147),
        ('Google', 0.0005312246),
        ('用戶', 0.00052248215),
        ('中國', 0.0004908782),
        ('功能', 0.0003593635),
        ('Instagram', 0.00032397028),
        ('就業', 0.000312239),
        ('公司', 0.00030972707),
        ('臉書', 0.00030043427),
        ('Pixel', 0.00029302927)]),
        (8,
        [('高雄', 0.0003946442),
        ('韓國瑜', 0.0003650911),
        ('直播', 0.0003070689),
        ('美國', 0.00024399607),
        ('姚文智', 0.00024140532),
        ('網友', 0.00022144533),
        ('真的', 0.00021597279),
        ('參選人', 0.00020309753),
        ('台灣', 0.00019835871),
        ('市長', 0.0001955111)]),
        (9,
        [('美國', 0.00063926395),
        ('中國', 0.00063527864),
        ('貿易', 0.00044569184),
        ('關稅', 0.00044224394),
        ('謝淑薇', 0.00028620602),
        ('影片', 0.0002654733),
        ('王石', 0.0002509555),
        ('川普', 0.00024060493),
        ('戰機', 0.00023965316),
        ('先發', 0.00023791452)])]


    @property
    def topics_list(self):
        return self.__topics_list

    @property
    def article_matched(self):
        self.__article_matched = self.lda.findArticleMatched()
        print(self.__article_matched)
        return self.__article_matched

    @property
    def topic_article_count(self):
        self.__topic_article_count = self.lda.getTopicArticleCount()
        return self.__topic_article_count

    def authentic_article(self, hc=True):
        # list = self.lda.showAuthenticArticle()
        list = [1145, 1227, 400, 1057, 41, 40, 1075, 49, 913, 1055]
        strlst = []
        for index in list:
            # article = self.newsList[index].encode(encoding='UTF-8',errors='strict')
            article = self.allNews[index]
            strlst.append(article)
        return strlst