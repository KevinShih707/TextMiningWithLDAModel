import json
# TODO: 更新註解
# TODO: 改成顯示為主題概率
def provide_bar_chart_data(result_topic_article_count):
    """
    提供繪製泡泡圖 barchart.js 所需 JSON 資料來源
    :param result_topic_article_count: list of tuple (主題編號，有幾篇) lda.getTopicArticleCount()
    :return:JSON
    """
    data = [
        {
            'values': [],
            'key': 'Serie 1',
            'yAxis': '1'
        }
    ]
    for l in result_topic_article_count:
        data[0]['values'].append({'x': '主題 ' + str(l[0]), 'y': l[1]})
    json.dumps(data, ensure_ascii=False)
    print(data)
    return data
