import numpy as np
import json
from pprint import pprint

test_data = [
    (0, [
        ('最新消息', 0.0012787223),
        ('台灣', 0.0011029018),
        ('說', 0.0007290501),
        ('被', 0.00066978607),
        ('對', 0.000664934),
        ('不', 0.0006514698),
        ('就', 0.0006274549),
        ('後', 0.00061623694),
        ('中國', 0.00060404866),
        ('和', 0.0005747937)]),
    (1, [('說', 0.0008123738),
         ('和', 0.00063568057),
         ('讓', 0.0006321331),
         ('長', 0.0006273311),
         ('台灣', 0.00061602687),
         ('人', 0.0005992431),
         ('後', 0.0005924274),
         ('年', 0.0005837633),
         ('對', 0.00058294577),
         ('自己', 0.0005773537)]
     )
]


def provide_bubble_chart_data(topics_list=None):
    """
    提供繪製泡泡圖 bubblechart.js 所需 JSON 資料來源
    :param topics_list:由LDA產生的List of tuple 主題
    :return:JSON
    """
    if topics_list == None:
        topics_list = test_data
    json_topic_list = {
        "name": "All Data",
        "children": []
    }
    for topic in topics_list:
        topic_id = topics_list.index(topic)
        json_topic_list["children"].append({"name": "主題 " + str(topic_id), "children": []})
        word_list = topics_list[topic_id][1]
        [json_topic_list["children"][topic_id]["children"]
            .append({"name": word_tuple[0], "size": np.float64(word_tuple[1])})
            for word_tuple in word_list]
    # pprint(json_topic_list)
    return json_topic_list
