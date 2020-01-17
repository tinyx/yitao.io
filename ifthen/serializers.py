from rest_framework import serializers

from .models import Game, Move, Player
from .statements.ifs import STATEMENTS as IF_STATEMENTS
from .statements.thens import STATEMENTS as THEN_STATEMENTS


class MoveSerializer(serializers.ModelSerializer):
    """
    Model serializer for Move
    """

    if_statement = serializers.SerializerMethodField()
    if_statement_options = serializers.SerializerMethodField()
    then_statement = serializers.SerializerMethodField()
    then_statement_options = serializers.SerializerMethodField()

    class Meta:
        model = Move
        fields = (
            "if_user",
            "if_statement_options",
            "if_statement",
            "then_user",
            "then_statement_options",
            "then_statement",
            "is_complete",
        )

    def get_if_statement(self, obj):
        """
        Return if_statement if the move has been completed, otherwise empty string
        """
        if obj.is_complete:
            return {
                "statement": IF_STATEMENTS[obj.if_statement].description,
                "id": obj.if_statement,
            }
        return None

    def get_if_statement_options(self, obj):
        """
        Return if_statement_options
        """
        return [
            {"statement": IF_STATEMENTS[statement_id].description, "id": statement_id}
            for statement_id in obj.if_statement_options.split(",")
        ]

    def get_then_statement(self, obj):
        """
        Return then_statement if the move has been completed, otherwise empty string
        """
        if obj.is_complete:
            return {
                "statement": THEN_STATEMENTS[obj.then_statement].description,
                "id": obj.then_statement,
            }
        return None

    def get_then_statement_options(self, obj):
        """
        Return then_statement_options
        """
        return [
            {"statement": THEN_STATEMENTS[statement_id].description, "id": statement_id}
            for statement_id in obj.then_statement_options.split(",")
        ]


class PlayerSerializer(serializers.ModelSerializer):
    """
    Model serializer for Player
    """

    class Meta:
        model = Player
        fields = ("hp", "attack", "defense", "agility")


class GameSerializer(serializers.ModelSerializer):
    """
    Model serializer for Game
    """

    state = serializers.CharField()
    moves = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ("state", "guid", "player1_user", "player2_user", "moves")

    def get_moves(self, obj):
        """
        Assemble previous moves with Move stats and Player stats
        """
        moves = []
        for move in obj.move_set.order_by("id"):
            if move.is_complete:
                obj.play_single_move(move)
            moves.append(
                {
                    "move": MoveSerializer(move).data,
                    "player1_stats": PlayerSerializer(obj.player1).data,
                    "player2_stats": PlayerSerializer(obj.player2).data,
                }
            )
        return moves
