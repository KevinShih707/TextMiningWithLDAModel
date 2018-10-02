import requests
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime


MONGO_HOST = 'mongodb://104820022:104820022@ds034677.mlab.com:34677/python'
MONGO_PORT = 27017
DOCUMENT_NAME = 'python'

def connect_mongo(COLLECTION_NAME):
    try:
        client = MongoClient(MONGO_HOST, MONGO_PORT)
        db = client[DOCUMENT_NAME]
        return db[COLLECTION_NAME]
    except Exception as e:
        print('Got an error!')
        print(e)

def save_to_mongo(d):
    collection = connect_mongo("updated_news")
    data = d

    try:
        result = collection.insert(data)
        print("sucess")
    except Exception as e:
        print('saving got an error!')
        print(e)

def remove_DB(office,classification):
    collection = connect_mongo("updated_news")
    try:
        collection.remove({"$and": [{"office": office}, {"classification": classification}]})
        print("sucess")
    except Exception as e:
        print('saving got an error!')
        print(e)

def crawlNews(office, classification, base_url, url, tag, liclass, liclass2, page_num):  #爬新聞 base_url:基本 url:某議題版面(頁面含多條連結)可能與base_url相同
    remove_DB(office,classification)
    pages = range(1, page_num)  # scrape for 40 pages, for each page with 25 news.
    links = []
    for page in pages:
        print(url + str(page) + ".html")
        print("===")
        yahoo_r = requests.get(url + str(page))
        yahoo_soup = BeautifulSoup(yahoo_r.text, 'html.parser')
        finance = yahoo_soup.findAll(tag,{'class':liclass})[:10]
        for info in finance:
            link = ""
            try:
                link = info.findAll('a',{'class':liclass2},href=True)[0]
                if link.get('href') != '#':
                    links.append(base_url + link.get("href"))
                    print(base_url + link.get("href"))
                    print('===')
            except:
                link = None
    content = ""
    retitle = ""
    recontent = ""
    for link in links:
        news = requests.get(link)
        single_news = BeautifulSoup(news.text, 'html.parser')
        try:
            re_h = re.compile(u"(<.*?>)|(\[)|(<h1.*?>)|(<\/h1>)|(\])")  # 去除HTML標籤
            content = single_news.findAll('p')
            recontent = re_h.sub(r'', str(content))
            print("---------------------------------------")
            d = {}
            d["office"] = office
            d["classification"] = classification
            d["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            d["content"] = str(recontent)
            print(d)
            save_to_mongo(d)
        except:
            print("error!!!")
        continue