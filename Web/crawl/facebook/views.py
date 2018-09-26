import sys
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import JsonResponse
from facebook.mlab import getAllDoc, getAllText
from facebook.crawlFB import crawl
from facebook.visual import bubblechart
from facebook.account import signup_db
import DataProcessing.ldadata as ldadata
import json
import numpy as np
from pprint import pprint
import pyrebase
import requests

# 重要Authentication API Key 請勿推上Github!!!
config = {
    'apiKey': "Your API Key",
    'authDomain': "your app",
    'databaseURL': "mtfking url",
    'projectId': "ur id",
    'storageBucket': "rehrerh",
    'messagingSenderId': "idididid"
}
# Firebase Authentication 初始化
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')  # TRUE: 開發環境, FALSE: Production


def index(request):
    return render(request, 'index.html')

def login(request):
    email = request.POST.get('email')
    meema = request.POST.get('meema')
    try:
        user = auth.sign_in_with_email_and_password(email, meema)
    except Exception as e:
        message = "Email 或密碼錯誤"
        return render(request, "index.html", {"message": message})
    pprint(user)
    return render(request, "index.html", {"email": email})

def sign_up(request):
    firstname = request.POST.get('first')
    lastname = request.POST.get('last')
    email = request.POST.get('email')
    meema = request.POST.get('meema')
    try:
        user = auth.create_user_with_email_and_password(email, meema)
        uid = user['localId']
        data = {"name": firstname, "status": "1"}
        signup_db.user_to_mongo(firstname, lastname, uid, email)
    except Exception as e:
        print(e)
        message = "註冊失敗，請再試一次"
        print(message)

        return render(request, "index.html", {"signup_error": message})
    return render(request, "index.html")


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


def word_cloud(request):
    """
    建立 theme 選單，選擇後
    呼叫繪製 Wordcloud 並顯示於網頁
    """
    from facebook import word_cloud as wc
    # 繪製圖檔，供網頁讀取用
    if not RUNNING_DEVSERVER:
        imgurl = 'https://storage.googleapis.com/crawl-curation.appspot.com/static/media/wordcloud_plot.png'
    else:
        imgurl = 'static/media/wordcloud_plot.png'
    wc_list = ["default", "cnanewstaiwan"]      # 前端讀取的 theme 選項 TODO: 未來改成動態取得
    # 如果接收到前端 theme 選單回傳的POST請求
    if request.method == "POST":
        selector = request.POST['theme']    # 由前端選單回傳的 theme 選項
        if selector != '':
            try:
                wc.draw_wordcloud(selector, imgurl, RUNNING_DEVSERVER)     # 進行 WC 繪製
                return render(request, "Visual/wordcloud.html", locals())  # 重載頁面顯示結果
            except Exception as e:
                return render(request, "error_page/error.html", locals())      # 失敗則導向至錯誤頁面

    return render(request, "Visual/wordcloud.html", locals())


def bubble(request):
    """ 氣泡圖頁面 """
    return render(request, "Visual/bubble.html", locals())


def bubble_json(request):
    """ 回傳單獨的JSON Http response給前端JS """
    json_res = bubblechart.provide_bubble_chart_data()
    pprint(json_res)
    return JsonResponse(json_res)


def bar_chart(request):
    """ 直條圖頁面，自帶JSON而非用Http request """
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
    response = render_to_response('error_page/505.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
