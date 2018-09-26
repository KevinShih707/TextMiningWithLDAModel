from pymongo import MongoClient
from pprint import pprint

MONGO_HOST = "mongodb://104820022:104820022@ds034677.mlab.com:34677/python"
DOCUMENT_NAME = "python"

client = MongoClient(MONGO_HOST)
db = client[DOCUMENT_NAME]


def get_user(email, attribute):
    """
    從DB撈會員的資訊
    :param email:
    :param attribute: 只能是 type|email|firstname|lastname|uid
    :return: String 包含指定資訊
    """
    user = db["member"].find({"email": email})
    while attribute not in ["type", "email", "firstname", "lastname", "uid"]:
        print("Wrong Attribute! Attribute must be one of the following: type|email|firstname|lastname|uid\n")
    return user[0][attribute]

