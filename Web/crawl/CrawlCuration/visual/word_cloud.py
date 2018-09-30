import sys
from os import path
from CrawlCuration.mlab import getVocabularyByTheme
from wordcloud import WordCloud
from google.cloud import storage
from pprint import pprint
import numpy as np
from PIL import Image
import urllib
import cv2

RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')
# 初始化 Google Cloud Storage 並帶入 Credentials
if RUNNING_DEVSERVER:
    client = storage.Client.from_service_account_json("D:\IndependentStudy\crawl-curation-c5731532bf6c.json");
else:
    client = storage.Client()
# 指定本專案的 Bucket name
bucket = client.get_bucket('crawl-curation.appspot.com')


def draw_wordcloud(title, user_id, RUNNING_DEVSERVER=True, imgurl=None):
    """
    讀取topic list，用Word Cloud 繪製圖片(numpy array)，OpenCV 編碼成PNG，上傳至 Google Cloud Storage
    :param title: 主題 ex.apple, free
    :param imgurl: deprecated
    :param user_id: 使用者ID 用於讀寫圖片
    :param RUNNING_DEVSERVER: 是否為本地端
    :return: Google Cloud Storage上面的圖片URL
    """
    cursor = getVocabularyByTheme(title)
    for document in cursor:
        vocabularyDict = document['vocabulary']
        print("[word_cloud.py]\t\tData from DB as following:")
        pprint(vocabularyDict)  # 把document print出來

    if RUNNING_DEVSERVER:
        d = path.dirname('.')
        save_path = path.join(d, imgurl)
        MASK_PATH = "static/media/mask.png"
        mask = np.array(Image.open(path.join(d, MASK_PATH)))
    else:
        MASK_PATH = "https://storage.googleapis.com/crawl-curation.appspot.com/static/media/mask.png"
        file = urllib.request.urlopen(MASK_PATH)
        mask = np.array(Image.open(file))

    FONT_PATH = "https://storage.googleapis.com/crawl-curation.appspot.com/static/NotoSansCJKtc-Light.otf"

    wc = WordCloud(font_path=FONT_PATH,
                   background_color="rgba(255, 255, 255, 0)", mode="RGBA",
                   max_words=len(vocabularyDict),   # 詞雲MAX數量
                   mask=mask,              # 背景圖片 做遮罩
                   max_font_size=180,
                   relative_scaling=0.9,
                   random_state=42,
                   colormap="rainbow",              # matplotlib 裡面的色票
                   width=600, height=600, margin=5, # margin 是字元和邊緣距離
                   )

    wc.generate_from_frequencies(vocabularyDict)

    # 保存圖檔
    if RUNNING_DEVSERVER:
        wc.to_file(save_path)

    # OpenCV 編碼
    image_array = wc.to_array()
    image_encode = cv2.imencode('.png', image_array)
    img_bytes = image_encode[1].tobytes()
    # 存到 Google Cloud Storage
    blob = bucket.blob("static/media/wc/" + user_id + "/" + title + ".png")
    blob.upload_from_string(data=img_bytes, content_type="image/png")

    return blob.public_url