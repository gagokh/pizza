class PriceCalculatorVisitor:
    def __init__(self):
        self.total_price = 0
        self.visited_components = set()  # Houd bij welke componenten al zijn bezocht

    def visit_pizza(self, pizza):
        if pizza not in self.visited_components:  # Controleer of pizza al is bezocht
            self.total_price += (pizza.price * pizza.quantity)
            self.visited_components.add(pizza)

    def visit_order(self, order):
        if order not in self.visited_components:  # Controleer of order al is bezocht
            self.visited_components.add(order)
            order.accept(self)  # Bezoek elk onderdeel van de bestelling
        return self.total_price

