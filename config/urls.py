"""yitao.io URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

from chrome_homepage.urls import urlpatterns as chrome_homepage_url
from gallery.urls import urlpatterns as gallery_url
from todolist.urls import urlpatterns as todolist_url
from wow_monitor.urls import urlpatterns as wow_monitor_url

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^chrome-homepage/', include(chrome_homepage_url)),
    url(r'^filer/', include('filer.urls')),
    url(r'^gallery/', include(gallery_url)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^todo/', include(todolist_url)),
    url(r'^wow-monitor/', include(wow_monitor_url)),
]
