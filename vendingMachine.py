import random
from .coin import *
from .beverage import *

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

def get_random_price():
    """Zwraca cene w zakresie 2.49 do 9 zł"""
    return random.randint(249, 900) / 100

def get_coins_value(coins):
    """Zwraca wartość monet w tablicy"""
    sum = 0
    for c in coins:
        sum = round(sum + c.get_value(), 2)
    return sum

class VendingMachine:
    """Instancja automatu sprzedażowego"""
    def __init__(self, amountOfEachItem):
        if amountOfEachItem < 1:
            raise BeveragesAmountException()
        self.__items = {n:BeveragesInfo(get_random_price(), amountOfEachItem, Beverage(f"Item {n}")) for n in range (30, 51)}
        self.__coins = {amount:[Coin(amount) for _ in range(0,10)] for amount in coin_values}
        self.__inserted_coins= []

    def __fetch_item(self, itemNumber):
        """Zwraca żądany napój albo zwraca błąd jeśli jest niedostępny"""
        try:
            item = self.__items[itemNumber].fetch_item()
            return item
        except OutOfStorageException as error:
            raise error
        except KeyError:
            raise BeverageNumberException()

    def get_items_list(self):
        """Zwraca numery i nazwę napojów"""
        return [(k, v.get_name()) for k, v in self.__items.items()]

    def get_item_details(self, itemNumber):
        """Zwraca nazwę, cenę oraz ilość danego napoju."""
        try:
            itemInfo = self.__items[itemNumber]
        except KeyError:
            raise BeverageNumberException()
        return itemInfo.get_name(), itemInfo.get_price(), itemInfo.get_amount()

    def insert_coin(self, coin):
        """Pobiera monete i dodaje ją do tablicy"""
        self.__inserted_coins.append(coin)

    def return_inserted_coins(self):
        """Zwraca monety klientowi"""
        coins = copy.deepcopy(self.__inserted_coins)
        self.__inserted_coins.clear()
        return coins

    def get_inserted_coins_value(self):
        """Zwraca wartość wprowadzonych monet"""
        return get_coins_value(self.__inserted_coins)

    def add_coins(self, coins):
        """Dodaje pobrane od klienta monety i dodaje je do monet w automacie"""
        for c in coins:
            self.__coins[c.get_value()].append(c)
        coins.clear()

    def __get_change(self, coinsValue, price):
        """Dodaje monety pobrane od klienta i wylicza reszte"""
        amount = coinsValue - price
        coins = []
        for cv in coin_values[::-1]:
            required_coin_count = amount // cv
            available_coin_count = len(self.__coins[cv])
            coin_count = int(min(required_coin_count, available_coin_count))
            for _ in range(0, coin_count):
                coins.append(self.__coins[cv].pop())
            amount = round(amount - coin_count * cv, 2)
        if amount > 0:
            raise ChangeOnlyException(amount)
        return coins

    def pay_for_item(self, itemNumber):
        """Próba zakupu napoju pobranymi monetami. Zwraca krotkę ze zmianami i napojem jeśli zakup się powiedzie"""

        coinsValue = self.get_inserted_coins_value()
        itemName, itemPrice, itemAmount = self.get_item_details(itemNumber)
        if coinsValue == itemPrice:
            try:
                item = self.__fetch_item(itemNumber)
                self.add_coins(self.__inserted_coins)
                return [], item
            except OutOfStorageException as e:
                raise e
        elif coinsValue >= itemPrice:
            self.add_coins(self.__inserted_coins)
            change = self.__get_change(coinsValue, itemPrice)
            return change, self.__fetch_item(itemNumber)
        else:
            raise MoneyException(coinsValue, itemPrice)