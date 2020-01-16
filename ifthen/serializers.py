from rest_framework import serializers

from .models import Game, Move


class MoveSerializer(serializers.ModelSerializer):
    """
    Model serializer for Move
    """

    if_statement = serializers.SerializerMethodField()
    then_statement = serializers.SerializerMethodField()

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
            return obj.if_statement
        return ""

    def get_then_statement(self, obj):
        """
        Return then_statement if the move has been completed, otherwise empty string
        """
        if obj.is_complete:
            return obj.then_statement
        return ""


class GameSerializer(serializers.ModelSerializer):
    """
    Model serializer for Game
    """

    state = serializers.CharField()
    moves = MoveSerializer(source="move_set", many=True, read_only=True)

    class Meta:
        model = Game
        fields = ("state", "guid", "player1_user", "player2_user", "moves")
