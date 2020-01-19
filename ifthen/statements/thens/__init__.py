from importlib import import_module


class ThenStatement(object):
    """
    Class represents a then-statement
    Containing id, description, and an execute function that operates on given player
    """

    def __init__(self, id, description, execute):
        self.id = id
        self.description = description
        self.execute = execute


DESCRIPTIONS = {
    "0001": "Your attack will be increased by 5",
    "0002": "You will attack your opponent",
    "0003": "You lose all hp",
    "0004": "You steal 5 hp from your opponent",
    "0005": "You swap your attack and your hp",
}

STATEMENTS = {}
for statement_id in DESCRIPTIONS:
    STATEMENTS[statement_id] = ThenStatement(
        statement_id,
        DESCRIPTIONS[statement_id],
        import_module(f"{__name__}.{statement_id}").execute,
    )
