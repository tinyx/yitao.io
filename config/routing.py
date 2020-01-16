from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import ifthen.routing


application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(ifthen.routing.websocket_urlpatterns))}
)
