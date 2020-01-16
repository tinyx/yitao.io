from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin

from .models import Game
from .serializers import GameSerializer


class GameView(RetrieveModelMixin, GenericViewSet):
    """
    API view returns information of a game
    """

    permission_classes = []
    queryset = Game.objects.all()
    serializer_class = GameSerializer
