def execute(operating_player, opponent_player):
    attack = operating_player.attack
    operating_player.attack = operating_player.hp
    opponent_player.hp = attack
