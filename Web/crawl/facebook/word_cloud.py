from os import path
from facebook.mlab import getVocabularyByTheme
from wordcloud import WordCloud
# from scipy.misc import imread
# import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
from PIL import Image
import urllib


def draw_wordcloud(title, imgurl, RUNNING_DEVSERVER=True):
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
        save_path = urllib.request.urlopen(imgurl)
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

    # # matplotlib只用於debug
    # plt.figure()
    # # matplotlib 繪圖
    # plt.imshow(wc)
    # plt.axis("off")
    # plt.show()
    # plt.savefig(imgurl)
    # plt.clf()
    # plt.close()

# TODO: R/W WC images from google cloud storage via API
    # 保存圖檔
    wc.to_file(save_path)
