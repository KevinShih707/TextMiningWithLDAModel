import sys
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import JsonResponse, HttpResponseRedirect
from crawl import apikey    # 這是另外的API Key, 需要使用的話可以問我
from pprint import pprint
import pyrebase
from CrawlCuration.visual.reco import Reco
from CrawlCuration.controller.ldaResult import Result


# Firebase Authentication 初始化: https://firebase.google.com/docs/web/setup
config = apikey.firebase_key()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()

RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')  # TRUE: 開發環境, FALSE: Production


def index(request):
    return render(request, 'index.html')


def login(request):
    """登入"""
    from CrawlCuration.account import login_db
    email = request.POST.get('email')
    meema = request.POST.get('meema')
    try:
        user = auth.sign_in_with_email_and_password(email, meema) # 從 Firebase Auth 驗證
        firstname = login_db.get_user(email, "firstname")   # 取得使用者名稱
    except Exception as e:
        message = "Email 或密碼錯誤"
        return render(request, "index.html", {"message": message})  # 登入失敗，強制回歸

    if user['registered']:
        # user_info = authentication.get_account_info(user['idToken'])
        request.session['idToken'] = user['idToken']    # token有時效性
        request.session['localId'] = user['localId']    # 唯一的User ID
        request.session['username'] = firstname
        request.session.set_expiry(1800)
        return render(request, "index.html")
    else:
        message = "Unknown Error"
        return render(request, 'index.html', {"message": message})


def sign_up(request):
    """註冊"""
    from CrawlCuration.account import signup_db, login_db
    firstname = request.POST.get('first')
    lastname = request.POST.get('last')
    email = request.POST.get('email')
    meema = request.POST.get('meema')
    try:
        if login_db.get_user(email, "uid"):
            message = "此 email 已經註冊"
            return render(request, "index.html", {"signup_error": message})
        user = auth.create_user_with_email_and_password(email, meema)
        uid = user['localId']
        signup_db.user_to_mongo(firstname, lastname, uid, email)
    except Exception as e:
        print(e)
        message = "註冊失敗，請再試一次"
        print(message)
        return render(request, "index.html", {"signup_error": message})
    request.session['idToken'] = user['idToken']  # token有時效性
    request.session['localId'] = user['localId']  # 唯一的User ID
    request.session['username'] = firstname
    request.session.set_expiry(1800)
    return render(request, "index.html")


def logout(request):
    """登出"""
    try:
        # 清除 Session
        del request.session['idToken']
        del request.session['localId']
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect('/')


def help(request):
    return render(request, 'help.html')


def error(request):
    return render(request, 'error_page/error.html')


def bubble(request, office, classification):
    """ 氣泡圖頁面 """
    office = office
    classification = classification
    return render(request, "Visual/bubble.html", locals())


def bubble_json(request, office, classification):
    """ 回傳單獨的JSON Http response給前端JS """
    # from CrawlCuration.visual import bubblechart
    result = Result("news_classify", office, classification)
    reco = Reco(result)
    json_res = reco.bubblechart()
    pprint(json_res)
    return JsonResponse(json_res)


def site_options(request):
    """網站按鈕選單頁面 ex.蘋果, 中時等等"""
    if request.session.get('idToken') is not None:
        from CrawlCuration.news_mgr import site_list
        SITE_LIST = site_list.get()
        return render(request, "Visual/site_options.html", locals())
    else:
        return render(request, 'index.html', {"login_trigger": True, "message": "請先登入"})


def recommendation(request, office, classification):
    """
    主要頁面，顯示包含詞雲、主題長條圖、代表性文章以及主題中之所有文章
    :param request: http 要求
    :param office: view回傳，指定網站進行爬取分析顯示
    :param classification: view回傳，指定該網站之分類，進行爬取分析顯示
    :return: 對指定新聞網站之分類做出的視覺化呈現
    """
    # from CrawlCuration.visual import barchart, word_cloud
    user_id = request.session['localId']
    result = Result("news_classify", office, classification)
    reco = Reco(result, user_id=user_id, RUNNING_DEVSERVER=RUNNING_DEVSERVER)
    office = office
    theme = classification
    user_id = request.session['localId']
    print("office name=", office, "\nclassification=", classification)
    data = reco.barchart()
    # data = barchart.provide_bar_chart_data(office, classification)
    wc_url = reco.wc()
    # wc_url = word_cloud.draw_wordcloud(office, classification, user_id, 0, RUNNING_DEVSERVER)
    numTopics = result.numTopics
    return render(request, "Visual/recommendation.html", locals())


def handler404(request, *args, **argv):
    """ Custom 404 Error Page """
    response = render_to_response('error_page/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    """ Custom 500 Error Page """
    response = render_to_response('error_page/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
