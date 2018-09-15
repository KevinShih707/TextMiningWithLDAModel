from os import path
# from mlab import getVocabularyByTheme
from facebook.mlab import getVocabularyByTheme
from wordcloud import WordCloud
from scipy.misc import imread
import matplotlib.pyplot as plt
from pprint import pprint


def draw_wordcloud(title, imgurl):
    cursor = getVocabularyByTheme(title)
    for document in cursor:
        vocabularyDict = document['vocabulary']
        print("[word_cloud.py]\t\tData from DB as following:")
        pprint(vocabularyDict)  # 把document print出來

    font_path = "fonts/NotoSansCJKtc-Light.otf"
    back_coloring_path = "facebook/mask.png"    # 用Python測試請改成 "mask.png"
    d = path.dirname('.')
    back_coloring = imread(path.join(d, back_coloring_path))

    wc = WordCloud(font_path=font_path,
                   background_color="#222222",
                   max_words=len(vocabularyDict),   # 詞雲MAX數量
                   mask=back_coloring,              # 背景圖片 做遮罩
                   max_font_size=180,
                   relative_scaling=0.9,
                   random_state=42,
                   colormap="rainbow",              # matplotlib 裡面的色票
                   width=600, height=600, margin=5, # margin 是字元和邊緣距離
                   )

    wc.generate_from_frequencies(vocabularyDict)

    plt.figure()
    # matplotlib 繪圖
    plt.imshow(wc)
    plt.axis("off")
    # plt.show()
    # plt.savefig(imgurl)
    plt.clf()
    plt.close()

    # 保存圖檔
    wc.to_file(path.join(d, imgurl))
