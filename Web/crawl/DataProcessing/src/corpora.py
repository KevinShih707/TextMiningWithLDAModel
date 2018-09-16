import csv
import re
import jieba
from gensim import corpora, models
from gensim.matutils import corpus2dense

class Corpora():
    def __init__(self, filePath = "DataProcessing/test_data/testData.csv", fileExtension = 'csv', stopwords = "DataProcessing/src/stopwords.txt", isDeleteUrl = True):
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
        self.isDeleteUrl = isDeleteUrl
        self.corpus = None

    def __createCorpus(self):
        '''
            簡易的proxy當需要文檔資訊時才實際依建構元參數建立文檔
        '''
        file = self.__openFile(self.filePath, self.fileExtension)
        if(self.isDeleteUrl):
            for article in file:
                file[file.index(article)] = self.__deleteUrl(article)
        self.corpus = self.__segmentWords(file)
        self.dictionary = corpora.Dictionary(self.corpus)
        if(self.stopwords != None):
            self.__delDictStopwords()

    def remove_emoji(self, text):
        '''使用正規表達法移除表情符號'''
        emoji_pattern = re.compile(
            u"[\r?\n]|"
            u"(\ud83d[\ude00-\ude4f])|"  # emoticons
            u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
            u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
            u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
            u"(\ud83c[\udde0-\uddff])|"  # flags (iOS)
            u"([\u2600-\u26ff])|"       # Miscellaneous Symbols
            u"([\U0001f300-\U0001f5ff])"      # Miscellaneous Symbols Unicode v6 加入
            "+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def remove_url(self, text):
        '''改善刪除URL之正規表達式，用法同remove_emoji'''
        urlregex = re.compile(u"(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+[\w\-\.,@?^=%&amp;:\/~‌​\+#]*[\w\-\@?^=%&amp‌​;\/~\+#]")
        return urlregex.sub(r'', text)

    def __deleteUrl(self, article, byWholeLine = False):
        '''
            刪除文中之url
            article: 欲刪除url文章
            byWholeLine = False: 刪除依整行
        '''
        if(byWholeLine):
            return re.sub(r".*https?:\/\/.*\n", '', article, flags = (re.MULTILINE | re.IGNORECASE))#匹配頭尾、忽略大小寫
        else:
            return re.sub(r"https?:\/\/.*[\r\n]*", ' ', article, flags = (re.IGNORECASE))#匹配頭尾、忽略大小寫

    def __openFile(self, path, extension, fieldnames = ['time', 'id', 'text', 'share', 'likecount', 'sharecount']):
        words = ""
        with open(path, encoding = 'utf-8') as file:
            if (extension == 'txt'):
                reader = file.read()
                words = reader.split('\n\n')
            elif (extension == 'csv'):
                reader = csv.DictReader(file, fieldnames)
                words = [self.remove_emoji(row['text']) for row in reader] #串列生成式
                words = [self.remove_url(word) for word in words] # 移除URL
                if (words[0] == "貼文內容"):
                    del words[0]
            else:
                raise Exception("Undefined file Extension")
        return words

    def __segmentWords(self, articles):
        '''斷詞'''
        return [jieba.lcut(article) for article in articles]

    def __delDictStopwords(self):
        if(type(self.stopwords) == str):
            with open(self.stopwords, encoding = 'utf-8') as file:
                read = file.read()
                self.stopwords = read.split("| ")
        badIds = []
        for key, value in self.dictionary.items():
            if value in self.stopwords:
                badIds.append(key)
        self.dictionary.filter_tokens(bad_ids = badIds)

    def __len__(self):
        if(self.corpus == None):
            self.__createCorpus()
        return len(self.corpus)

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