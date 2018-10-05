import unittest
from ..src.corpora import Corpora
from ..src.lda import Lda
import numpy as np
import os
import math

class TestLda(unittest.TestCase):
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"
    STOPWORDS_FILE_PATH = "DataProcessing/test_data/testStopwords.txt"

    def setUp(self):
        self.corpora = Corpora(filePath = self.CSV_FILE_PATH, isDeleteUrl = False)
        self.lda = Lda(self.corpora, numTopics = 2, seed = 10)

    def test_createBySavingModel(self):
        self.lda.saveModel("DataProcessing/test_data/model_test.pkl")
        corpora = Corpora(filePath = self.CSV_FILE_PATH, isDeleteUrl = True)
        lda = Lda(corpora = corpora, savedModel = "DataProcessing/test_data/model_test.pkl")
        lda.showTopicsList()

    def test_isWellClassify(self):
        fakedata = [[(0,0.1), (1,0.4), (2,0.5)],
                    [(0,0.2), (1,0.3), (2,0.5)],
                    [(0,0.3), (1,0.2), (2,0.5)],
                    [(0,0.4), (1,0.1), (2,0.5)]]
        self.assertFalse(self.lda._Lda__isWellClassify(0.6,fakedata))
        self.assertTrue(self.lda._Lda__isWellClassify(0.5,fakedata))

    def test_saveModel(self):
        if(os.path.exists("DataProcessing/test_data/model_test.pkl")):
            os.remove("DataProcessing/test_data/model_test.pkl")
        self.assertFalse(os.path.exists("DataProcessing/test_data/model_test.pkl"))
        self.lda.saveModel("DataProcessing/test_data/model_test.pkl")
        self.assertTrue(os.path.exists("DataProcessing/test_data/model_test.pkl"))

    def test_classifyTopic(self):
        fakedata = [[(0,0.2), (1,0.5), (2,0.3)],
                    [(0,0.8), (1,0.1), (2,0.1)],
                    [(0,0.0), (1,0.0), (2,1.0)],
                    [(0,0.4), (1,0.1), (2,0.5)]]
        expectResult = [1, 0, 2, 2]
        self.assertEqual(expectResult, self.lda.classifyTopic(fakedata))

    def test_findArticleMatched(self):
        fakedata = [1, 2, 3, 0, 2, 0, 0, 1, 3, 0, 0, 1 ,2 ,3 ,0 ,0 ,2 ,1 ,3, 1]
        expectResult = [[3, 5, 6, 9, 10, 14, 15],
                        [0, 7, 11, 17, 19],
                        [1, 4, 12, 16],
                        [2, 8, 13, 18]]
        self.assertEqual(expectResult, self.lda.findArticleMatched(fakedata))

    def test_getArticleCount(self):
        fakedata = [[3, 5, 6, 9, 10, 14, 15],
                    [0, 7, 11, 17, 19],
                    [1, 4, 12, 16],
                    [2, 8, 13, 18]]
        expectResult = [(0, 7), (1, 5), (2, 4), (3, 4)]
        self.assertEqual(expectResult, self.lda.getArticleCount(fakedata))

    def test_relativeEntropy(self):
        p = [0.1, 0.2, 0.3, 0.4]
        q = [0.4, 0.3, 0.2, 0.1]
        r = [0.0, 0.1, 0.2, 0.3]
        self.assertEqual(0.0, self.lda._Lda__relativeEntropy(p, p))
        self.assertEqual(0.45643481914678347, self.lda._Lda__relativeEntropy(p, q))
        self.assertEqual(math.inf, self.lda._Lda__relativeEntropy(p, r))

    # def test_showRelativeEntropy(self):
    #     from pprint import pprint
    #     pprint (
    #     self.lda.showRelativeEntropy(1, self.corpora.DtMatrix)
    #     )

    # def test_showAuthenticArticle(self):
    #     print(
    #     self.lda.showAuthenticArticle(0, num = 3)
    #     )
if __name__ == "__main__":
    unittest.main()
