from gensim.models.ldamodel import LdaModel
import numpy as np
from functools import reduce
import operator
import math

class Lda():
    def __init__(self, corpora = None, savedModle = None, numTopics = 10, seed = None):
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
        self.ldaModel.save(fname = name)

    def showTopicsStr(self):
        return self.ldaModel.show_topics(self.numTopics)

    def showTopicsList(self):
        result = []
        for topic in self.ldaModel.show_topics(self.numTopics):
            words = topic[1].split(' + ')
            result.append([(word.split("*")[0], word.split("*")[1][1:-1]) for word in words])
        # result = [[(word.split("*")[0], word.split("*")[1][1:-1]) for word in topic[1].split(' + ')] for topic in self.ldaModel.show_topics(self.numTopics)]
        return result

    # def showTopicsListId(self):
    #     topicList = self.showTopicsList()
    #     result = []
    #     for prob, word in topicList


    def topicsDistribution(self, tfidf = None):
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

    def showAuthenticArticle(self, topicId, num = 1):
        '''代表性文章'''
        #p
        probWords = self.showTopicsList()[topicId]#取得主題詞彙及其概率
        probs = [float(pw[0]) for pw in probWords]#取出概率
        keyWords = [pw[1] for pw in probWords]#取出單詞

        #q
        candidatesIds = self.findArticleMatched(topicId)#取得歸類於給定主題之文本
        dtpair = self.corpora.DtPair
        klMeans = []
        for id in candidatesIds:
            wordId = [dtp[0] for dtp in dtpair[id]]#取得候選文單詞
            wordCount = [dtp[1] for dtp in dtpair[id]]#取得候選文單詞統計
            totalWordCount = sum(wordCount)#統計文本總詞數
            q = []
            for keyWord in keyWords:
                keyWordId = self.corpora.checkWordInDictionary(keyWord)#將單詞轉為代號
                if(keyWordId in wordId):
                    q.append(wordCount[wordId.index(keyWordId)] / totalWordCount)
                else:
                    q.append(0.000000001)
            klMeans.append((id,self.__relativeEntropy(probs, q)))
        print(klMeans)
