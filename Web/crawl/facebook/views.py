from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import JsonResponse
from facebook.mlab import getAllDoc, getAllText
from facebook.crawlFB import crawl
from facebook.crawlFB2 import crawl2
from facebook.visual import bubblechart
import DataProcessing.ldadata as ldadata
import json
import numpy as np
from pprint import pprint
# Create your views here.


def index(request):
    return render(request, 'index.html')


def text(request):
    units = getAllDoc("post")
    return render(request, "text.html", locals())


def help(request):
    return render(request, 'help.html')


def error(request):
    return render(request, 'error_page/error.html')


def get(request):
    if request.method == "POST":		# 如果是以POST方式才處理
        mess = request.POST['token']
        mess2 = request.POST['page_id']
        if mess == '':
            mess = "請輸入token"
        elif mess2 == '':
            mess2 = "請輸入粉絲專頁ID"
        else:
            crawl(mess, mess2)
            return redirect('/text/')
    else:
        mess = "token尚未送出!"
        mess2 = "粉絲專頁ID尚未送出!"
    return render(request, "get.html", locals())


def comming_soon(request):
    return render(request, "soon.html")


def word_cloud(request):
    """
    建立 theme 選單，選擇後
    呼叫繪製 Wordcloud 並顯示於網頁
    """
    from facebook import word_cloud as wc
    imgurl = 'static/media/wordcloud_plot.png'  # 繪製圖檔，供網頁讀取用
    wc_list = ["default", "cnanewstaiwan"]      # 前端讀取的 theme 選項 TODO: 未來改成動態取得
    # 如果接收到前端 theme 選單回傳的POST請求
    if request.method == "POST":
        selector = request.POST['theme']    # 由前端選單回傳的 theme 選項
        if selector != '':
            try:
                wc.draw_wordcloud(selector, imgurl)     # 進行 WC 繪製
                return render(request, "Visual/wordcloud.html", locals())  # 重載頁面顯示結果
            except Exception as e:
                return render(request, "error.html", locals())      # 失敗則導向至錯誤頁面

    return render(request, "Visual/wordcloud.html", locals())


def bubble(request):
    return render(request, "Visual/bubble.html", locals())


def bubble_json(request):
    json_res = bubblechart.provide_bubble_chart_data()
    pprint(json_res)
    return JsonResponse(json_res)


def bar_chart(request):
    lda = ldadata.get_lda_by_path("DataProcessing/test_data/cnanewstaiwan.csv", "DataProcessing/src/stopwords.txt")
    list = ldadata.topics_list(lda)
    data = [
        {
            'values': [],
            'key': 'Serie 1',
            'yAxis': '1'
        }
    ]
    for l in list:
        data[0]['values'].append({'x': l[0], 'y': np.float64(l[1])})
    # print(data)
    json.dumps(data, ensure_ascii=False)
    return render_to_response('Visual/barchart.html', locals())


def handler404(request, *args, **argv):
    """ Custom 404 Error Page """
    response = render_to_response('error_page/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    """ Custom 505 Error Page """
    response = render_to_response('error_page/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
