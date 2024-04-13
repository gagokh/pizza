class PizzaComponent:
    def accept(self, visitor):
        raise NotImplementedError


class Pizza(PizzaComponent):
    def __init__(self, name, price, quantity, topping):
        self.name = name
        self.topping = topping
        self.quantity = quantity
        self.price = price

    def accept(self, visitor):
        return visitor.visit_pizza(self)

    def get_price(self):
        return self.price


class Topping(PizzaComponent):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def accept(self, visitor):
        return visitor.visit_topping(self)
