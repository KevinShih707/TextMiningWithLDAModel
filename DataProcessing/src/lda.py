from gensim.models.ldamodel import LdaModel
from gensim import corpora
import numpy as np
import scipy.stats
from functools import reduce
import operator
import math

class Lda():
    def __init__(self, corpora = None, savedModel = None, numTopics = 10, seed = None):
        '''
            corpora: Corpora 結構化之文本數據
            saveModel: str = None 欲載入之model路徑
            numTopics: int = 10 欲生成之主題數量
            seed: int = None 使用特定亂數種子碼
        '''
        self.corpora = corpora
        self.numTopics = numTopics
        self.seed = seed

        if(savedModel != None):
            self.ldaModel = LdaModel.load(savedModel+".pkl")
            self.corpora.changeDictionary(corpora.Dictionary.load_from_text(savedModel))
        else:
            self.ldaModel = None

    def __trainingModel(self):
        if(self.seed != None):
            self.ldaModel = LdaModel(corpus = self.corpora.TfidfPair,
                                id2word = self.corpora.Dictionary,
                                num_topics = self.numTopics,
                                random_state = np.random.RandomState(self.seed))
        else:
            self.ldaModel = LdaModel(corpus = self.corpora.TfidfPair,
                                id2word = self.corpora.Dictionary,
                                num_topics = self.numTopics)
        print("Training success")

    def __isWellClassify(self, threshold = 0.8, test = None):
        '''
            確認個文本至少有一主題之吻合度(概率)大於標準值
            threshold = 0.8: 最小接受之主題分佈(標準值)
            (test : 測試用的虛擬分佈)
        '''
        if(test == None):
            test = self.topicsDistribution()
        for tdb in test:
            ambiguous = True
            for prob in tdb:
                if(prob[1] >= threshold):
                    ambiguous = False
                    break
            if(ambiguous):
                return False
        return True

    def saveModel(self, name = "my_model"):
        '''
            儲存訓練完成之model
            name: str = "my_modle" 儲存路徑
        '''
        if(self.ldaModel == None):
            self.__trainingModel()
        self.ldaModel.save(fname = name+".pkl")
        self.corpora.Dictionary.save_as_text(fname = name)

    def showTopicsStr(self, topn = 10):
        '''
            以字串顯示訓練lda主題
            topn: 欲顯示的詞彙個數
            EX:[(0, '0.001*"網址" + 0.001*"https"'), (1, '0.001*"我們" + 0.001*"www"')]
        '''
        if(self.ldaModel == None):
            self.__trainingModel()
        return self.ldaModel.show_topics(num_topics = self.numTopics, num_words = topn)

    def showTopicsList(self, topn = 10):
        '''
            以list of tuple 顯示主題
            topn: 欲顯示的詞彙個數
            EX:[(0, [('網址', 0.00094305066), ('https', 0.0008922861)]), (1, [('我們', 0.00081777375), ('www', 0.0008147125)])]
        '''
        if(self.ldaModel == None):
            self.__trainingModel()
        return self.ldaModel.show_topics(num_topics = self.numTopics, num_words = topn, formatted = False)

    def topicsDistribution(self, tfidf = None):
        '''
        以該模型分析待定之結構化文檔
        Input:
            tfidf: 2d_list: tfidf矩陣
        output:
            2d_list: 文檔對各主題歸屬之概率
        '''
        if(tfidf == None):
            tfidf = self.corpora.TfidfPair
        if(self.ldaModel == None):
            self.__trainingModel()
        return [self.ldaModel[article] for article in tfidf]

    def __classifyTopic(self, topicsDistr = None):
        '''回傳存有文本對應主題之list'''
        if(topicsDistr == None):
            topicsDistr = self.topicsDistribution()
        result = []
        for article in topicsDistr: #針對每一篇文章測試
            sortedByDb = sorted(article, key = lambda x:x[1], reverse = True)
            result.append(sortedByDb[0][0]) #機率最高的ID
        return result

    def findArticleMatched(self, classifiedTopic = None):
        '''將文本依主題歸類後做成list回傳'''
        if(classifiedTopic == None):
            classifiedTopic = self.__classifyTopic()
        result = [[] for num in range(0, self.NumTopics)]
        counter = 0
        while (counter < len(classifiedTopic)):
            result[classifiedTopic[counter]].append(counter) #把文章丟進對應的主題桶子
            counter += 1
        return result

    def getTopicArticleCount(self, ArticleMached = None):
        '''回傳分類後各組題包含幾篇文章'''
        if(ArticleMached == None):
            ArticleMached = self.findArticleMatched()
        if(self.ldaModel == None):
            self.__trainingModel()
        count = [len(mached) for mached in ArticleMached]
        index = [x for x in range(len(ArticleMached))]
        return list(zip(index, count))

    def __subTfidfPair(self, tfidfPair, sequence):
        '''
            裁減tfidfPPair僅保留序列中的詞, 入部存在則補零
            tfidfPair:Cprpora.TfidfPair
            sequence:欲保留的key序列
        '''
        tfpSpeKey = [pair[0] for pair in tfidfPair]
        tfpSpePro = [pair[1] for pair in tfidfPair]
        result = list()
        padingCount = 0#紀錄共有幾個零
        for key in sequence:
            if(key in tfpSpeKey):
                result.append((key, tfpSpePro[tfpSpeKey.index(key)]))
            else:
                result.append((key, 0.0))
                padingCount += 1
        return [result, padingCount]

    def __relativeEntropy(self, p , q):#KL-mean
        '''sum(p*log(p/q))'''
        # if(0 in q):
        #     return math.inf #infinity
        # return reduce(operator.add, map(lambda x, y: x*math.log(x/y), p, q))
        return scipy.stats.entropy(p, q)

    def __ArticleMatchKl(self, articleMached = None):
        '''
            計算出代表性文章的kl
            output:[[(topicid, kl), ...],
                    [(topicid, kl), ...],
                    ....]
        '''
        if(self.ldaModel == None):
            self.__trainingModel()
        if(articleMached == None):
            articleMached = self.findArticleMatched()#取得歸類於各主題之文本

        result = list()
        for i in range(self.NumTopics):
            topicTrem = [self.ldaModel.get_topic_terms(topicid = i, topn = 10)][0]
            sequence = [pair[0] for pair in topicTrem]
            topicProb = [pair[1] for pair in topicTrem]
            topicProb.append(1 - sum(topicProb))#將非代表詞加總視為「其他」的概率
            topicMatch = articleMached[i]
            klThisTopic = list()
            for candidateId in topicMatch:
                tfp = self.corpora.TfidfPair[candidateId]
                subTfpb = self.__subTfidfPair(tfp, sequence)
                if(subTfpb[1] != 0):#含有零
                    klThisTopic.append((candidateId, subTfpb[1]))
                else:
                    subTfpbProb = [pair [1] for pair in subTfpb[0]]
                    subTfpbProb.append(1 - sum(subTfpbProb))#將非代表詞加總視為「其他」的概率
                    klThisTopic.append((candidateId, scipy.stats.entropy(subTfpbProb, topicProb)))
            result.append(klThisTopic)
        return result

    def showAuthenticArticle(self, articleMatchKl_input = None):
        '''代表性文章'''
        if (articleMatchKl_input is None):
            articleMatchKl = self.__ArticleMatchKl()
        else:
            articleMatchKl = articleMatchKl_input
        result = []
        for eachTopic in articleMatchKl:
            result.append(sorted(eachTopic, key = lambda x:x[1])[0][0])
        return result

    @property
    def NumTopics(self):
        '''Model 的 topic 數量'''
        if(self.ldaModel == None):
            self.__trainingModel()
        return len(self.ldaModel.get_topics())
