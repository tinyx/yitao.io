from channels.generic.websocket import JsonWebsocketConsumer

from .models import Game
from .constants import MessageType
from .exceptions import ValidationError


class GameConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.user = self.scope["user"]
        self.accept()
        print(self.game_id, self.user)

    def send_error(self, message):
        self.send_json({"message": message, "type": MessageType.ERROR.value})

    def receive_json(self, content):
        try:
            game = Game.objects.get(id=self.game_id)
        except Game.DoesNotExist:
            return self.send_error("The game you are looking for doesn't exist")
        print(game.state)
        if "type" not in content or content["type"] not in [
            message_type.value for message_type in MessageType
        ]:
            return self.send_error(
                'Your message is missing "type" field or it contains invalid value'
            )
        try:
            if content["type"] == MessageType.JOIN_GAME.value:
                game.join(self.user)
            elif content["type"] == MessageType.MAKE_MOVE.value:
                statement_id = content["statement_id"]
                game.make_move(self.user, statement_id)
        except ValidationError as e:
            return self.send_json({"message": e.message})
