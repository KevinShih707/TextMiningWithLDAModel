from gensim.models.ldamodel import LdaModel
import numpy as np
from functools import reduce
import operator
import math

class Lda():
    def __init__(self, corpora = None, savedModle = None, numTopics = 10, seed = None, autoAproach = False):
        '''
            corpora: Corpora 結構化之文本數據
            saveModel: str = None 欲載入之model路徑
            numTopics: int = 10 欲生成之主題數量
            seed: int = None 使用特定亂數種子碼
            autoAproach = False 是否自動調整主題數目找出適當值
        '''
        self.corpora = corpora
        self.numTopics = numTopics
        self.seed = seed

        if(savedModle == None):
            self.__trainingModel()
        else:
            self.ldaModel = LdaModel.load(savedModle)

        if(autoAproach):
            wellLastTime = False
            while(self.__isWellClassify() or not wellLastTime):
                if(self.__isWellClassify()):
                    wellLastTime = True
                    savedModle(name = "temp")
                    self.numTopics -= 1
                    self.__trainingModel()
                elif(not wellLastTime):
                    self.numTopics += 2
                    self.__trainingModel()
            # else:
            self.numTopics += 1
            LdaModel.load("temp.pkl")

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
        self.ldaModel.save(fname = name)

    def showTopicsStr(self, topn = 10):
        '''以字串顯示訓練lda主題'''
        return self.ldaModel.show_topics(num_topics = self.numTopics, num_words = topn)

    def showTopicsList(self, topn = 10):
        '''以list of tuple 顯示主題'''
        return self.ldaModel.show_topics(num_topics = self.numTopics, num_words = topn, formatted = False)

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
            topicId = 0
            distribution = self.ldaModel[article]
            for pb in distribution:
                if(pb[1] > distribution[topicId][1]):
                    topicId = pb[0]
            result.append(topicId)
        return result

    def findArticleMatched(self):
        '''將文本依主題歸類後做成list回傳'''
        # if(topicId != 'all'):
        #     return [index for index,tid in enumerate(self.classifyTopic()) if tid == topicId]
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
        candidatesIds = self.findArticleMatched()[topicId]#取得歸類於給定主題之文本
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
