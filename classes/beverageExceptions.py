class BeveragesAmountException(Exception):
    """Reaguje na ilość poniżej 0"""
    def __init__(self, amount):
        super().__init__(f"Podano za małą ilość: {amount}")

class BeveragesPriceException(Exception):
    """Reaguje na cenę mniejszą od 1 gr"""
    def __init__(self, price):
        super().__init__(f"Podano złą cenę: {price}")
    
class OutOfStorageException(Exception):
    """Nie ma napojów"""
    def __init__(self):
        super().__init__("Nie ma już więcej sztuk")