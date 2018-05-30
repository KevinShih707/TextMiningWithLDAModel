from django.shortcuts import render,redirect
from facebook.mlab import getAllDoc
from facebook.crawlFB import crawl
# Create your views here.

def index(request):
    return render(request, 'index.html')

def text(request):
	units = getAllDoc("post")
	return render(request, "text.html", locals())	

def get(request):
	if request.method == "POST":		#如果是以POST方式才處理
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
		mess="token尚未送出!"	
		mess2="粉絲專頁ID尚未送出!"
	return render(request, "get.html", locals())