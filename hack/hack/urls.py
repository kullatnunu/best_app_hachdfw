"""hack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from hack_app.views import sayhello, hello2, hello3, run, track_human, video_feed

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', sayhello),
    url(r'^hello2/(\w+)/$', hello2),
    url(r'^hello3/(\w+)/$', hello3),
    url(r'^run/(\w+)/$', run),
    url(r'^video_feed/$', video_feed),
]
