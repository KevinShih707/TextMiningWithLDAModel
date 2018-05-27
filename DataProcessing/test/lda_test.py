import unittest
from ..src.corpora import Corpora
from ..src.lda import Lda
import numpy as np

class TestLda(unittest.TestCase):
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"

    def setUp(self):
        self.corpora = Corpora(filePath = self.CSV_FILE_PATH, stopwords = "DataProcessing/src/stopwords.txt")
        # self.corpora.filterFrequentWord()
        self.lda = Lda(self.corpora, numTopics = 10)

    # def test_showTopicsStr(self):
    #     """需要固定亂數種子,否則無法測"""
    #     from pprint import pprint
    #     print("\n")
    #     pprint(self.lda.showTopicsStr())
    #  
    # def test_showTopicsList(self):
    #     from pprint import pprint
    #     pprint(self.lda.showTopicsList())
    #
    # def test_matchTopic(self):
    #     print(self.lda.matchingTopics(tfidf = self.corpora.TfidfPair))
