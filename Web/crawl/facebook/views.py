from django.shortcuts import render, redirect
from facebook.mlab import getAllDoc, getAllText
from facebook.crawlFB import crawl
from facebook.crawlFB2 import crawl2
# Create your views here.


def index(request):
    return render(request, 'index.html')


def text(request):
    units = getAllDoc("post")
    return render(request, "text.html", locals())


def help(request):
    return render(request, 'help.html')


def error(request):
    return render(request, 'error.html')


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
                return render(request, "wordcloud.html", locals())  # 重載頁面顯示結果
            except Exception as e:
                return render(request, "error.html", locals())      # 失敗則導向至錯誤頁面

    return render(request, "wordcloud.html", locals())
