from django.test.testcases import TestCase

from .models import Player, Game, Move
from .statements.ifs import STATEMENTS as IF_STATEMENTS
from .statements.thens import STATEMENTS as THEN_STATEMENTS


class GameTestCases(TestCase):
    def test_simulate_all_statements(self):
        """
        Execute all statement combinations to at least make sure the statement syntax is correct
        """
        for if_statement in IF_STATEMENTS:
            for then_statement in THEN_STATEMENTS:
                player1 = Player.objects.create(
                    attack=20, defense=10, agility=10, hp=20
                )
                player2 = Player.objects.create(attack=10, defense=0, agility=10, hp=10)
                game = Game.objects.create(player1=player1, player2=player2)
                move = Move(
                    game=game,
                    if_statement=if_statement,
                    then_statement=then_statement,
                )
                print("\n------------------------\n")
                print("Player status before move:")
                print("Player 1: ", game.player1)
                print("Player 2: ", game.player2)
                print("\nMove: ", move)
                game.play(move)
                print("\nPlayer status after move:")
                print("Player 1: ", game.player1)
                print("Player 2: ", game.player2)
                print("\nGame status: ", game)
