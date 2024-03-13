# Define an abstract class representing an order component
class OrderComponent:
    def display(self):
        pass

# Define a class representing a single order, inheriting from OrderComponent
class SingleOrder(OrderComponent):
    def __init__(self, name):
        self.name = name

    def display(self):
        print(f"Bestelling: {self.name}")

    def accept(self, visitor):
        # Accept a visitor and call its visit_single_order method, passing itself as an argument
        visitor.visit_single_order(self)

# Define a class representing a composite order, inheriting from OrderComponent
class CompositeOrder(OrderComponent):
    def __init__(self, name):
        self.name = name
        self.orders = []

    def add_order(self, order):
        # Add an order to the list of orders in the composite order
        self.orders.append(order)

    def display(self):
        # Override the display method to print information about the composite order and each sub-order it contains
        print(f"Gecombineerde bestelling: {self.name}")
        for order in self.orders:
            order.display()
            
    def accept(self, visitor):
        # Accept a visitor, call its visit_composite_order method, passing itself as an argument
        visitor.visit_composite_order(self)
        # Iterate through each sub-order and call their accept method with the visitor
        for sub_order in self.orders:
            sub_order.accept(visitor)
