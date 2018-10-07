from os import path
from wordcloud import WordCloud
from google.cloud import storage
import numpy as np
from PIL import Image
import urllib
import cv2

# TODO: 更新註解
class WC():
    def __init__(self, result, result_topics_list, user_id, topic_id, RUNNING_DEVSERVER=False):
        self.result = result
        self.topics_list = result_topics_list
        self.user_id = user_id
        self.topic_id = topic_id
        self.office = result.office
        self.classification = result.classification
        self.RUNNING_DEVSERVER = RUNNING_DEVSERVER

    def draw_wordcloud(self):
        """
        讀取topic list，用Word Cloud 繪製圖片(numpy array)，OpenCV 編碼成PNG，上傳至 Google Cloud Storage
        :param office: 要爬哪一家網站
        :param classification: 指定新聞分類
        :param user_id: 使用者ID 用於讀寫圖片
        :param topicId: number 指定主題
        :param RUNNING_DEVSERVER: 是否為本地端
        :return: Google Cloud Storage上面的圖片URL
        """
        # 初始化 Google Cloud Storage 並帶入 Credentials
        if self.RUNNING_DEVSERVER:
            client = storage.Client.from_service_account_json("D:\IndependentStudy\crawl-curation-c5731532bf6c.json");
        else:
            try:
                client = storage.Client()
            except Exception as e:
                print(e)
                raise EnvironmentError("無法取得Google App Engine之Credentials：", e)

        # 指定本專案的 Bucket name
        bucket = client.get_bucket('crawl-curation.appspot.com')

        topic_tuple = self.topics_list[self.topic_id][1]
        topic_dict = dict(topic_tuple)
        for key, val in topic_dict.items():
            topic_dict[key] = np.float64(val)

        if self.RUNNING_DEVSERVER:
            d = path.dirname('.')
            MASK_PATH = "static/media/mask.png"
            mask = np.array(Image.open(path.join(d, MASK_PATH)))
        else:
            MASK_PATH = "https://storage.googleapis.com/crawl-curation.appspot.com/static/media/mask.png"
            file = urllib.request.urlopen(MASK_PATH)
            mask = np.array(Image.open(file))

        FONT_PATH = "NotoSansCJKtc-Light.otf"

        wc = WordCloud(font_path=FONT_PATH,
                       background_color="rgba(255, 255, 255, 0)", mode="RGBA",
                       max_words=len(topic_dict),   # 詞雲MAX數量
                       mask=mask,              # 背景圖片 做遮罩
                       max_font_size=180,
                       relative_scaling=0.9,
                       random_state=42,
                       colormap="rainbow",              # matplotlib 裡面的色票
                       width=600, height=600, margin=5, # margin 是字元和邊緣距離
                       )

        wc.generate_from_frequencies(topic_dict)

        # OpenCV 編碼
        image_array = wc.to_array()
        image_encode = cv2.imencode('.png', image_array)
        img_bytes = image_encode[1].tobytes()

        # 存到 Google Cloud Storage
        blob = bucket.blob("static/media/wc/" + self.user_id + "/" + self.office + "-" + self.classification
                                + "-topic" + str(self.topic_id) + ".png")
        blob.upload_from_string(data=img_bytes, content_type="image/png")

        return blob.public_url