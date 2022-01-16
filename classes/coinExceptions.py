class CoinValueException(Exception):
    def __init__(self,value):
        super().__init__(f"Nieprawidłowa wartość: {value}")