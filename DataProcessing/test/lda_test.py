import unittest
from ..src.corpora import Corpora
from ..src.lda import Lda
import numpy as np

class TestLda(unittest.TestCase):
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"

    def setUp(self):
        self.corpora = Corpora(filePath = self.CSV_FILE_PATH, stopwords = "DataProcessing/src/stopwords.txt")
        # self.corpora.filterFrequentWord()
        self.lda = Lda(self.corpora, numTopics = 2)

    # def test_showTopics(self):
    #     print(self.lda.showTopics())
    #     exceptResult = [(0, '0.001*"-" + 0.001*" " + 0.001*"_" + 0.001*"圖表" + 0.001*"、" + 0.001*"「" + 0.001*"你" + 0.001*"," + 0.001*"有" + 0.001*"在"'), (1, '0.001*"-" + 0.001*" " + 0.001*"」" + 0.001*"「" + 0.001*"圖表" + 0.001*"與" + 0.001*"、" + 0.001*"你" + 0.001*"來" + 0.001*"覺化"')]
    #     self.assertEqual(exceptResult, self.lda.showTopics())
    #     print(list(self.corpora.dictionary.items()))
