import unittest
from ..src.corpora import Corpora
from ..src.lda import Lda
import numpy as np
import os
import math

class TestLdaFn(unittest.TestCase):

    def setUp(self):
        self.corpora = Corpora()
        self.lda = Lda(self.corpora, numTopics = 2, seed = 10)

    def test_isWellClassify(self):
        fakedata = [[(0,0.1), (1,0.4), (2,0.5)],
                    [(0,0.2), (1,0.3), (2,0.5)],
                    [(0,0.3), (1,0.2), (2,0.5)],
                    [(0,0.4), (1,0.1), (2,0.5)]]
        self.assertFalse(self.lda._Lda__isWellClassify(0.6,fakedata))
        self.assertTrue(self.lda._Lda__isWellClassify(0.5,fakedata))

    def test_classifyTopic(self):
        fakedata = [[(0,0.2), (1,0.5), (2,0.3)],
                    [(0,0.8), (1,0.1), (2,0.1)],
                    [(0,0.0), (1,0.0), (2,1.0)],
                    [(0,0.4), (1,0.1), (2,0.5)],
                    [(0,0.2), (2,0.8)]]
        expectResult = [1, 0, 2, 2, 2]
        self.assertEqual(expectResult, self.lda._Lda__classifyTopic(fakedata))

    def test_findArticleMatched(self):
        fakedata = [1, 2, 3, 0, 2, 0, 0, 1, 3, 0, 0, 1 ,2 ,3 ,0 ,0 ,2 ,1 ,3, 1]
        expectResult = [[3, 5, 6, 9, 10, 14, 15],
                        [0, 7, 11, 17, 19],
                        [1, 4, 12, 16],
                        [2, 8, 13, 18]]
        self.assertEqual(expectResult, self.lda.findArticleMatched(fakedata))

    def test_getTopicArticleCount(self):
        fakedata = [[3, 5, 6, 9, 10, 14, 15],
                    [0, 7, 11, 17, 19],
                    [1, 4, 12, 16],
                    [2, 8, 13, 18]]
        expectResult = [(0, 7), (1, 5), (2, 4), (3, 4)]
        self.assertEqual(expectResult, self.lda.getTopicArticleCount(fakedata))

    def test_subTfidfPair(self):
        leaveKeySequence = [1, 2, 5, 7]
        tfidfPair = [(0, 0.0), (1, 0.1), (3, 0.3), (4, 0.4),
                     (5, 0.5), (6, 0.6), (8, 0.8), (9, 0.9)]
        result = self.lda._Lda__subTfidfPair(tfidfPair, leaveKeySequence)
        self.assertEqual([(1, 0.1), (2, 0.0), (5,0.5), (7, 0.0)], result[0])
        self.assertEqual(2, result[1])#padungCount

    def test_relativeEntropy(self):
        p = [0.1, 0.2, 0.3, 0.4]
        q = [0.4, 0.3, 0.2, 0.1]
        r = [0.0, 0.1, 0.2, 0.3]
        self.assertEqual(0.0, self.lda._Lda__relativeEntropy(p, p))
        self.assertEqual(0.45643481914678347, self.lda._Lda__relativeEntropy(p, q))
        self.assertEqual(math.inf, self.lda._Lda__relativeEntropy(p, r))

class TestLda(unittest.TestCase):
    TEXT_FILE_PATH = "DataProcessing/test_data/testData.txt"
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"
    STOPWORDS_FILE_PATH = "DataProcessing/test_data/testStopwords.txt"
    MODEL_SAVING_PATH = "DataProcessing/test_data/model_test"
    MODEL_SAVING_PATH_WITH_EXTENSION = MODEL_SAVING_PATH + ".pkl"

    def setUp(self):
        self.corpora = Corpora(filePath = self.CSV_FILE_PATH, isDeleteUrl = False)
        self.lda = Lda(self.corpora, numTopics = 2, seed = 10)

    def test_saveModel(self):
        if(os.path.exists(self.MODEL_SAVING_PATH_WITH_EXTENSION)):
            os.remove(self.MODEL_SAVING_PATH_WITH_EXTENSION)
        if(os.path.exists(self.MODEL_SAVING_PATH)):
            os.remove(self.MODEL_SAVING_PATH)
        self.assertFalse(os.path.exists(self.MODEL_SAVING_PATH_WITH_EXTENSION))
        self.assertFalse(os.path.exists(self.MODEL_SAVING_PATH))
        self.lda.saveModel(self.MODEL_SAVING_PATH)
        self.assertTrue(os.path.exists(self.MODEL_SAVING_PATH_WITH_EXTENSION))
        self.assertTrue(os.path.exists(self.MODEL_SAVING_PATH))

    def test_createBySavingModel(self):
        if(not os.path.exists(self.MODEL_SAVING_PATH_WITH_EXTENSION)):
            self.lda.saveModel(self.MODEL_SAVING_PATH)
        corpora = Corpora(filePath = self.CSV_FILE_PATH, isDeleteUrl = True)
        lda = Lda(corpora = corpora, savedModel = self.MODEL_SAVING_PATH)
        lda.showTopicsList()

    def test_createBySavingDictLoading(self):
        corpora1 = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt', isDeleteUrl = True)
        corpora2 = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt', isDeleteUrl = True)
        ldaBySaving = Lda(corpora1, self.MODEL_SAVING_PATH)
        ldaDirectTraining = Lda(corpora2, savedModel = None)
        self.assertNotEqual(ldaBySaving.corpora.DtPair, ldaDirectTraining.corpora.DtPair)

    def test_showAuthenticArticle(self):
        fakedata = [[(0, 0.253), (1, 0.251), (2, 0.176), (3, 0.132), (4, 0.116), (15, 0.164), (16, 0.176), (17, 0.121), (18, 0.116), (19, 0.068)],
                    [(5, 0.192), (6, 0.252), (7, 0.528), (8, 0.076), (9, 0.383), (10, 0.107), (11, 0.121), (12, 0.252), (13, 0.192), (14, 0.152)]]
        self.assertEqual([19,8], self.lda.showAuthenticArticle(fakedata))
        self.assertTrue(self.lda.showAuthenticArticle()[0] in self.lda.findArticleMatched()[0])
        self.assertTrue(self.lda.showAuthenticArticle()[1] in self.lda.findArticleMatched()[1])

    def test_NumTopics(self):
        self.assertEqual(2, self.lda.NumTopics)

class TestLdaOtherCrop(unittest.TestCase):
    TEXT_FILE_PATH = "DataProcessing/test_data/10articles.txt"
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"
    STOPWORDS_FILE_PATH = "DataProcessing/test_data/testStopwords.txt"
    MODEL_SAVING_PATH = "DataProcessing/test_data/mode2_test"
    MODEL_SAVING_PATH_WITH_EXTENSION = MODEL_SAVING_PATH + ".pkl"

    def setUp(self):
        self.corporaCsv = Corpora(filePath = self.CSV_FILE_PATH)
        self.corporaTxt = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt')
        self.ldaCsv = Lda(self.corporaCsv, numTopics = 10, seed = 10)
        self.ldaCsv.saveModel(self.MODEL_SAVING_PATH)
        self.ldaTxt = Lda(corpora = self.corporaTxt, savedModel = self.MODEL_SAVING_PATH)

    def tearDown(self):
        if(os.path.exists(self.MODEL_SAVING_PATH_WITH_EXTENSION)):
            os.remove(self.MODEL_SAVING_PATH_WITH_EXTENSION)
            os.remove(self.MODEL_SAVING_PATH_WITH_EXTENSION + ".expElogbeta.npy")
            os.remove(self.MODEL_SAVING_PATH_WITH_EXTENSION + ".id2word")
            os.remove(self.MODEL_SAVING_PATH_WITH_EXTENSION + ".state")
        if(os.path.exists(self.MODEL_SAVING_PATH)):
            os.remove(self.MODEL_SAVING_PATH)

    def test_foo(self):
        print()
        print("\n代表性文章")
        print(self.ldaCsv.showAuthenticArticle())
        print("\n文本對應主題，每個list一個主題內裝對應到他的文章No.")
        print(self.ldaTxt.findArticleMatched())
        print("\n(主題編號，有幾篇)")
        print(self.ldaTxt.getTopicArticleCount())
        print("\n總共有幾篇文章")
        print(len(self.corporaTxt))

    '''
        代表性文章
        [48, 22, 58, 2, 12, 6, 84, 47, 1, 32]

        文本對應主題，每個list一個主題內裝對應到他的文章No.
        [[], [], [6], [2], [0, 3, 5], [4], [], [], [1]]

        (主題編號，有幾篇)
        [(0, 0), (1, 0), (2, 1), (3, 1), (4, 3), (5, 1), (6, 0), (7, 0), (8, 1)]

        總共有幾篇文章
        7
    '''

if __name__ == "__main__":
    unittest.main()
