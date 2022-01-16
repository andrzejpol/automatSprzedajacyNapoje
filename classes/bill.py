from beverage import Beverage

class Bill:

    def __init__(self):
        self.beverages = []

    def add_discount(self):
        pass
    
    def calculate(self):
        totalCost = 0.0
        for beverage in self.beverages:
            totalCost += beverage.price
        return totalCost
    
    def print_to_file(self):
        pass

    def add_meal(self, name, price):
        beverage = Beverage(name, price)
        self.beverages.append(beverage)