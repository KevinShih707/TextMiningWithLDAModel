import unittest
from ..src import corpora
from ..src.corpora import Corpora
import numpy as np

class TestCorpora(unittest.TestCase):
    TEXT_FILE_PATH = "DataProcessing/test_data/testData.txt"
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"
    STOPWORDS_FILE_PATH = "DataProcessing/test_data/testStopwords.txt"

    def setUp(self):
        self.corporaTxt = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt')
        self.corporaCsv = Corpora(filePath = self.CSV_FILE_PATH)

    def tearDown(self):
        del self.corporaCsv
        del self.corporaTxt

    def test_segmentWoeds(self):
        #txt
        exceptResult = "智者 守時 而 盡 其智 ， \n"
        self.assertEqual(exceptResult, " ".join(self.corporaTxt.segmentWords()[0]))
        self.assertEqual(2, len(self.corporaTxt.segmentWords()))
        #csv
        exceptResultCsv = "適當 的 使用 動畫 可以 為 你 的 作品 加 分 ， 但動畫 不是 人人 都 會 做 ， 所以 這次 我們 為 大家 介紹 如何 透過   loading . io   圖示 庫 快速 製 作 屬 於 自己 的 動畫 圖示 。 \n \n 全文 :   http : / / blog . infographics . tw / 2018 / 02 / loading - io - animated - icons /"
        self.assertEqual(exceptResultCsv, " ".join(self.corporaCsv.segmentWords()[0]))
        self.assertEqual(100, len(self.corporaCsv.segmentWords()))

    def test_getDtPair(self):
        exceptResult = np.array([[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
                                 [(0, 1), (4, 1), (5, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1)]])
        self.assertTrue(np.array_equal(exceptResult, self.corporaTxt.DtPair))
        self.assertEqual(2, len(self.corporaTxt.DtPair))

    def test_getDtMatrix(self):
        expectResult = np.array([[1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0.],
                                 [1., 0., 0., 0., 1., 1., 0., 1., 1., 1., 1., 1.]])
        self.assertTrue(np.array_equal(expectResult, self.corporaTxt.DtMatrix))
        self.assertEqual(2, len(self.corporaTxt.DtMatrix))

    def test_getTfidfPair(self):
        exceptResult = np.array([(1, 0.5), (2, 0.5), (3, 0.5), (6, 0.5)])
        self.assertTrue(np.array_equal(exceptResult, self.corporaTxt.TfidfPair[0]))
        self.assertEqual(2, len(self.corporaTxt.TfidfPair))

    def test_getTfidfMatrix(self):
        expectResult = np.array([0., 0.5, 0.5, 0.5, 0., 0., 0.5, 0., 0., 0., 0., 0.])
        self.assertTrue(np.array_equal(expectResult, self.corporaTxt.TfidfMatrix[0]))
        self.assertEqual(2, len(self.corporaTxt.TfidfMatrix))

    def test_delDictStopwords(self):
        corpora = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt', stopwords = self.STOPWORDS_FILE_PATH)
        self.assertFalse(',' in corpora.corpus)
        self.assertFalse('\n' in corpora.corpus)
        self.assertFalse('。' in corpora.corpus)
        self.assertFalse(' ' in corpora.corpus)
        corpora2 = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt', stopwords = ['\n', '，', '。', ' '])
        self.assertFalse(',' in corpora2.corpus)
        self.assertFalse('\n' in corpora2.corpus)
        self.assertFalse('。' in corpora2.corpus)
        self.assertFalse(' ' in corpora2.corpus)
