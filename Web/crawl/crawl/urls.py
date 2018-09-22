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
from facebook import views

RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')  # TRUE: 開發環境, FALSE: Production
print('[django urls.py]\tRunning on devserver:', RUNNING_DEVSERVER)

# 開發環境才會import
if RUNNING_DEVSERVER:
    from django.conf import settings
    from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^index/(\d+)/$', views.index),
    url(r'^text/$', views.text),
    url(r'^soon/', views.comming_soon),
    url(r'^get/$', views.get),
    url(r'^help/', views.help),
    url(r'^error/$', views.error),
    url(r'^wc/', views.word_cloud),
    url(r'^bubble/$', views.bubble),
    url(r'^bar_chart/$', views.bar_chart),
]
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) if RUNNING_DEVSERVER else urlpatterns
