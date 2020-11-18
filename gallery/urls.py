from django.conf.urls import url
from gallery.views import CategoryListView, ImageListView

urlpatterns = [
    url(r'^categories/$', CategoryListView.as_view(), name='gallery_categories'),
    url(r'^images/(?P<category>[^/]*)$', ImageListView.as_view(), name='gallery_imgaes'),
    url(r'^images/$', ImageListView.as_view(), name='gallery_imgaes'),
]
