import pymongo
from pymongo import MongoClient
import csv
import codecs

MONGO_HOST = "mongodb://104820002:104820002@ds034677.mlab.com:34677/python"


DOCUMENT_NAME = "python"
COLLECTION_NAME = 'post'

FILENAME = 'testData.csv'
COLUMNS = ('time', 'id', 'text', 'share', 'likecount', 'sharecount')


def connect_mongo():
    try:
        client = MongoClient(MONGO_HOST)
        db = client[DOCUMENT_NAME]
        return db[COLLECTION_NAME]
    except Exception as e:
        print('Got an error!')
        print(e)


def read_csv():
    reader = open(FILENAME, 'r', encoding='utf8')
    return csv.DictReader(reader, COLUMNS)


def save_to_mongo():
    collection = connect_mongo()
    data = read_csv()

    try:
        result = collection.insert_many(data)
        print('%d rows are saved to "%s" collection in "%s" document successfully!' % (len(result.inserted_ids), COLLECTION_NAME, DOCUMENT_NAME))
    except Exception as e:
        print('Got an error!')
        print(e)


save_to_mongo()


#myClient = MongoClient("mongodb://104820002:104820002@ds034677.mlab.com:34677/python")
#myDB = myClient.python
#myCollection = myDB.post
#print(myCollection.count())