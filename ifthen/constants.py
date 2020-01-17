from enum import Enum


class GameState(Enum):
    """
    [Empty Game]
      - player join: [Half Joined Game]
      - anonymous player join: [Empty Game]

    [Half Joined Game]
      - player join: [Setup Game]
      - anonymous player join: [Half Joined Game]

    [Setup Game]:
      - Setup Game: [Half Setup Game]

    [Half Setup Game]:
      - Setup Game: [Generate Move]

    [Generate Move]:
      - move generated: [Waiting For Two Moves]

    [Waiting For Two Moves]:
      - player make a move: [Waiting For One Move]

    [Waiting For One Move]:
      - player make a move: [Game Ended](one player dead)
                            [Draw Game](both players dead)
                            [Generate Move](both players alive)
    """

    EMPTY_GAME = "empty game"
    HALF_JOINED_GAME = "half joined game"
    SETUP_GAME = "setup game"
    HALF_SETUP_GAME = "half setup game"
    GENERATE_MOVE = "generate move"
    WAITING_FOR_TWO_MOVES = "waiting for two moves"
    WAITING_FOR_ONE_MOVE = "waiting for one move"
    END_GAME = "end game"
    DRAW_GAME = "draw game"


class MessageType(Enum):
    """
    Available message types client can send
    """

    JOIN_GAME = "join game"
    SETUP_GAME = "setup game"
    MAKE_MOVE = "make move"
    ERROR = "error"

    REFRESH_GAME = "refresh game"
