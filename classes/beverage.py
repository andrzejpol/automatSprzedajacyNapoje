from .beverageExceptions import *
import copy

class Beverage:
    """Napój używany w automacie"""
    def __init__(self, name):
        self.__beverageName = name
    def get_name(self):
        """Zwraca nazwę napoju"""
        return self.__beverageName

class BeveragesInfo:
    """Zawiera informacje o cenie, ilości i instancji"""
    def __init__(self, price, amount, item):
        self.set_amount(amount)
        self.set_price(price)
        self.__item = item

    def set_amount(self, amount):
        """Ustawia ilosc napojów"""
        if amount < 0:
            raise BeveragesAmountException(amount)
        else:
            self.__amount = amount

    def set_price(self, price):
        """Ustawia cene napoju"""
        if price < 0.01:
            raise BeveragesPriceException(price)
        else:
            self.__price = price
    
    def fetch_item(self):
        """Obniża ilość sztuk napoju i zwraca kopie instancji. Kiedy ilość obniży się od 0 zwróci błąd."""
        if self.__amount == 0:
            raise OutOfStorageException()
        else: 
            self.set_amount(self.__amount - 1)
            return copy.deepcopy(self.__item)

    def get_amount(self):
        """Zwraca ilość napojów"""
        return self.__amount
    
    def get_name(self):
        """Zwraca nazwę napoju"""
        return self.__item.get_name()

    def get_price(self):
        """Zwraca cene napoju"""
        return self.__price
