from gensim.models.ldamodel import LdaModel
import numpy as np
from functools import reduce
import operator
import math

class Lda():
    def __init__(self, corpora = None, savedModle = None, numTopics = 10, seed = None):
        '''
            corpora: Corpora 結構化之文本數據
            saveModel: str = None 欲載入之model路徑
            numTopics: int = 10 欲生成之主題數量
            seed: int = None 使用特定亂數種子碼
        '''
        self.numTopics = numTopics
        self.corpora = corpora
        if(savedModle == None):
            if(seed != None):
                self.ldaModel = LdaModel(corpus = corpora.TfidfPair, id2word = corpora.Dictionary, num_topics = numTopics, random_state = np.random.RandomState(seed))
            else:
                self.ldaModel = LdaModel(corpus = corpora.TfidfPair, id2word = corpora.Dictionary, num_topics = numTopics)
        else:
            self.ldaModel = LdaModel.load(savedModle)

    def saveModel(self, name = "my_model"):
        '''
            儲存訓練完成之model
            name: str = "my_modle" 儲存路徑
        '''
        self.ldaModel.save(fname = name)

    @property
    def TopicsStr(self):
        '''以字串顯示訓練lda主題'''
        # return self.ldaModel.show_topics(self.numTopics)
        return self.ldaModel.show_topics(num_topics = self.numTopics, num_words = 10, log = False, formatted = True)

    @property
    def TopicsList(self):
        '''以list of tuple 顯示主題'''
        # #將TopicStr經字串處裡拆解開來
        # # return [[(word.split("*")[0], word.split("*")[1][1:-1]) for word in topic[1].split(' + ')] for topic in self.ldaModel.show_topics(self.numTopics)]
        # result = list()
        # for topic in self.ldaModel.show_topics(self.numTopics):
        #     words = topic[1].split(' + ')
        #     result.append([(word.split("*")[0], word.split("*")[1][1:-1]) for word in words])
        # return result
        return self.ldaModel.show_topics(num_topics = self.numTopics, num_words = 10, log = False, formatted = False)

    # @property
    # def TopicsListId(self):
    #     '''
    #     將TopicList中的
    #     probility由str轉為float
    #     word轉為dicitonary key(wordId)
    #     '''
    #     topicList = self.TopicsList
    #     # return [[(prob, self.corpora.InvertDictionary[word]) for prob, word in topic] for topic in topicsList]
    #     result = list()
    #     for topic in topicList:
    #         result.append([(float(prob), self.corpora.InvertDictionary[word]) for prob, word in topic])
    #     return result

    def topicsDistribution(self, tfidf = None):
        '''
        以該模型分析代定之結構化文檔
        Input:
            tfidf: 2d_list: tfidf矩陣
        output:
            2d_list: 文檔對各主題歸屬之概率
        '''
        if(tfidf == None):
            tfidf = self.corpora.TfidfPair
        return [self.ldaModel[article] for article in tfidf]

    def classifyTopic(self, tfidf = None):
        '''回傳存有文本對應主題之list'''
        if(tfidf == None):
            tfidf = self.corpora.TfidfPair
        result = []
        for article in tfidf:
            topicId = 0;
            distribution = self.ldaModel[article]
            for pb in distribution:
                if(pb[1] > distribution[topicId][1]):
                    topicId = pb[0]
            result.append(topicId)
        return result

    def findArticleMatched(self, topicId = 'all'):
        '''將文本依主題歸類後做成list回傳'''
        if(topicId != 'all'):
            return [index for index,tid in enumerate(self.classifyTopic()) if tid == topicId]
        result = [[] for num in range(0, self.numTopics)]
        classified = self.classifyTopic()
        counter = 0
        while (counter < len(self.corpora)):
            result[classified[counter]].append(counter)
            counter += 1
        return result

    def __relativeEntropy(self, p , q):#q編碼p所需額外位元
        '''sum(p*log(p/q))'''
        if(0 in q):
            return math.inf #infinity
        return reduce(operator.add, map(lambda x, y: x*math.log(x/y), p, q))

    def showRelativeEntropy(self, topicId, dtMatrix):
        '''計算給定詞頻矩陣與該model之相對熵'''
        klMeans = list()
        p = self.ldaModel.get_topics()[topicId]
        #q
        candidatesIds = self.findArticleMatched(topicId)#取得歸類於給定主題之文本
        for id in candidatesIds:
            dtm = dtMatrix[id]
            totalWordCount = sum(dtm)#取得文章總辭彙數用於醬詞頻轉為概率
            q = list()
            for prob in dtm:
                if (prob == 0):
                    q.append(1e-20)
                else:
                    q.append(prob/totalWordCount)
            klMeans.append((id, self.__relativeEntropy(p, q)))
        return klMeans

    def showAuthenticArticle(self, topicId, num = 1):
        '''代表性文章'''
        entropy = self.showRelativeEntropy(topicId, self.corpora.DtMatrix)
        sortedEntropy = sorted(entropy, key = lambda x: x[1])
        return [t[0] for t in sortedEntropy[:num]]
