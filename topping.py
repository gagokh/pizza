from product import Product


class Topping(Product):

    def __init__(self, name, price):
        self.__name = name
        self.__price = price

    def name(self):
        return self.__name

    def price(self):
        return self.__price
