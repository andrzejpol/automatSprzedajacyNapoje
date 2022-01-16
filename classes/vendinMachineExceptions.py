class BeverageNumberException(Exception):
    """Pojawia sie gdy nie ma takiego numeru napoju"""
    def __init__(self):
        super().__init__("Nie znaleziono takiego napoju")

class MoneyException(Exception):
    """Pojawia się gdy daliśmy za mało pieniędzy"""
    def __init__(self, provided, required):
        super().__init__(f"Za mało pieniędzy")

class ChangeOnlyException(Exception):
    """Pojawia się gdy nie można wydac reszty"""
    def __init__(self, amount):
        super().__init__(f"Tylko odliczona gotówka")