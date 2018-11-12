from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from wow_monitor import views

urlpatterns = [
    url(r'(?P<server_name>\w+)/(?P<name>\w+)/$', views.WowMonitorView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
