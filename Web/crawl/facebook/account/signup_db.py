from pymongo import MongoClient

MONGO_HOST = "mongodb://104820022:104820022@ds034677.mlab.com:34677/python"
DOCUMENT_NAME = "python"

client = MongoClient(MONGO_HOST)
db = client[DOCUMENT_NAME]


def user_to_mongo(firstname, lastname, uid, email):
    collection = db["member"]
    data = {
        "type": "user",
        "uid" : uid,
        "firstname" : firstname,
        "lastname": lastname,
        "email": email
    }

    collection.insert(data)
    print(data)

