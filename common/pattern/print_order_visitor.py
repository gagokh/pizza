class PrintOrderVisitor:
    def __init__(self):
        self.visited_components = set()  # Houd bij welke componenten al zijn bezocht
        self.order_string = ""

    def visit_pizza(self, pizza):
        if pizza not in self.visited_components:  # Controleer of pizza al is bezocht
            self.order_string += f"{pizza.quantity}x {pizza.name} ({pizza.topping})\n"

    def visit_order(self, order):
        if order not in self.visited_components:  # Controleer of order al is bezocht
            self.visited_components.add(order)
            order.accept(self)  # Bezoek elk onderdeel van de bestelling
        return self.order_string
