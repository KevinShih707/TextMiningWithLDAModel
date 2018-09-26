from pymongo import MongoClient

MONGO_HOST = "mongodb://104820022:104820022@ds034677.mlab.com:34677/python"
DOCUMENT_NAME = "python"

client = MongoClient(MONGO_HOST)
db = client[DOCUMENT_NAME]


def get_user(email):
    db["member"].find({})