import unittest
from ..src import segmentWords

class TestSegment(unittest.TestCase):
    TEXT_FILE_PATH = "DataProcessing/test_data/testData.txt"
    CSV_FILE_PATH = "DataProcessing/test_data/testData.csv"

    def test_cutTextFile(self):
        segmented = segmentWords.cutTextFile(self.TEXT_FILE_PATH)
        self.assertEqual("智者 守時 而 盡 其智 ， 不肖 者 守命 而 盡 其力 。 \n", segmented)

    def test_openCsvFileAsDict(self):
        dataDict = segmentWords.openCsvFileAsDict(self.CSV_FILE_PATH)
        self.assertEqual('2018-02-09 03:45:00+00:00', dataDict[0]['time'])
        self.assertEqual('137698833067234_800064190164025', dataDict[0]['id'])
        self.assertEqual('適當的使用動畫可以為你的作品加分，但動畫不是人人都會做，所以這次我們為大家介紹如何透過 loading.io 圖示庫快速製作屬於自己的動畫圖示。\n\n全文: http://blog.infographics.tw/2018/02/loading-io-animated-icons/', dataDict[0]['text'])
        self.assertEqual('441', dataDict[0]['likecount'])
        self.assertEqual('124', dataDict[0]['sharecount'])

    def test_cutCsvFile(self):
        dataDict = segmentWords.cutCsvFile(self.CSV_FILE_PATH)
        self.assertEqual('適當 的 使用 動畫 可以 為 你 的 作品 加 分 ， 但動畫 不是 人人 都 會 做 ， 所以 這次 我們 為 大家 介紹 如何 透過   loading . io   圖示 庫 快速 製 作 屬 於 自己 的 動畫 圖示 。 \n \n 全文 :   http : / / blog . infographics . tw / 2018 / 02 / loading - io - animated - icons /', dataDict[0]['text'])
