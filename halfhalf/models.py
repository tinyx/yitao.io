import uuid
import logging

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .if_statements import STATEMENTS as IF_STATEMENTS
from .then_statements import STATEMENTS as THEN_STATEMENTS


class Character(models.Model):
    """
    Model that holds information to represent a character
    A Character can join a game and become a Player
    """

    guid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text="GUID of this character"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user this player represents"
    )
    exp = models.IntegerField(default=1, help_text="Total experience of this player")
    level = models.IntegerField(default=1, help_text="Level of this player")
    hp = models.IntegerField(default=20, help_text="Total health points of this player")
    talent_points = models.IntegerField(
        default=20, help_text="Total available talent points of this player"
    )

    def consume_exp(self, exp):
        """
        Consumes given additional experience and level up if conditions are met
        """
        self.exp = self.exp + exp
        self.save()
        if False:  # figure out exp/level model
            self.level_up()

    def level_up(self):
        """
        Update the stats of this player according to current level:
            level +1 for every level
            hp +1 for every level
            talent_points +1 for every 2 levels
        """
        self.level = self.level + 1
        self.hp = self.hp + 1
        if self.level % 2 == 0:
            self.talent_points = self.talent_points + 1
        self.save()


class Player(models.Model):
    """
    Model that holds information to represent a player
    A Player only last through one game
    """

    guid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text="GUID of this player"
    )
    attack = models.IntegerField(
        blank=False, null=False, help_text="Attack point of this player"
    )
    defense = models.IntegerField(
        blank=False, null=False, help_text="Defense point of this player"
    )
    agility = models.IntegerField(
        blank=False, null=False, help_text="Agility point of this player"
    )
    hp = models.IntegerField(
        blank=False, null=False, help_text="Current health point of this player"
    )

    def __str__(self):
        return (
            f"HP: {self.hp} | Attack: {self.attack} | "
            f"Defense: {self.defense} | Agility: {self.agility}"
        )

    def save(self, force=False, *args, **kwargs):
        """
        Set this model to be immutable - we never want the stats to be accidentally modified
        """
        if self.pk and not force:
            raise ValidationError("Son, just don't")
        super().save(*args, **kwargs)

    @property
    def is_dead(self):
        """
        Property that returns whether this player is dead
        """
        return self.hp <= 0


class Game(models.Model):
    """
    Model holds information of a game
    """

    guid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text="GUID of this game"
    )
    player1 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Player 1 of this game",
    )
    player2 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Player 2 of this game",
    )
    winner = models.ForeignKey(
        Player,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="won_games",
        help_text="Winner of the game",
    )
    loser = models.ForeignKey(
        Player,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="lost_games",
        help_text="Loser of the game",
    )
    is_draw = models.BooleanField(default=False)

    def __str__(self):
        if self.is_draw:
            return "Game ended. Draw game"
        if self.winner:
            return f"Game ended. Winner: {self.winner} | Loser: {self.loser}"
        return "Game is still going"

    def play(self, move):
        if self.winner or self.loser or self.is_draw:
            raise ValidationError("This game is already over")
        move.evaluate()
        if self.player1.is_dead or self.player2.is_dead:
            if self.player1.is_dead and self.player2.is_dead:
                self.is_draw = True
            if self.player1.is_dead:
                self.winner = self.player2
                self.loser = self.player1
            if self.player2.is_dead:
                self.winner = self.player1
                self.loser = self.player2
            self.save()

    def replay(self):
        for move in self.move_set.order_by("id"):  # Apply moves in their original order
            move.evaluate()
            if self.player1.is_dead or self.player2.is_dead:
                return


class Move(models.Model):
    """
    Model holds information of a move
    """

    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, help_text="The game that this move happens in"
    )
    if_statement = models.CharField(
        choices=IF_STATEMENTS, max_length=65534, help_text="Executable if statement"
    )
    then_statement = models.CharField(
        choices=THEN_STATEMENTS, max_length=65534, help_text="Executable then statement"
    )

    def __str__(self):
        return f"If {self.if_statement}, then {self.then_statement}"

    def evaluate(self):
        """
        Evaluate the condition and event statements and update the stats of each player

        if_statement examples:
            "operating_player.attack > opponent_player.attack" (Player who has higher attack)
            "operating_player.hp > 30" (Player whose hp is higher than 30)

        then_statement examples:
                "operating_player.attack = operating_player.attack + 5" (Will increase attack by 5)
                "operating_player.hp = operating_player.hp - opponent_player.attack"
                (Will lose hp by the attack of the other player)
        """
        player1 = "self.game.player1"
        player2 = "self.game.player2"
        if eval(
            self.if_statement.format(operating_player=player1, opponent_player=player2)
        ):  # if (self.game.player1.attack > self.game.player2.attack)
            exec(
                self.then_statement.format(
                    operating_player=player1, opponent_player=player2
                )
            )
            # self.game.player1.hp = self.game.player1.hp - self.game.player2.attack
        # Switch the order and execute again to make sure we update the right player
        if eval(
            self.if_statement.format(operating_player=player2, opponent_player=player1)
        ):
            exec(
                self.then_statement.format(
                    operating_player=player2, opponent_player=player1
                )
            )
