class PriceCalculatorVisitor:
    def __init__(self):
        self.total_price = 0
        self.visited_components = set()
        self.order_string = ""

    def visit_pizza(self, pizza):
        # Check if pizza is already visited
        if pizza not in self.visited_components:
            # Calculate the price of the toppings
            number_of_toppings = len(pizza.topping.split(','))
            topping_price = 0
            if number_of_toppings > 1:
                topping_price = 1 * number_of_toppings

            # Add the price of the pizza and toppings to the total price
            self.total_price += (pizza.price + topping_price) * pizza.quantity
            self.visited_components.add(pizza)

    def visit_order(self, order):
        # Check if order is already visited
        if order not in self.visited_components:
            self.visited_components.add(order)
            # Visit each component of the order
            order.accept(self)
        return self.total_price
