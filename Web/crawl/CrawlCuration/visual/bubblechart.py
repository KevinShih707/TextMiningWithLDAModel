import numpy as np

# TODO: 更新註解
def provide_bubble_chart_data(result_topics_list):#office, classification
    """
    提供繪製泡泡圖 bubblechart.js 所需 JSON 資料來源
    :param office: 要爬哪一家網站
    :param classification: 指定新聞分類
    :return: JSON
    """
    topics_list = result_topics_list
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
