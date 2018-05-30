import pymongo
from pymongo import MongoClient
# import csv
# import codecs
# import os
# from mongoengine import connect, Document, StringField,DateTimeField

MONGO_HOST = "mongodb://104820022:104820022@ds034677.mlab.com:34677/python"


DOCUMENT_NAME = "python"
'''
def mongoengine():
    # get the mlab URI from environment variables
    uri = os.getenv("mongodb://104820022:104820022@ds034677.mlab.com:34677/python")

    # connect to our database at MLAB
    connect(db='python',username='104820022',password='104820022',host=uri)
'''


def connect_mongo(collection_input):
    try:
        client = MongoClient(MONGO_HOST)
        db = client[DOCUMENT_NAME]
        return db[collection_input]
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
'''
def read_csv():
    reader = open(FILENAME, 'r', encoding='utf8')
    return csv.DictReader(reader, COLUMNS)
'''


def save_to_mongo(collection_input, input_data):
    collection = connect_mongo(collection_input)
    # data = read_csv()

    try:
        collection.drop()
        collection.insert_many(input_data)
        # result = collection.insert_many(data)
        # print('%d rows are saved to "%s" collection in "%s" document successfully!' % (len(result.inserted_ids), COLLECTION_NAME, DOCUMENT_NAME))
    except Exception as e:
        print('Got an error!')
        print(e)

