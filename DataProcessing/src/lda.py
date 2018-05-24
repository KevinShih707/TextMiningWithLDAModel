from gensim.models.ldamodel import LdaModel

class Lda():
    def __init__(self, corpora = None, savedModle = None, numTopics = 10):
        self.numTopics = numTopics
        self.corpora = corpora
        self.ldaModel = LdaModel(corpus = corpora.TfidfPair, id2word = corpora.Dictionary, num_topics = numTopics)

    def showTopicsStr(self):
        return self.ldaModel.show_topics(self.numTopics)

    def showTopicsList(self):
        result = []
        for topic in self.ldaModel.show_topics(self.numTopics):
            words = topic[1].split(' + ')
            result.append([(word.split("*")[0], word.split("*")[1][1:-1]) for word in words])
        # result = [[(word.split("*")[0], word.split("*")[1][1:-1]) for word in topic[1].split(' + ')] for topic in self.ldaModel.show_topics(self.numTopics)]
        return result
