from channels.routing import URLRouter
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(
        r"^ws/", URLRouter([url(r"^game/(?P<game_id>[^/]+)$", consumers.GameConsumer)]),
    )
]
