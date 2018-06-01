import jieba
import csv
from gensim import corpora, models
from gensim.matutils import corpus2dense

class Corpora():
    def __init__(self, filePath = "DataProcessing/test_data/testData.csv", fileExtension = 'csv', stopwords = "DataProcessing/src/stopwords.txt", isDelLinesHasUrl = True):
        '''
        Input:
            filePath:str 欲開啟檔案路徑
            fileExtension: str = 'csv' 副檔名接受'txt'及'csv'檔案格式
            stopwords:停用詞 接受list或txt file路徑(格是參考.stopwords.txt)
            isDelLinesHasUrl:bool = true 是否刪除文當中含URl的行
        '''
        self.filePath = filePath
        self.fileExtension = fileExtension
        self.stopwords = stopwords
        self.isDelLinesHasUrl = isDelLinesHasUrl
        self.corpus = None

    def __createCorpus(self):
        file = self.__openFile(self.filePath, self.fileExtension)
        if(self.isDelLinesHasUrl):
            for article in file:
                file[file.index(article)] = self.__delLinesHasUrl(article)
        self.corpus = self.__segmentWords(file)
        self.dictionary = corpora.Dictionary(self.corpus)
        if(self.stopwords != None):
            self.__delDictStopwords()

    def __openFile(self, path, extension, fieldnames = ['time', 'id', 'text', 'share', 'likecount', 'sharecount']):
        words = ""
        with open(path, encoding = 'utf-8') as file:
            if (extension == 'txt'):
                reader = file.read()
                words = reader.split('\n\n')
            elif (extension == 'csv'):
                reader = csv.DictReader(file, fieldnames)
                words = [row['text'] for row in reader] #串列生成式
                if (words[0] == "貼文內容"):
                    del words[0]
            else:
                raise Exception("Undefined file Extension")
        return words

    def __segmentWords(self, articles):
        return [jieba.lcut(article) for article in articles]


    def __delLinesHasUrl(self, article):
        lines = article.splitlines()
        for line in lines:
            if ('http://' in line or 'https://' in line):
                lines.remove(line)
        return '\n'.join(lines)

    def __delDictStopwords(self):
        if(type(self.stopwords) == str):
            with open(self.stopwords, encoding = 'utf-8') as file:
                read = file.read()
                self.stopwords = read.splitlines()
        badIds = []
        for key, value in self.dictionary.items():
            if value in self.stopwords:
                badIds.append(key)
        self.dictionary.filter_tokens(bad_ids = badIds)

    def __len__(self):
        if(self.corpus == None):
            self.__createCorpus()
        return len(self.corpus)

    def checkWordInDictionary(self, word):
        '''if word in dictionary return wordId else return none'''
        return self.InvertDictionary.get(word)

    def filterFrequentWord(self, num = 10):
        self.dictionary.filter_n_most_frequent(num)

    @property
    def Corpus(self):
        '''回傳段詞後文檔'''
        if(self.corpus == None):
            self.__createCorpus()
        return self.corpus

    @property
    def Dictionary(self):
        '''語意庫辭典{id:word}'''
        if(self.corpus == None):
            self.__createCorpus()
        return self.dictionary

    @property
    def InvertDictionary(self):
        '''反轉語意庫辭典{word:id}'''
        return {word: id for id,word in self.Dictionary.items()}

    @property
    def DtPair(self):
        '''以tuple方式回傳詞頻矩陣(wordID, count)'''
        if(self.corpus == None):
            self.__createCorpus()
        return [self.dictionary.doc2bow(text) for text in self.corpus]

    @property
    def DtMatrix(self):
        '''以矩陣方式回傳詞頻矩陣'''
        return corpus2dense(self.DtPair, len(self.dictionary)).T

    @property
    def TfidfPair(self):
        '''以tuple回傳辭頻-逆向文檔辭頻矩陣(wordID, value)'''
        if(self.corpus == None):
            self.__createCorpus()
        tfidfModel = models.TfidfModel(self.DtPair)
        return tfidfModel[self.DtPair]

    @property
    def TfidfMatrix(self):
        '''以矩陣方式回傳辭頻-逆向文檔辭頻矩陣'''
        return corpus2dense(self.TfidfPair, len(self.dictionary)).T

# def creatDTVectorSpace(texts):#distributed representation
    # modelDR = gensim.models.Word2Vec(texts, size=100, window=5, min_count=5)
