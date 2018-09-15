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

    def test_showTopicsStr(self):
        expectResult = [(0, '0.001*"圖表" + 0.001*"覺化" + 0.001*"我們" + 0.001*"為" + 0.001*"圖" + 0.001*"視" + 0.001*"看" + 0.001*"地圖" + 0.001*"到" + 0.001*"網址"'),
                        (1, '0.001*"圖表" + 0.001*"網站" + 0.001*"讓" + 0.001*"圖" + 0.001*"www" + 0.001*"製" + 0.001*"覺化" + 0.001*"用" + 0.001*"https" + 0.001*"工具"')]
        self.assertEqual(expectResult, self.lda.showTopicsStr())

    def test_showTopicsList(self):
        result = self.lda.showTopicsList()[0][1]
        expectResult = [('圖表', 0.00095605757), ('覺化', 0.0007138438), ('我們', 0.000669788), ('為', 0.00065392844), ('圖', 0.0006407069),
                        ('視', 0.00063143723), ('看', 0.00062479294), ('地圖', 0.00062458095), ('到', 0.00062102964), ('網址', 0.00060864916)]
        count = len(result) - 1
        while(count >= 0):
            self.assertEqual(expectResult[count][0], result[count][0])
            self.assertTrue(abs(expectResult[count][1] - result[count][1]), 0.00000000001)
            count -= 1

    # def test_topicsDistribution(self):
    #     from pprint import pprint
    #     pprint(self.lda.topicsDistribution(tfidf = self.corpora.TfidfPair)[38])

    def test_saveModel(self):
        if(os.path.exists("DataProcessing/test_data/model_test.pkl")):
            os.remove("DataProcessing/test_data/model_test.pkl")
        self.assertFalse(os.path.exists("DataProcessing/test_data/model_test.pkl"))
        self.lda.saveModel("DataProcessing/test_data/model_test.pkl")
        self.assertTrue(os.path.exists("DataProcessing/test_data/model_test.pkl"))

    def test_classifyTopic(self):
        expectResult = [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1,
                        0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1,
                        0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
                        1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0,
                        1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1]
        self.assertEqual(expectResult, self.lda.classifyTopic())

    def test_findArticleMatched(self):
        result = self.lda.findArticleMatched()
        self.assertEqual([0,  2,  3,  4,  6,  7,  8,  9, 11, 12], result[0][:10])
        self.assertEqual([1,  5, 10, 13, 14, 17, 18, 19, 21, 22], result[1][:10])

    def test_relativeEntropy(self):
        p = [0.1, 0.2, 0.3, 0.4]
        q = [0.4, 0.3, 0.2, 0.1]
        r = [0.0, 0.1, 0.2, 0.3]
        self.assertEqual(0.0, self.lda._Lda__relativeEntropy(p, p))
        self.assertEqual(0.4564348191467835, self.lda._Lda__relativeEntropy(p, q))
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

    def test_isWellClassify(self):
        fackdata = [[(1,0.1), (2,0.4), (3,0.5)],
                    [(1,0.2), (2,0.3), (3,0.5)],
                    [(1,0.3), (2,0.2), (3,0.5)],
                    [(1,0.4), (2,0.1), (3,0.5)]]
        self.assertFalse(self.lda._Lda__isWellClassify(0.6,fackdata))
        self.assertTrue(self.lda._Lda__isWellClassify(0.5,fackdata))

if __name__ == "__main__":
    unittest.main()
