from product import Product


class Pizza(Product):

    def __init__(self, name, price, toppings):
        self.__name = name
        self.__price = price
        self.__toppings = toppings

    def name(self):
        return self.__name

    def price(self):
        total = 0
        for topping in self.__toppings:
            total += topping.price()
        total += self.__price
        return total

    def add_topping(self, topping):
        self.__toppings.append(topping)

    def remove_topping(self, topping):
        self.__toppings.remove(topping)