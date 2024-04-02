from abc import ABC, abstractmethod


class Product(ABC):

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def price(self):
        pass


