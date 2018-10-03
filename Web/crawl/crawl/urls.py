"""crawl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import sys
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from CrawlCuration import views

RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')  # TRUE: 開發環境, FALSE: Production
print('[django urls.py]\tRunning on devserver:', RUNNING_DEVSERVER)

# 處理404/505顯示錯誤訊息頁面，這樣失敗時心情會好一些
handler404 = 'CrawlCuration.views.handler404'
handler500 = 'CrawlCuration.views.handler500'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^index/(\d+)/$', views.index),
    url(r'^text/$', views.text),
    # url(r'^get/$', views.get),
    url(r'^help/', views.help),
    url(r'^error/$', views.error),
    url(r'^word_cloud/$', views.word_cloud),
    url(r'^bubble/$', views.bubble),
    url(r'^bubble_json/', views.bubble_json),
    url(r'^bar_chart/$', views.bar_chart),
    url(r'^login/$', views.login),
    url(r'^sign_up/', views.sign_up),
    url(r'^logout/$', views.logout),
    url(r'^site_options/', views.site_options),
]

if not RUNNING_DEVSERVER:
    urlpatterns  += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

