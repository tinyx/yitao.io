from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from .models import Game
from .constants import MessageType
from .exceptions import ValidationError


class GameConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.user = self.scope["user"]
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.channel_group_name, self.channel_name
        )
        print(self.game_id, self.user)

    def disconnect_json(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_group_name, self.channel_name
        )

    @property
    def channel_group_name(self):
        return f"game_{self.game_id}"

    def send_refresh_signal(self):
        async_to_sync(self.channel_layer.group_send)(
            self.channel_group_name, {"type": "refresh.game"}
        )

    def refresh_game(self, event):
        self.send_json({"type": MessageType.REFRESH_GAME.value})

    def send_error(self, message):
        self.send_json({"message": message, "type": MessageType.ERROR.value})

    def receive_json(self, content):
        try:
            game = Game.objects.get(id=self.game_id)
        except Game.DoesNotExist:
            return self.send_error("The game you are looking for doesn't exist")
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
            return self.send_error(e.message)
        self.send_refresh_signal()
