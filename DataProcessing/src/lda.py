from gensim.models.ldamodel import LdaModel

class Lda():
    def __init__(self, corpora = None, savedModle = None, numTopics = 10):
        self.numTopics = numTopics
        self.corpora = corpora
        self.ldaModel = LdaModel(corpus = corpora.TfidfPair, id2word = corpora.Dictionary, num_topics = numTopics)

    def showTopics(self):
        return self.ldaModel.show_topics(self.numTopics)
