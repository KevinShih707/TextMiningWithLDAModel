import requests
import pandas as pd
from dateutil.parser import parse
from CrawlCuration.mlab import getAllDoc, save_to_mongo


def crawl(input_token, input_pageid):
    token = input_token

    # 粉專ID

    # fanpage_id = '137698833067234'
    fanpage_id = input_pageid

    # 抓取貼文時間、ID、內文、分享內容

    res = requests.get('https://graph.facebook.com/v2.12/{}/posts?limit=100&access_token={}'.format(fanpage_id, token))

    # 建立空的list

    posts = []
    page = 1
    while 'paging' in res.json():
        print('目前正在抓取第%d頁' % page)

        for post in res.json()['data']:
            # 透過貼文ID來抓取讚數與分享數

            res2 = requests.get(
                'https://graph.facebook.com/v2.12/{}?fields=likes.limit(0).summary(True), shares&access_token={}'.format(
                    post['id'], token))
            # 取得讚數
            if 'likes' in res2.json():
                likes = res2.json()['likes']['summary'].get('total_count')
            else:
                likes = 0
            # 取得分享數
            if 'shares' in res2.json():
                shares = res2.json()['shares'].get('count')
            else:
                shares = 0

            posts.append([parse(post['created_time']),  # 貼文時間
                      post['id'],                   # 貼文ID
                      post.get('message'),          # 貼文內容
                      post.get('story'),            # 分享內容(若無則留空)
                      likes,                        # 讚數
                      shares                        # 分享數
                      ])

            #print(posts)

        if 'next' in res.json()['paging']:
            res = requests.get(res.json()['paging']['next'])
            page += 1
         #測試時，暫時限制爬的分量
        if page == 3:
            break
        else:
            break

    print('完成!')

    # 檔案輸出

    df = pd.DataFrame(posts)
    df.columns = ['time', 'id', 'text', 'share', 'likecount', 'sharecount']
    records = df.to_dict('records') # 參數 record 代表把列轉成個別物件
    save_to_mongo("post",records,fanpage_id)
    # 寫CSV時編碼格式要用'utf_8_sig'
    #df.to_csv('CrawlResult.csv', index=False, encoding='utf_8_sig')
    