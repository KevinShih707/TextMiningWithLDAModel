import requests
import re
from bs4 import BeautifulSoup

base_url = "https://tw.appledaily.com"
url = "https://tw.appledaily.com/column/index/768/"
pages = range(1, 5)  # scrape for 40 pages, for each page with 25 news.

links = []
for page in pages:
    print(url + str(page) + ".html")
    print("===")
    yahoo_r = requests.get(url + str(page))
    yahoo_soup = BeautifulSoup(yahoo_r.text, 'html.parser')
    finance = yahoo_soup.findAll('div', {'class': 'aht_title'})
    for info in finance:
        link = ""
        try:
            link = info.findAll('a', href=True)[0]
            if link.get('href') != '#':
                links.append(base_url + link.get("href"))
                print(base_url + link.get("href"))
                print('===')
        except:
            link = None

title = ""
time = ""
content = ""
test = True
for link in links:
    news = requests.get(link)
    single_news = BeautifulSoup(news.text, 'html.parser')

    try:
        re_h = re.compile(u"(<.*?>)|(\[)|(<h1.*?>)|(<\/h1>)|(\])")  # 去除HTML標籤
        title = single_news.findAll(id="h1")    # Title 資料型態為 bs4.element.ResultSet
        retitle = re_h.sub(r'', str(title))     # 將 Title 轉成 String 才能讓 re 吃
        time = single_news.findAll('abbr')[0].get('title')
        time = time.replace(':', '-')
        content = single_news.find_all('p', {'id':'bcontent'})
        file_path = '{timestamp}.txt'.format(timestamp=time)
        with open(file_path, 'w') as textfile:
            # print(title[0].text)
            textfile.write(title[0].text + '\n')
            textfile.write(time + '\n\n')
            try:
                for line in content[0].text.split('\n'):
                    if line.strip() != '':
                        textfile.write(line)
            except:
                print('error!')
            textfile.close()
    except:
        print(retitle)
        print(time)
    continue