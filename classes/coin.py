from .coinExceptions import *

coin_values = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]

class Coin:
    """Monety jakie mogą zostać użyte w automacie"""
    def __init__(self,value):
        if value in coin_values:
            self.__value = value
        else:
            raise CoinValueException(value)
    
    def get_value(self):
        """Zwraca wartość monety"""
        return self.__value
    
    def __eq__(self,other):
        """Porównuje wartość monet"""
        return isinstance(other, Coin) and self.__value == other._Coin__value