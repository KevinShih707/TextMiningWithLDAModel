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


# Word Cloud Beta
def word_cloud(request):
    from facebook.word_cloud import draw_wordcloud
    imgurl = 'static/media/wordcloud_plot.png'
    try:
        draw_wordcloud("default", imgurl)
    except:
        return render(request, "error.html")

    return render(request, "wordcloud.html")
