import jieba
import csv
from gensim import corpora, models
from gensim.matutils import corpus2dense

class Corpora():
    def __init__(self, filePath = "DataProcessing/test_data/testData.csv", fileExtension = 'csv', stopwords = None):
        self.filePath = filePath
        self.fileExtension = fileExtension
        self.stopwords = stopwords
        self.segmentWords()
        self.dictionary = corpora.Dictionary(self.corpus)
        if(self.stopwords != None):
            self.delDictStopwords()

    def segmentWords(self):
        with open(self.filePath, encoding = 'utf-8') as file:
            if (self.fileExtension == 'txt'):
                lines = file.readlines()#暫存爆炸
                words = [jieba.lcut(line) for line in lines]
                self.corpus = words
                return words
            elif (self.fileExtension == 'csv'):
                reader = csv.DictReader(file, fieldnames = ['time', 'id', 'text', 'share', 'likecount', 'sharecount'])
                words = [jieba.lcut(row['text']) for row in reader] #串列生成式
                if (words[0] == ["貼文", "內容"]):
                    del words[0]
                self.corpus = words
                return words
        raise Exception("Undefined file Extension")

    def delDictStopwords(self):
        if(type(self.stopwords) == str):
            with open(self.stopwords, encoding = 'utf-8') as file:
                read = file.read()
                self.stopwords = read.splitlines()
        badIds = []
        for key, value in self.dictionary.items():
            if value in self.stopwords:
                badIds.append(key)
        self.dictionary.filter_tokens(bad_ids = badIds)

    def filterFrequentWord(self, num = 10):
        self.dictionary.filter_n_most_frequent(num)

    @property
    def Dictionary(self):
        return self.dictionary

    @property
    def DtPair(self):#list of (wordID,count)
        return [self.dictionary.doc2bow(text) for text in self.corpus]

    @property
    def DtMatrix(self):#one_hot_represent matrix
        return corpus2dense(self.DtPair, len(self.dictionary)).T

    @property
    def TfidfPair(self):#辭頻-逆向文檔辭頻
        tfidfModel = models.TfidfModel(self.DtPair)
        return tfidfModel[self.DtPair]

    @property
    def TfidfMatrix(self):
        return corpus2dense(self.TfidfPair, len(self.dictionary)).T

# def creatDTVectorSpace(texts):#distributed representation
    # modelDR = gensim.models.Word2Vec(texts, size=100, window=5, min_count=5)
