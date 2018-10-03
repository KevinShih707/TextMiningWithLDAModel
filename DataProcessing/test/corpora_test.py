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
        segmentedArticle = self.mockCorpora._Corpora__segmentWords(articles, getAll = True)
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
        expectResult0 = "適當的使用動畫可以為你的作品加分"
        expectResult1 = "你能畫出騙過 A* 的絕妙迷宮嗎？網址: http://qiao.github.io/PathFinding.js/visual"
        self.assertEqual(expectResult0, contentCsv[0][:16])
        self.assertEqual(expectResult1, contentCsv[99][-64:])

    def test_removeUrl(self):
        article = "第一行\n快速連結  ： https://www.ntut.edu.tw/\n第三行\n網址: http://qiao.github.io/PathFinding.js/visual\n第五行"
        #whole line mode
        expectResult = "第一行\n\n第三行\n\n第五行"
        self.assertEqual(expectResult, self.mockCorpora._Corpora__removeUrl(article))


    def test_delDictStopwords(self):
        corpora = Corpora(filePath = self.TEXT_FILE_PATH, fileExtension = 'txt', stopwords = self.STOPWORDS_FILE_PATH)
        self.assertFalse(',' in corpora.InvertDictionary)
        self.assertFalse('\n' in corpora.InvertDictionary)
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

    def test_creatByStringList(self):
        testData = ["孔子曰：「大道之行也，與三代之英，丘未之逮也，而有志焉。",
                    "大道之行也，天下為公。選賢與能，講信修睦，故人不獨親其親，不獨子其子",
                    "使老有所終，壯有所用，幼有所長，矜寡孤獨廢疾者皆有所養。男有分，女有歸。",
                    "貨惡其棄於地也，不必藏於己；力惡其不出於身也，不必為己。",
                    "是故謀閉而不興，盜竊亂賊而不作，故外戶而不閉，是謂『大同』"]
        corpora = Corpora(testData)
        self.assertEqual("三代",corpora.Dictionary.get(0))
        corpora.DtPair
        corpora.TfidfPair
        self.assertEqual(5, len(corpora))

    def test_Dictionary(self):
        self.assertEqual('不肖', self.corporaTxt.Dictionary.get(0))
        self.assertEqual(None, self.corporaTxt.Dictionary.get(-1))
        self.assertEqual(0, self.corporaTxt.InvertDictionary.get('不肖'))
        self.assertEqual(None, self.corporaTxt.InvertDictionary.get('zzz'))

    def test_getDtPair(self):
        expectResult = np.array([[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 2), (7, 1), (8, 2)],
                                 [(0, 1), (3, 1), (4, 1), (5, 1), (7, 1)]])
        self.assertTrue(np.array_equal(expectResult, self.corporaTxt.DtPair))

    def test_getDtMatrix(self):
        expectResult = np.array([[1., 1., 1., 1., 1., 1., 2., 1., 2.],
                                 [1., 0., 0., 1., 1., 1., 0., 1., 0.]])
        self.assertTrue(np.array_equal(expectResult, self.corporaTxt.DtMatrix))

    def test_getTfidfPair(self):
        expectResult = [[(1, 0.31622776601683794), (2, 0.31622776601683794), (6, 0.6324555320336759), (8, 0.6324555320336759)],[ ]]
        self.assertTrue(np.array_equal(expectResult, self.corporaTxt.TfidfPair))

    def test_getTfidfMatrix(self):
        expectResult = np.array([[0., 0.31622776, 0.31622776, 0., 0., 0., 0.6324555 , 0., 0.6324555],[0., 0., 0., 0., 0., 0., 0., 0., 0.]])
        minus = self.corporaTxt.TfidfMatrix - expectResult
        for row in minus:
            for a in row:
                self.assertTrue(abs(a) < 0.0000001)

    def test_lenOfCorpus(self):
        self.assertEqual(2, len(self.corporaTxt))

if __name__ == "__main__":
    unittest.main()
