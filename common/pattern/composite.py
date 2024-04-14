from ..pizza import PizzaComponent


class Composite(PizzaComponent):
    def __init__(self):
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def find_and_remove_pizza(self, pizza_name):
        # Zoek naar de pizza met de opgegeven naam en verwijder deze
        pizza_to_remove = None
        for child in self.children:
            if isinstance(child, PizzaComponent) and child.name == pizza_name:
                pizza_to_remove = child
                break

        if pizza_to_remove:
            self.remove(pizza_to_remove)
            print(f"Pizza '{pizza_name}' is verwijderd uit de bestelling.")
        else:
            print(f"Pizza '{pizza_name}' niet gevonden in de bestelling.")

    def accept(self, visitor):
        visitor.visit_order(self)
        for child in self.children:
            child.accept(visitor)

