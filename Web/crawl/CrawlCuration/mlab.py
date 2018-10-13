from pymongo import MongoClient

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

def DB_Size():
    try:
        client = MongoClient(MONGO_HOST)
        db = client[DOCUMENT_NAME]
        return db.stats()
    except Exception as e:
        print('Got an error!')
        print(e)

def getAllDoc(collection_input):
    try:
        collection = connect_mongo(collection_input)
        return collection.find({})
    except Exception as e:
        print('Got an error!')
        print(e)

def getNewsContent(collection_input, office, classification):
    """
    給getNewsInStringList呼叫，請勿直接使用
    :param collection_input: DB collection 名稱
    :param office: 哪一家網站
    :param classification: 分類
    :return: pymongo.cursor.Cursor
    """
    try:
        collection = connect_mongo(collection_input)
        content = collection.find({"office": office, "classification": classification},{'_id':0,'content':1,'by':1})
        return content
    except Exception as e:
        print('Got an error!')
        print(e)


def getNewsInStringList(collection_input, office, classification, col="content"):
    """
    抓下資料庫的文章(內文)
    :param collection_input: mongoDB上面的collection
    :param office:
    :param classification:
    :param col: 預設為content, 欲查詢標題請改"title"
    :return: 文章內容(List of Strings)
    """
    news = getNewsContent(collection_input, office, classification)
    list = [m[col] for m in news]
    return list


def getAllNewsContent(collection_input):
    """
    建Model用 實際不會用
    :param collection_input: DB collection 名稱
    :return: string list
    """
    try:
        collection = connect_mongo(collection_input)
        content = collection.find({},{'_id':0,'content':1,'by':1})
    except Exception as e:
        print('Got an error!')
        print(e)
    list = [m['content'] for m in content]
    return list


def getAllText(collection_input):
    try:
        collection = connect_mongo(collection_input)
        return collection.find({},{'_id':0,'text':1,'by':1})
    except Exception as e:
        print('Got an error!')
        print(e)

def getTextById(collection_input, Pageid):
    try:
        collection = connect_mongo(collection_input)
        return collection.find({'id':{'$regex':Pageid}},{'_id':0,'text':1,'by':1})
    except Exception as e:
        print('Got an error!')
        print(e)

def get_classification_count(collection_input="news_demo"):
    """查詢DB中每個分類有幾篇"""
    collection_input = collection_input
    collection = connect_mongo(collection_input)
    classlist = [
    ("free",  "finance"),
    ("free",  "health"),
    ("free",  "3c"),
    ("china", "sport"),
    ("china", "military"),
    ("china", "entertainment"),
    ("china", "election"),
    ("china", "travel"),
    ("apple", "iphone"),
    ("apple", "career"),
    ("apple", "liveStream"),
    ("apple", "trading")
    ]
    for single_class in classlist:
        class_count = collection.count({"office": single_class[0], "classification": single_class[1]})
        print(single_class[0], "\t", single_class[1], ":\t", class_count, "\n")

