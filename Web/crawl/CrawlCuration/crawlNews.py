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
    collection = connect_mongo("news_demo")
    data = d

    try:
        collection.insert(data)
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

def crawlNews(office, classification, base_url, url, tag, liclass, liclass2, page_num, news_num,titleclass,titleid, titlename):  #爬新聞 base_url:基本 url:某議題版面(頁面含多條連結)可能與base_url相同
    #remove_DB(office,classification)
    pages = range(1, page_num)  # scrape for 40 pages, for each page with 25 news.
    links = []
    news_counter = 0
    for page in pages:
        # print(url + str(page) + ".html")
        # print("===")
        yahoo_r = requests.get(url + str(page))
        yahoo_soup = BeautifulSoup(yahoo_r.text, 'html.parser')
        if(classification == "finance" or classification == "health"):
            finance = yahoo_soup.findAll(tag,{'class':liclass})
        else:
            finance = yahoo_soup.findAll(tag, {'class': liclass})[:news_num]
        for info in finance:
            try:
                link = info.findAll('a',{'class':liclass2},href=True)[0]
                if link.get('href') != '#':
                    links.append(base_url + link.get("href"))
                    # print(base_url + link.get("href"))
                    # print('===')
            except Exception as e:
                links = list()
            news_counter += 1

    print("正在爬取", office, classification, "\t共", news_counter, "篇\n")

    for link in links:
        news = requests.get(link)
        single_news = BeautifulSoup(news.text, 'html.parser')
        try:
            re_h = re.compile(u"(<.*?>)|(\[)|(<h1.*?>)|(<\/h1>)|(\])")  # 去除HTML標籤
            title = single_news.findAll(titleclass, {titleid: titlename})
            retitle = re_h.sub(r'', str(title))
            retitle = re.sub('\s+', ' ', retitle)
            content = single_news.findAll('p')
            recontent = re_h.sub(r'', str(content))
            recontent = re.sub('\s+', ' ', recontent)
            # print("---------------------------------------")
            d = {}
            d["office"] = office
            d["classification"] = classification
            d["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            d["title"] = str(retitle)
            d["content"] = str(recontent)
            # print(d,"\n")
            save_to_mongo(d)
        except Exception as e:
            print(e)
        continue

    print("爬蟲完成！")


def crawlToDB(office, classification, page_num, news_num):
    """
    把新聞爬取+存到DB
    :param office: str 網站: apple | free | china
    :param classification: str 分類
    :param page_num: int 頁數
    :param news_num: int 定義分量的數字
    """
    if office == "free" and classification == "finance":
        crawlNews("free", "finance", "", "http://ec.ltn.com.tw/list/securities/", 'li', '', 'boxText', page_num, news_num, "h1", "", "")
    if office == "free" and classification == "3c":
        crawlNews("free", "3c", "http://3c.ltn.com.tw/", "http://3c.ltn.com.tw/menu/internet/", 'li', 'list_box', '', page_num, news_num, "h1", "", "")
    if office == "free" and classification == "health":
        crawlNews("free", "health", "", "http://ec.ltn.com.tw/list/securities/", 'li', '', 'boxText', page_num, news_num, "h1", "", "")

    if office == "apple" and classification == "iphone":
        crawlNews("apple", "iphone", "https://tw.appledaily.com", "https://tw.appledaily.com/column/index/768/", 'div','aht_title', "", page_num, news_num, "h1", "id", "h1")
    if office == "apple" and classification == "career":
        crawlNews("apple", "career", "https://tw.appledaily.com", "https://tw.appledaily.com/column/index/540/", 'div','aht_title', "", page_num, news_num, "h1", "id", "h1")
    if office == "apple" and classification == "liveStream":
        crawlNews("apple", "liveStream", "https://tw.appledaily.com", "https://tw.appledaily.com/column/index/532/", 'div', 'aht_title', "", page_num, news_num, "h1", "id", "h1")
    if office == "apple" and classification == "trading":
        crawlNews("apple", "trading", "https://tw.appledaily.com", "https://tw.appledaily.com/column/index/660/", 'div', 'aht_title', "", page_num, news_num, "h1", "id", "h1")

    if office == "china" and classification == "sport":
        crawlNews("china", "sport", "http:", "http://www.chinatimes.com/sports/total/?page=", 'h3', '', "", page_num, news_num, "h1", "id", "h1")
    if office == "china" and classification == "military":
        crawlNews("china", "military", "https://www.chinatimes.com", "https://www.chinatimes.com/armament/total?page=", 'h3', '', "", page_num, news_num, "h1", "id", "h1")
    if office == "china" and classification == "entertainment":
        crawlNews("china", "entertainment", "https:", "https://www.chinatimes.com/star/total/?page=", 'h3', '', "", page_num, news_num, "h1", "id", "h1")
    if office == "china" and classification == "election":
        crawlNews("china", "election", "", "https://www.chinatimes.com/vote2018/total?page=", 'h3', '', "", page_num, news_num, "h1", "id", "h1")
    if office == "china" and classification == "travel":
        crawlNews("china", "travel", "https:", "https://www.chinatimes.com/travel/total?page=", 'h3', '', "", page_num, news_num, "h1", "id", "h1")

def getUpdatedNews(office, classification, number):
    collection = connect_mongo("updated_news")
    try:
        news = collection.find({"$and": [{"office": office}, {"classification": classification}]}).limit(number).sort("date",-1)
        list = [m["content"] for m in news]
        return list
    except Exception as e:
        print('querying got an error!')
        print(e)

def crawl_all_news_with_appropriate_amount():
    # 約98篇
    crawlToDB("free", "finance", 3, 100)
    crawlToDB("free", "health", 3, 100)

    # 100
    crawlToDB("free", "3c", 6, 100)

    # 約120篇
    crawlToDB("china", "sport", 5, 100)
    crawlToDB("china", "military", 5, 100)
    crawlToDB("china", "entertainment", 5, 100)
    crawlToDB("china", "election", 5, 100)
    crawlToDB("china", "travel", 5, 100)

    # 約104篇
    crawlToDB("apple","iphone",6,26)
    crawlToDB("apple", "career", 6, 26)
    crawlToDB("apple", "liveStream", 6, 26)
    crawlToDB("apple", "trading", 6, 26)
