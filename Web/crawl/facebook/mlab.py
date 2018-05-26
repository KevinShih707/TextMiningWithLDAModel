import pymongo
from pymongo import MongoClient
#import os
#from mongoengine import connect, Document, StringField,DateTimeField

def mongoengine():
    # get the mlab URI from environment variables
    uri = os.getenv("mongodb://104820022:104820022@ds034677.mlab.com:34677/python")

    # connect to our database at MLAB
    connect(db='python',username='104820022',password='104820022',host=uri)

def getAllDoc():
    try:
        myClient = MongoClient("mongodb://104820022:104820022@ds034677.mlab.com:34677/python")
        myDB = myClient.python
        myCollection = myDB.post
        return myCollection.find({})
    except Exception as e:
        print('Got an error!')
        print(e)