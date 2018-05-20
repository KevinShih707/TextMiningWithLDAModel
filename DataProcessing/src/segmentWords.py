import jieba
import csv
from gensim import corpora, models
from gensim.matutils import corpus2dense

def cutTextFile(path = ""):
    with open (path, "rt", encoding = 'utf-8') as file:
        content = file.read()#有暫存問題v.s readline
        words = jieba.lcut(content)
    return words

def cutCsvFile(dataDict):
    for row in dataDict:
        row['text'] = jieba.lcut(row['text'])
    return dataDict

def stopwordsFilter(sentence, stopwords):
    result = []
    for seg in sentence:
        if seg not in stopwords: #過濾停用辭
            result.append(seg)
    return result

def openCsvFileAsDict(path = "", cutText = False, stopwords = None):
    with open (path, "rt", encoding = 'utf-8') as file:
        reader = csv.DictReader(file, fieldnames = ['time', 'id', 'text', 'share', 'likecount', 'sharecount'])
        content = [row for row in reader] #字典串列生成式
    if (content[0]['likecount'] == '讚數'): #移除資料說明欄
        del content[0]

    if(cutText):
        content = cutCsvFile(content)
        # if(stopwords != None):
        #     for row in content:
        #         row['text'] = stopwordsFilter(content, stopwords)

    return content

def createDtm(texts):#建立文檔辭頻矩陣
    dictionary = corpora.Dictionary(texts)
    wordCount = [dictionary.doc2bow(text) for text in texts]#list of (wordID,count)
    dtm = corpus2dense(wordCount, len(dictionary))#one_hot_represent matrix
    return dtm.T

def createTfidf(texts):#辭頻-逆向文檔辭頻
    dictionary = corpora.Dictionary(texts)
    wordCount = [dictionary.doc2bow(text) for text in texts]#list of (wordID,count)
    tfidfModel = models.TfidfModel(wordCount)
    tfidf = tfidfModel[wordCount]
    tfidfMatrix = corpus2dense(tfidf, len(dictionary))#(data,featureCount)
    return tfidfMatrix.T

# def creatDTVectorSpace(texts):#distributed representation
    # modelDR = gensim.models.Word2Vec(texts, size=100, window=5, min_count=5)


if __name__ == "__main__":
    cutTextFile("DataProcessing/test_data/testData.txt")
    cutCsvFile("DataProcessing/test_data/testData.csv")
