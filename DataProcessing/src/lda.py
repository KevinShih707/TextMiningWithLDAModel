from gensim.models.ldamodel import LdaModel
import numpy as np

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
            self.ldaModel = LdaModel.load(saveModel)

    def saveModel(self, name):
        LdaModel.save(name)

    def showTopicsStr(self):
        return self.ldaModel.show_topics(self.numTopics)

    def showTopicsList(self):
        result = []
        for topic in self.ldaModel.show_topics(self.numTopics):
            words = topic[1].split(' + ')
            result.append([(word.split("*")[0], word.split("*")[1][1:-1]) for word in words])
        # result = [[(word.split("*")[0], word.split("*")[1][1:-1]) for word in topic[1].split(' + ')] for topic in self.ldaModel.show_topics(self.numTopics)]
        return result

    def matchingTopics(self, tfidf = None):
        if(tfidf == None):
            tfidf = self.corpora.TfidfPair
        return [self.ldaModel[article] for article in tfidf]
