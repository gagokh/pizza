from ..pizza import PizzaComponent


class Composite(PizzaComponent):
    def __init__(self):
        self.children = []

    def add(self, component):
        self.children.append(component)

    def accept(self, visitor):
        visitor.visit_order(self)
        for child in self.children:
            child.accept(visitor)

