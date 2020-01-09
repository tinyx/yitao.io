STATEMENTS = [
    (
        "{operating_player}.attack = {operating_player}.attack + 5",
        "Your attack will be increased by 5",
    ),
    (
        "{opponent_player}.hp = {opponent_player}.hp + "
        "{opponent_player}.defense - {operating_player}.attack",
        "You will attack your opponent",
    ),
]
