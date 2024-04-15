class PrintOrderVisitor:
    def __init__(self):
        self.visited_components = set()
        self.order_string = ""

    def visit_pizza(self, pizza):
        # Check if pizza is already visited
        if pizza not in self.visited_components:
            formated_toppings = '\n'.join(pizza.topping.split(','))
            self.order_string += f"{pizza.name}\n{pizza.quantity}x\n{len(pizza.topping.split(','))}x\n{formated_toppings} "


    def visit_order(self, order):
        # Check if order is already visited
        if order not in self.visited_components:
            self.visited_components.add(order)
            order.accept(self)
        return self.order_string
