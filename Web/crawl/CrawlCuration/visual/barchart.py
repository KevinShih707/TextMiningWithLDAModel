from CrawlCuration.controller.ldaResult import Result
import json
import numpy as np

# TODO: 改成顯示為主題概率
def provide_bar_chart_data(office, classification):
    """
    提供繪製泡泡圖 barchart.js 所需 JSON 資料來源
    :param office: 要爬哪一家網站
    :param classification: 指定新聞分類
    :return: JSON
    """
    result = Result("news_classify", office, classification)
    topics_list = result.topics_list()[0][1]
    data = [
        {
            'values': [],
            'key': 'Serie 1',
            'yAxis': '1'
        }
    ]
    for l in topics_list:
        data[0]['values'].append({'x': l[0], 'y': np.float64(l[1])})
    json.dumps(data, ensure_ascii=False)

    return data
