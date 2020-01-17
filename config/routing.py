from channels.routing import ProtocolTypeRouter, URLRouter
from main.middlewares.token_auth import TokenAuthMiddleware
import ifthen.routing


application = ProtocolTypeRouter(
    {"websocket": TokenAuthMiddleware(URLRouter(ifthen.routing.websocket_urlpatterns))}
)
