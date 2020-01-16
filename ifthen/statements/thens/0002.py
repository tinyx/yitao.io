def execute(operating_player, opponent_player):
    opponent_player.hp = (
        opponent_player.hp + opponent_player.defense - operating_player.attack
    )
