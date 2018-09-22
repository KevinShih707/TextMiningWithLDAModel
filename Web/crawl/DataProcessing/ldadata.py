"""
Django 與 LDA 之整合
"""
# from src.corpora import Corpora
# from src.lda import Lda
from DataProcessing.src.lda import Lda
from DataProcessing.src.corpora import Corpora
from pymongo import MongoClient
import numpy as np


MONGO_HOST = "mongodb://104820022:104820022@ds034677.mlab.com:34677/python"
DOCUMENT_NAME = "python"
def connect_mongo(collection_input):
    try:
        client = MongoClient(MONGO_HOST)
        db = client[DOCUMENT_NAME]
        return db[collection_input]
    except Exception as e:
        print('Got an error!')
        print(e)

def save_to_mongo(collection_input, input_data):
    collection = connect_mongo(collection_input)
    try:
        # DeleteById(collection_input,id)
        collection.insert(input_data)
        print("[save_to_mongo()]\tSuccess!\n")
    except Exception as e:
        print('Got an error!')
        print(e)

def get_lda_by_path(filepath, stopwords, numTopics=2, seed=10):
    """
    透過檔案路徑取得LDA結果
    filepath: 文本路徑
    stopwords: stopwords路徑
    """
    CSV_FILE_PATH = filepath
    STOPWORDS_FILE_PATH = stopwords
    corpora = Corpora(filePath=CSV_FILE_PATH, isDeleteUrl=False, stopwords=STOPWORDS_FILE_PATH)
    lda = Lda(corpora, numTopics=numTopics, seed=seed)
    return lda


def topics_list(lda, title=None, topic_id=None):
    """
    將lda.showTopicsList()的結果傳到DB
    :param lda: Lda回傳結果
    :param title: 主題名稱，DB識別用 (如果沒提供，則當作回傳結果函式)
    """
    topic_tuple = lda.showTopicsList()[0][1]
    # 單純回傳結果，資料型態：array of dicts [(string, float)]
    if title == None:
        if topic_id == None:
            return lda.showTopicsList()[0][1]
        else:
            try:
                return lda.showTopicsList()[topic_id][1]
            except topic_id < 0:
                print("[ldadata.topics_list] \ttopic_id couldn't be negative!")
    # 有 title 則儲存至DB
    else:
        topic_dict = dict(topic_tuple)
        for key, val in topic_dict.items():
            topic_dict[key] = np.float64(val)
        print(topic_dict)
        topic_data = {"title": title, "theme": "visualize", "vocabulary": topic_dict}
        print("json sent to mongo:\n", topic_data, "\n")
        save_to_mongo("theme", topic_data)


# def topics_list(lda):
#     print(lda.showTopicsList()[0][1])
#     return lda.showTopicsList()[0][1]


def topics_string(lda):
    print(lda.showTopicsStr())
    return lda.showTopicsStr()

# 測試範例
# lda = get_lda_by_path("test_data/cnanewstaiwan.csv", "src/stopwords.txt")
# topic_list_to_db(lda, 'cnanewstaiwan')
# topics_string(lda)
# print(topics_list(lda))
