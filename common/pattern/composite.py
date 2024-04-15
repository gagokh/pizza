from ..pizza import PizzaComponent


class Composite(PizzaComponent):
    def __init__(self):
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def find_and_remove_pizza(self, pizza_name):
        # Search the order for the pizza to remove
        pizza_to_remove = None
        for child in self.children:
            if isinstance(child, PizzaComponent) and child.name == pizza_name:
                pizza_to_remove = child
                break

        # Remove the pizza if found
        if pizza_to_remove:
            self.remove(pizza_to_remove)
            print(f"Pizza '{pizza_name}' is verwijderd uit de bestelling.")
        else:
            print(f"Pizza '{pizza_name}' niet gevonden in de bestelling.")

    # Visit the composite
    def accept(self, visitor):
        visitor.visit_order(self)
        for child in self.children:
            child.accept(visitor)

