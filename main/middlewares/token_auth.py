import jwt
import traceback
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser, User
from django.conf import LazySettings
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from urllib import parse

settings = LazySettings()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        scope["user"] = AnonymousUser()
        try:
            query = parse.parse_qs(scope["query_string"].decode("utf-8"))["jwt"][0]
            if query:
                try:
                    user_jwt = jwt.decode(query, settings.SECRET_KEY,)
                    scope["user"] = User.objects.get(id=user_jwt["user_id"])
                except (
                    InvalidSignatureError,
                    KeyError,
                    ExpiredSignatureError,
                    DecodeError,
                ):
                    traceback.print_exc()
                    pass
                except Exception as e:
                    traceback.print_exc()

            return self.inner(scope)
        except:
            return self.inner(scope)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
