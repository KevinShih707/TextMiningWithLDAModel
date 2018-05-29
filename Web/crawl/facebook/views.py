from django.shortcuts import render
from facebook.mlab import getAllDoc
# Create your views here.

def index(request):
    return render(request, 'index.html')

def text(request):
	units = getAllDoc("post")
	return render(request, "text.html", locals())	