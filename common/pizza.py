class PizzaComponent:
    def accept(self, visitor):
        raise NotImplementedError


class Pizza(PizzaComponent):
    def __init__(self, name, topping, quantity, price):
        self.name = name
        self.topping = topping
        self.quantity = quantity
        self.price = price

    def accept(self, visitor):
        return visitor.visit_pizza(self)

