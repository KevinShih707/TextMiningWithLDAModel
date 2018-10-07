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

    def classifyTopic(self, topicsDistr = None):
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
            classifiedTopic = self.classifyTopic()
        numOfTopic = max(classifiedTopic) + 1
        result = [[] for num in range(0, numOfTopic)]
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

    def __relativeEntropy(self, p , q):#KL-mean
        '''sum(p*log(p/q))'''
        # if(0 in q):
        #     return math.inf #infinity
        # return reduce(operator.add, map(lambda x, y: x*math.log(x/y), p, q))
        return scipy.stats.entropy(p, q)

    def showRelativeEntropy(self, topicId, dtMatrix):
        '''
            計算給定詞頻矩陣與該model之相對熵
            topicId: 愈比對之主題ID
            dtMatrix: 愈比對之文本[[], [], []...]
        '''
        if(self.ldaModel == None):
            self.__trainingModel()
        klMeans = list()
        p = self.ldaModel.get_topics()[topicId]
        #q
        candidatesIds = self.findArticleMatched()[topicId]#取得歸類於給定主題之文本
        for id in candidatesIds:
            dtm = dtMatrix[id]
            totalWordCount = sum(dtm)#取得文章總辭彙數用於將詞頻轉為概率
            q = list()
            for prob in dtm:
                if (prob == 0):
                    q.append(1e-20)
                else:
                    q.append(prob/totalWordCount)
            klMeans.append((id, self.__relativeEntropy(p, q)))
        return klMeans

    def showAuthenticArticle(self):
        '''代表性文章'''
        # entropy = self.showRelativeEntropy(topicId, self.corpora.DtMatrix)
        # sortedEntropy = sorted(entropy, key = lambda x: x[1])
        # return [t[0] for t in sortedEntropy[:num]]

        return [i for i in range(len(self.ldaModel.get_topics()))]
