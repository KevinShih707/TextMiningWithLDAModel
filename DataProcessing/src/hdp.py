from gensim.models import HdpModel

class Hdp():
    def __init__(self, corpora = None):
        ''' corpora: Corpora 結構化之文本數據 '''
        self.hdp = HdpModel(corpora.TfidfPair, corpora.Dictionary, max_time = 60)

    def showTopicsStr(self, topn = 10):
        return self.hdp.show_topics(num_topics=topn, num_words = 10)
