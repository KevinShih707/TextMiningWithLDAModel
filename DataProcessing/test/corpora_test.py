import unittest
from ..src import corpora
from ..src.corpora import Corpora
import numpy as np

class TestCorpora(unittest.TestCase):
    TEXT_FILE_PATH = "DataProcessing/test_data/testData.txt"
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"
    STOPWORDS_FILE_PATH = "DataProcessing/test_data/testStopwords.txt"

    def setUp(self):
        self.mockCorpora = Corpora(filePath = "")

    def tearDown(self):
        del self.mockCorpora

    def test_segmentWoeds(self):
        articles = ["智者守時而盡其智，\n不肖者守命而盡其力。", "夫戰勝攻取，而不修其攻者凶，命曰費留。", "主不可以怒而興師，將不可以慍而致戰；合于利而動，不合于利而止。"]
        segmentedArticle = self.mockCorpora._Corpora__segmentWords(articles)
        expectResult = ["智者", "守時", "而", "盡", "其智", "，", "\n","不肖", "者", "守命", "而", "盡", "其力", "。"]
        self.assertEqual(expectResult, segmentedArticle[0])

    def test_openFile(self):
        #txt
        contentTxt = self.mockCorpora._Corpora__openFile(self.TEXT_FILE_PATH, 'txt')
        expectResult0 = "智者守時而盡其智，\n不肖者守命而盡其力。"
        expectResult1 = "智者守時，\n不肖者守命。\n"
        self.assertEqual(expectResult0, contentTxt[0])
        self.assertEqual(expectResult1, contentTxt[1])

        #csv
        contentCsv = self.mockCorpora._Corpora__openFile(self.CSV_FILE_PATH, 'csv', ['time', 'id', 'text', 'share', 'likecount', 'sharecount'])
        expectResult0 = "適當的使用動畫可以為你的作品加分，但動畫不是人人都會做，所以這次我們為大家介紹如何透過 loading.io 圖示庫快速製作屬於自己的動畫圖示。"
        expectResult1 = "你能畫出騙過 A* 的絕妙迷宮嗎？\n\n網址: http://qiao.github.io/PathFinding.js/visual"
        self.assertEqual(expectResult0, contentCsv[0][:72])
        self.assertEqual(expectResult1, contentCsv[99][-66:])

    def test_delLinesHasUrl(self):
        article = "第一行\nhttps://www.ntut.edu.tw/\n第三行\nhttp://www.ntut.edu.tw/\n第五行"
        noUrlArticle = self.mockCorpora._Corpora__delLinesHasUrl(article)
        expectResult = "第一行\n第三行\n第五行"
        self.assertEqual(expectResult, noUrlArticle)

    def test_delDictStopwords(self):
        corpora = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt', stopwords = self.STOPWORDS_FILE_PATH)
        self.assertFalse(',' in corpora.InvertDictionary)
        # self.assertFalse('\n' in corpora.InvertDictionary)
        self.assertFalse('。' in corpora.InvertDictionary)
        self.assertFalse(' ' in corpora.InvertDictionary)
        corpora2 = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt', stopwords = ['\n', '，', '。', ' '])
        self.assertFalse(',' in corpora2.InvertDictionary)
        self.assertFalse('\n' in corpora2.InvertDictionary)
        self.assertFalse('。' in corpora2.InvertDictionary)
        self.assertFalse(' ' in corpora2.InvertDictionary)

class TestCorporaProperties(unittest.TestCase):
    TEXT_FILE_PATH = "DataProcessing/test_data/testData.txt"
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"
    STOPWORDS_FILE_PATH = "DataProcessing/test_data/testStopwords.txt"

    def setUp(self):
        self.corporaTxt = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt', stopwords = self.STOPWORDS_FILE_PATH)

    def tearDown(self):
        del self.corporaTxt

    def test_checkWordInDictionary(self):
        self.assertEqual(0, self.corporaTxt.checkWordInDictionary('\n'))
        self.assertEqual(1, self.corporaTxt.checkWordInDictionary('不肖'))
        self.assertEqual(2, self.corporaTxt.checkWordInDictionary('其力'))
        self.assertEqual(3, self.corporaTxt.checkWordInDictionary('其智'))
        self.assertEqual(4, self.corporaTxt.checkWordInDictionary('守命'))
        self.assertEqual(5, self.corporaTxt.checkWordInDictionary('守時'))
        self.assertEqual(6, self.corporaTxt.checkWordInDictionary('智者'))
        self.assertEqual(7, self.corporaTxt.checkWordInDictionary('盡'))
        self.assertEqual(8, self.corporaTxt.checkWordInDictionary('者'))
        self.assertEqual(9, self.corporaTxt.checkWordInDictionary('而'))
        self.assertEqual(None, self.corporaTxt.checkWordInDictionary('瞎掰的'))

    def test_Dictionary(self):
        self.assertEqual('不肖', self.corporaTxt.Dictionary.get(1))
        self.assertEqual(None, self.corporaTxt.Dictionary.get(-1))
        self.assertEqual(1, self.corporaTxt.InvertDictionary.get('不肖'))
        self.assertEqual(None, self.corporaTxt.InvertDictionary.get('zzz'))

    def test_getDtPair(self):
        expectResult = np.array([[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 2), (8, 1), (9, 2)],
                                 [(0, 1), (1, 1), (4, 1), (5, 1), (6, 1), (8, 1)]])
        self.assertTrue(np.array_equal(expectResult, self.corporaTxt.DtPair))

    def test_getDtMatrix(self):
        print()
        expectResult = np.array([[1., 1., 1., 1., 1., 1., 1., 2., 1., 2.],
                                 [1., 1., 0., 0., 1., 1., 1., 0., 1., 0.]])
        self.assertTrue(np.array_equal(expectResult, self.corporaTxt.DtMatrix))

    def test_getTfidfPair(self):
        expectResult = [[(2, 0.31622776601683794), (3, 0.31622776601683794), (7, 0.6324555320336759), (9, 0.6324555320336759)],[ ]]
        self.assertTrue(np.array_equal(expectResult, self.corporaTxt.TfidfPair))

    def test_getTfidfMatrix(self):
        expectResult = np.array([[0., 0., 0.31622776, 0.31622776, 0., 0., 0., 0.6324555 , 0., 0.6324555],[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])
        minus = self.corporaTxt.TfidfMatrix - expectResult
        for row in minus:
            for a in row:
                self.assertTrue(a < 0.00001)

    def test_lenOfCorpus(self):
        self.assertEqual(2, len(self.corporaTxt))
