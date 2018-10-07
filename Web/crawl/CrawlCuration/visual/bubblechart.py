import numpy as np
from CrawlCuration.controller.ldaResult import Result


def provide_bubble_chart_data(office=None, classification=None):
    """
    提供繪製泡泡圖 bubblechart.js 所需 JSON 資料來源
    :param topics_list:由LDA產生的List of tuple 主題
    :return:JSON
    """
    if office == None and classification == None:
        topics_list = test_data
    else:
        result = Result("updated_news", office, classification)
        topics_list = result.show_topics_list()
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
    return json_topic_list
