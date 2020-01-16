from importlib import import_module


class IfStatement(object):
    """
    Class represents a if-statement
    Containing id, description, and an evaluate function that returns a boolean
    """

    def __init__(self, id, description, evaluate):
        self.id = id
        self.description = description
        self.evaluate = evaluate


DESCRIPTIONS = {
    "0001": "If your attack is higher than your opponent",
    "0002": "Your HP is higher than 15",
    "0003": "You have no defense",
    "0004": "Earth still exists",
}

STATEMENTS = {}
for statement_id in DESCRIPTIONS:
    STATEMENTS[statement_id] = IfStatement(
        statement_id,
        DESCRIPTIONS[statement_id],
        import_module(f"{__name__}.{statement_id}").evaluate,
    )
