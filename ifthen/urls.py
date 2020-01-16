from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import GameView

urlpatterns = [
    url(r"games/(?P<pk>\w+)/$", GameView.as_view({"get": "retrieve"})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
