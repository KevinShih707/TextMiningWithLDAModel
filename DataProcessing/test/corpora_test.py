import unittest
from ..src import corpora
from ..src.corpora import Corpora
import numpy as np

class TestCorpora(unittest.TestCase):
    TEXT_FILE_PATH = "DataProcessing/test_data/testData.txt"
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"

    def setUp(self):
        self.corporaTxt = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt')
        self.corporaCsv = Corpora(filePath = self.CSV_FILE_PATH)

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
        print(self.corporaTxt.TfidfPair[0])
        exceptResult = np.array([(1, 0.5), (2, 0.5), (3, 0.5), (6, 0.5)])
        self.assertTrue(np.array_equal(exceptResult, self.corporaTxt.TfidfPair[0]))
        self.assertEqual(2, len(self.corporaTxt.TfidfPair))

    def test_getTfidfMatrix(self):
        expectResult = np.array([0., 0.5, 0.5, 0.5, 0., 0., 0.5, 0., 0., 0., 0., 0.])
        self.assertTrue(np.array_equal(expectResult, self.corporaTxt.TfidfMatrix[0]))
        self.assertEqual(2, len(self.corporaTxt.TfidfMatrix))

    def test_stopwordsFilter(self):
        victimText = ["帥哥", "是", "你", "#", "你是", "@", "帥哥"]
        stopwords = ["#", "@", "是", "不是"]
        result = " ".join(corpora.stopwordsFilter(victimText, stopwords))
        self.assertEqual("帥哥 你 你是 帥哥", result)

    # def test_cutCsvFileWithStopwords(self):
    #     stopwords = ["#", "@", "是", "不是"]
    #     dataDict = segmentWords.openCsvFileAsDict(self.CSV_FILE_PATH, cutText = True, stopwords = stopwords)
    #     self.assertEqual('適當 的 使用 動畫 可以 為 你 的 作品 加 分 ， 但動畫 不是 人人 都 會 做 ， 所以 這次 我們 為 大家 介紹 如何 透過   loading . io   圖示 庫 快速 製 作 屬 於 自己 的 動畫 圖示 。 \n \n 全文 :   http : / / blog . infographics . tw / 2018 / 02 / loading - io - animated - icons /', dataDict[0]['text'])

    # def test_ldaTraining(self):
    #     dataDicts = segmentWords.openCsvFileAsDict(self.CSV_FILE_PATH , cutText = True)
    #     texts = [dataDict['text'] for dataDict in dataDicts]
    #     segmentWords.ldaTraining(texts)
