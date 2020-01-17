import random
import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .statements.ifs import STATEMENTS as IF_STATEMENTS
from .statements.thens import STATEMENTS as THEN_STATEMENTS
from .constants import GameState
from .exceptions import ValidationError


class Character(models.Model):
    """
    Model that holds information to represent a character
    A Character can join a game and become a Player
    """

    guid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text="GUID of this character"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user this character belongs to"
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
        """
        String representation of this player
        """
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
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Player 1 of this game",
    )
    player1_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="The user player1 represents",
    )
    player2 = models.ForeignKey(
        Player,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Player 2 of this game",
    )
    player2_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="The user player2 represents",
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
        """
        String representation of this game
        """
        if self.is_draw:
            return "Game ended. Draw game"
        if self.winner:
            return f"Game ended. Winner: {self.winner} | Loser: {self.loser}"
        return "Game is still going"

    @property
    def state(self):
        """
        Get the current state of this game
        """
        if self.player1_user is None and self.player2_user is None:
            return GameState.EMPTY_GAME.value
        if self.player1_user is None or self.player2_user is None:
            return GameState.HALF_JOINED_GAME.value
        # Now we know all players are joined
        if self.player1 is None and self.player2 is None:
            return GameState.SETUP_GAME.value
        if self.player1 is None or self.player2 is None:
            return GameState.HALF_SETUP_GAME.value
        if self.winner:
            return GameState.END_GAME.value
        if self.is_draw:
            return GameState.DRAW_GAME.value
        last_move = self.get_last_move()
        if last_move is None or last_move.is_complete:
            return GameState.GENERATE_MOVE.value
        if last_move.if_statement == "" and last_move.then_statement == "":
            return GameState.WAITING_FOR_TWO_MOVES.value
        if last_move.if_statement == "" or last_move.then_statement == "":
            return GameState.WAITING_FOR_ONE_MOVE.value

    def get_last_move(self):
        """
        Get latest move on the given game
        """
        return self.move_set.order_by("id").last()

    def join(self, user):
        """
        Join the given user to this game if that's possible
        ValidationError will be thrown if not
        """
        game_state = self.state
        if not (
            game_state == GameState.EMPTY_GAME.value
            or game_state == GameState.HALF_JOINED_GAME.value
        ):
            raise ValidationError(message="The game cannot be joined right now")
        if not user.is_authenticated:
            raise ValidationError(message="You must sign in in order to join the game")
        if self.player1_user == user or self.player2_user == user:
            raise ValidationError(message="You have already joined this game")
        if self.player1_user is None:
            self.player1_user = user
            return self.save()
        if self.player1_user is not None and self.player2_user is None:
            self.player2_user = user
            self.save()
            return self.setup(user)
        raise ValidationError(message="You cannot join since the game is full")

    def setup(self, user):
        """
        Allow user to distribute stats on their own
        FOR NOW, SKIPPING THAT AND PRESET THE SAME STATS FOR BOTH PLAYERS
        """
        self.player1 = Player.objects.create(attack=10, defense=10, agility=10, hp=30)
        self.player2 = Player.objects.create(attack=10, defense=10, agility=10, hp=30)
        self.save()
        self.generate_empty_move()

    def generate_empty_move(self):
        if self.state != GameState.GENERATE_MOVE.value:
            raise ValidationError("A move cannot be generated right now")
        self.move_set.create(
            if_user=self.player1_user,
            if_statement_options=",".join(random.sample(list(IF_STATEMENTS.keys()), 3)),
            then_user=self.player2_user,
            then_statement_options=",".join(
                random.sample(list(THEN_STATEMENTS.keys()), 3)
            ),
        )

    def make_move(self, user, statement_id):
        game_state = self.state
        if not (
            game_state == GameState.WAITING_FOR_ONE_MOVE.value
            or game_state == GameState.WAITING_FOR_TWO_MOVES.value
        ):
            raise ValidationError("A move cannot be made right now")
        last_move = self.get_last_move()
        if last_move.if_user == user:
            if last_move.if_statement == "":
                if statement_id in last_move.if_statement_options:
                    last_move.if_statement = statement_id
                    last_move.save()
                else:
                    raise ValidationError("You can only choose a move from available moves")
            else:
                raise ValidationError("You cannot retract your previous choice")
        elif last_move.then_user == user:
            if last_move.then_statement == "":
                if statement_id in last_move.then_statement_options:
                    last_move.then_statement = statement_id
                    last_move.save()
                else:
                    raise ValidationError("You can only choose a move from available moves")
            else:
                raise ValidationError("you cannot retract your previous choice")
        last_move.refresh_from_db()
        if last_move.is_complete:
            self.play()

    def play_single_move(self, move):
        """
        Evaluate a single move on the current game
        Move is passed in as a parameter so you can potentially apply any arbitrary move to a game
        just to see the outcome
        """
        if move.is_complete:
            move.evaluate()
        else:
            raise ValidationError("You are playing a move that's not completed")

    def play(self):
        """
        TRY to apply given move on the game and see what happens
        self.player1 and self.player2 will be manipulated in memory to render the result,
        but they will not be written into the database
        """
        if self.winner or self.loser or self.is_draw:
            raise ValidationError("This game is already over")
        self.refresh_from_db()
        for move in self.move_set.order_by("id"):
            try:
                self.play_single_move(move)
            except ValidationError:
                break
        if self.player1.is_dead or self.player2.is_dead:
            if self.player1.is_dead and self.player2.is_dead:
                self.is_draw = True
            if self.player1.is_dead:
                self.winner = self.player2
                self.loser = self.player1
            if self.player2.is_dead:
                self.winner = self.player1
                self.loser = self.player2
            return self.save()
        self.generate_empty_move()


class Move(models.Model):
    """
    Model holds information of a move
    """

    guid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text="GUID of this move"
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, help_text="The game that this move happens in"
    )
    if_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="The user who chooses the if statement",
    )
    if_statement_options = models.CharField(
        max_length=255, help_text="Available if statement ids"
    )
    if_statement = models.CharField(max_length=255, help_text="Executable if statement")
    then_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="The user who chooses the then statement",
    )
    then_statement_options = models.CharField(
        max_length=255, help_text="Available then statement ids"
    )
    then_statement = models.CharField(
        max_length=255, help_text="Executable then statement"
    )

    def __str__(self):
        """
        String representation of this move
        """
        return f"If {self.if_statement}, then {self.then_statement}"

    @property
    def is_complete(self):
        """
        Return true if both if_statement and then_statement are filled in
        """
        return self.if_statement != "" and self.then_statement != ""

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
        player1 = self.game.player1
        player2 = self.game.player2
        if IF_STATEMENTS[self.if_statement].evaluate(
            operating_player=player1, opponent_player=player2
        ):
            # if (self.game.player1.attack > self.game.player2.attack)
            THEN_STATEMENTS[self.then_statement].execute(
                operating_player=player1, opponent_player=player2
            )

        # self.game.player1.hp = self.game.player1.hp - self.game.player2.attack
        # Switch the order and execute again to make sure we update the right player
        if IF_STATEMENTS[self.if_statement].evaluate(
            operating_player=player2, opponent_player=player1
        ):
            THEN_STATEMENTS[self.then_statement].execute(
                operating_player=player2, opponent_player=player1
            )
