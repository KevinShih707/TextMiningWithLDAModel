import unittest
from ..src.corpora import Corpora
from ..src.lda import Lda
import numpy as np
import os

class TestLda(unittest.TestCase):
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"

    def setUp(self):
        self.corpora = Corpora(filePath = self.CSV_FILE_PATH, stopwords = "DataProcessing/src/stopwords.txt")
        self.lda = Lda(self.corpora, numTopics = 2, seed = 10)

    def test_showTopicsStr(self):
        expectResult = [(0, '0.001*"來" + 0.001*"圖表" + 0.001*"你" + 0.001*"與" + 0.001*"讓" + 0.001*"在" + 0.001*"有" + 0.001*"吧" + 0.001*"圖" + 0.001*"也"'),
                        (1, '0.001*"圖表" + 0.001*"你" + 0.001*"在" + 0.001*"與" + 0.001*"覺化" + 0.001*"圖" + 0.001*"為" + 0.001*"台灣" + 0.001*"上" + 0.001*"呢"')]
        self.assertEqual(expectResult, self.lda.showTopicsStr())

    def test_showTopicsList(self):
        expectResult = [[('0.001', '來'), ('0.001', '圖表'), ('0.001', '你'), ('0.001', '與'), ('0.001', '讓'), ('0.001', '在'), ('0.001', '有'), ('0.001', '吧'), ('0.001', '圖'), ('0.001', '也')],
                        [('0.001', '圖表'), ('0.001', '你'), ('0.001', '在'), ('0.001', '與'), ('0.001', '覺化'), ('0.001', '圖'), ('0.001', '為'), ('0.001', '台灣'), ('0.001', '上'), ('0.001', '呢')]]
        self.assertEqual(expectResult, self.lda.showTopicsList())

    # def test_matchTopic(self):
    #     print(self.lda.matchingTopics(tfidf = self.corpora.TfidfPair))

    def test_saveModel(self):
        if(os.path.exists("DataProcessing/test_data/model_test.pkl")):
            os.remove("DataProcessing/test_data/model_test.pkl")
        self.assertFalse(os.path.exists("DataProcessing/test_data/model_test.pkl"))
        self.lda.saveModel("DataProcessing/test_data/model_test.pkl")
        self.assertTrue(os.path.exists("DataProcessing/test_data/model_test.pkl"))
