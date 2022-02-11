import random
from main.Automat.AutomatExceptions import *
from ..Coin.Coin import *
from ..Item.Item import *
from ..ItemInfo.ItemInfo import *
from ..ItemInfo.ItemInfoExceptions import InvalidItemAmountException

def get_random_price():
    """Zwraca losową cenę w zakresie od 1.5zl do 6zl"""
    return random.randint(150,600)/100

def get_coins_value(coins):
    """Zwraca wartość monet"""
    sum = 0
    for c in coins:
        sum += c.get_value()
    return round(sum,2)

class Automat:
    """Reprezentuje automat sprzedazowy"""
    def __init__(self, amountOfEachItem):
        if amountOfEachItem < 1:
            raise InvalidItemAmountException()
        self.__items = { n:ItemInfo(get_random_price(), amountOfEachItem, Item(f"Napój {n}")) for n in range(30, 51) }
        self.__coins = { amount:[Coin(amount) for _ in range(0,10)] for amount in coin_values }
        self.__inserted_coins: "list[Coin]" = []

    def __fetch_item(self, itemNumber):
        """Zwraca zadany napoj i pokazuje blad jesli napoj jest niedostepny"""
        try:
            item = self.__items[itemNumber].fetch_item()
            return item
        except NoItemsLeftException as e:
            raise e
        except KeyError:
            raise InvalidItemNumberException()

    def get_items_list(self):
        """Zwraca numer i nazwe napojow"""
        return [(k, v.get_name()) for k, v in self.__items.items()]

    def get_item_details(self, itemNumber):
        """Zwraca nazwe cene oraz ilośc danego napoju"""
        try:
            itemInfo = self.__items[itemNumber]
        except KeyError:
            raise InvalidItemNumberException()
        return itemInfo.get_name(), itemInfo.get_price(), itemInfo.get_amount()

    def insert_coin(self, coin):
        """Pobiera monete od klienta"""
        self.__inserted_coins.append(coin)

    def return_inserted_coins(self):
        """Zwraca monety do klienta"""
        coins = copy.deepcopy(self.__inserted_coins)
        self.__inserted_coins.clear()
        return coins

    def get_inserted_coins_value(self):
        """Zwraca wartosc wrzuconych monet"""
        return get_coins_value(self.__inserted_coins)

    def add_coins(self, coins):
        """Dodaje monety do monet w maszynie"""
        for c in coins:
            self.__coins[c.get_value()].append(c)
        coins.clear() #czysci liste monet wrzuconych przez klienta

    def __get_change(self, coinsValue, price):
        """Dodaje monety od klienta do monet maszyny i oblicza ilosc reszty"""
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
            raise ExactChangeOnlyException(amount)
        return coins

    def pay_for_item(self, itemNumber):
        """Probuje kupic napoj. Zwraca krotke z reszta oraz napoj."""
        coinsValue = self.get_inserted_coins_value()
        itemName, itemPrice, itemAmount = self.get_item_details(itemNumber)
        if coinsValue == itemPrice:
            #dokladna ilosc gotowki
            try:
                item = self.__fetch_item(itemNumber)
                self.add_coins(self.__inserted_coins)
                return [], item
            except NoItemsLeftException as e:
                raise e
        elif coinsValue >= itemPrice:
            #za duzo monet
            self.add_coins(self.__inserted_coins)
            change = self.__get_change(coinsValue, itemPrice)
            return change, self.__fetch_item(itemNumber)
        else:
            #za malo gotowki
            raise NotEnoughMoneyException(coinsValue, itemPrice)